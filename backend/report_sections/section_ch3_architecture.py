"""
Chương 3: Phân tích & Thiết kế Hệ thống (Phiên bản Mở rộng Chuyên sâu 100+ Trang)
Bao gồm: Context diagram, Layered architecture, 6 Activity diagrams, 4 Sequence diagrams, State machine với phân tích luồng điều khiển và giao dịch dữ liệu chi tiết.
"""

import os

def build_chapter_3(builder, diagrams_dir):
    builder.add_heading_1("CHƯƠNG 3: PHÂN TÍCH & THIẾT KẾ HỆ THỐNG", chapter_num=3)

    # 3.1. Sơ đồ bối cảnh hệ thống
    builder.add_heading_2("3.1. Sơ đồ Bối cảnh Hệ thống (System Context Diagram)")
    builder.add_paragraph(
        "Sơ đồ bối cảnh hệ thống (Context Diagram - Mức 0) mô tả vị trí trung tâm của Hệ thống Quản lý Thư viện AI "
        "trong mối tương quan toàn diện với các tác nhân người dùng (Quản trị viên, Thủ thư, Độc giả) và các thực thể "
        "dịch vụ ngoại vi (Hệ quản trị CSDL SQLite / PostgreSQL, Dịch vụ Google Gemini AI 1.5 Flash).",
        bold_prefix="Mô tả ranh giới hệ thống: "
    )
    builder.add_paragraph(
        "Hệ thống đóng vai trò điều phối trung tâm: tiếp nhận các yêu cầu HTTP RESTful từ giao diện Web Client, "
        "thực thi xác thực bảo mật JWT, xử lý logic nghiệp vụ mượn/trả/phạt, tương tác với CSDL để bảo toàn dữ liệu ACID, "
        "và đóng gói các Prompt có cấu trúc ngữ cảnh để giao tiếp an toàn với mô hình ngôn ngữ lớn Google Gemini."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "01_context_diagram.png"),
        "Sơ đồ Bối cảnh Hệ thống Quản lý Thư viện Tích hợp AI (System Context Diagram)"
    )

    # 3.2. Sơ đồ Kiến trúc phân tầng
    builder.add_heading_2("3.2. Sơ đồ Kiến trúc Phân tầng Hệ thống (Layered Architecture)")
    builder.add_paragraph(
        "Để đảm bảo tính module hóa cao, khả năng mở rộng (Scalability), tính dễ bảo trì (Maintainability) và "
        "khả năng kiểm thử tự động độc lập, hệ thống được thiết kế theo mô hình Kiến trúc 4 tầng phân lập rõ ràng "
        "(Separation of Concerns):",
        bold_prefix="Thiết kế kiến trúc phân tầng: "
    )
    builder.add_bullet(
        "1. Tầng Trình diễn (Presentation Layer - Client): ",
        "Được xây dựng trên nền tảng HTML5, Vanilla CSS Modern Glassmorphism/White Theme và JavaScript module bất đồng bộ. "
        "Tầng này hoàn toàn độc lập với backend, giao tiếp với máy chủ 100% qua chuẩn JSON RESTful API. Tích hợp thư viện "
        "Chart.js để hiển thị biểu đồ phân tích dữ liệu thời gian thực và các hiệu ứng chuyển động vi mô (Micro-animations) "
        "giúp tối ưu hóa trải nghiệm người dùng."
    )
    builder.add_bullet(
        "2. Tầng Điều khiển API (API Routing & Controller Layer): ",
        "Xây dựng bằng framework FastAPI tốc độ cao, bao gồm 7 Router độc lập: `auth_router`, `books_router`, `readers_router`, "
        "`borrows_router`, `reservations_router`, `statistics_router`, `ai_router`. Tầng này chịu trách nhiệm điều hướng URL, "
        "kiểm tra chữ ký bảo mật JWT Token qua Middleware HTTPBearer, phân quyền vai trò người dùng (RBAC Dependency Injection) "
        "và xác thực tính hợp lệ của toàn bộ dữ liệu Request/Response thông qua các Schema Pydantic v2."
    )
    builder.add_bullet(
        "3. Tầng Nghiệp vụ (Service Layer): ",
        "Chứa toàn bộ các thuật toán và quy tắc nghiệp vụ cốt lõi: `BorrowService` (xử lý kiểm tra điều kiện mượn, giảm tồn kho, "
        "tự động phát hiện quá hạn, tính tiền phạt theo đơn giá ngày, gia hạn sách và chuyển trạng thái đơn đặt trước); `AIService` "
        "(quản lý vòng đời kết nối Gemini 1.5, cấu hình Timeout 15s, thuật toán Retry x2 với Exponential Backoff và kích hoạt Mock "
        "Fallback Engine khi ngắt mạng); và `Prompt Engine` (quản lý, định dạng các khuôn mẫu Prompt chuẩn hóa)."
    )
    builder.add_bullet(
        "4. Tầng Dữ liệu & Dịch vụ Ngoài (Data & External Services Layer): ",
        "Bao gồm hệ thống ánh xạ quan hệ đối tượng SQLAlchemy 2.0 ORM, kết nối linh hoạt tới Cơ sở Dữ liệu quan hệ SQLite (trong môi trường "
        "phát triển và kiểm thử) hoặc PostgreSQL/MySQL (trong môi trường Production). Đồng thời quản lý kết nối bảo mật HTTPS ra "
        "dịch vụ điện toán đám mây Google Gemini AI API."
    )

    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "16_system_architecture.png"),
        "Sơ đồ Kiến trúc Phân tầng Hệ thống (Layered Architecture Diagram)"
    )

    # 3.3. Bộ 6 Sơ đồ Hoạt động
    builder.add_heading_2("3.3. Bộ Sơ đồ Hoạt động Nghiệp vụ (Activity Diagrams)")
    builder.add_paragraph(
        "Các sơ đồ hoạt động (UML Activity Diagrams) dưới đây mô tả chi tiết từng bước rẽ nhánh điều kiện, xử lý ngoại lệ "
        "và luồng điều khiển trong các nghiệp vụ thư viện và tương tác AI:"
    )

    builder.add_heading_3("3.3.1. Sơ đồ Hoạt động Quy trình Mượn Sách tại Quầy")
    builder.add_paragraph(
        "Quy trình mượn sách mô tả 4 bước kiểm tra nghiêm ngặt: (1) Kiểm tra tính hợp lệ và thời hạn của thẻ độc giả; "
        "(2) Kiểm tra hạn mức số lượng sách đang mượn (< 5 cuốn); (3) Kiểm tra nợ phạt quá hạn chưa thanh toán; "
        "(4) Kiểm tra số lượng sách khả dụng trong kho (available_quantity > 0). Khi mọi điều kiện thỏa mãn, "
        "hệ thống tạo phiếu mượn với thời hạn 14 ngày, giảm số lượng sách khả dụng và cập nhật đơn đặt trước tương ứng."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "05_activity_borrow.png"),
        "Sơ đồ Hoạt động (Activity Diagram) Quy trình Mượn sách tại Quầy"
    )

    builder.add_heading_3("3.3.2. Sơ đồ Hoạt động Quy trình Trả Sách & Tính Phạt Quá Hạn")
    builder.add_paragraph(
        "Khi tiếp nhận trả sách, hệ thống cập nhật ngày trả thực tế và đổi trạng thái phiếu mượn sang RETURNED, "
        "đồng thời tăng số lượng khả dụng của sách lên 1. Nếu ngày trả vượt quá hạn trả (due_date), hệ thống "
        "tự động tính số ngày quá hạn và phát sinh bản ghi phạt với mức 2.000 VNĐ/ngày. Sau đó, hệ thống kiểm tra "
        "hàng đợi đặt trước và chuyển đơn sớm nhất sang trạng thái READY."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "06_activity_return.png"),
        "Sơ đồ Hoạt động (Activity Diagram) Quy trình Trả sách và Tự động Tính phạt Quá hạn"
    )

    builder.add_heading_3("3.3.3. Sơ đồ Hoạt động Quy trình Gia Hạn Sách (+7 ngày)")
    builder.add_paragraph(
        "Quy trình gia hạn đảm bảo 3 điều kiện: (1) Phiếu mượn đang ở trạng thái BORROWING và chưa quá hạn; "
        "(2) Phiếu mượn chưa từng gia hạn trước đó (renew_count = 0); (3) Sách không có người khác đặt trước. "
        "Khi thỏa mãn, hạn trả được cộng thêm 7 ngày và số lần gia hạn được cập nhật thành 1."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "07_activity_renew.png"),
        "Sơ đồ Hoạt động (Activity Diagram) Quy trình Gia hạn Sách"
    )

    builder.add_heading_3("3.3.4. Sơ đồ Hoạt động Quy trình Xếp Hàng Đặt Trước Sách")
    builder.add_paragraph(
        "Mô tả vòng đời đơn đặt trước: Độc giả đăng ký khi sách hết hàng (available = 0) -> Hệ thống ghi nhận đơn PENDING -> "
        "Khi có sách trả về kho, hệ thống tự động đổi sang READY và giữ chỗ ưu tiên trong vòng 7 ngày -> Độc giả đến mượn "
        "sách và đơn chuyển sang COMPLETED."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "08_activity_reservation.png"),
        "Sơ đồ Hoạt động (Activity Diagram) Quy trình Xếp hàng Đặt trước Sách"
    )

    builder.add_heading_3("3.3.5. Sơ đồ Hoạt động Quy trình Xử Lý Nộp & Miễn Giảm Phạt")
    builder.add_paragraph(
        "Thủ thư tra cứu danh sách phiếu phạt PENDING, lựa chọn hình thức: 'Thu tiền phạt' (PAID) hoặc 'Miễn giảm phạt' "
        "(WAIVED kèm lý do). Sau khi cập nhật, nếu độc giả không còn nợ phạt nào khác, quyền mượn sách sẽ được mở khóa tự động."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "09_activity_fine.png"),
        "Sơ đồ Hoạt động (Activity Diagram) Quy trình Xử lý Nộp & Miễn giảm Tiền phạt"
    )

    builder.add_heading_3("3.3.6. Sơ đồ Hoạt động Luồng Chatbot AI Tra Cứu")
    builder.add_paragraph(
        "Mô tả chi tiết luồng xử lý câu hỏi tự nhiên: Tiếp nhận câu hỏi -> Kiểm tra độ dài <= 500 ký tự -> Truy vấn DB "
        "lấy danh mục sách thực tế -> Đóng gói Grounded Context Prompt -> Gọi Gemini 1.5 Flash (hoặc Mock Fallback khi offline) -> "
        "Trích xuất thực thể sách khớp với CSDL -> Trả về kết quả hoàn chỉnh cho người dùng."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "10_activity_ai_chat.png"),
        "Sơ đồ Hoạt động (Activity Diagram) Luồng Chatbot AI Tra cứu Ngôn ngữ Tự nhiên"
    )

    # 3.4. Bộ 4 Sơ đồ Tuần tự
    builder.add_heading_2("3.4. Bộ Sơ đồ Tuần tự Nghiệp vụ (Sequence Diagrams)")
    builder.add_paragraph(
        "Các sơ đồ tuần tự thể hiện trình tự trao đổi thông điệp (Messages/Calls) theo thời gian giữa các thành phần: "
        "Giao diện người dùng (UI Client), Tầng điều khiển (FastAPI Router), Tầng dịch vụ (Service Layer), "
        "Cơ sở dữ liệu (SQLAlchemy ORM) và Dịch vụ ngoài (Google Gemini API)."
    )

    builder.add_heading_3("3.4.1. Sơ đồ Tuần tự Nghiệp vụ Mượn Sách")
    builder.add_paragraph(
        "Thể hiện các bước gọi API POST /api/borrows/, truy vấn kiểm tra điều kiện tại BorrowService, thực thi Database "
        "Transaction trừ số lượng sách, tạo bản ghi BorrowRecord và trả về mã phản hồi HTTP 201 Created."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "11_sequence_borrow.png"),
        "Sơ đồ Tuần tự (Sequence Diagram) Nghiệp vụ Lập Phiếu Mượn Sách"
    )

    builder.add_heading_3("3.4.2. Sơ đồ Tuần tự Nghiệp vụ Trả Sách & Xử Lý Phạt")
    builder.add_paragraph(
        "Thể hiện lời gọi PUT /api/borrows/{id}/return, logic tính số ngày trễ hạn, tạo bản ghi Fine nếu quá hạn, "
        "hoàn tồn kho và kiểm tra hàng đợi Reservation để kích hoạt đơn chờ sớm nhất."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "12_sequence_return.png"),
        "Sơ đồ Tuần tự (Sequence Diagram) Nghiệp vụ Trả Sách và Xử lý Phạt Quá Hạn"
    )

    builder.add_heading_3("3.4.3. Sơ đồ Tuần tự Chatbot AI Tra Cứu Thông Minh")
    builder.add_paragraph(
        "Thể hiện luồng tương tác bất đồng bộ qua endpoint POST /api/ai/search, quá trình đóng gói Grounded Prompt, "
        "giao tiếp HTTPS với Google Gemini 1.5 API, cơ chế kích hoạt Mock Fallback khi offline và hàm trích xuất thực thể sách."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "13_sequence_ai_chat.png"),
        "Sơ đồ Tuần tự (Sequence Diagram) Luồng Chatbot AI Tra cứu Ngôn ngữ Tự nhiên"
    )

    builder.add_heading_3("3.4.4. Sơ đồ Tuần tự AI Gợi Ý Sách Cá Nhân Hóa")
    builder.add_paragraph(
        "Thể hiện lời gọi GET /api/ai/suggest, quy trình trích xuất lịch sử mượn đã ẩn danh hóa thông tin cá nhân, "
        "gửi Prompt phân tích gu đọc sang Gemini và trả về danh sách 3-5 cuốn sách phù hợp nhất."
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "14_sequence_ai_suggest.png"),
        "Sơ đồ Tuần tự (Sequence Diagram) Luồng AI Gợi ý Sách theo Gu Đọc Cá nhân"
    )

    # 3.5. Sơ đồ Vòng đời Trạng thái
    builder.add_heading_2("3.5. Sơ đồ Vòng đời Trạng thái (State Machine Diagram)")
    builder.add_paragraph(
        "Hệ thống quản lý chặt chẽ vòng đời của 2 thực thể nghiệp vụ cốt lõi thông qua các máy trạng thái hữu hạn (Finite State Machines):",
        bold_prefix="Mô hình trạng thái: "
    )
    builder.add_bullet(
        "Vòng đời Phiếu mượn (BorrowRecord Status): ",
        "Bắt đầu ở trạng thái `BORROWING` khi lập phiếu -> Nếu trả đúng hạn chuyển sang `RETURNED` -> Nếu quá hạn chuyển sang `OVERDUE` "
        "(phát sinh bản ghi phạt `Fine`) -> Khi hoàn trả sách quá hạn chuyển sang `RETURNED` -> Trường hợp mất sách chuyển sang `LOST`."
    )
    builder.add_bullet(
        "Vòng đời Đơn đặt trước (Reservation Status): ",
        "Khởi tạo ở trạng thái `PENDING` khi sách hết bản khả dụng -> Khi có người trả sách về kho, hệ thống tự động đổi sang `READY` "
        "(khóa giữ sách trong 7 ngày) -> Khi độc giả đến nhận mượn sách chuyển sang `COMPLETED` -> Nếu quá 7 ngày không đến lấy chuyển sang `EXPIRED` / `CANCELLED`."
    )

    builder.doc.add_page_break()
