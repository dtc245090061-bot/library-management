"""
Router: Borrow/Return/Renew - Mượn, trả, gia hạn sách
"""
import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional
from datetime import date
from database import get_db
from models.borrow import BorrowRecord, BorrowStatus
from models.reader import Reader
from models.fine import Fine, FineStatus
from schemas import BorrowCreate, BorrowReturn, BorrowRenew, BorrowOut, FineOut, FineUpdate
from dependencies import get_current_user, require_librarian
from models.user import User, UserRole
from services.borrow_service import borrow_book, return_book, renew_book, update_overdue_status

router = APIRouter(prefix="/api/borrows", tags=["Borrows"])
fine_router = APIRouter(prefix="/api/fines", tags=["Fines"])


@router.get("/", response_model=dict)
async def list_borrows(
    reader_id: Optional[int] = None,
    book_id: Optional[int] = None,
    status: Optional[str] = None,
    overdue_only: bool = False,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Danh sách phiếu mượn"""
    query = db.query(BorrowRecord)

    # Độc giả chỉ xem phiếu của mình
    if current_user.role == UserRole.READER:
        reader = db.query(Reader).filter(Reader.user_id == current_user.id).first()
        if reader:
            query = query.filter(BorrowRecord.reader_id == reader.id)

    if reader_id:
        query = query.filter(BorrowRecord.reader_id == reader_id)
    if book_id:
        query = query.filter(BorrowRecord.book_id == book_id)
    if status:
        query = query.filter(BorrowRecord.status == status)
    if overdue_only:
        today = date.today()
        query = query.filter(
            BorrowRecord.status.in_([BorrowStatus.BORROWING, BorrowStatus.OVERDUE]),
            BorrowRecord.due_date < today
        )

    total = query.count()
    records = query.order_by(BorrowRecord.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [BorrowOut.model_validate(r) for r in records]
    }


@router.get("/overdue", response_model=dict)
async def list_overdue(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Danh sách sách quá hạn"""
    # Cập nhật trạng thái trước
    update_overdue_status(db)

    today = date.today()
    query = db.query(BorrowRecord).filter(
        BorrowRecord.status == BorrowStatus.OVERDUE
    )
    total = query.count()
    records = query.offset((page-1)*page_size).limit(page_size).all()

    return {
        "total": total,
        "items": [BorrowOut.model_validate(r) for r in records]
    }


@router.get("/{record_id}", response_model=BorrowOut)
async def get_borrow(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
    if not record:
        raise HTTPException(404, "Không tìm thấy phiếu mượn")
    return record


@router.post("/", response_model=BorrowOut, status_code=201)
async def create_borrow(
    data: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):
    """Tạo phiếu mượn mới"""
    record = borrow_book(
        reader_id=data.reader_id,
        book_id=data.book_id,
        notes=data.notes or "",
        librarian_id=current_user.id,
        db=db
    )
    return record


@router.put("/{record_id}/return", response_model=BorrowOut)
async def return_borrow(
    record_id: int,
    data: BorrowReturn,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Trả sách"""
    record = return_book(record_id=record_id, notes=data.notes or "", db=db)
    return record


@router.put("/{record_id}/renew", response_model=BorrowOut)
async def renew_borrow(
    record_id: int,
    data: BorrowRenew,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Gia hạn sách"""
    record = renew_book(record_id=record_id, notes=data.notes or "", db=db)
    return record


# ===== FINES =====
@fine_router.get("/", response_model=dict)
async def list_fines(
    reader_id: Optional[int] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Fine)

    if current_user.role == UserRole.READER:
        reader = db.query(Reader).filter(Reader.user_id == current_user.id).first()
        if reader:
            query = query.filter(Fine.reader_id == reader.id)

    if reader_id:
        query = query.filter(Fine.reader_id == reader_id)
    if status:
        query = query.filter(Fine.status == status)

    total = query.count()
    fines = query.offset((page-1)*page_size).limit(page_size).all()

    return {
        "total": total,
        "items": [FineOut.model_validate(f) for f in fines],
        "total_amount": sum(f.total_amount for f in fines if f.status == FineStatus.PENDING)
    }


@fine_router.put("/{fine_id}", response_model=FineOut)
async def update_fine(
    fine_id: int,
    data: FineUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Cập nhật trạng thái phạt (thanh toán, miễn)"""
    from datetime import date as dt
    fine = db.query(Fine).filter(Fine.id == fine_id).first()
    if not fine:
        raise HTTPException(404, "Không tìm thấy phiếu phạt")

    fine.status = data.status
    if data.status == FineStatus.PAID:
        fine.paid_date = dt.today()
    if data.notes:
        fine.notes = data.notes

    db.commit()
    db.refresh(fine)
    return fine


# ===== EXPORT CSV =====
@router.get("/export/csv")
async def export_borrows_csv(
    status: Optional[str] = None,
    overdue_only: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Xuất danh sách phiếu mượn ra file CSV"""
    # Cập nhật trạng thái quá hạn trước
    update_overdue_status(db)

    query = db.query(BorrowRecord)
    if status:
        query = query.filter(BorrowRecord.status == status)
    if overdue_only:
        today = date.today()
        query = query.filter(
            BorrowRecord.status.in_([BorrowStatus.BORROWING, BorrowStatus.OVERDUE]),
            BorrowRecord.due_date < today
        )

    records = query.order_by(BorrowRecord.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "Mã phiếu", "Độc giả", "Mã thẻ", "Tên sách", "Mã sách",
        "Ngày mượn", "Hạn trả", "Ngày trả",
        "Số lần gia hạn", "Trạng thái", "Ghi chú"
    ])

    status_labels = {
        "borrowing": "Đang mượn",
        "returned": "Đã trả",
        "overdue": "Quá hạn",
        "lost": "Mất sách"
    }

    for r in records:
        writer.writerow([
            r.borrow_code,
            r.reader.user.full_name if r.reader and r.reader.user else "",
            r.reader.reader_code if r.reader else "",
            r.book.title if r.book else "",
            r.book.code if r.book else "",
            r.borrow_date.isoformat() if r.borrow_date else "",
            r.due_date.isoformat() if r.due_date else "",
            r.return_date.isoformat() if r.return_date else "",
            r.renew_count,
            status_labels.get(r.status.value if hasattr(r.status, 'value') else r.status, r.status),
            r.notes or ""
        ])

    output.seek(0)
    content = output.getvalue().encode("utf-8-sig")

    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=phieu_muon.csv",
            "Content-Type": "text/csv; charset=utf-8"
        }
    )
