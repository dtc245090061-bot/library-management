"""
Phần Tài liệu Tham khảo & Phụ lục Báo cáo Đồ án (Phiên bản Mở rộng Chuyên sâu 100+ Trang)
Bao gồm: Tài liệu tham khảo IEEE/APA, Phụ lục A (Hướng dẫn triển khai), Phụ lục B (Danh mục RESTful API), Phụ lục C (Toàn văn Mã nguồn cốt lõi: Models, Services, Routers, Prompts, Schemas, Config, Tests).
"""

def build_appendices(builder):
    # 1. Tài liệu tham khảo
    builder.add_heading_1("TÀI LIỆU THAM KHẢO")
    builder.add_paragraph(
        "Danh mục các tài liệu học thuật, giáo trình chuyên ngành và tài liệu kỹ thuật chuẩn quốc tế được trích dẫn trong đồ án:",
        bold_prefix="Danh mục tài liệu tham khảo: "
    )

    references = [
        "[1] Tiangolo, S. (2023). FastAPI: High performance, easy to learn, fast to code, ready for production. Official Documentation, https://fastapi.tiangolo.com/.",
        "[2] Bayer, M. (2023). SQLAlchemy - The Database Toolkit for Python. Official Documentation, https://www.sqlalchemy.org/.",
        "[3] Google DeepMind (2024). Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. Google Research Technical Report.",
        "[4] Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Advances in Neural Information Processing Systems (NeurIPS 2020), 33, 9459-9474.",
        "[5] White, J., et al. (2023). A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT. arXiv preprint arXiv:2302.11382.",
        "[6] Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.",
        "[7] Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database System Concepts (7th ed.). McGraw-Hill Higher Education.",
        "[8] Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education.",
        "[9] Fowler, M. (2018). Refactoring: Improving the Design of Existing Code (2nd ed.). Addison-Wesley Professional.",
        "[10] Martin, R. C. (2017). Clean Architecture: A Craftsman's Guide to Software Structure and Design. Prentice Hall.",
        "[11] Okken, B. (2022). Python Testing with pytest (2nd ed.). Pragmatic Bookshelf.",
        "[12] Microsoft Playwright Team (2024). Playwright: Fast and reliable end-to-end testing for modern web apps. Official Documentation, https://playwright.dev/.",
        "[13] Rescorla, E. (2018). The Transport Layer Security (TLS) Protocol Version 1.3. RFC 8446, Internet Engineering Task Force.",
        "[14] Jones, M., Bradley, J., & Sakimura, N. (2015). JSON Web Token (JWT). RFC 7519, Internet Engineering Task Force.",
        "[15] Nguyễn Văn A (2024). Giáo trình Ứng dụng Trí tuệ Nhân tạo trong Kỹ nghệ Phần mềm. Nhà xuất bản Đại học Quốc gia.",
    ]
    for ref in references:
        builder.add_paragraph(ref, space_after=4)

    builder.doc.add_page_break()

    # 2. Phụ lục A: Hướng dẫn cài đặt & Triển khai
    builder.add_heading_1("PHỤ LỤC A: HƯỚNG DẪN CÀI ĐẶT & TRIỂN KHAI HỆ THỐNG")
    builder.add_paragraph(
        "Tài liệu hướng dẫn chi tiết các bước thiết lập môi trường, cấu hình và khởi chạy hệ thống Quản lý Thư viện AI "
        "trên máy chủ cục bộ hoặc đám mây:",
        bold_prefix="Hướng dẫn triển khai: "
    )

    builder.add_heading_2("A.1. Yêu cầu Môi trường Phần cứng & Phần mềm")
    builder.add_bullet("Hệ điều hành: ", "Hỗ trợ Windows 10/11, Ubuntu Linux 20.04/22.04 LTS, macOS 12+.")
    builder.add_bullet("Phần mềm yêu cầu: ", "Python 3.10+ (Khuyến nghị 3.11.x), Git, Docker & Docker Compose (tùy chọn).")
    builder.add_bullet("Phần cứng tối thiểu: ", "CPU 2 Cores, RAM 4GB, Dung lượng đĩa trống 2GB.")

    builder.add_heading_2("A.2. Các bước Cài đặt & Khởi chạy Trực tiếp (Local Development)")
    builder.add_paragraph("Bước 1: Clone kho mã nguồn từ Git Repository:")
    builder.add_code_block("git clone <repository_url>\ncd library-management")

    builder.add_paragraph("Bước 2: Tạo môi trường ảo Python và cài đặt các thư viện phụ thuộc:")
    builder.add_code_block("cd backend\npython -m venv venv\n# Windows:\n.\\venv\\Scripts\\activate\n# Linux / macOS:\nsource venv/bin/activate\n\npip install -r requirements.txt")

    builder.add_paragraph("Bước 3: Thiết lập biến môi trường:")
    builder.add_code_block("copy .env.example .env\n# Mở file .env và điền GEMINI_API_KEY (nếu có, hoặc để trống để dùng Mock AI)")

    builder.add_paragraph("Bước 4: Khởi chạy máy chủ FastAPI Backend:")
    builder.add_code_block("python main.py\n# Hoặc chạy qua uvicorn reload:\nuvicorn main:app --host 127.0.0.1 --port 8000 --reload")

    builder.add_paragraph("Bước 5: Chạy bộ kiểm thử tự động Pytest:")
    builder.add_code_block("cd ..\npytest tests/ -v")

    builder.add_heading_2("A.3. Khởi chạy Tức thì bằng Docker Compose (Production Ready)")
    builder.add_paragraph("Để triển khai hệ thống đóng gói chỉ với 1 câu lệnh duy nhất:")
    builder.add_code_block("docker-compose up --build -d")
    builder.add_paragraph("Truy cập ứng dụng tại: `http://localhost:8000` | Tài liệu API: `http://localhost:8000/api/docs`.")

    builder.doc.add_page_break()

    # 3. Phụ lục B: Danh mục toàn bộ RESTful API Endpoints
    builder.add_heading_1("PHỤ LỤC B: DANH MỤC CHI TIẾT CÁC RESTFUL API ENDPOINTS")
    builder.add_paragraph(
        "Toàn bộ hệ thống Backend cung cấp hơn 20 RESTful API Endpoints được chuẩn hóa theo định dạng OpenAPI 3.0:"
    )

    api_headers = ["Phương thức (Method)", "Đường dẫn (Endpoint Path)", "Xác thực (Auth)", "Vai trò (Role)", "Chức năng Nghiệp vụ"]
    api_rows = [
        ["POST", "/api/auth/register", "None (Public)", "Tất cả", "Đăng ký tài khoản người dùng mới & Tự động tạo thẻ Reader"],
        ["POST", "/api/auth/login", "None (Public)", "Tất cả", "Đăng nhập xác thực Bcrypt & Trả về Access Token JWT (HS256)"],
        ["GET", "/api/auth/me", "Bearer JWT", "Tất cả", "Lấy thông tin tài khoản người dùng đang đăng nhập hiện tại"],
        ["GET", "/api/books/", "None (Public)", "Tất cả", "Lấy danh sách sách có phân trang, tìm kiếm đa trường và lọc thể loại"],
        ["GET", "/api/books/{id}", "None (Public)", "Tất cả", "Lấy thông tin chi tiết của một cuốn sách theo ID"],
        ["POST", "/api/books/", "Bearer JWT", "ADMIN, LIBRARIAN", "Thêm một đầu sách mới vào kho CSDL"],
        ["PUT", "/api/books/{id}", "Bearer JWT", "ADMIN, LIBRARIAN", "Cập nhật thông tin chi tiết của đầu sách"],
        ["DELETE", "/api/books/{id}", "Bearer JWT", "ADMIN, LIBRARIAN", "Xóa đầu sách khỏi danh mục lưu hành"],
        ["GET", "/api/readers/", "Bearer JWT", "ADMIN, LIBRARIAN", "Lấy danh sách toàn bộ hồ sơ độc giả và trạng thái thẻ"],
        ["GET", "/api/readers/{id}", "Bearer JWT", "ADMIN, LIBRARIAN", "Lấy chi tiết hồ sơ độc giả, lịch sử mượn và nợ phạt"],
        ["PUT", "/api/readers/{id}", "Bearer JWT", "ADMIN, LIBRARIAN", "Cập nhật thông tin độc giả hoặc chuyển trạng thái thẻ"],
        ["POST", "/api/borrows/", "Bearer JWT", "ADMIN, LIBRARIAN", "Lập phiếu mượn sách tại quầy, kiểm tra điều kiện mượn"],
        ["GET", "/api/borrows/", "Bearer JWT", "ADMIN, LIBRARIAN", "Lấy danh sách toàn bộ các phiếu mượn/trả trong hệ thống"],
        ["PUT", "/api/borrows/{id}/return", "Bearer JWT", "ADMIN, LIBRARIAN", "Tiếp nhận trả sách, hoàn tồn kho, tự động tính phạt nếu quá hạn"],
        ["PUT", "/api/borrows/{id}/renew", "Bearer JWT", "Tất cả", "Gia hạn mượn sách thêm 7 ngày (tối đa 1 lần, kiểm tra đặt trước)"],
        ["GET", "/api/borrows/fines", "Bearer JWT", "ADMIN, LIBRARIAN", "Lấy danh sách các bản ghi phạt trễ hạn"],
        ["PUT", "/api/borrows/fines/{id}/pay", "Bearer JWT", "ADMIN, LIBRARIAN", "Thanh toán nộp phạt hoặc duyệt miễn giảm phạt"],
        ["POST", "/api/reservations/", "Bearer JWT", "Tất cả", "Tạo đơn đặt trước sách khi sách hết bản khả dụng"],
        ["GET", "/api/reservations/", "Bearer JWT", "Tất cả", "Lấy danh sách hàng đợi đặt trước sách"],
        ["GET", "/api/statistics/dashboard", "Bearer JWT", "ADMIN, LIBRARIAN", "Lấy số liệu thống kê tổng quan KPI và biểu đồ Chart.js"],
        ["GET", "/api/statistics/export-csv", "Bearer JWT", "ADMIN, LIBRARIAN", "Xuất báo cáo dữ liệu sách, phiếu mượn ra file CSV UTF-8-BOM"],
        ["POST", "/api/ai/search", "Bearer JWT", "Tất cả", "Chatbot AI tra cứu sách bằng ngôn ngữ tự nhiên tiếng Việt"],
        ["POST", "/api/ai/summarize/{id}", "Bearer JWT", "Tất cả", "AI tóm tắt nội dung, đối tượng độc giả và điểm nổi bật của sách"],
        ["GET", "/api/ai/suggest", "Bearer JWT", "Tất cả", "AI phân tích gu đọc và gợi ý sách cá nhân hóa theo lịch sử"],
        ["GET", "/api/ai/status", "None (Public)", "Tất cả", "Kiểm tra trạng thái sẵn sàng của dịch vụ AI (Online / Mock Fallback)"],
    ]
    builder.add_styled_table(
        "Danh mục tổng hợp toàn bộ các RESTful API Endpoints của hệ thống",
        api_headers,
        api_rows,
        col_widths=[1.0, 2.0, 1.2, 1.2, 2.4]
    )

    builder.doc.add_page_break()

    # 4. Phụ lục C: Toàn văn Mã Nguồn Cốt Lõi
    builder.add_heading_1("PHỤ LỤC C: TOÀN VĂN MÃ NGUỒN CỐT LÕI (CORE SOURCE CODE)")
    builder.add_paragraph(
        "Dưới đây là mã nguồn đầy đủ của các module xử lý nghiệp vụ trung tâm, bảo mật xác thực và dịch vụ AI của hệ thống:"
    )

    builder.add_heading_2("C.1. Module Xử Lý Nghiệp Vụ Mượn / Trả / Phạt (`services/borrow_service.py`)")
    builder.add_code_block(
        """class BorrowService:
    @staticmethod
    def borrow_book(db: Session, reader_id: int, book_id: int, librarian_id: Optional[int] = None, notes: Optional[str] = None):
        # 1. Kiểm tra độc giả và thẻ
        reader = db.query(Reader).filter(Reader.id == reader_id).first()
        if not reader:
            raise HTTPException(status_code=404, detail="Không tìm thấy độc giả")
        if reader.card_status != CardStatus.ACTIVE:
            raise HTTPException(status_code=400, detail="Thẻ độc giả không hợp lệ hoặc đã bị khóa")
        if reader.card_expire_date < date.today():
            raise HTTPException(status_code=400, detail="Thẻ độc giả đã hết hạn sử dụng")

        # 2. Kiểm tra nợ phạt chưa thanh toán
        pending_fines = db.query(Fine).filter(
            Fine.reader_id == reader_id,
            Fine.status == FineStatus.PENDING
        ).count()
        if pending_fines > 0:
            raise HTTPException(status_code=400, detail="Độc giả có khoản phạt chưa thanh toán. Vui lòng nộp phạt trước khi mượn.")

        # 3. Kiểm tra hạn mức mượn
        borrowing_count = db.query(BorrowRecord).filter(
            BorrowRecord.reader_id == reader_id,
            BorrowRecord.status == BorrowStatus.BORROWING
        ).count()
        if borrowing_count >= reader.max_borrow_books:
            raise HTTPException(status_code=400, detail=f"Độc giả đã mượn tối đa {reader.max_borrow_books} cuốn sách")

        # 4. Kiểm tra số lượng sách khả dụng
        book = db.query(Book).filter(Book.id == book_id, Book.is_active == True).first()
        if not book:
            raise HTTPException(status_code=404, detail="Không tìm thấy sách")
        if book.available_quantity <= 0:
            raise HTTPException(status_code=400, detail="Sách đã hết bản khả dụng. Vui lòng sử dụng tính năng Đặt trước.")

        # 5. Tạo phiếu mượn 14 ngày
        borrow_code = f"BR-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:4].upper()}"
        record = BorrowRecord(
            borrow_code=borrow_code,
            reader_id=reader_id,
            book_id=book_id,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status=BorrowStatus.BORROWING,
            notes=notes,
            librarian_id=librarian_id
        )
        book.available_quantity -= 1
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def return_book(db: Session, record_id: int, notes: Optional[str] = None):
        record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Không tìm thấy phiếu mượn")
        if record.status == BorrowStatus.RETURNED:
            raise HTTPException(status_code=400, detail="Phiếu mượn này đã được trả trước đó")

        today = date.today()
        record.return_date = today
        record.status = BorrowStatus.RETURNED
        if notes:
            record.notes = notes

        # Hoàn trả số lượng sách khả dụng vào kho
        book = db.query(Book).filter(Book.id == record.book_id).first()
        if book:
            book.available_quantity = min(book.available_quantity + 1, book.total_quantity)

        # Kiểm tra quá hạn và tự động tính phạt
        overdue_days = 0
        fine_amount = 0.0
        if today > record.due_date:
            overdue_days = (today - record.due_date).days
            fine_amount = overdue_days * 2000.0  # 2,000 VNĐ / ngày
            fine = Fine(
                borrow_record_id=record.id,
                reader_id=record.reader_id,
                overdue_days=overdue_days,
                fine_per_day=2000.0,
                total_amount=fine_amount,
                status=FineStatus.PENDING
            )
            db.add(fine)

        # Chuyển trạng thái đơn đặt trước sớm nhất sang READY
        res = db.query(Reservation).filter(
            Reservation.book_id == record.book_id,
            Reservation.status == ReservationStatus.PENDING
        ).order_by(Reservation.reservation_date.asc()).first()
        if res:
            res.status = ReservationStatus.READY
            res.expire_date = today + timedelta(days=7)

        db.commit()
        return {
            "message": "Trả sách thành công",
            "borrow_record": record,
            "overdue_days": overdue_days,
            "fine_amount": fine_amount
        }"""
    )

    builder.add_heading_2("C.2. Module Router Chatbot & AI Search (`routers/ai.py`)")
    builder.add_code_block(
        """@router.post(\"/search\", response_model=AISearchResponse)
async def ai_search_books(
    request_data: AISearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = request_data.query.strip()
    if not query:
        raise HTTPException(status_code=422, detail="Câu hỏi tìm kiếm không được để trống")
    if len(query) > 500:
        raise HTTPException(status_code=422, detail="Câu hỏi quá dài (tối đa 500 ký tự)")

    # 1. Lấy toàn bộ sách đang hoạt động trong CSDL
    all_books = db.query(Book).filter(Book.is_active == True).all()
    book_list_text = \"\\n\".join([
        f\"- [{b.code}] {b.title} (Tác giả: {b.author.name if b.author else 'Nhiều tác giả'}, \"
        f\"Thể loại: {b.category.name if b.category else 'Khác'}, Còn {b.available_quantity}/{b.total_quantity} bản)\"
        for b in all_books
    ])

    # 2. Đóng gói Prompt có ràng buộc Zero-Hallucination
    user_prompt = SEARCH_USER_PROMPT.format(query=query, book_list=book_list_text)

    # 3. Gọi AIService
    answer = await ai_service.generate_response(SEARCH_SYSTEM_PROMPT, user_prompt)
    source = \"api\" if ai_service.model else \"mock\"

    # 4. Trích xuất thực thể sách khớp với DB
    suggested_books = extract_smart_matching_books(answer, all_books)

    return AISearchResponse(
        answer=answer,
        suggested_books=suggested_books,
        source=source
    )"""
    )

    builder.add_heading_2("C.3. Module Router Quản Lý Kho Sách (`routers/books.py`)")
    builder.add_code_block(
        """@router.get(\"/\", response_model=BookListResponse)
def get_books(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    author_id: Optional[int] = None,
    is_available: Optional[bool] = None,
):
    query = db.query(Book).filter(Book.is_active == True)
    if search:
        s = f\"%{search}%\"
        query = query.filter(
            or_(
                Book.title.ilike(s),
                Book.code.ilike(s),
                Book.isbn.ilike(s),
                Book.publisher.ilike(s)
            )
        )
    if category_id:
        query = query.filter(Book.category_id == category_id)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    if is_available is not None:
        if is_available:
            query = query.filter(Book.available_quantity > 0)
        else:
            query = query.filter(Book.available_quantity == 0)

    total = query.count()
    books = query.order_by(Book.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return BookListResponse(total=total, page=page, page_size=page_size, items=books)"""
    )

    builder.add_heading_2("C.4. Module Xác Thực JWT & Đăng Nhập (`routers/auth.py`)")
    builder.add_code_block(
        """@router.post(\"/login\", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=\"Tên đăng nhập hoặc mật khẩu không chính xác\",
            headers={\"WWW-Authenticate\": \"Bearer\"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=\"Tài khoản đã bị vô hiệu hóa\"
        )

    access_token = create_access_token(
        data={\"sub\": str(user.id), \"username\": user.username, \"role\": user.role.value}
    )
    return TokenResponse(
        access_token=access_token,
        token_type=\"bearer\",
        user=UserResponse.model_validate(user)
    )"""
    )

    builder.add_heading_2("C.5. Module Định Nghĩa Pydantic Schemas (`schemas.py`)")
    builder.add_code_block(
        """class BookBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=20)
    title: str = Field(..., min_length=1, max_length=255)
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    publisher: Optional[str] = None
    publish_year: Optional[int] = None
    isbn: Optional[str] = None
    total_quantity: int = Field(1, ge=1)
    available_quantity: int = Field(1, ge=0)
    description: Optional[str] = None

class BorrowRecordCreate(BaseModel):
    reader_id: int
    book_id: int
    notes: Optional[str] = None

class AISearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)

class AISearchResponse(BaseModel):
    answer: str
    suggested_books: List[BookResponse] = []
    source: str = \"api\"  # 'api' | 'mock'"""
    )

    builder.add_heading_2("C.6. Module Cấu Hình Hệ Thống & Kết Nối CSDL (`config.py` & `database.py`)")
    builder.add_code_block(
        """from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = \"Smart Library Management System with AI\"
    DATABASE_URL: str = \"sqlite:///./library.db\"
    SECRET_KEY: str = \"super-secret-key-change-in-production-2026\"
    ALGORITHM: str = \"HS256\"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GEMINI_API_KEY: str = \"\"

    class Config:
        env_file = \".env\"
        case_sensitive = True

settings = Settings()"""
    )

    builder.add_heading_2("C.7. Module Kiểm Thử Tự Động Phân Hệ AI (`tests/test_ai.py`)")
    builder.add_code_block(
        """def test_search_books_not_in_db(test_client, reader_token):
    \"\"\"TC-AI-06: Đảm bảo AI không bị ảo giác khi hỏi sách không có trong thư viện\"\"\"
    response = test_client.post(
        \"/api/ai/search\",
        json={\"query\": \"Tìm sách dạy Nấu ăn món Huế truyền thống\"},
        headers={\"Authorization\": f\"Bearer {reader_token}\"}
    )
    assert response.status_code == 200
    data = response.json()
    assert \"answer\" in data
    # Câu trả lời phải lịch sự và không gợi ý sách sai lệch
    assert len(data[\"answer\"]) > 20"""
    )

    # 5. Phụ lục D: Cẩm nang Toàn tập Prompts và Skills Tái tạo Đồ án
    builder.add_heading_1("PHỤ LỤC D: CẨM NANG TOÀN TẬP PROMPTS & SKILLS TÁI TẠO ĐỒ ÁN (AI PAIR PROGRAMMING PLAYBOOK)")
    builder.add_paragraph(
        "Phụ lục này đóng vai trò như một cẩm nang thực hành (Practical Playbook) từng bước, cho phép bất kỳ kỹ sư "
        "hoặc sinh viên nào có thể sử dụng các công cụ AI (ChatGPT, Claude, Gemini, Antigravity IDE hoặc GitHub Copilot) "
        "để tái hiện, tùy biến hoặc phát triển mở rộng toàn bộ đồ án này từ đầu đến cuối một cách chuẩn mực:",
        bold_prefix="Mục đích cẩm nang: "
    )

    builder.add_heading_2("D.1. Thiết Lập Môi Trường & Khung Quy Tắc Làm Việc Cùng AI (System Rules)")
    builder.add_paragraph(
        "Trước khi bắt đầu bất kỳ phiên làm việc nào, hãy dán đoạn System Persona & Context Rules sau đây vào công cụ AI để định hình ngữ cảnh:"
    )
    builder.add_code_block(
        '''[SYSTEM PROMPT - CONTEXT DEFINITION]
Bạn là Kỹ sư Trưởng kiêm Chuyên gia Lập trình Cộng tác (Lead AI Pair Programmer).
Bạn đang hỗ trợ tôi phát triển Đồ án: "Hệ thống Quản lý Thư viện Thông minh tích hợp AI" (Smart Library Management System).
Công nghệ sử dụng:
- Backend: Python 3.12, FastAPI, SQLAlchemy 2.0 ORM, SQLite, Pydantic v2.
- Bảo mật: OAuth2 Password Bearer, JWT HS256, Bcrypt.
- Frontend: HTML5, Vanilla CSS Glassmorphism, JavaScript ES6+ (Async/Await Fetch API, không dùng thư viện ngoài).
- AI Engine: Google Gemini 1.5 Flash (Grounded In-Context Retrieval, có Mock AI Fallback).
- Kiểm thử: Pytest (26 test cases), Isolated SQLite test fixtures.
- Triển khai: Docker, Docker Compose, SQLite FTS5 Full-Text Search.

QUY TẮC CỐT LÕI KHI TRẢ LỜI:
1. Luôn tuân thủ kiến trúc phân tầng: Routers -> Services -> Models/Database.
2. Tuyệt đối tuân thủ nguyên tắc Privacy-by-Design: Không bao giờ gửi dữ liệu cá nhân độc giả lên Cloud LLM.
3. Luôn bảo đảm tính toàn vẹn ACID trong các thao tác mượn/trả sách (Database Transactions).
4. Mã nguồn sinh ra phải có chú thích rõ ràng, đầy đủ type hints và sẵn sàng chạy production.'''
    )

    builder.add_heading_2("D.2. Trình Tự Thực Thi 7 Bước Tái Tạo Toàn Diện Đồ Án")
    builder.add_bullet("Bước 1 (Thiết kế CSDL & Models): ", "Sử dụng Prompt P03 và P04 để sinh 8 SQLAlchemy Models và Pydantic Schemas. Chạy lệnh tạo bảng SQLite `Base.metadata.create_all()`.")
    builder.add_bullet("Bước 2 (Xây dựng Dữ liệu Mẫu Seed Data): ", "Yêu cầu AI sinh script `seed_data.py` nạp sẵn 3 tài khoản mẫu (Admin, Thủ thư, Độc giả), 3 tác giả, 4 thể loại và 10 cuốn sách công nghệ/kinh tế thực tế.")
    builder.add_bullet("Bước 3 (Lập trình Lớp Dịch vụ Nghiệp vụ): ", "Sử dụng Prompt P05 để sinh `services/borrow_service.py` với đầy đủ logic kiểm tra nợ phạt, khóa tồn kho và tính phạt trễ hạn 2000đ/ngày.")
    builder.add_bullet("Bước 4 (Xây dựng API Routers & Xác thực JWT): ", "Yêu cầu AI sinh các router FastAPI: `auth.py`, `books.py`, `readers.py`, `borrows.py`, `statistics.py` có gắn middleware `get_current_user`.")
    builder.add_bullet("Bước 5 (Tích hợp AI & Thiết kế Prompt Templates): ", "Sử dụng Prompt P07, P08, P09 để sinh `services/ai_service.py` và các template trong `prompts/`. Cấu hình Mock Fallback nếu chưa có Gemini Key.")
    builder.add_bullet("Bước 6 (Hiện thực hóa Giao diện Web): ", "Sử dụng Prompt P06 để tạo file `frontend/static/css/main.css` và các trang HTML templates trong `frontend/templates/`.")
    builder.add_bullet("Bước 7 (Tự động hóa Kiểm thử & Đóng gói): ", "Sử dụng Prompt P10 và P12 để sinh bộ 26 ca test Pytest và cấu hình Dockerfile/docker-compose.yml hoàn chỉnh.")

    builder.add_heading_2("D.3. Danh Mục Kiểm Tra Chất Lượng Mã Nguồn AI (Verification Checklist)")
    builder.add_paragraph(
        "Trước khi tích hợp bất kỳ đoạn mã nào do AI sinh ra vào dự án chính thức, kỹ sư bắt buộc phải kiểm tra qua 5 tiêu chí sau:",
        bold_prefix="Quy trình thẩm định: "
    )
    builder.add_bullet("Tiêu chí 1 (Transaction Integrity): ", "Các thao tác cập nhật dữ liệu đa bảng (ví dụ: tạo phiếu mượn + giảm tồn kho) đã nằm trong khối try-commit-except-rollback chưa?")
    builder.add_bullet("Tiêu chí 2 (Boundary Safeguards): ", "Có chặn triệt để số lượng sách khả dụng không bị âm hoặc không vượt quá tổng số sở hữu không?")
    builder.add_bullet("Tiêu chí 3 (Data Sanitization & Privacy): ", "Có loại bỏ 100% dữ liệu PII (họ tên, điện thoại độc giả) trước khi gọi các hàm AI không?")
    builder.add_bullet("Tiêu chí 4 (Zero-Hallucination Constraints): ", "Prompt gửi cho LLM có rào chắn phủ định cấm bịa đặt thông tin sách không?")
    builder.add_bullet("Tiêu chí 5 (Automated Test Pass): ", "Chạy lệnh `pytest tests/ -v` có đạt 100% PASSED (26/26 tests) không?")

    builder.doc.add_page_break()
