"""
Pydantic schemas cho tất cả models
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import date, datetime
from models.user import UserRole
from models.reader import ReaderType, CardStatus
from models.borrow import BorrowStatus, ReservationStatus
from models.fine import FineStatus


# ===== AUTH SCHEMAS =====
class Token(BaseModel):
    access_token: str
    token_type: str
    user: "UserOut"


class TokenData(BaseModel):
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    role: UserRole = UserRole.READER


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


# ===== CATEGORY SCHEMAS =====
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)


# ===== AUTHOR SCHEMAS =====
class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = None


class AuthorOut(BaseModel):
    id: int
    name: str
    bio: Optional[str]

    model_config = ConfigDict(from_attributes=True)


# ===== BOOK SCHEMAS =====
class BookCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=20)
    title: str = Field(..., min_length=1, max_length=255)
    author_id: int
    category_id: int
    publisher: Optional[str] = None
    publish_year: Optional[int] = Field(None, ge=1000, le=2100)
    isbn: Optional[str] = None
    total_quantity: int = Field(1, ge=1)
    available_quantity: Optional[int] = None
    description: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    publisher: Optional[str] = None
    publish_year: Optional[int] = None
    isbn: Optional[str] = None
    total_quantity: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class BookOut(BaseModel):
    id: int
    code: str
    title: str
    author: AuthorOut
    category: CategoryOut
    publisher: Optional[str]
    publish_year: Optional[int]
    isbn: Optional[str]
    total_quantity: int
    available_quantity: int
    description: Optional[str]
    is_active: bool
    is_available: bool

    model_config = ConfigDict(from_attributes=True)


class BookSearch(BaseModel):
    keyword: Optional[str] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    available_only: bool = False
    page: int = 1
    page_size: int = 20


# ===== READER SCHEMAS =====
class ReaderCreate(BaseModel):
    user_id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = "123456"

    reader_code: str = Field(..., min_length=3, max_length=20)
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    reader_type: ReaderType = ReaderType.STUDENT
    card_expire_date: Optional[date] = None
    max_borrow_books: int = 5

    @field_validator('date_of_birth', 'card_expire_date', mode='before')
    @classmethod
    def parse_flexible_date(cls, v):
        if not v or v == "":
            return None
        if isinstance(v, str):
            v_clean = v.split('T')[0].strip()
            if not v_clean:
                return None
            return date.fromisoformat(v_clean)
        return v


class ReaderUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    reader_type: Optional[ReaderType] = None
    card_status: Optional[CardStatus] = None
    card_expire_date: Optional[date] = None
    max_borrow_books: Optional[int] = None

    @field_validator('card_expire_date', mode='before')
    @classmethod
    def parse_flexible_date(cls, v):
        if not v or v == "":
            return None
        if isinstance(v, str):
            v_clean = v.split('T')[0].strip()
            if not v_clean:
                return None
            return date.fromisoformat(v_clean)
        return v


class ReaderOut(BaseModel):
    id: int
    reader_code: str
    user: UserOut
    phone: Optional[str]
    address: Optional[str]
    date_of_birth: Optional[date]
    reader_type: ReaderType
    card_status: CardStatus
    card_issued_date: date
    card_expire_date: Optional[date]
    max_borrow_books: int

    model_config = ConfigDict(from_attributes=True)


# ===== BORROW SCHEMAS =====
class BorrowCreate(BaseModel):
    reader_id: int
    book_id: int
    notes: Optional[str] = None


class BorrowReturn(BaseModel):
    notes: Optional[str] = None


class BorrowRenew(BaseModel):
    notes: Optional[str] = None


class BorrowOut(BaseModel):
    id: int
    borrow_code: str
    reader: ReaderOut
    book: BookOut
    borrow_date: date
    due_date: date
    return_date: Optional[date]
    renew_count: int
    status: BorrowStatus
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


# ===== RESERVATION SCHEMAS =====
class ReservationCreate(BaseModel):
    book_id: int
    notes: Optional[str] = None


class ReservationOut(BaseModel):
    id: int
    reader: ReaderOut
    book: BookOut
    reservation_date: datetime
    expire_date: Optional[date]
    status: ReservationStatus
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


# ===== FINE SCHEMAS =====
class FineOut(BaseModel):
    id: int
    borrow_record_id: int
    reader: ReaderOut
    overdue_days: int
    fine_per_day: float
    total_amount: float
    status: FineStatus
    paid_date: Optional[date]
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class FineUpdate(BaseModel):
    status: FineStatus
    notes: Optional[str] = None


# ===== AI SCHEMAS =====
class AISearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)


class AISearchResponse(BaseModel):
    answer: str
    suggested_books: List[dict] = []
    source: str = "ai"  # "ai" hoặc "mock"


class AISummarizeResponse(BaseModel):
    book_id: int
    book_title: str
    summary: str
    source: str = "ai"


class AISuggestResponse(BaseModel):
    suggestions: List[dict]
    reason: str
    source: str = "ai"


# ===== STATISTICS SCHEMAS =====
class DashboardStats(BaseModel):
    total_books: int
    total_readers: int
    active_borrows: int
    overdue_borrows: int
    total_fines_pending: float


class TopBook(BaseModel):
    book_id: int
    title: str
    borrow_count: int


class TopReader(BaseModel):
    reader_id: int
    reader_code: str
    full_name: str
    borrow_count: int

