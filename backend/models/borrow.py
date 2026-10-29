"""
Models: BorrowRecord (Phiếu mượn/trả), Reservation (Đặt trước)
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone
import enum


class BorrowStatus(str, enum.Enum):
    BORROWING = "borrowing"   # Đang mượn
    RETURNED = "returned"     # Đã trả
    OVERDUE = "overdue"       # Quá hạn
    LOST = "lost"             # Mất sách


class ReservationStatus(str, enum.Enum):
    PENDING = "pending"       # Đang chờ
    READY = "ready"           # Sách đã sẵn sàng
    COMPLETED = "completed"   # Đã lấy sách
    CANCELLED = "cancelled"   # Đã hủy
    EXPIRED = "expired"       # Hết hạn đặt trước


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    borrow_code = Column(String(30), unique=True, nullable=False, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)           # Ngày mượn
    due_date = Column(Date, nullable=False)              # Ngày hẹn trả
    return_date = Column(Date, nullable=True)            # Ngày trả thực tế
    renew_count = Column(Integer, default=0)             # Số lần gia hạn
    status = Column(Enum(BorrowStatus), default=BorrowStatus.BORROWING)
    notes = Column(Text, nullable=True)
    librarian_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Thủ thư xử lý
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    reader = relationship("Reader", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")
    fines = relationship("Fine", back_populates="borrow_record")


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reservation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expire_date = Column(Date, nullable=True)  # Hạn giữ chỗ
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    reader = relationship("Reader", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")
