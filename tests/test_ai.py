"""
Tests: AI Chatbot / Summarize / Suggest
Chạy: pytest tests/test_ai.py -v
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as DBSession

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import Base, get_db
from models import User, Reader, Book, Category, Author
from models.user import UserRole
from models.reader import ReaderType, CardStatus
from auth_utils import get_password_hash
from datetime import date, timedelta

# ===== TEST DATABASE (riêng cho AI tests) =====
AI_TEST_DB = "sqlite:///./test_ai_isolated.db"
ai_test_engine = create_engine(AI_TEST_DB, connect_args={"check_same_thread": False})
AITestSession = sessionmaker(autocommit=False, autoflush=False, bind=ai_test_engine)


@pytest.fixture(autouse=True)
def setup_ai_db():
    """Tạo và xóa bảng trước/sau mỗi test"""
    try:
        ai_test_engine.dispose()
        Base.metadata.drop_all(bind=ai_test_engine)
    except Exception:
        pass
    Base.metadata.create_all(bind=ai_test_engine)
    yield
    try:
        ai_test_engine.dispose()
        Base.metadata.drop_all(bind=ai_test_engine)
    except Exception:
        pass
    # Không xóa file vì Windows lock SQLite file


@pytest.fixture
def db():
    s = AITestSession()
    yield s
    s.close()


@pytest.fixture
def client(setup_ai_db):
    """Client với DB override đúng engine"""
    # Import app SAU KHI setup db để tránh side effects
    from main import app

    def override_db():
        s = AITestSession()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def seed(db):
    """Dữ liệu mẫu cho AI tests"""
    user = User(
        username="ai_test_user",
        email="ai@test.com",
        hashed_password=get_password_hash("Test@123"),
        full_name="AI Test User",
        role=UserRole.READER
    )
    db.add(user)
    db.commit()

    cat1 = Category(name="Trí tuệ nhân tạo")
    cat2 = Category(name="Lập trình")
    author = Author(name="Test Author AI")
    db.add_all([cat1, cat2, author])
    db.commit()

    books = [
        Book(
            code="AI001",
            title="Nhập môn AI",
            author_id=author.id,
            category_id=cat1.id,
            total_quantity=3,
            available_quantity=3,
            description="Sách giới thiệu về trí tuệ nhân tạo cho người mới bắt đầu"
        ),
        Book(
            code="AI002",
            title="Machine Learning cơ bản",
            author_id=author.id,
            category_id=cat1.id,
            total_quantity=2,
            available_quantity=0,
            description="Học máy từ A đến Z"
        ),
        Book(
            code="PY001",
            title="Python Programming",
            author_id=author.id,
            category_id=cat2.id,
            total_quantity=4,
            available_quantity=4,
            description="Lập trình Python từ cơ bản đến nâng cao"
        ),
    ]
    db.add_all(books)
    db.commit()

    reader = Reader(
        user_id=user.id,
        reader_code="DG_AI_001",
        reader_type=ReaderType.STUDENT,
        card_status=CardStatus.ACTIVE,
        card_issued_date=date.today(),
        card_expire_date=date.today() + timedelta(days=365)
    )
    db.add(reader)
    db.commit()

    return {"user": user, "books": books, "reader": reader}


def get_token(client, username="ai_test_user", password="Test@123"):
    res = client.post("/api/auth/login", data={"username": username, "password": password})
    assert res.status_code == 200, f"Login failed: {res.text}"
    return res.json()["access_token"]


def auth(client):
    return {"Authorization": f"Bearer {get_token(client)}"}


# ===== TEST AI SEARCH =====
class TestAISearch:
    def test_search_with_valid_query(self, client, seed):
        """TC-AI-01: Tìm kiếm với câu hỏi hợp lệ"""
        res = client.post(
            "/api/ai/search",
            json={"query": "Tôi muốn học về trí tuệ nhân tạo"},
            headers=auth(client)
        )
        assert res.status_code == 200
        data = res.json()
        assert "answer" in data
        assert len(data["answer"]) > 0
        assert data["source"] in ["ai", "mock"]

    def test_search_empty_query_rejected(self, client, seed):
        """TC-AI-02: Câu hỏi rỗng bị từ chối (validation error 422)"""
        res = client.post(
            "/api/ai/search",
            json={"query": ""},
            headers=auth(client)
        )
        assert res.status_code == 422  # Validation error

    def test_search_requires_auth(self, client, seed):
        """TC-AI-03: Tìm kiếm phải có xác thực"""
        res = client.post(
            "/api/ai/search",
            json={"query": "Tìm sách Python"}
        )
        assert res.status_code == 403

    def test_search_very_long_query(self, client, seed):
        """TC-AI-04: Câu hỏi quá dài bị từ chối"""
        long_query = "Tìm sách " * 100
        res = client.post(
            "/api/ai/search",
            json={"query": long_query},
            headers=auth(client)
        )
        assert res.status_code == 422  # max_length=500

    def test_search_returns_structure(self, client, seed):
        """TC-AI-05: Kết quả trả về đúng cấu trúc"""
        res = client.post(
            "/api/ai/search",
            json={"query": "Sách lập trình Python"},
            headers=auth(client)
        )
        assert res.status_code == 200
        data = res.json()
        assert "answer" in data
        assert "suggested_books" in data
        assert "source" in data
        assert isinstance(data["suggested_books"], list)

    def test_search_books_not_in_db(self, client, seed):
        """TC-AI-06: Tìm sách không có trong thư viện"""
        res = client.post(
            "/api/ai/search",
            json={"query": "Sách nấu ăn Việt Nam"},  # Không có trong DB
            headers=auth(client)
        )
        assert res.status_code == 200
        # AI vẫn trả lời nhưng không bịa sách
        assert len(res.json()["answer"]) > 0


# ===== TEST AI SUMMARIZE =====
class TestAISummarize:
    def test_summarize_book_with_description(self, client, seed):
        """TC-AI-07: Tóm tắt sách có mô tả"""
        book_id = seed["books"][0].id
        res = client.post(f"/api/ai/summarize/{book_id}", headers=auth(client))
        assert res.status_code == 200
        data = res.json()
        assert data["book_id"] == book_id
        assert len(data["summary"]) > 0

    def test_summarize_nonexistent_book(self, client, seed):
        """TC-AI-08: Tóm tắt sách không tồn tại"""
        res = client.post("/api/ai/summarize/99999", headers=auth(client))
        assert res.status_code == 404

    def test_summarize_book_without_description(self, client, seed, db):
        """TC-AI-09: Tóm tắt sách không có mô tả"""
        book = seed["books"][0]
        book.description = None
        db.commit()

        res = client.post(f"/api/ai/summarize/{book.id}", headers=auth(client))
        assert res.status_code == 200
        assert len(res.json()["summary"]) > 0


# ===== TEST AI SUGGEST =====
class TestAISuggest:
    def test_suggest_for_reader_with_history(self, client, seed, db):
        """TC-AI-10: Gợi ý cho độc giả có lịch sử mượn"""
        from models.borrow import BorrowRecord, BorrowStatus

        record = BorrowRecord(
            borrow_code="TEST_AI_001",
            reader_id=seed["reader"].id,
            book_id=seed["books"][0].id,
            borrow_date=date.today() - timedelta(days=10),
            due_date=date.today() + timedelta(days=4),
            status=BorrowStatus.BORROWING
        )
        db.add(record)
        db.commit()

        res = client.get("/api/ai/suggest", headers=auth(client))
        assert res.status_code == 200
        data = res.json()
        assert "suggestions" in data
        assert len(data["suggestions"]) > 0

    def test_suggest_for_reader_without_history(self, client, seed):
        """TC-AI-11: Gợi ý cho độc giả chưa có lịch sử"""
        res = client.get("/api/ai/suggest", headers=auth(client))
        assert res.status_code == 200  # Vẫn trả về gợi ý chung

    def test_ai_status_endpoint(self, client, seed):
        """TC-AI-12: Kiểm tra trạng thái AI service"""
        res = client.get("/api/ai/status", headers=auth(client))
        assert res.status_code == 200
        data = res.json()
        assert "is_mock" in data
        assert "status" in data
        assert data["status"] == "ready"
