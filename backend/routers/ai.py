"""
Router: AI features - Chatbot, Summary, Suggest
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.book import Book, Author, Category
from models.reader import Reader
from models.borrow import BorrowRecord, BorrowStatus
from models.user import User
from schemas import AISearchRequest, AISearchResponse, AISummarizeResponse, AISuggestResponse
from dependencies import get_current_user, require_any
from services.ai_service import ai_service
from prompts.search_prompt import SEARCH_SYSTEM_PROMPT, SEARCH_USER_PROMPT
from prompts.summary_prompt import SUMMARY_SYSTEM_PROMPT, SUMMARY_USER_PROMPT
from prompts.suggest_prompt import SUGGEST_SYSTEM_PROMPT, SUGGEST_USER_PROMPT
from config import settings

router = APIRouter(prefix="/api/ai", tags=["AI Features"])


def format_book_for_ai(book: Book) -> str:
    """Format thông tin sách để đưa vào prompt (không có thông tin cá nhân)"""
    status = f"Còn {book.available_quantity} bản" if book.available_quantity > 0 else "Hết sách"
    return (
        f"- Mã: {book.code} | Tên: {book.title} | "
        f"Tác giả: {book.author.name} | Thể loại: {book.category.name} | "
        f"NXB: {book.publisher or 'Không rõ'} | Năm: {book.publish_year or 'Không rõ'} | "
        f"Tình trạng: {status}"
    )


import re

STOP_WORDS = {
    "tôi", "muốn", "tìm", "sách", "về", "cho", "người", "mới", "bắt", "đầu",
    "có", "không", "nào", "nhé", "giúp", "với", "hãy", "gợi", "ý", "cuốn",
    "những", "các", "quyển", "ở", "trong", "thư", "viện", "hay", "nhất",
    "của", "tác", "giả", "thể", "loại", "đang", "được", "là", "và", "hoặc"
}


def extract_smart_matching_books(books: list, query: str, ai_answer: str = "") -> list:
    """
    Trích xuất và xếp hạng sách phù hợp dựa trên:
    1. Sách được nhắc trực tiếp trong câu trả lời của AI (mã sách hoặc tên sách)
    2. Điểm tương đồng từ khóa giữa câu hỏi và thông tin sách (title, author, category, description)
    """
    scored_books = []
    words = re.findall(r'\w+', query.lower())
    keywords = [w for w in words if len(w) > 1 and w not in STOP_WORDS]
    answer_lower = ai_answer.lower()

    for book in books:
        score = 0
        title_lower = book.title.lower()
        author_lower = book.author.name.lower() if book.author else ""
        category_lower = book.category.name.lower() if book.category else ""
        code_lower = book.code.lower()
        desc_lower = (book.description or "").lower()

        # Điểm cao nhất: Được AI trực tiếp nhắc đến trong câu trả lời
        if code_lower in answer_lower:
            score += 100
        if title_lower in answer_lower:
            score += 80

        # Kiểm tra query trực tiếp
        query_clean = query.lower().strip()
        if query_clean and (query_clean in title_lower or title_lower in query_clean):
            score += 50
        if query_clean and (query_clean in author_lower or author_lower in query_clean):
            score += 40
        if query_clean and (query_clean in category_lower or category_lower in query_clean):
            score += 40

        # Khớp theo từng từ khóa
        for kw in keywords:
            if kw in title_lower:
                score += 15
            if kw in category_lower:
                score += 12
            if kw in author_lower:
                score += 10
            if kw in desc_lower:
                score += 5

        if score > 0:
            scored_books.append((score, book))

    # Sắp xếp theo điểm giảm dần
    scored_books.sort(key=lambda x: x[0], reverse=True)
    top_books = [b for score, b in scored_books[:5]]

    return [
        {
            "id": b.id,
            "code": b.code,
            "title": b.title,
            "author": b.author.name if b.author else "Không rõ",
            "category": b.category.name if b.category else "Chung",
            "available": b.available_quantity > 0
        }
        for b in top_books
    ]


@router.post("/search", response_model=AISearchResponse)
async def ai_search_books(
    request: AISearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Chatbot tra cứu sách bằng ngôn ngữ tự nhiên.
    AI chỉ gợi ý sách có trong CSDL thư viện.
    """
    # Lấy danh sách sách để đưa vào prompt
    books = db.query(Book).filter(Book.is_active == True).all()

    if not books:
        return AISearchResponse(
            answer="Thư viện hiện chưa có sách trong hệ thống.",
            suggested_books=[],
            source="system"
        )

    # Tạo danh sách sách cho AI (không có dữ liệu cá nhân)
    book_list = "\n".join([format_book_for_ai(b) for b in books])

    user_prompt = SEARCH_USER_PROMPT.format(
        query=request.query,
        book_list=book_list
    )

    try:
        answer = await ai_service.generate(SEARCH_SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        raise HTTPException(500, f"Lỗi xử lý AI: {str(e)}")

    # Trích xuất danh sách sách gợi ý thông minh từ DB & AI response
    suggested_books = extract_smart_matching_books(books, request.query, answer)

    return AISearchResponse(
        answer=answer,
        suggested_books=suggested_books,
        source="mock" if ai_service.is_mock else "ai"
    )


@router.post("/summarize/{book_id}", response_model=AISummarizeResponse)
async def ai_summarize_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Tóm tắt nội dung sách bằng AI.
    Chỉ dùng mô tả sách, không gửi dữ liệu cá nhân.
    """
    book = db.query(Book).filter(Book.id == book_id, Book.is_active == True).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")

    user_prompt = SUMMARY_USER_PROMPT.format(
        title=book.title,
        author=book.author.name,
        category=book.category.name,
        publisher=book.publisher or "Không rõ",
        publish_year=book.publish_year or "Không rõ",
        description=book.description or "Chưa có mô tả"
    )

    try:
        summary = await ai_service.generate(SUMMARY_SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        raise HTTPException(500, f"Lỗi xử lý AI: {str(e)}")

    return AISummarizeResponse(
        book_id=book.id,
        book_title=book.title,
        summary=summary,
        source="mock" if ai_service.is_mock else "ai"
    )


@router.get("/suggest", response_model=AISuggestResponse)
async def ai_suggest_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gợi ý sách cá nhân hóa dựa trên lịch sử mượn.
    KHÔNG gửi thông tin cá nhân của độc giả cho AI.
    """
    reader = db.query(Reader).filter(Reader.user_id == current_user.id).first()

    # Lấy lịch sử mượn (ẩn thông tin nhạy cảm)
    borrow_history = "Chưa có lịch sử mượn sách."
    if reader:
        borrows = db.query(BorrowRecord).filter(
            BorrowRecord.reader_id == reader.id
        ).order_by(BorrowRecord.borrow_date.desc()).limit(20).all()

        if borrows:
            history_items = []
            for b in borrows:
                history_items.append(
                    f"- {b.book.title} ({b.book.category.name}) - {b.book.author.name}"
                )
            borrow_history = "\n".join(history_items)

    # Lấy sách còn sẵn
    available_books = db.query(Book).filter(
        Book.is_active == True,
        Book.available_quantity > 0
    ).all()

    available_list = "\n".join([format_book_for_ai(b) for b in available_books])

    user_prompt = SUGGEST_USER_PROMPT.format(
        borrow_history=borrow_history,
        available_books=available_list
    )

    try:
        suggestion_text = await ai_service.generate(SUGGEST_SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        raise HTTPException(500, f"Lỗi xử lý AI: {str(e)}")

    return AISuggestResponse(
        suggestions=[{"text": suggestion_text}],
        reason="Dựa trên lịch sử mượn sách của bạn",
        source="mock" if ai_service.is_mock else "ai"
    )


@router.get("/status")
async def ai_status(current_user: User = Depends(get_current_user)):
    """Kiểm tra trạng thái AI service"""
    return {
        "is_mock": ai_service.is_mock,
        "model": ai_service.active_model_name if not ai_service.is_mock else "mock",
        "status": "ready",
        "message": "AI đang hoạt động" if not ai_service.is_mock else "Đang dùng smart local AI"
    }

