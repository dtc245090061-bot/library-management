"""
Router: Statistics (Thống kê thư viện)
"""
import csv
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date, timedelta
from database import get_db
from models.book import Book
from models.reader import Reader
from models.borrow import BorrowRecord, BorrowStatus
from models.fine import Fine, FineStatus
from models.user import User
from schemas import DashboardStats
from dependencies import require_librarian

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Thống kê tổng quan cho dashboard"""
    total_books = db.query(Book).filter(Book.is_active == True).count()
    total_readers = db.query(Reader).count()
    today = date.today()

    active_borrows = db.query(BorrowRecord).filter(
        BorrowRecord.status.in_([BorrowStatus.BORROWING, BorrowStatus.OVERDUE])
    ).count()

    overdue_borrows = db.query(BorrowRecord).filter(
        BorrowRecord.status == BorrowStatus.OVERDUE
    ).count()

    # Tổng tiền phạt chưa thu
    pending_fine_result = db.query(func.sum(Fine.total_amount)).filter(
        Fine.status == FineStatus.PENDING
    ).scalar()
    total_fines_pending = float(pending_fine_result or 0)

    return DashboardStats(
        total_books=total_books,
        total_readers=total_readers,
        active_borrows=active_borrows,
        overdue_borrows=overdue_borrows,
        total_fines_pending=total_fines_pending
    )


@router.get("/top-borrowed-books")
async def top_borrowed_books(
    limit: int = 10,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Top sách được mượn nhiều nhất"""
    results = db.query(
        Book.id,
        Book.title,
        func.count(BorrowRecord.id).label("borrow_count")
    ).join(BorrowRecord).group_by(Book.id).order_by(desc("borrow_count")).limit(limit).all()

    return [{"book_id": r[0], "title": r[1], "borrow_count": r[2]} for r in results]


@router.get("/top-active-readers")
async def top_active_readers(
    limit: int = 10,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Top độc giả mượn nhiều nhất"""
    from models.user import User as UserModel
    results = db.query(
        Reader.id,
        Reader.reader_code,
        UserModel.full_name,
        func.count(BorrowRecord.id).label("borrow_count")
    ).join(BorrowRecord, Reader.id == BorrowRecord.reader_id
    ).join(UserModel, Reader.user_id == UserModel.id
    ).group_by(Reader.id).order_by(desc("borrow_count")).limit(limit).all()

    return [
        {"reader_id": r[0], "reader_code": r[1], "full_name": r[2], "borrow_count": r[3]}
        for r in results
    ]


@router.get("/monthly-borrows")
async def monthly_borrows(
    months: int = 6,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Thống kê mượn theo tháng (6 tháng gần nhất)"""
    results = []
    today = date.today()

    for i in range(months - 1, -1, -1):
        month_start = date(today.year, today.month, 1) - timedelta(days=30 * i)
        if month_start.month == 12:
            month_end = date(month_start.year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(month_start.year, month_start.month + 1, 1) - timedelta(days=1)

        count = db.query(BorrowRecord).filter(
            BorrowRecord.borrow_date >= month_start,
            BorrowRecord.borrow_date <= month_end
        ).count()

        results.append({
            "month": month_start.strftime("%m/%Y"),
            "borrow_count": count
        })

    return results


@router.get("/overdue-summary")
async def overdue_summary(
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Tóm tắt sách quá hạn"""
    today = date.today()
    overdue = db.query(BorrowRecord).filter(
        BorrowRecord.status == BorrowStatus.OVERDUE
    ).all()

    total_overdue = len(overdue)
    total_fine_estimate = sum(
        (today - r.due_date).days * 2000 for r in overdue if today > r.due_date
    )

    return {
        "total_overdue": total_overdue,
        "estimated_fine": total_fine_estimate,
        "records": [
            {
                "borrow_code": r.borrow_code,
                "due_date": r.due_date.isoformat(),
                "overdue_days": (today - r.due_date).days
            }
            for r in overdue[:20]
        ]
    }


@router.get("/category-distribution")
async def category_distribution(
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Phân bổ sách theo thể loại"""
    from models.book import Category
    results = db.query(
        Category.name,
        func.count(Book.id).label("book_count")
    ).join(Book, Book.category_id == Category.id
    ).filter(Book.is_active == True
    ).group_by(Category.id).all()

    return [{"category": r[0], "count": r[1]} for r in results]


@router.get("/export/csv")
async def export_statistics_csv(
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Xuất báo cáo thống kê tổng hợp ra CSV"""
    from models.book import Category
    output = io.StringIO()
    writer = csv.writer(output)

    # Báo cáo 1: Tổng quan
    today = date.today()
    total_books = db.query(Book).filter(Book.is_active == True).count()
    total_readers = db.query(Reader).count()
    active_borrows = db.query(BorrowRecord).filter(
        BorrowRecord.status.in_([BorrowStatus.BORROWING, BorrowStatus.OVERDUE])
    ).count()
    overdue_borrows = db.query(BorrowRecord).filter(
        BorrowRecord.status == BorrowStatus.OVERDUE
    ).count()
    from models.fine import FineStatus
    pending_fine = db.query(func.sum(Fine.total_amount)).filter(
        Fine.status == FineStatus.PENDING
    ).scalar() or 0

    writer.writerow(["BÁO CÁO THỐNG KÊ THƯ VIỆN"])
    writer.writerow(["Ngày xuất", today.strftime("%d/%m/%Y")])
    writer.writerow([])
    writer.writerow(["TỔNG QUAN"])
    writer.writerow(["Tiêu chí", "Giá trị"])
    writer.writerow(["Tổng sách", total_books])
    writer.writerow(["Tổng độc giả", total_readers])
    writer.writerow(["Sách đang mượn", active_borrows])
    writer.writerow(["Sách quá hạn", overdue_borrows])
    writer.writerow(["Tiền phạt chưa thu (VND)", float(pending_fine)])
    writer.writerow([])

    # Báo cáo 2: Top sách mượn nhiều
    writer.writerow(["TOP 10 SÁCH MƯỢN NHIỀU NHẤT"])
    writer.writerow(["STT", "Tên sách", "Số lượt mượn"])
    top_books = db.query(
        Book.title,
        func.count(BorrowRecord.id).label("cnt")
    ).join(BorrowRecord).group_by(Book.id).order_by(desc("cnt")).limit(10).all()
    for i, r in enumerate(top_books, 1):
        writer.writerow([i, r[0], r[1]])
    writer.writerow([])

    # Báo cáo 3: Phân bố thể loại
    writer.writerow(["PHÂN BỐ SÁCH THEO THỂ LOẠI"])
    writer.writerow(["Thể loại", "Số đầu sách"])
    cat_dist = db.query(
        Category.name,
        func.count(Book.id).label("cnt")
    ).join(Book, Book.category_id == Category.id
    ).filter(Book.is_active == True
    ).group_by(Category.id).all()
    for r in cat_dist:
        writer.writerow([r[0], r[1]])
    writer.writerow([])

    # Báo cáo 4: Sách quá hạn
    writer.writerow(["SÁCH QUÁ HẠN HIỆN TẠI"])
    writer.writerow(["Mã phiếu", "Hạn trả", "Số ngày quá hạn", "Tiền phạt ước tính"])
    overdue_records = db.query(BorrowRecord).filter(
        BorrowRecord.status == BorrowStatus.OVERDUE
    ).all()
    for r in overdue_records:
        days = (today - r.due_date).days if today > r.due_date else 0
        writer.writerow([r.borrow_code, r.due_date.isoformat(), days, days * 2000])

    output.seek(0)
    content = output.getvalue().encode("utf-8-sig")
    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=bao_cao_thu_vien_{today.strftime('%Y%m%d')}.csv",
            "Content-Type": "text/csv; charset=utf-8"
        }
    )
