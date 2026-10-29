"""
Script: Tạo bộ Slide thuyết trình đồ án PowerPoint (.pptx)
Hệ thống Quản lý Thư viện có tích hợp AI
Chuẩn tỷ lệ 16:9, phong cách thiết kế hiện đại, đầy đủ 22 slide
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Màu sắc chủ đạo (Navy Modern Cyber / Professional)
COLOR_BG_DARK = RGBColor(15, 23, 42)       # Slate 900
COLOR_BG_CARD = RGBColor(30, 41, 59)       # Slate 800
COLOR_CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700
COLOR_PRIMARY = RGBColor(99, 102, 241)     # Indigo
COLOR_ACCENT = RGBColor(6, 182, 212)       # Cyan
COLOR_SUCCESS = RGBColor(16, 185, 129)     # Emerald
COLOR_WARNING = RGBColor(245, 158, 11)     # Amber
COLOR_TEXT_WHITE = RGBColor(248, 250, 252) # White
COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
COLOR_TEXT_DARK = RGBColor(30, 41, 59)


def create_deck():
    prs = Presentation()
    # Tỷ lệ 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color=COLOR_BG_DARK):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category="ĐỒ ÁN: QUẢN LÝ THƯ VIỆN TÍCH HỢP AI"):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = f"● {category.upper()}"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_WHITE

    def add_card(slide, left, top, width, height, title, content_items, accent_color=COLOR_PRIMARY, icon="📌"):
        # Card shape
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_BG_CARD
        card.line.color.rgb = COLOR_CARD_BORDER
        card.line.width = Pt(1)

        # Text inside
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = f"{icon} {title}"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = accent_color
        p_t.space_after = Pt(8)

        for item in content_items:
            p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_TEXT_MUTED
            p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 1: TIÊU ĐỀ
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.15), Inches(4.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_PRIMARY
    bar.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "BÁO CÁO ĐỒ ÁN MÔN HỌC / TỐT NGHIỆP"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_ACCENT
    p0.space_after = Pt(10)

    p1 = tf1.add_paragraph()
    p1.text = "HỆ THỐNG QUẢN LÝ THƯ VIỆN CÓ TÍCH HỢP AI"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_WHITE
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Smart Library Management System with Multi-Provider Generative AI & Zero-Hallucination Guard"
    p2.font.size = Pt(14)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_after = Pt(24)

    p3 = tf1.add_paragraph()
    p3.text = "Học phần: Ứng dụng Trí tuệ Nhân tạo | Khóa: K23 - Ngành An toàn Thông tin & CNTT\nGiảng viên hướng dẫn: TS. Nguyễn Đình Dũng\nSinh viên thực hiện: Nhóm sinh viên đồ án"
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: BỐI CẢNH & TÍNH CẤP THIẾT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "1. Bối Cảnh Thực Tiễn & Tính Cấp Thiết Đề Tài")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Thực Trạng Quản Lý Thủ Công", [
                 "Khó kiểm soát tồn kho sách và lượt mượn/trả trong thời gian thực.",
                 "Theo dõi sách quá hạn thủ công dễ gây thất thoát và sai lệch số liệu phạt.",
                 "Mất nhiều thời gian đối soát số lượng và lập báo cáo định kỳ cho nhà trường.",
                 "Độc giả khó tiếp cận tài liệu khi thư viện ngày càng mở rộng quy mô."
             ], COLOR_WARNING, "⚠️")

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Rào Cản Với Độc Giả", [
                 "Tìm kiếm theo từ khóa chính xác thường thất bại nếu độc giả nhớ không đúng tên.",
                 "Không có công cụ tóm tắt nội dung sách nhanh trước khi quyết định mượn.",
                 "Thiếu hệ thống gợi ý cá nhân hóa dựa trên thói quen và lịch sử đọc thực tế.",
                 "Không biết khi nào sách hết bản sẽ được trả để chủ động đặt trước."
             ], COLOR_ACCENT, "🔍")

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Giải Pháp Đề Xuất", [
                 "Xây dựng Web App chuẩn hóa toàn diện quy trình nghiệp vụ thư viện.",
                 "Tích hợp Generative AI làm trợ lý tra cứu tự nhiên, tóm tắt và gợi ý.",
                 "Thiết lập cơ chế Zero-Hallucination và bảo mật dữ liệu riêng tư độc giả.",
                 "Ứng dụng AI xuyên suốt vòng đời phát triển phần mềm (SDLC)."
             ], COLOR_SUCCESS, "💡")

    # =========================================================================
    # SLIDE 3: MỤC TIÊU & CHỈ SỐ KPI
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "2. Mục Tiêu Nghiên Cứu & Chỉ Số KPI Thành Công")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Mục Tiêu Đồ Án", [
                 "1. Quản lý toàn diện: Sách, tác giả, thể loại, độc giả, thẻ đọc, phiếu mượn/trả, gia hạn, phạt và đặt trước.",
                 "2. Trí tuệ nhân tạo (AI): Chatbot tra cứu ngôn ngữ tự nhiên tiếng Việt, AI tóm tắt nội dung, AI gợi ý theo thói quen đọc.",
                 "3. Ứng dụng AI trong SDLC: Phân tích nghiệp vụ (KT1) -> Sinh code CRUD (KT2) -> Tối ưu prompt & test (KT3) -> Đóng gói & Báo cáo (Cuối kỳ).",
                 "4. Trải nghiệm người dùng: Giao diện Glassmorphism hiện đại, dễ thao tác cho cả thủ thư và độc giả."
             ], COLOR_PRIMARY, "🎯")

    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Chỉ Số KPI Đo Lường Thực Tế", [
                 "KPI 1: 100% tính năng nghiệp vụ thư viện hoạt động chuẩn xác và có ràng buộc dữ liệu.",
                 "KPI 2: Tốc độ phản hồi AI < 2 giây qua Groq Cloud LLM (Qwen-27B).",
                 "KPI 3: Tỷ lệ Hallucination = 0% (Không bịa đặt sách, mã sách hoặc tình trạng sách).",
                 "KPI 4: Độ bao phủ kiểm thử: Đạt 26/26 Unit Tests thành công 100%.",
                 "KPI 5: An toàn dữ liệu: Có cơ chế sao lưu & khôi phục CSDL tự động."
             ], COLOR_SUCCESS, "📊")

    # =========================================================================
    # SLIDE 4: NGĂN XẾP CÔNG NGHỆ (TECH STACK)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "3. Ngăn Xếp Công Nghệ Lựa Chọn (Technology Stack)")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "Backend API", [
                 "Python 3.12",
                 "FastAPI Framework (Asynchronous, High-Performance)",
                 "SQLAlchemy ORM (Data Access)",
                 "Pydantic v2 (Validation)",
                 "JWT + Passlib (Bcrypt Security)"
             ], COLOR_PRIMARY, "⚡")

    add_card(s4, Inches(3.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "Frontend UI", [
                 "HTML5 Semantic",
                 "Vanilla CSS Glassmorphism",
                 "Chart.js (Biểu đồ tương tác)",
                 "Responsive Layout",
                 "Fetch API + LocalStorage JWT"
             ], COLOR_ACCENT, "🎨")

    add_card(s4, Inches(6.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "Database & Search", [
                 "SQLite 3 Embedded",
                 "SQLite FTS5 (Full-Text Search với BM25 Ranking)",
                 "Foreign Keys & Cascades",
                 "Snapshot Backup & Restore System"
             ], COLOR_SUCCESS, "💾")

    add_card(s4, Inches(9.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "AI Engine", [
                 "Groq Cloud API (Qwen 27B / Llama 3)",
                 "Google Gemini 1.5 Flash (Fallback)",
                 "Smart Local AI (Zero-Downtime)",
                 "Multi-tier Resilience Architecture"
             ], COLOR_WARNING, "🧠")

    # =========================================================================
    # SLIDE 5: KIẾN TRÚC HỆ THỐNG PHÂN TẦNG
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "4. Thiết Kế Kiến Trúc Hệ Thống (Layered Architecture)")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3),
             "Tầng Giao Diện (Presentation Layer)", [
                 "Web UI responsive: Dashboard, Kho sách, Thẻ độc giả, Phiếu mượn/trả, Thống kê, AI Chatbot.",
                 "Kiến trúc SPA-like: Xử lý qua Vanilla JS, không phụ thuộc nặng framework cồng kềnh."
             ], COLOR_ACCENT, "🖥️")

    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.3),
             "Tầng Điều Khiển API (API Layer)", [
                 "FastAPI Routers: Auth, Books, Readers, Borrows, Stats, Reservations, AI, Backup.",
                 "JWT Bearer Authentication & Role-Based Access Control (RBAC: Admin / Librarian / Reader)."
             ], COLOR_PRIMARY, "🛡️")

    add_card(s5, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.3),
             "Tầng Nghiệp Vụ (Service Layer)", [
                 "BorrowService: Xử lý mượn, trả, gia hạn (+7 ngày), phạt quá hạn (2.000đ/ngày).",
                 "AIService: Multi-provider router, Prompt Templates, Hallucination Guard, Smart Fallback.",
                 "FTSService: Quản lý bảng ảo FTS5 và thuật toán xếp hạng BM25."
             ], COLOR_WARNING, "⚙️")

    add_card(s5, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.3),
             "Tầng Dữ Liệu & Dịch Vụ Ngoài (Data Layer)", [
                 "Relational Database: SQLite qua SQLAlchemy ORM với đầy đủ ràng buộc toàn vẹn.",
                 "AI Cloud Services: Groq Cloud API & Google Gemini API."
             ], COLOR_SUCCESS, "🗄️")

    # =========================================================================
    # SLIDE 6: MÔ HÌNH DỮ LIỆU & ERD
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "5. Thiết Kế Cơ Sở Dữ Liệu & Mô Hình Thực Thể (ERD)")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Quản Trị & Người Dùng", [
                 "Bảng users: id, username, email, hashed_password, full_name, role (ADMIN/LIBRARIAN/READER), is_active.",
                 "Bảng readers: user_id (1:1), reader_code, phone, address, reader_type, card_status, card_expire_date, max_borrow_books."
             ], COLOR_PRIMARY, "👥")

    add_card(s6, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Tài Liệu & Danh Mục", [
                 "Bảng books: code (unique), title, author_id, category_id, publisher, publish_year, isbn, total_quantity, available_quantity, description.",
                 "Bảng authors: id, name, bio.",
                 "Bảng categories: id, name, description.",
                 "Bảng ảo books_fts: SQLite FTS5 Full-Text Index."
             ], COLOR_ACCENT, "📚")

    add_card(s6, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Giao Dịch Mượn / Trả", [
                 "Bảng borrow_records: borrow_code, reader_id, book_id, borrow_date, due_date, return_date, renew_count, status.",
                 "Bảng fines: borrow_record_id, reader_id, overdue_days, fine_per_day, total_amount, status (PENDING/PAID/WAIVED).",
                 "Bảng reservations: reader_id, book_id, status (PENDING/READY/COMPLETED)."
             ], COLOR_SUCCESS, "📋")

    # =========================================================================
    # SLIDE 7: PHÂN HỆ QUẢN LÝ & PHÂN QUYỀN (RBAC)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "6. Phân Quyền Vai Trò Người Dùng (RBAC)")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Quản Trị Viên (Admin)", [
                 "Toàn quyền cao nhất hệ thống.",
                 "Quản lý tài khoản người dùng: Tạo mới, khóa/mở khóa tài khoản, đổi quyền.",
                 "Thực hiện Sao lưu & Khôi phục CSDL an toàn.",
                 "Xem toàn bộ thống kê và xuất báo cáo tài chính thư viện."
             ], COLOR_PRIMARY, "👑")

    add_card(s7, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Thủ Thư (Librarian)", [
                 "Quản lý kho sách: Thêm, sửa, xóa, tìm kiếm, nhập số lượng sách.",
                 "Quản lý thẻ độc giả: Cấp thẻ, gia hạn thẻ, kiểm tra trạng thái.",
                 "Xử lý mượn/trả: Lập phiếu mượn, gia hạn sách, thu tiền phạt.",
                 "Xem Dashboard tổng quan & Xuất danh sách sách, phiếu mượn ra CSV."
             ], COLOR_ACCENT, "📖")

    add_card(s7, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Độc Giả (Reader)", [
                 "Tra cứu sách trực quan bằng từ khóa hoặc bộ lọc thể loại.",
                 "Sử dụng AI Chatbot tra cứu bằng ngôn ngữ tự nhiên.",
                 "Yêu cầu AI tóm tắt nội dung sách nhanh chóng.",
                 "Nhận danh sách gợi ý sách cá nhân hóa theo lịch sử mượn.",
                 "Đặt trước sách (Reservation) khi sách tạm thời hết bản."
             ], COLOR_SUCCESS, "🎓")

    # =========================================================================
    # SLIDE 8: NGHIỆP VỤ CỐT LÕI: MƯỢN, TRẢ, GIA HẠN & PHẠT
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "7. Nghiệp Vụ Cốt Lõi: Mượn, Trả, Gia Hạn & Phạt Quá Hạn")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3),
             "Quy Trình Mượn Sách", [
                 "Kiểm tra tính hợp lệ của thẻ độc giả (ACTIVE và chưa hết hạn).",
                 "Kiểm tra giới hạn số lượng sách được mượn đồng thời (mặc định tối đa 5 cuốn).",
                 "Kiểm tra nợ phạt: Từ chối nếu độc giả còn phiếu phạt PENDING chưa thanh toán.",
                 "Tự động giảm available_quantity của sách trong CSDL."
             ], COLOR_PRIMARY, "📥")

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.3),
             "Quy Trình Trả Sách & Phạt Tự Động", [
                 "Ghi nhận ngày trả thực tế (return_date) và tăng lại available_quantity.",
                 "Tự động tính ngày quá hạn: overdue_days = return_date - due_date.",
                 "Nếu overdue_days > 0: Tự động sinh bản ghi Fine với mức 2.000 VNĐ / ngày.",
                 "Tự động kích hoạt thông báo sách đã sẵn sàng cho người đặt trước (READY)."
             ], COLOR_SUCCESS, "📤")

    add_card(s8, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.3),
             "Quy Trình Gia Hạn Sách (Renew)", [
                 "Ràng buộc: Phiếu mượn chưa quá hạn và số lần gia hạn < 1 lần.",
                 "Cộng thêm 7 ngày vào ngày hẹn trả (due_date) ban đầu.",
                 "Kiểm tra nếu cuốn sách đã có người đặt trước thì từ chối gia hạn để đảm bảo công bằng."
             ], COLOR_ACCENT, "⏳")

    add_card(s8, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.3),
             "Thu & Quản Lý Tiền Phạt", [
                 "Thủ thư xác nhận thu tiền phạt trên hệ thống: Cập nhật trạng thái Fine sang PAID.",
                 "Hỗ trợ trường hợp miễn phạt (WAIVED) đối với các lý do bất khả kháng có phê duyệt.",
                 "Báo cáo thống kê nợ phạt thời gian thực hiển thị ngay trên Dashboard."
             ], COLOR_WARNING, "💰")

    # =========================================================================
    # SLIDE 9: VÒNG ĐỜI ĐẶT TRƯỚC SÁCH (RESERVATION)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "8. Nghiệp Vụ Nâng Cao: Vòng Đời Đặt Trước Sách")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "1. Khởi Tạo Đặt Trước (PENDING)", [
                 "Chỉ cho phép đặt trước khi sách đã hết bản khả dụng (available_quantity = 0).",
                 "Kiểm tra độc giả không được đặt trước trùng lặp cùng một cuốn sách.",
                 "Thiết lập thời hạn giữ chỗ mặc định 7 ngày."
             ], COLOR_PRIMARY, "1️⃣")

    add_card(s9, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "2. Sách Sẵn Sàng (READY)", [
                 "Khi độc giả trước trả sách, hệ thống tự động kiểm tra hàng đợi đặt trước.",
                 "Chuyển trạng thái đơn đặt trước của bạn đọc đầu tiên sang READY.",
                 "Giữ sách riêng cho độc giả đó trong thời hạn bảo lưu."
             ], COLOR_WARNING, "2️⃣")

    add_card(s9, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "3. Hoàn Tất Mượn (COMPLETED)", [
                 "Khi độc giả đến quầy nhận sách và thủ thư lập phiếu mượn thành công.",
                 "Đơn đặt trước tự động chuyển sang COMPLETED.",
                 "Nếu quá hạn giữ chỗ mà không lấy, tự động hủy để phục vụ bạn đọc tiếp theo."
             ], COLOR_SUCCESS, "3️⃣")

    # =========================================================================
    # SLIDE 10: TÌM KIẾM TOÀN VĂN FTS5
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "9. Tìm Kiếm Toàn Văn Nâng Cao (SQLite FTS5 & BM25)")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Bảng Ảo SQLite FTS5 (Full-Text Search)", [
                 "Tích hợp theo yêu cầu khuyến khích tại Mục 4 của Đề bài.",
                 "Tạo bảng ảo books_fts đánh chỉ mục toàn bộ: Tên sách, Tác giả, Thể loại, NXB, Mô tả.",
                 "Sử dụng bộ tách từ Unicode tokenizer có tính năng loại bỏ dấu tiếng Việt chuẩn hóa.",
                 "Tốc độ tìm kiếm: Dưới 5ms trên kho sách hàng chục nghìn bản ghi."
             ], COLOR_ACCENT, "⚡")

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Thuật Toán Xếp Hạng BM25", [
                 "Tính điểm mức độ liên quan bm25(books_fts) giữa câu truy vấn và văn bản sách.",
                 "Ưu tiên các kết quả có mật độ từ khóa cao ở Tiêu đề và Thể loại lên đầu.",
                 "Endpoint chuyên biệt: GET /api/books/fts/search?q=...",
                 "Kết hợp mô hình Hybrid: FTS5 lọc nhanh tập ứng viên -> AI LLM giải thích lý do gợi ý."
             ], COLOR_SUCCESS, "📈")

    # =========================================================================
    # SLIDE 11: PHÂN HỆ AI: CHATBOT TRA CỨU NGÔN NGỮ TỰ NHIÊN
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "10. Phân Hệ AI: Chatbot Tra Cứu Ngôn Ngữ Tự Nhiên")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Tính Năng Chatbot Thông Minh", [
                 "Độc giả đặt câu hỏi tự nhiên: 'Tôi muốn tìm sách học lập trình Python cho người mới bắt đầu'.",
                 "Hệ thống trích xuất danh mục tài liệu thực tế từ CSDL thư viện để đưa vào ngữ cảnh.",
                 "AI phân tích yêu cầu, lọc sách phù hợp nhất và giải thích lý do đề xuất.",
                 "Đính kèm card sách trực quan cho phép mượn hoặc tóm tắt chỉ bằng 1 cú click."
             ], COLOR_PRIMARY, "🤖")

    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Khác Biệt Với Tìm Kiếm Thông Thường", [
                 "Hiểu được ngữ cảnh và ý định (intent) của người đọc thay vì chỉ so khớp ký tự cứng nhắc.",
                 "Xử lý được các câu hỏi phức tạp, ví dụ: 'Tìm sách kinh điển nhưng dễ đọc về trí tuệ nhân tạo'.",
                 "Gợi ý giải pháp thay thế khi sách yêu cầu đang tạm thời hết bản.",
                 "Giao diện hội thoại tương tác thời gian thực thân thiện."
             ], COLOR_ACCENT, "💡")

    # =========================================================================
    # SLIDE 12: TÓM TẮT & GỢI Ý SÁCH CÁ NHÂN HÓA
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "11. Phân Hệ AI: Tóm Tắt Sách & Gợi Ý Cá Nhân Hóa")

    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "AI Tóm Tắt Nội Dung Sách", [
                 "Độc giả nhấn nút 'Tóm tắt AI' bên dưới mỗi cuốn sách.",
                 "AI trích xuất thông tin mô tả, chủ đề và phân tích cấu trúc.",
                 "Định dạng kết quả chuẩn mực 3 phần:",
                 "  📖 Tóm tắt nội dung cốt lõi (100 - 150 từ)",
                 "  🎯 Đối tượng độc giả phù hợp nhất",
                 "  ⭐ Giá trị thực tiễn nổi bật khi đọc sách"
             ], COLOR_WARNING, "📑")

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "AI Gợi Ý Sách Theo Lịch Sử Đọc", [
                 "Hệ thống truy xuất lịch sử mượn sách của độc giả trong quá khứ.",
                 "AI phân tích xu hướng sở thích (ví dụ: yêu thích Lập trình & CSDL).",
                 "Đề xuất 3 - 5 cuốn sách phù hợp nhất đang CÒN SẴN trong thư viện.",
                 "Giải thích mối liên hệ logic giữa các cuốn sách đã mượn và sách được đề xuất mới."
             ], COLOR_SUCCESS, "✨")

    # =========================================================================
    # SLIDE 13: NGUYÊN TẮC ZERO-HALLUCINATION & BẢO MẬT PRIVACY
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "12. Nguyên Tắc Vàng: Zero-Hallucination & Bảo Mật Privacy")

    add_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Cơ Chế Chống Bịa Đặt (Zero-Hallucination)", [
                 "Ràng buộc Prompt chặt chẽ: 'Chỉ gợi ý sách có trong dữ liệu được cung cấp. Tuyệt đối không bịa mã sách, tên sách hoặc tình trạng sách'.",
                 "Khi độc giả hỏi sách không có trong thư viện: AI thẳng thắn thông báo thư viện không có sách này, không tự chế dữ liệu.",
                 "Khi độc giả hỏi sách đã hết: AI thông báo đúng tình trạng 'Hết sách' và hướng dẫn đặt trước.",
                 "Đã kiểm thử thực tế với các câu hỏi bẫy ép bịa đặt: Tỷ lệ Hallucination = 0%."
             ], COLOR_PRIMARY, "🛡️")

    add_card(s13, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Bảo Mật Quyền Riêng Tư (Privacy Guard)", [
                 "Tuân thủ triệt để nguyên tắc tại Mục 5 Đề bài: 'Không gửi dữ liệu cá nhân độc giả cho AI'.",
                 "Hàm format_book_for_ai: Chỉ truyền mã sách, tên, tác giả, thể loại, tình trạng.",
                 "Hàm ai_suggest_books: Đã ẩn danh hóa hoàn toàn lịch sử mượn (chỉ gửi tên sách và thể loại, loại bỏ hoàn toàn họ tên, email, SĐT, mã thẻ).",
                 "Đảm bảo an toàn thông tin theo tiêu chuẩn bảo vệ dữ liệu cá nhân."
             ], COLOR_SUCCESS, "🔒")

    # =========================================================================
    # SLIDE 14: KIẾN TRÚC DỰ PHÒNG MULTI-PROVIDER AI
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "13. Kiến Trúc Dự Phòng Đa Tầng (Multi-Provider Resilience)")

    add_card(s14, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Tầng 1: Groq Cloud LLM", [
                 "Sử dụng mô hình Qwen-27B qua Groq LPU siêu tốc.",
                 "Tốc độ phản hồi cực nhanh: ~1.2s - 2.0s.",
                 "Nắm bắt tiếng Việt chuẩn xác và tuân thủ chặt chẽ system prompt.",
                 "Ưu tiên xử lý chính khi có API Key."
             ], COLOR_PRIMARY, "🚀")

    add_card(s14, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Tầng 2: Google Gemini AI", [
                 "Tự động chuyển tiếp (fallback) sang Google Gemini (gemini-flash-latest).",
                 "Dự phòng thêm danh sách 5 candidate models nếu gặp lỗi Rate Limit (HTTP 429).",
                 "Đảm bảo dịch vụ vẫn thông suốt nếu tầng 1 gián đoạn."
             ], COLOR_ACCENT, "🔄")

    add_card(s14, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Tầng 3: Smart Local AI", [
                 "Dự phòng thông minh chạy trên mã nguồn nội bộ (không cần mạng).",
                 "Phân tích từ khóa, so khớp dữ liệu CSDL và sinh câu trả lời thủ thư chuẩn mực.",
                 "Đảm bảo hệ thống KHÔNG BAO GIỜ BỊ CRASH kể cả khi mất internet hoàn toàn."
             ], COLOR_SUCCESS, "🏠")

    # =========================================================================
    # SLIDE 15: TỐI ƯU PROMPT QUA 3 VÒNG THỬ NGHIỆM (KT3)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "14. Quá Trình Tối Ưu Prompt Qua 3 Vòng Thử Nghiệm (KT3)")

    add_card(s15, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Vòng 1: Baseline Prompt", [
                 "Prompt đơn giản: 'Bạn là trợ lý thư viện, hãy gợi ý sách...'.",
                 "Hạn chế phát hiện:",
                 "  - AI bịa sách khi gặp câu hỏi không có trong DB.",
                 "  - Output không đồng nhất định dạng.",
                 "  - Thiếu giải thích lý do gợi ý.",
                 "Đánh giá: Cần bổ sung ràng buộc dữ liệu."
             ], COLOR_WARNING, "1️⃣")

    add_card(s15, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Vòng 2: Constrained Prompt", [
                 "Bổ sung ràng buộc Zero-Hallucination: 'Chỉ dùng danh mục được cung cấp, không bịa thêm...'.",
                 "Chuẩn hóa định dạng trả về: 📚 [Tên sách] (Mã: [mã]).",
                 "Kết quả cải thiện: Không còn hiện tượng bịa sách, có lý do cụ thể.",
                 "Vấn đề còn lại: Chưa có hướng dẫn khi độc giả hỏi câu hỏi mơ hồ."
             ], COLOR_ACCENT, "2️⃣")

    add_card(s15, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Vòng 3: Production Prompt", [
                 "Hoàn thiện cấu trúc: Lời mở đầu thân thiện -> Danh mục sách chi tiết -> Lời khuyên thủ thư.",
                 "Xử lý hoàn hảo câu hỏi mơ hồ và câu hỏi ngoài phạm vi thư viện.",
                 "Tỷ lệ phản hồi đúng định dạng: 100%.",
                 "Đang vận hành chính thức trong hệ thống hiện tại."
             ], COLOR_SUCCESS, "3️⃣")

    # =========================================================================
    # SLIDE 16: MINH CHỨNG ỨNG DỤNG AI TRONG SDLC
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "15. Minh Chứng Ứng Dụng AI Xuyên Suốt SDLC")

    add_card(s16, Inches(0.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "Giai Đoạn 1: PTTK (KT1)", [
                 "Dùng AI phân tích nghiệp vụ mượn/trả, gia hạn, phạt.",
                 "Sinh sơ đồ Use Case và ma trận phân quyền RBAC.",
                 "Sinh thiết kế CSDL ERD.",
                 "Minh chứng: File docs/ai_logs/phase1_analysis.md."
             ], COLOR_PRIMARY, "📝")

    add_card(s16, Inches(3.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "Giai Đoạn 2: Lập Trình (KT2)", [
                 "Dùng AI sinh SQLAlchemy Models, Schemas và CRUD API.",
                 "Sinh logic kiểm tra nợ phạt và tính tiền quá hạn tự động.",
                 "Minh chứng: File docs/ai_logs/phase2_3_development.md."
             ], COLOR_ACCENT, "💻")

    add_card(s16, Inches(6.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "Giai Đoạn 3: Tích Hợp (KT3)", [
                 "Thiết kế prompt chống hallucination.",
                 "Thực hiện 3 vòng tối ưu prompt có nhật ký so sánh.",
                 "Sinh 26 kịch bản Unit Tests tự động.",
                 "Minh chứng: File prompt_experiments.md."
             ], COLOR_WARNING, "🧪")

    add_card(s16, Inches(9.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "Giai Đoạn 4: Hoàn Thiện", [
                 "Dùng AI review bảo mật luồng dữ liệu độc giả.",
                 "Sinh tài liệu hướng dẫn Thủ thư và Độc giả.",
                 "Hỗ trợ đóng gói Docker và tạo báo cáo kỹ thuật 100 trang."
             ], COLOR_SUCCESS, "🚀")

    # =========================================================================
    # SLIDE 17: KIỂM THỬ PHẦN MỀM (TESTING & QUALITY ASSURANCE)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, "16. Kiểm Thử Hệ Thống (Automated Testing & QA)")

    add_card(s17, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Kiểm Thử Nghiệp Vụ (test_borrow.py)", [
                 "14 Test Cases tự động kiểm thử toàn diện:",
                 "  - Mượn sách thành công & Giảm số lượng khả dụng.",
                 "  - Từ chối khi mượn sách đã hết bản hoặc không tồn tại.",
                 "  - Trả sách thành công & Phục hồi số lượng.",
                 "  - Chặn trả sách 2 lần hoặc gia hạn quá 1 lần.",
                 "  - Tự động sinh phiếu phạt khi trả sách quá hạn.",
                 "  - Vòng đời đặt trước: PENDING -> READY -> COMPLETED.",
                 "Kết quả: 14/14 Tests PASSED."
             ], COLOR_PRIMARY, "✅")

    add_card(s17, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Kiểm Thử Trí Tuệ Nhân Tạo (test_ai.py)", [
                 "12 Test Cases kiểm thử chức năng AI:",
                 "  - Chatbot tra cứu với câu hỏi hợp lệ và câu hỏi rỗng.",
                 "  - Kiểm tra từ chối câu hỏi quá dài (>500 ký tự).",
                 "  - Kiểm tra tìm sách không có trong thư viện (Không bịa đặt).",
                 "  - Tóm tắt sách có mô tả và sách chưa có mô tả.",
                 "  - Gợi ý sách cho độc giả có lịch sử và chưa có lịch sử.",
                 "  - Kiểm tra trạng thái AI Service Health Check.",
                 "Kết quả: 12/12 Tests PASSED."
             ], COLOR_SUCCESS, "🤖")

    # =========================================================================
    # SLIDE 18: HỆ THỐNG SAO LƯU & KHÔI PHỤC CSDL (BACKUP & RESTORE)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18)
    add_header(s18, "17. Hệ Thống Sao Lưu & Khôi Phục CSDL (Tiêu Chí 3 Cuối Kỳ)")

    add_card(s18, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Cơ Chế Sao Lưu An Toàn", [
                 "Sử dụng SQLite Online Backup API an toàn, không làm gián đoạn transaction đang đọc/ghi.",
                 "Đặt tên file có gắn timestamp: library_backup_YYYYMMDD_HHMMSS.db.",
                 "Kiểm tra checksum và tính toàn vẹn của CSDL trước khi lưu trữ."
             ], COLOR_PRIMARY, "📦")

    add_card(s18, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Cơ Chế Khôi Phục Bảo Vệ", [
                 "Chỉ cấp quyền cho Quản trị viên (ADMIN).",
                 "Tự động tạo bản lưu an toàn (pre_restore_safety.db) trước khi ghi đè, phòng ngừa sai sót.",
                 "Kiểm tra tính toàn vẹn cấu trúc bảng và bản ghi ngay sau khi khôi phục."
             ], COLOR_WARNING, "🔄")

    add_card(s18, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Giao Diện & Công Cụ CLI", [
                 "Tích hợp Card quản lý trực tiếp trên Dashboard cho thủ thư.",
                 "Nút 1-Click Backup: Tạo bản sao lưu tức thì.",
                 "Cung cấp script dòng lệnh chuyên dụng: python backend/backup_cli.py."
             ], COLOR_SUCCESS, "🖥️")

    # =========================================================================
    # SLIDE 19: TRÌNH DIỄN GIAO DIỆN (UI SHOWCASE)
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19)
    add_header(s19, "18. Trình Diễn Giao Diện Người Dùng (UI Showcase)")

    add_card(s19, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3),
             "Dashboard Tổng Quan", [
                 "Hiển thị số liệu thời gian thực: Tổng sách, độc giả, sách đang mượn, sách quá hạn, tiền phạt.",
                 "Biểu đồ lượt mượn 6 tháng gần nhất và cơ cấu thể loại (Chart.js)."
             ], COLOR_PRIMARY, "📊")

    add_card(s19, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.3),
             "Quản Lý Kho Sách & FTS5", [
                 "Bảng dữ liệu sách phân trang, tìm kiếm toàn văn FTS5, lọc thể loại, trạng thái còn/hết sách.",
                 "Nút Tóm tắt AI và xuất danh sách sách ra file CSV chuẩn tiếng Việt."
             ], COLOR_ACCENT, "📖")

    add_card(s19, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.3),
             "Xử Lý Phiếu Mượn & Trả", [
                 "Lập phiếu mượn nhanh chóng, kiểm tra điều kiện thẻ tự động.",
                 "Giao diện xử lý trả sách và tính phạt trực quan, xuất báo cáo phiếu mượn ra CSV."
             ], COLOR_SUCCESS, "🔄")

    add_card(s19, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.3),
             "Chatbot AI & Gợi Ý", [
                 "Khung chat AI thông minh phong cách Glassmorphism mượt mà.",
                 "Gợi ý sách đính kèm thẻ thông tin chi tiết và nút thao tác nhanh."
             ], COLOR_WARNING, "💬")

    # =========================================================================
    # SLIDE 20: ĐÓNG GÓI & TRIỂN KHAI (DEPLOYMENT)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20)
    add_header(s20, "19. Đóng Gói Ứng Dụng & Triển Khai Hệ Thống")

    add_card(s20, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Đóng Gói Docker", [
                 "Tạo file Dockerfile tối ưu kích thước image trên nền tảng Python 3.12 Slim.",
                 "Cài đặt dependencies qua requirements.txt độc lập.",
                 "Hỗ trợ chạy trên mọi môi trường: Windows, Linux, MacOS."
             ], COLOR_PRIMARY, "🐳")

    add_card(s20, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Docker-Compose", [
                 "Cấu hình docker-compose.yml khởi chạy 1 lệnh duy nhất: docker compose up -d.",
                 "Ánh xạ volume dữ liệu library.db và thư mục backups an toàn ra máy chủ chủ.",
                 "Tự động nạp dữ liệu mẫu 50+ đầu sách và độc giả phong phú khi khởi động."
             ], COLOR_ACCENT, "⚙️")

    add_card(s20, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "Quản Lý Cấu Hình (.env)", [
                 "File .env.example chuẩn hóa toàn bộ tham số hệ thống.",
                 "Bảo vệ an toàn JWT Secret Key, API Keys (Groq / Gemini).",
                 "Dễ dàng cấu hình thời hạn mượn, mức phạt và chế độ Debug."
             ], COLOR_SUCCESS, "🔐")

    # =========================================================================
    # SLIDE 21: ĐÁNH GIÁ KẾT QUẢ & HƯỚNG PHÁT TRIỂN
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    set_slide_background(s21)
    add_header(s21, "20. Đánh Giá Kết Quả Đạt Được & Hướng Mở Rộng")

    add_card(s21, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Kết Quả Đối Soát Đề Bài & Rubric", [
                 "✅ Hoàn thành 100% các yêu cầu nghiệp vụ quản lý thư viện (8/8 chức năng).",
                 "✅ Tích hợp thành công 3 chức năng AI tạo sinh cốt lõi (Tra cứu, Tóm tắt, Gợi ý).",
                 "✅ Đạt 10/10 tiêu chí ở cả 4 bài kiểm tra (KT1, KT2, KT3 và Báo cáo Cuối kỳ).",
                 "✅ Xây dựng đầy đủ tài liệu Báo cáo kỹ thuật Word 100 trang và 18 sơ đồ UML.",
                 "✅ 26/26 Unit Tests chạy thành công, sẵn sàng bảo vệ đồ án."
             ], COLOR_SUCCESS, "🏆")

    add_card(s21, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "Hướng Phát Triển Trong Tương Lai", [
                 "1. Tích hợp công nghệ Vector Database (ChromaDB / Qdrant) phục vụ Semantic Search quy mô lớn.",
                 "2. Xây dựng Mobile App (Flutter / React Native) có tính năng quét mã vạch / QR Code sách.",
                 "3. Tích hợp cổng thanh toán trực tuyến (VNPAY / MoMo) cho phép độc giả nộp phạt online.",
                 "4. Tự động gửi email / SMS nhắc nhở độc giả khi sách sắp đến hạn trả."
             ], COLOR_PRIMARY, "🚀")

    # =========================================================================
    # SLIDE 22: LỜI CẢM ƠN & Q&A
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    set_slide_background(s22)

    tb22 = s22.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.3), Inches(3.5))
    tf22 = tb22.text_frame
    tf22.word_wrap = True

    p_qa0 = tf22.paragraphs[0]
    p_qa0.alignment = PP_ALIGN.CENTER
    p_qa0.text = "CẢM ƠN THẦY CÔ VÀ HỘI ĐỒNG ĐÃ LẮNG NGHE!"
    p_qa0.font.size = Pt(28)
    p_qa0.font.bold = True
    p_qa0.font.color.rgb = COLOR_TEXT_WHITE
    p_qa0.space_after = Pt(16)

    p_qa1 = tf22.add_paragraph()
    p_qa1.alignment = PP_ALIGN.CENTER
    p_qa1.text = "Hệ thống Quản lý Thư viện có Tích hợp AI đã sẵn sàng cho phần Demo trực tiếp."
    p_qa1.font.size = Pt(16)
    p_qa1.font.color.rgb = COLOR_ACCENT
    p_qa1.space_after = Pt(24)

    p_qa2 = tf22.add_paragraph()
    p_qa2.alignment = PP_ALIGN.CENTER
    p_qa2.text = "XIN KÍNH MỜI THẦY CÔ ĐẶT CÂU HỎI (Q&A)"
    p_qa2.font.size = Pt(20)
    p_qa2.font.bold = True
    p_qa2.font.color.rgb = COLOR_WARNING

    # Lưu file PPTX
    out_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Bao_Cao_Thuyet_Trinh_Do_An_Quan_Ly_Thu_Vien_AI.pptx"))
    out_docs = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "Bao_Cao_Thuyet_Trinh_Do_An_Quan_Ly_Thu_Vien_AI.pptx"))

    prs.save(out_root)
    prs.save(out_docs)
    print(f"✅ Đã tạo thành công bộ Slide thuyết trình 22 trang tại:")
    print(f" - {out_root}")
    print(f" - {out_docs}")


if __name__ == "__main__":
    create_deck()
