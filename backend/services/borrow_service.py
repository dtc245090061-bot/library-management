"""
Service: Borrow/Return/Renew business logic
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date, timedelta
from models.borrow import BorrowRecord, BorrowStatus, Reservation, ReservationStatus
from models.book import Book
from models.reader import Reader, CardStatus
from models.fine import Fine, FineStatus
from config import settings
import random
import string


def generate_borrow_code() -> str:
    """Sinh mã phiếu mượn tự động"""
    today = date.today()
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"PM{today.strftime('%Y%m%d')}{suffix}"


def check_reader_eligibility(reader: Reader, db: Session) -> None:
    """Kiểm tra độc giả có đủ điều kiện mượn không"""
    if reader.card_status != CardStatus.ACTIVE:
        raise HTTPException(400, f"Thẻ độc giả đang ở trạng thái: {reader.card_status.value}")

    # Kiểm tra quá hạn thẻ
    if reader.card_expire_date and reader.card_expire_date < date.today():
        raise HTTPException(400, "Thẻ độc giả đã hết hạn")

    # Kiểm tra số sách đang mượn
    active_borrows = db.query(BorrowRecord).filter(
        BorrowRecord.reader_id == reader.id,
        BorrowRecord.status.in_([BorrowStatus.BORROWING, BorrowStatus.OVERDUE])
    ).count()

    if active_borrows >= reader.max_borrow_books:
        raise HTTPException(400, f"Độc giả đã mượn tối đa {reader.max_borrow_books} cuốn sách")

    # Kiểm tra còn nợ phạt chưa thanh toán
    pending_fines = db.query(Fine).filter(
        Fine.reader_id == reader.id,
        Fine.status == FineStatus.PENDING
    ).count()

    if pending_fines > 0:
        raise HTTPException(400, "Độc giả còn khoản phạt chưa thanh toán. Vui lòng thanh toán trước khi mượn thêm.")


def borrow_book(reader_id: int, book_id: int, notes: str, librarian_id: int, db: Session) -> BorrowRecord:
    """Tạo phiếu mượn sách"""
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(404, "Không tìm thấy độc giả")

    book = db.query(Book).filter(Book.id == book_id, Book.is_active == True).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")

    check_reader_eligibility(reader, db)

    if book.available_quantity <= 0:
        raise HTTPException(400, "Sách hiện không có sẵn để mượn")

    today = date.today()
    due_date = today + timedelta(days=settings.DEFAULT_BORROW_DAYS)

    record = BorrowRecord(
        borrow_code=generate_borrow_code(),
        reader_id=reader_id,
        book_id=book_id,
        borrow_date=today,
        due_date=due_date,
        status=BorrowStatus.BORROWING,
        notes=notes,
        librarian_id=librarian_id
    )

    # Giảm số lượng sách có sẵn
    book.available_quantity -= 1

    # Nếu độc giả này có đơn đặt trước cho cuốn sách này, chuyển thành COMPLETED
    user_reservation = db.query(Reservation).filter(
        Reservation.reader_id == reader_id,
        Reservation.book_id == book_id,
        Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.READY])
    ).first()
    if user_reservation:
        user_reservation.status = ReservationStatus.COMPLETED

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def return_book(record_id: int, notes: str, db: Session) -> BorrowRecord:
    """Trả sách và tính phạt nếu quá hạn"""
    record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
    if not record:
        raise HTTPException(404, "Không tìm thấy phiếu mượn")

    if record.status == BorrowStatus.RETURNED:
        raise HTTPException(400, "Sách đã được trả rồi")

    today = date.today()
    record.return_date = today
    record.status = BorrowStatus.RETURNED
    if notes:
        record.notes = notes

    # Tăng số lượng sách có sẵn
    book = db.query(Book).filter(Book.id == record.book_id).first()
    if book:
        book.available_quantity = min(book.available_quantity + 1, book.total_quantity)

    # Nếu có độc giả đặt trước cuốn sách này, chuyển trạng thái đơn đặt trước sớm nhất sang READY
    pending_res = db.query(Reservation).filter(
        Reservation.book_id == record.book_id,
        Reservation.status == ReservationStatus.PENDING
    ).order_by(Reservation.reservation_date.asc()).first()
    if pending_res:
        pending_res.status = ReservationStatus.READY

    # Tính phạt nếu quá hạn
    if today > record.due_date:
        overdue_days = (today - record.due_date).days
        fine_amount = overdue_days * settings.FINE_PER_DAY

        fine = Fine(
            borrow_record_id=record.id,
            reader_id=record.reader_id,
            overdue_days=overdue_days,
            fine_per_day=settings.FINE_PER_DAY,
            total_amount=fine_amount,
            status=FineStatus.PENDING
        )
        db.add(fine)

    db.commit()
    db.refresh(record)
    return record


def renew_book(record_id: int, notes: str, db: Session) -> BorrowRecord:
    """Gia hạn sách"""
    record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
    if not record:
        raise HTTPException(404, "Không tìm thấy phiếu mượn")

    if record.status != BorrowStatus.BORROWING:
        raise HTTPException(400, "Chỉ có thể gia hạn sách đang mượn")

    if record.renew_count >= settings.MAX_RENEW_COUNT:
        raise HTTPException(400, f"Đã đạt giới hạn gia hạn ({settings.MAX_RENEW_COUNT} lần)")

    # Kiểm tra sách có được đặt trước không
    from models.borrow import Reservation, ReservationStatus
    has_reservation = db.query(Reservation).filter(
        Reservation.book_id == record.book_id,
        Reservation.status == ReservationStatus.PENDING
    ).first()
    if has_reservation:
        raise HTTPException(400, "Sách đang được độc giả khác đặt trước, không thể gia hạn")

    # Kiểm tra nếu đã quá hạn thì không được gia hạn
    if date.today() > record.due_date:
        raise HTTPException(400, "Sách đã quá hạn, không thể gia hạn. Vui lòng trả sách và nộp phạt.")

    record.due_date = record.due_date + timedelta(days=settings.RENEW_DAYS)
    record.renew_count += 1
    if notes:
        record.notes = notes

    db.commit()
    db.refresh(record)
    return record


def update_overdue_status(db: Session) -> int:
    """Cập nhật trạng thái quá hạn cho tất cả phiếu mượn"""
    today = date.today()
    overdue_records = db.query(BorrowRecord).filter(
        BorrowRecord.status == BorrowStatus.BORROWING,
        BorrowRecord.due_date < today
    ).all()

    count = 0
    for record in overdue_records:
        record.status = BorrowStatus.OVERDUE
        count += 1

    db.commit()
    return count
