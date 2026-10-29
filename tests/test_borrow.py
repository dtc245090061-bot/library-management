"""
Tests: Borrow / Return / Renew / Overdue / Fine
Chạy: pytest tests/test_borrow.py -v
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import Base, get_db
from models import User, Reader, Book, Category, Author, BorrowRecord, Fine
from models.user import UserRole
from models.reader import ReaderType, CardStatus
from models.borrow import BorrowStatus, Reservation
from models.fine import FineStatus
from auth_utils import get_password_hash

# ===== TEST DATABASE (riêng cho borrow tests) =====
BORROW_TEST_DB = "sqlite:///./test_borrow_isolated.db"
borrow_test_engine = create_engine(BORROW_TEST_DB, connect_args={"check_same_thread": False})
BorrowTestSession = sessionmaker(autocommit=False, autoflush=False, bind=borrow_test_engine)


@pytest.fixture(autouse=True)
def setup_db():
    """Tạo và xóa bảng trước/sau mỗi test"""
    Base.metadata.create_all(bind=borrow_test_engine)
    yield
    Base.metadata.drop_all(bind=borrow_test_engine)
    # Không xóa file vì Windows lock SQLite file


@pytest.fixture
def db():
    session = BorrowTestSession()
    yield session
    session.close()


@pytest.fixture
def client(setup_db):
    """Client với DB override đúng engine"""
    from main import app

    def override_get_db():
        s = BorrowTestSession()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_data(db):
    """Tạo dữ liệu test cơ bản"""
    # Users
    admin = User(
        username="admin_t", email="admin@t.com",
        hashed_password=get_password_hash("Admin@123"),
        full_name="Admin Test", role=UserRole.ADMIN
    )
    librarian = User(
        username="lib_t", email="lib@t.com",
        hashed_password=get_password_hash("Lib@123"),
        full_name="Thủ thư Test", role=UserRole.LIBRARIAN
    )
    reader_user = User(
        username="reader_t", email="reader@t.com",
        hashed_password=get_password_hash("Reader@123"),
        full_name="Độc giả Test", role=UserRole.READER
    )
    db.add_all([admin, librarian, reader_user])
    db.commit()

    # Category & Author
    cat = Category(name="Test Category")
    author = Author(name="Test Author")
    db.add_all([cat, author])
    db.commit()

    # Books
    book1 = Book(
        code="TEST001", title="Sách Test 1",
        author_id=author.id, category_id=cat.id,
        total_quantity=3, available_quantity=3
    )
    book2 = Book(
        code="TEST002", title="Sách Test 2",
        author_id=author.id, category_id=cat.id,
        total_quantity=1, available_quantity=0  # Hết sách
    )
    db.add_all([book1, book2])
    db.commit()

    # Reader
    reader = Reader(
        user_id=reader_user.id, reader_code="DG_TEST_001",
        reader_type=ReaderType.STUDENT, card_status=CardStatus.ACTIVE,
        card_issued_date=date.today(),
        card_expire_date=date.today() + timedelta(days=365)
    )
    db.add(reader)
    db.commit()

    return {
        "admin": admin, "librarian": librarian, "reader_user": reader_user,
        "reader": reader, "book1": book1, "book2": book2,
        "cat": cat, "author": author
    }


def get_token(client, username, password):
    res = client.post("/api/auth/login", data={"username": username, "password": password})
    assert res.status_code == 200, f"Login failed: {res.text}"
    return res.json()["access_token"]


def librarian_headers(client):
    token = get_token(client, "lib_t", "Lib@123")
    return {"Authorization": f"Bearer {token}"}


def reader_headers(client):
    token = get_token(client, "reader_t", "Reader@123")
    return {"Authorization": f"Bearer {token}"}


# ===== TEST BORROW =====
class TestBorrow:
    def test_borrow_book_success(self, client, test_data, db):
        """TC01: Mượn sách thành công"""
        reader_id = test_data["reader"].id
        book_id = test_data["book1"].id
        initial_qty = test_data["book1"].available_quantity

        res = client.post("/api/borrows/", json={
            "reader_id": reader_id,
            "book_id": book_id,
            "notes": "Test mượn sách"
        }, headers=librarian_headers(client))

        assert res.status_code == 201, res.text
        data = res.json()
        assert data["status"] == "borrowing"
        assert data["reader"]["id"] == reader_id
        assert data["book"]["id"] == book_id

        # Kiểm tra số lượng sách giảm
        db.refresh(test_data["book1"])
        assert test_data["book1"].available_quantity == initial_qty - 1

    def test_borrow_book_not_available(self, client, test_data):
        """TC02: Mượn sách đã hết"""
        res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book2"].id,  # Sách hết
        }, headers=librarian_headers(client))

        assert res.status_code == 400
        assert "không có sẵn" in res.json()["detail"].lower() or "hết" in res.json()["detail"].lower()

    def test_borrow_book_not_found(self, client, test_data):
        """TC03: Mượn sách không tồn tại"""
        res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": 99999,
        }, headers=librarian_headers(client))

        assert res.status_code in [404, 400]

    def test_return_book_success(self, client, test_data, db):
        """TC04: Trả sách thành công"""
        # Mượn trước
        borrow_res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book1"].id,
        }, headers=librarian_headers(client))
        borrow_id = borrow_res.json()["id"]

        # Trả sách
        return_res = client.put(
            f"/api/borrows/{borrow_id}/return",
            json={"notes": "Trả sách bình thường"},
            headers=librarian_headers(client)
        )
        assert return_res.status_code == 200
        assert return_res.json()["status"] == "returned"
        assert return_res.json()["return_date"] is not None

        # Số lượng sách phải tăng lại
        db.refresh(test_data["book1"])
        assert test_data["book1"].available_quantity == test_data["book1"].total_quantity

    def test_return_already_returned(self, client, test_data, db):
        """TC05: Trả sách đã trả rồi"""
        borrow_res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book1"].id,
        }, headers=librarian_headers(client))
        borrow_id = borrow_res.json()["id"]

        # Trả lần 1
        client.put(f"/api/borrows/{borrow_id}/return", json={}, headers=librarian_headers(client))

        # Trả lần 2 - phải lỗi
        res = client.put(f"/api/borrows/{borrow_id}/return", json={}, headers=librarian_headers(client))
        assert res.status_code == 400

    def test_renew_book_success(self, client, test_data, db):
        """TC06: Gia hạn sách thành công"""
        borrow_res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book1"].id,
        }, headers=librarian_headers(client))
        borrow_id = borrow_res.json()["id"]
        original_due = borrow_res.json()["due_date"]

        renew_res = client.put(
            f"/api/borrows/{borrow_id}/renew",
            json={}, headers=librarian_headers(client)
        )
        assert renew_res.status_code == 200
        assert renew_res.json()["renew_count"] == 1

        # Hạn mới phải sau hạn cũ
        new_due = renew_res.json()["due_date"]
        assert new_due > original_due

    def test_renew_over_limit(self, client, test_data, db):
        """TC07: Gia hạn vượt quá giới hạn"""
        borrow_res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book1"].id,
        }, headers=librarian_headers(client))
        borrow_id = borrow_res.json()["id"]

        # Gia hạn lần 1 (OK)
        client.put(f"/api/borrows/{borrow_id}/renew", json={}, headers=librarian_headers(client))

        # Gia hạn lần 2 - phải lỗi
        res = client.put(f"/api/borrows/{borrow_id}/renew", json={}, headers=librarian_headers(client))
        assert res.status_code == 400
        assert "giới hạn" in res.json()["detail"].lower()

    def test_borrow_requires_auth(self, client, test_data):
        """TC08: Mượn sách phải có xác thực"""
        res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book1"].id,
        })
        assert res.status_code == 403  # No auth

    def test_reader_cannot_create_borrow(self, client, test_data):
        """TC09: Độc giả không được tạo phiếu mượn (chỉ thủ thư)"""
        res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book1"].id,
        }, headers=reader_headers(client))
        assert res.status_code == 403

    def test_list_borrows(self, client, test_data):
        """TC10: Lấy danh sách phiếu mượn"""
        res = client.get("/api/borrows/", headers=librarian_headers(client))
        assert res.status_code == 200
        assert "items" in res.json()
        assert "total" in res.json()


# ===== TEST FINE =====
class TestFine:
    def test_fine_created_on_overdue_return(self, client, test_data, db):
        """TC11: Tự động tạo phiếu phạt khi trả sách quá hạn"""
        # Mượn sách
        borrow_res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book1"].id,
        }, headers=librarian_headers(client))
        borrow_id = borrow_res.json()["id"]

        # Simulate quá hạn bằng cách thay đổi due_date
        record = db.query(BorrowRecord).filter(BorrowRecord.id == borrow_id).first()
        record.due_date = date.today() - timedelta(days=5)  # Quá hạn 5 ngày
        db.commit()

        # Trả sách
        client.put(f"/api/borrows/{borrow_id}/return", json={}, headers=librarian_headers(client))

        # Kiểm tra phiếu phạt đã được tạo
        fine = db.query(Fine).filter(Fine.borrow_record_id == borrow_id).first()
        assert fine is not None
        assert fine.overdue_days == 5
        assert fine.total_amount == 5 * 2000  # 10,000 VNĐ
        assert fine.status == FineStatus.PENDING

    def test_pay_fine(self, client, test_data, db):
        """TC12: Thanh toán tiền phạt"""
        # Tạo phiếu phạt trực tiếp
        borrow_res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book1"].id,
        }, headers=librarian_headers(client))
        borrow_id = borrow_res.json()["id"]
        record = db.query(BorrowRecord).filter(BorrowRecord.id == borrow_id).first()
        record.due_date = date.today() - timedelta(days=3)
        db.commit()
        client.put(f"/api/borrows/{borrow_id}/return", json={}, headers=librarian_headers(client))

        fine = db.query(Fine).filter(Fine.borrow_record_id == borrow_id).first()
        assert fine is not None

        # Thanh toán
        pay_res = client.put(
            f"/api/fines/{fine.id}",
            json={"status": "paid"},
            headers=librarian_headers(client)
        )
        assert pay_res.status_code == 200
        assert pay_res.json()["status"] == "paid"


class TestReservationAndAuth:
    def test_register_creates_reader_card(self, client, db):
        """TC13: Đăng ký độc giả mới tự động tạo thẻ Reader ACTIVE"""
        res = client.post("/api/auth/register", json={
            "username": "new_reader_99",
            "email": "new99@test.com",
            "password": "Password@123",
            "full_name": "Nguyen Van Test",
            "role": "reader"
        })
        assert res.status_code == 201
        user_id = res.json()["id"]

        reader = db.query(Reader).filter(Reader.user_id == user_id).first()
        assert reader is not None
        assert reader.card_status == CardStatus.ACTIVE
        assert reader.max_borrow_books == 5

    def test_reservation_lifecycle_on_return_and_borrow(self, client, test_data, db):
        """TC14: Vòng đời đặt trước: PENDING -> READY khi trả sách -> COMPLETED khi mượn"""
        from models.borrow import Reservation, ReservationStatus

        # Đặt trước sách 2 (hết sách)
        res_record = Reservation(
            reader_id=test_data["reader"].id,
            book_id=test_data["book2"].id,
            status=ReservationStatus.PENDING
        )
        db.add(res_record)
        db.commit()

        # Tạo phiếu mượn giả định cho sách 2 để trả
        borrow_rec = BorrowRecord(
            borrow_code="PM_RES_TEST",
            reader_id=test_data["reader"].id,
            book_id=test_data["book2"].id,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status=BorrowStatus.BORROWING
        )
        db.add(borrow_rec)
        db.commit()

        # Trả sách 2 -> đơn đặt trước chuyển sang READY
        ret_res = client.put(f"/api/borrows/{borrow_rec.id}/return", json={}, headers=librarian_headers(client))
        assert ret_res.status_code == 200

        db.refresh(res_record)
        assert res_record.status == ReservationStatus.READY

        # Độc giả mượn cuốn sách 2 -> đơn đặt trước chuyển sang COMPLETED
        borrow_res = client.post("/api/borrows/", json={
            "reader_id": test_data["reader"].id,
            "book_id": test_data["book2"].id,
        }, headers=librarian_headers(client))
        assert borrow_res.status_code == 201

        db.refresh(res_record)
        assert res_record.status == ReservationStatus.COMPLETED

