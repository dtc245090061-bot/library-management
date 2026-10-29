"""
Router: Reservations (Đặt trước sách)
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, timedelta
from database import get_db
from models.borrow import Reservation, ReservationStatus, BorrowStatus
from models.book import Book
from models.reader import Reader
from schemas import ReservationCreate, ReservationOut
from dependencies import get_current_user, require_librarian
from models.user import User, UserRole

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])


@router.get("/", response_model=dict)
async def list_reservations(
    reader_id: Optional[int] = None,
    book_id: Optional[int] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Reservation)

    if current_user.role == UserRole.READER:
        reader = db.query(Reader).filter(Reader.user_id == current_user.id).first()
        if reader:
            query = query.filter(Reservation.reader_id == reader.id)

    if reader_id:
        query = query.filter(Reservation.reader_id == reader_id)
    if book_id:
        query = query.filter(Reservation.book_id == book_id)
    if status:
        query = query.filter(Reservation.status == status)

    total = query.count()
    reservations = query.order_by(Reservation.reservation_date.desc()).offset((page-1)*page_size).limit(page_size).all()

    return {
        "total": total,
        "items": [ReservationOut.model_validate(r) for r in reservations]
    }


@router.post("/", response_model=ReservationOut, status_code=201)
async def create_reservation(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Đặt trước sách đang được mượn"""
    reader = db.query(Reader).filter(Reader.user_id == current_user.id).first()
    if not reader:
        raise HTTPException(400, "Tài khoản của bạn chưa có thẻ độc giả để thực hiện đặt trước")
    reader_id = reader.id

    book = db.query(Book).filter(Book.id == data.book_id, Book.is_active == True).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")

    if book.available_quantity > 0:
        raise HTTPException(400, "Sách còn sẵn, bạn có thể mượn trực tiếp")

    # Kiểm tra đã đặt trước chưa
    existing = db.query(Reservation).filter(
        Reservation.reader_id == reader_id,
        Reservation.book_id == data.book_id,
        Reservation.status == ReservationStatus.PENDING
    ).first()
    if existing:
        raise HTTPException(400, "Bạn đã đặt trước cuốn sách này rồi")

    reservation = Reservation(
        reader_id=reader_id,
        book_id=data.book_id,
        expire_date=date.today() + timedelta(days=7),
        status=ReservationStatus.PENDING,
        notes=data.notes
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation


@router.put("/{res_id}/cancel", response_model=ReservationOut)
async def cancel_reservation(
    res_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Hủy đặt trước"""
    reservation = db.query(Reservation).filter(Reservation.id == res_id).first()
    if not reservation:
        raise HTTPException(404, "Không tìm thấy đặt trước")

    reservation.status = ReservationStatus.CANCELLED
    db.commit()
    db.refresh(reservation)
    return reservation
