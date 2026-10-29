"""
Model: Reader (Độc giả)
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, date, timezone
import enum


class ReaderType(str, enum.Enum):
    STUDENT = "student"       # Học sinh/Sinh viên
    TEACHER = "teacher"       # Giáo viên/Giảng viên
    STAFF = "staff"           # Nhân viên
    EXTERNAL = "external"     # Bên ngoài


class CardStatus(str, enum.Enum):
    ACTIVE = "active"         # Đang hoạt động
    EXPIRED = "expired"       # Hết hạn
    SUSPENDED = "suspended"   # Bị đình chỉ
    CANCELLED = "cancelled"   # Đã hủy


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    reader_code = Column(String(20), unique=True, nullable=False, index=True)  # Mã thẻ
    phone = Column(String(15), nullable=True)
    address = Column(String(255), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    reader_type = Column(Enum(ReaderType), default=ReaderType.STUDENT)
    card_status = Column(Enum(CardStatus), default=CardStatus.ACTIVE)
    card_issued_date = Column(Date, default=date.today)
    card_expire_date = Column(Date, nullable=True)
    max_borrow_books = Column(Integer, default=5)  # Số sách mượn tối đa
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="reader")
    borrow_records = relationship("BorrowRecord", back_populates="reader")
    reservations = relationship("Reservation", back_populates="reader")
    fines = relationship("Fine", back_populates="reader")
