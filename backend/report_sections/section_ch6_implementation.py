"""
Chương 6: Cài đặt & Hiện thực hóa Giao diện (Phiên bản Mở rộng Chuyên sâu 100+ Trang)
Bao gồm: Cấu trúc mã nguồn, Router code, Design system tokens, JavaScript API & UI Controller, và 10 ảnh chụp màn hình UI thực tế kèm phân tích UX.
"""

import os

def build_chapter_6(builder, screenshots_dir):
    builder.add_heading_1("CHƯƠNG 6: CÀI ĐẶT & HIỆN THỰC HÓA GIAO DIỆN", chapter_num=6)

    # 6.1. Cấu trúc tổ chức mã nguồn
    builder.add_heading_2("6.1. Cấu trúc Tổ chức Mã nguồn Dự án")
    builder.add_paragraph(
        "Mã nguồn của hệ thống được tổ chức khoa học, module hóa chặt chẽ theo cấu trúc phân tầng chuẩn của FastAPI "
        "và giao diện Web tĩnh hiện đại:",
        bold_prefix="Tổ chức mã nguồn: "
    )

    source_tree = """library-management/
├── backend/
│   ├── main.py                  # Điểm khởi chạy ứng dụng FastAPI & Cấu hình Routers/Lifespan
│   ├── config.py                # Cấu hình biến môi trường (.env) và cài đặt JWT
│   ├── database.py              # Khởi tạo SQLAlchemy Engine, SessionLocal & Base Model
│   ├── dependencies.py          # FastAPI Dependencies (get_db, get_current_user, require_role)
│   ├── auth_utils.py            # Hàm tiện ích băm mật khẩu Bcrypt & tạo JWT Token
│   ├── schemas.py               # Toàn bộ Pydantic v2 Schemas cho Request/Response Validation
│   ├── seed_data.py             # Dữ liệu mẫu khởi tạo (20 sách, 8 tác giả, 5 thể loại, 3 tài khoản)
│   ├── models/                  # Định nghĩa các SQLAlchemy ORM Models (User, Book, Reader,...)
│   ├── routers/                 # Tầng điều khiển API (auth, books, readers, borrows, statistics, ai)
│   ├── services/                # Tầng nghiệp vụ xử lý logic (borrow_service, ai_service)
│   └── prompts/                 # Các khuôn mẫu System & User Prompt cho phân hệ AI
├── frontend/
│   ├── static/
│   │   ├── css/style.css        # Toàn bộ CSS Vanilla Modern Glassmorphism / White Theme
│   │   └── js/                  # Các module JavaScript xử lý gọi API và render giao diện
│   └── templates/               # Các trang HTML Jinja2 (dashboard, books, borrows, readers, ai, users)
├── docs/                        # Tài liệu kỹ thuật, sơ đồ diagrams PNG, ảnh chụp screenshots
├── tests/                       # Bộ kiểm thử tự động Pytest (test_borrow.py, test_ai.py)
├── Dockerfile                   # Kịch bản đóng gói Container ứng dụng
├── docker-compose.yml           # Cấu hình khởi chạy nhanh đa dịch vụ
└── requirements.txt             # Danh mục thư viện phụ thuộc Python"""

    builder.add_code_block(source_tree)

    # 6.2. Hiện thực hóa API & Middleware bảo mật
    builder.add_heading_2("6.2. Hiện thực hóa các API Endpoints và Middleware Bảo mật JWT")
    builder.add_paragraph(
        "Hệ thống triển khai cơ chế bảo mật xác thực người dùng thông qua giao thức JSON Web Token (JWT) "
        "và FastAPI Dependency Injection:",
        bold_prefix="Cơ chế bảo mật API: "
    )
    builder.add_bullet("Cơ chế xác thực (Authentication): ", "Khi người dùng đăng nhập thành công qua `POST /api/auth/login`, backend sinh token JWT có chứa `sub: user_id`, `role`, `exp` (hết hạn sau 60 phút) được ký bằng khóa bí mật `SECRET_KEY` theo thuật toán HS256.")
    builder.add_bullet("Dependency `get_current_user`: ", "Giải mã JWT token từ Header `Authorization: Bearer <token>`, kiểm tra chữ ký số và thời hạn hiệu lực, tự động truy vấn CSDL để lấy thông tin đối tượng User hiện tại.")
    builder.add_bullet("Dependency `require_role(['ADMIN', 'LIBRARIAN'])`: ", "Kiểm tra quyền hạn của người dùng trước khi cho phép thực thi endpoint. Nếu người dùng không đủ quyền, trả về mã lỗi HTTP 403 Forbidden.")

    builder.add_heading_3("6.2.1. Mã Nguồn Xử Lý Lập Phiếu Mượn Sách (`routers/borrows.py`)")
    builder.add_code_block(
        """@router.post(\"/\", response_model=BorrowRecordResponse, status_code=status.HTTP_201_CREATED)
def create_borrow_record(
    borrow_in: BorrowRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.LIBRARIAN]))
):
    \"\"\"Lập phiếu mượn sách - Chỉ Admin hoặc Librarian có quyền\"\"\"
    return BorrowService.borrow_book(
        db=db,
        reader_id=borrow_in.reader_id,
        book_id=borrow_in.book_id,
        librarian_id=current_user.id,
        notes=borrow_in.notes
    )"""
    )

    # 6.2.2. Design System & Frontend Architecture
    builder.add_heading_3("6.2.2. Thiết Kế Hệ Thống Giao Diện (Design System) & Vanilla CSS Tokens")
    builder.add_paragraph(
        "Giao diện sử dụng bộ biến CSS Design Tokens đồng nhất, tạo nên phong cách White Theme hiện đại "
        "kết hợp hiệu ứng kính mờ Glassmorphism cao cấp:"
    )
    builder.add_code_block(
        """:root {
    --primary-color: #4F46E5;       /* Indigo 600 */
    --primary-hover: #4338CA;       /* Indigo 700 */
    --secondary-color: #06B6D4;     /* Cyan 500 */
    --bg-main: #F8FAFC;             /* Slate 50 */
    --card-bg: rgba(255, 255, 255, 0.85); /* Glassmorphism Base */
    --card-border: rgba(226, 232, 240, 0.8);
    --backdrop-blur: blur(12px);
    --text-main: #0F172A;           /* Slate 900 */
    --text-muted: #64748B;          /* Slate 500 */
    --success: #10B981;             /* Emerald 500 */
    --warning: #F59E0B;             /* Amber 500 */
    --danger: #EF4444;              /* Rose 500 */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}"""
    )

    builder.add_heading_3("6.2.3. Hiện Thực Hóa JavaScript Client Gọi API Bất Đồng Bộ (`frontend/static/js/api.js`)")
    builder.add_paragraph(
        "Tầng giao tiếp API phía Client được thiết kế dạng wrapper module xử lý tự động đính kèm JWT Token và bắt lỗi mạng:"
    )
    builder.add_code_block(
        """const API = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('access_token');
        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            ...options.headers
        };

        try {
            const response = await fetch(endpoint, { ...options, headers });
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                window.location.href = '/login';
                return null;
            }
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Có lỗi xảy ra trong quá trình xử lý');
            }
            return data;
        } catch (error) {
            UI.showToast(error.message, 'danger');
            throw error;
        }
    }
};"""
    )

    # 6.3. Chi tiết giao diện người dùng & 10 Ảnh chụp thực tế
    builder.add_heading_2("6.3. Hiện thực hóa Giao diện Người dùng & Ảnh chụp Màn hình Thực tế")
    builder.add_paragraph(
        "Dưới đây là 10 màn hình giao diện thực tế của hệ thống Quản lý Thư viện AI, được chụp trực tiếp từ máy chủ "
        "vận hành trên nền giao diện sáng (White Theme Glassmorphism) với đầy đủ dữ liệu mẫu:",
        bold_prefix="Giao diện người dùng: "
    )

    # UI 1: Login
    builder.add_heading_3("6.3.1. Giao diện Đăng nhập & Đăng ký Tài khoản (ui_01_login.png)")
    builder.add_paragraph(
        "Màn hình đăng nhập được thiết kế tinh tế với nền chuyển màu mượt mà, khung đăng nhập kính mờ (Glassmorphism), "
        "tích hợp sẵn 3 nút đăng nhập nhanh tài khoản Demo (Admin, Thủ thư, Độc giả). Hỗ trợ chuyển đổi mượt sang tab Đăng ký tài khoản mới."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_01_login.png"),
        "Giao diện Đăng nhập Hệ thống có hỗ trợ Demo Accounts (ui_01_login.png)"
    )

    # UI 2: Dashboard
    builder.add_heading_3("6.3.2. Giao diện Dashboard Tổng quan & Biểu đồ Thống kê (ui_02_dashboard.png)")
    builder.add_paragraph(
        "Màn hình trung tâm quản trị: 4 thẻ thống kê số liệu quan trọng (Tổng sách, Sách đang mượn, Độc giả, Phiếu quá hạn) "
        "với biểu tượng màu sắc trực quan; Biểu đồ đường (Line Chart) xu hướng mượn sách theo tháng và Biểu đồ tròn (Doughnut Chart) "
        "tỷ lệ phân bố thể loại sách được tích hợp mượt mà qua thư viện Chart.js."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_02_dashboard.png"),
        "Giao diện Dashboard Tổng quan với Thẻ KPI và Biểu đồ Thống kê Trực quan (ui_02_dashboard.png)"
    )

    # UI 3: Books
    builder.add_heading_3("6.3.3. Giao diện Quản lý Kho Sách & Bộ lọc Tìm kiếm (ui_03_books.png)")
    builder.add_paragraph(
        "Danh mục quản lý kho sách: Bảng dữ liệu hiển thị mã sách, tên sách, tác giả, thể loại, nhà xuất bản, năm, "
        "số lượng khả dụng / tổng số, nhãn trạng thái (Còn sách / Hết sách). Cung cấp thanh tìm kiếm tức thời đa trường, "
        "bộ lọc theo thể loại, nút 'Thêm sách mới', 'Xuất CSV' và các nút thao tác chi tiết / sửa / xóa trên từng dòng."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_03_books.png"),
        "Giao diện Quản lý Kho Sách kèm Bộ lọc và Thao tác CRUD (ui_03_books.png)"
    )

    # UI 4: Readers
    builder.add_heading_3("6.3.4. Giao diện Quản lý Hồ sơ Độc giả & Thẻ Thư viện (ui_04_readers.png)")
    builder.add_paragraph(
        "Quản lý hồ sơ độc giả: Hiển thị mã thẻ, họ tên, email, số điện thoại, loại độc giả (Sinh viên / Giảng viên), "
        "ngày hết hạn thẻ và nhãn trạng thái (Active / Expired / Suspended). Cho phép thủ thư cấp thẻ mới, chỉnh sửa thông tin "
        "hoặc khóa thẻ độc giả có vi phạm chỉ bằng 1 thao tác."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_04_readers.png"),
        "Giao diện Quản lý Hồ sơ Độc giả và Trạng thái Thẻ Thư viện (ui_04_readers.png)"
    )

    # UI 5: Borrows
    builder.add_heading_3("6.3.5. Giao diện Mượn / Trả Sách & Xử lý Phiếu Mượn (ui_05_borrows.png)")
    builder.add_paragraph(
        "Khu vực xử lý mượn/trả: Biểu mẫu tạo phiếu mượn nhanh (nhập ID độc giả và ID sách), danh sách phiếu mượn đang lưu hành, "
        "thông tin ngày mượn, hạn trả, số lần gia hạn. Cảnh báo màu đỏ nổi bật cho các phiếu quá hạn và nút 'Trả sách' thao tác tức thì."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_05_borrows.png"),
        "Giao diện Lập Phiếu Mượn và Nhận Trả Sách tại Quầy (ui_05_borrows.png)"
    )

    # UI 6: Fines
    builder.add_heading_3("6.3.6. Giao diện Quản lý & Thu Tiền Phạt Quá Hạn (ui_06_fines.png)")
    builder.add_paragraph(
        "Tab quản lý phạt: Thống kê chi tiết các khoản phạt quá hạn phát sinh tự động khi trả sách trễ hạn (2.000 VNĐ/ngày). "
        "Hiển thị tên độc giả, mã phiếu, số ngày quá hạn, tổng tiền và trạng thái (PENDING / PAID / WAIVED). "
        "Nút xử lý thanh toán 'Thu tiền' hoặc 'Miễn giảm' phục hồi quyền mượn sách cho độc giả."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_06_fines.png"),
        "Giao diện Quản lý và Xử lý Thu / Miễn Tiền Phạt Quá Hạn (ui_06_fines.png)"
    )

    # UI 7: Reservations
    builder.add_heading_3("6.3.7. Giao diện Quản lý Đặt Trước Sách (ui_07_reservations.png)")
    builder.add_paragraph(
        "Quản lý hàng đợi đặt trước: Hiển thị danh sách các đơn đặt trước của độc giả khi sách hết bản khả dụng. "
        "Thể hiện rõ thứ tự ưu tiên thời gian, ngày hết hạn giữ chỗ (7 ngày) và nhãn trạng thái (PENDING / READY / COMPLETED). "
        "Tự động chuyển sang READY khi có độc giả khác trả sách về kho."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_07_reservations.png"),
        "Giao diện Quản lý Hàng đợi Đặt Trước Sách (ui_07_reservations.png)"
    )

    # UI 8: Statistics
    builder.add_heading_3("6.3.8. Giao diện Báo cáo Thống kê Chuyên sâu & Xuất CSV (ui_08_statistics.png)")
    builder.add_paragraph(
        "Trung tâm báo cáo quản trị: Bảng xếp hạng Top 10 cuốn sách được mượn nhiều nhất, Top 10 độc giả tích cực nhất, "
        "Báo cáo sách quá hạn cần thu hồi và Tổng hợp doanh thu tiền phạt. Tích hợp các nút xuất báo cáo ra file CSV mã hóa UTF-8-BOM."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_08_statistics.png"),
        "Giao diện Báo cáo Thống kê Nghiệp vụ và Xuất Báo cáo CSV (ui_08_statistics.png)"
    )

    # UI 9: AI Chatbot
    builder.add_heading_3("6.3.9. Giao diện Trợ lý AI Chatbot & Gợi ý Sách Thông minh (ui_09_ai_chatbot.png)")
    builder.add_paragraph(
        "Không gian tương tác AI: Cung cấp khung chat trực quan cho phép độc giả đặt câu hỏi tự nhiên bằng tiếng Việt, "
        "hiển thị phản hồi thân thiện từ Gemini 1.5 Flash kèm các thẻ Card sách tương tác trực tiếp (hình ảnh, tên sách, tác giả, "
        "tình trạng còn/hết và nút xem chi tiết tóm tắt)."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_09_ai_chatbot.png"),
        "Giao diện Trợ lý AI Chatbot Đối thoại và Gợi ý Sách (ui_09_ai_chatbot.png)"
    )

    # UI 10: Users
    builder.add_heading_3("6.3.10. Giao diện Quản trị viên Phân quyền Tài khoản (ui_10_users.png)")
    builder.add_paragraph(
        "Phân hệ quản trị User dành cho ADMIN: Quản lý danh sách toàn bộ người dùng trong hệ thống, phân quyền vai trò "
        "(ADMIN / LIBRARIAN / READER), tạo tài khoản thủ thư mới, đặt lại mật khẩu và khóa/mở khóa tài khoản bảo mật."
    )
    builder.add_image_with_caption(
        os.path.join(screenshots_dir, "ui_10_users.png"),
        "Giao diện Quản trị viên Quản lý Tài khoản và Phân quyền RBAC (ui_10_users.png)"
    )

    builder.doc.add_page_break()
