"""
Model: Fine (Phiếu phạt quá hạn)
"""
from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone
import enum


class FineStatus(str, enum.Enum):
    PENDING = "pending"     # Chưa thanh toán
    PAID = "paid"           # Đã thanh toán
    WAIVED = "waived"       # Được miễn


class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True, index=True)
    borrow_record_id = Column(Integer, ForeignKey("borrow_records.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    overdue_days = Column(Integer, nullable=False)          # Số ngày quá hạn
    fine_per_day = Column(Float, nullable=False)            # Mức phạt/ngày (VNĐ)
    total_amount = Column(Float, nullable=False)            # Tổng tiền phạt
    status = Column(Enum(FineStatus), default=FineStatus.PENDING)
    paid_date = Column(Date, nullable=True)                 # Ngày thanh toán
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    borrow_record = relationship("BorrowRecord", back_populates="fines")
    reader = relationship("Reader", back_populates="fines")
