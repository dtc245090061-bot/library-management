"""
Models: Category, Author, Book
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    books = relationship("Book", back_populates="category")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)  # Mã sách
    title = Column(String(255), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    publisher = Column(String(150), nullable=True)   # Nhà xuất bản
    publish_year = Column(Integer, nullable=True)     # Năm xuất bản
    isbn = Column(String(20), unique=True, nullable=True)
    total_quantity = Column(Integer, default=1, nullable=False)      # Số lượng tổng
    available_quantity = Column(Integer, default=1, nullable=False)  # Số lượng còn
    description = Column(Text, nullable=True)  # Mô tả / giới thiệu sách
    cover_image = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    author = relationship("Author", back_populates="books")
    category = relationship("Category", back_populates="books")
    borrow_records = relationship("BorrowRecord", back_populates="book")
    reservations = relationship("Reservation", back_populates="book")

    @property
    def is_available(self) -> bool:
        return self.available_quantity > 0
