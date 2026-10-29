"""
Router: Books, Categories, Authors
"""
import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from database import get_db
from models.book import Book, Category, Author
from schemas import (BookCreate, BookUpdate, BookOut, BookSearch,
                     CategoryCreate, CategoryOut, AuthorCreate, AuthorOut)
from dependencies import get_current_user, require_librarian
from models.user import User

router = APIRouter(prefix="/api/books", tags=["Books"])
category_router = APIRouter(prefix="/api/categories", tags=["Categories"])
author_router = APIRouter(prefix="/api/authors", tags=["Authors"])


# ===== CATEGORIES =====
@category_router.get("/", response_model=List[CategoryOut])
async def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.post("/", response_model=CategoryOut, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    if db.query(Category).filter(Category.name == data.name).first():
        raise HTTPException(400, "Thể loại đã tồn tại")
    cat = Category(**data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@category_router.delete("/{cat_id}", status_code=204)
async def delete_category(
    cat_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    cat = db.query(Category).filter(Category.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "Không tìm thấy thể loại")
    db.delete(cat)
    db.commit()


# ===== AUTHORS =====
@author_router.get("/", response_model=List[AuthorOut])
async def list_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


@author_router.post("/", response_model=AuthorOut, status_code=201)
async def create_author(
    data: AuthorCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    author = Author(**data.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


# ===== BOOKS =====
@router.get("/", response_model=dict)
async def list_books(
    keyword: Optional[str] = Query(None, description="Tìm theo tên/tác giả/ISBN"),
    category_id: Optional[int] = None,
    author_id: Optional[int] = None,
    available_only: bool = False,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Danh sách sách với tìm kiếm và lọc"""
    query = db.query(Book).filter(Book.is_active == True)

    if keyword:
        query = query.join(Author).join(Category).filter(
            or_(
                Book.title.ilike(f"%{keyword}%"),
                Book.code.ilike(f"%{keyword}%"),
                Book.isbn.ilike(f"%{keyword}%"),
                Author.name.ilike(f"%{keyword}%"),
                Category.name.ilike(f"%{keyword}%"),
            )
        )
    if category_id:
        query = query.filter(Book.category_id == category_id)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    if available_only:
        query = query.filter(Book.available_quantity > 0)

    total = query.count()
    books = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [BookOut.model_validate(b) for b in books]
    }


@router.get("/fts/search", response_model=dict)
async def fts_search_books(
    q: str = Query(..., min_length=1, description="Từ khóa tìm kiếm toàn văn FTS5"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Tìm kiếm sách nâng cao bằng SQLite FTS5 (Full-Text Search) với điểm xếp hạng BM25"""
    from services.fts_service import fts_service
    fts_results = fts_service.search_fts(query=q, limit=limit)
    if not fts_results:
        return {"total": 0, "query": q, "items": []}

    book_ids = [r["book_id"] for r in fts_results]
    books_map = {b.id: b for b in db.query(Book).filter(Book.id.in_(book_ids), Book.is_active == True).all()}

    ranked_items = []
    for r in fts_results:
        b = books_map.get(r["book_id"])
        if b:
            item = BookOut.model_validate(b).model_dump()
            item["relevance_score"] = r["relevance_score"]
            ranked_items.append(item)

    return {
        "total": len(ranked_items),
        "query": q,
        "search_engine": "SQLite FTS5 (BM25)",
        "items": ranked_items
    }



@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id, Book.is_active == True).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")
    return book


@router.post("/", response_model=BookOut, status_code=201)
async def create_book(
    data: BookCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Thêm sách mới"""
    if db.query(Book).filter(Book.code == data.code).first():
        raise HTTPException(400, f"Mã sách '{data.code}' đã tồn tại")

    # Kiểm tra author và category
    if not db.query(Author).filter(Author.id == data.author_id).first():
        raise HTTPException(404, "Tác giả không tồn tại")
    if not db.query(Category).filter(Category.id == data.category_id).first():
        raise HTTPException(404, "Thể loại không tồn tại")

    book_data = data.model_dump()
    if book_data.get("available_quantity") is None:
        book_data["available_quantity"] = book_data["total_quantity"]

    book = Book(**book_data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookOut)
async def update_book(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Cập nhật thông tin sách"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Xóa mềm sách"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")
    book.is_active = False
    db.commit()


# ===== EXPORT CSV =====
@router.get("/export/csv")
async def export_books_csv(
    keyword: Optional[str] = None,
    category_id: Optional[int] = None,
    available_only: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Xuất danh sách sách ra file CSV"""
    query = db.query(Book).filter(Book.is_active == True)

    if keyword:
        query = query.join(Author).join(Category).filter(
            or_(
                Book.title.ilike(f"%{keyword}%"),
                Book.code.ilike(f"%{keyword}%"),
                Book.isbn.ilike(f"%{keyword}%"),
                Author.name.ilike(f"%{keyword}%"),
                Category.name.ilike(f"%{keyword}%"),
            )
        )
    if category_id:
        query = query.filter(Book.category_id == category_id)
    if available_only:
        query = query.filter(Book.available_quantity > 0)

    books = query.all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "Mã sách", "Tên sách", "Tác giả", "Thể loại",
        "Nhà xuất bản", "Năm XB", "ISBN",
        "Tổng số lượng", "Số lượng còn", "Trạng thái"
    ])

    # Data rows
    for book in books:
        writer.writerow([
            book.code,
            book.title,
            book.author.name if book.author else "",
            book.category.name if book.category else "",
            book.publisher or "",
            book.publish_year or "",
            book.isbn or "",
            book.total_quantity,
            book.available_quantity,
            "Còn sách" if book.available_quantity > 0 else "Hết sách"
        ])

    output.seek(0)
    content = output.getvalue().encode("utf-8-sig")  # utf-8-sig cho Excel đọc đúng tiếng Việt

    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=danh_sach_sach.csv",
            "Content-Type": "text/csv; charset=utf-8"
        }
    )
