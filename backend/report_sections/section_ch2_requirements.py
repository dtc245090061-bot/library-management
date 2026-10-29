"""
Chương 2: Phân tích Yêu cầu Nghiệp vụ & Use Case (Phiên bản Mở rộng Chuyên sâu 100+ Trang)
Bao gồm: Khảo sát quy trình 5 luồng, RBAC, FR01-FR12, NFR01-NFR08, 3 Sơ đồ Use Case, và 10 Bảng đặc tả Use Case chi tiết hoàn chỉnh với Business Rules & Error Handling.
"""

import os

def build_chapter_2(builder, diagrams_dir):
    builder.add_heading_1("CHƯƠNG 2: PHÂN TÍCH YÊU CẦU NGHIỆP VỤ & USE CASE", chapter_num=2)

    # 2.1. Khảo sát & Mô hình hóa nghiệp vụ
    builder.add_heading_2("2.1. Khảo sát & Mô hình hóa quy trình nghiệp vụ thư viện")
    builder.add_paragraph(
        "Dựa trên kết quả khảo sát thực tế tại các trung tâm học liệu đại học, nhóm tác giả đã mô hình hóa "
        "quy trình nghiệp vụ thư viện thành 5 luồng xử lý tương tác chính với các quy tắc nghiệp vụ chặt chẽ:",
        bold_prefix="Khảo sát nghiệp vụ: "
    )
    builder.add_bullet(
        "1. Quy trình Lập phiếu Mượn sách tại quầy: ",
        "Độc giả xuất trình thẻ thư viện và mang các cuốn sách cần mượn đến quầy thủ thư. Thủ thư quét mã thẻ và mã sách. "
        "Hệ thống tiến hành xác thực tự động qua 4 bước kiểm tra: (a) Thẻ độc giả phải ở trạng thái ACTIVE và còn hạn sử dụng; "
        "(b) Tổng số sách độc giả đang mượn hiện tại cộng với số sách muốn mượn không vượt quá hạn mức quy định (tối đa 5 cuốn); "
        "(c) Độc giả không có bất kỳ khoản nợ phạt trễ hạn nào ở trạng thái PENDING; (d) Cuốn sách yêu cầu phải còn bản khả dụng "
        "(available_quantity > 0). Khi cả 4 điều kiện được thỏa mãn, hệ thống tạo bản ghi phiếu mượn với thời hạn tiêu chuẩn 14 ngày, "
        "tự động trừ số lượng sách khả dụng đi 1 đơn vị, và cập nhật trạng thái đơn đặt trước của độc giả này (nếu có) sang COMPLETED."
    )
    builder.add_bullet(
        "2. Quy trình Tiếp nhận Trả sách & Xử lý Phạt trễ hạn: ",
        "Độc giả mang sách trả tại quầy. Thủ thư tra cứu phiếu mượn theo mã phiếu hoặc mã độc giả và bấm nút 'Trả sách'. "
        "Hệ thống ghi nhận ngày trả thực tế (return_date = today), chuyển trạng thái phiếu mượn sang RETURNED, và tự động "
        "tăng số lượng sách khả dụng trong kho lên 1 đơn vị. Đồng thời, hệ thống tự động so sánh ngày trả với ngày hẹn trả (due_date): "
        "nếu trả trễ hạn, hệ thống tự động tính số ngày quá hạn và tạo bản ghi phạt (Fine) với công thức quy định: "
        "Tổng tiền phạt = Số ngày trễ hạn * 2.000 VNĐ (trạng thái PENDING). Sau đó, hệ thống tự động kiểm tra hàng đợi đặt trước "
        "của cuốn sách này, nếu có độc giả đang chờ, hệ thống đổi trạng thái đơn đặt trước sớm nhất sang READY và giữ chỗ ưu tiên 7 ngày."
    )
    builder.add_bullet(
        "3. Quy trình Gia hạn Thời gian Mượn sách: ",
        "Độc giả có nhu cầu giữ sách thêm để phục vụ nghiên cứu có thể yêu cầu thủ thư gia hạn trực tiếp tại quầy hoặc "
        "thực hiện qua cổng thông tin cá nhân. Hệ thống áp dụng quy tắc kiểm soát nghiêm ngặt: (a) Phiếu mượn phải đang ở trạng thái "
        "BORROWING và chưa bị quá hạn; (b) Phiếu mượn chưa từng được gia hạn trước đó (renew_count = 0, mỗi phiếu chỉ được gia hạn "
        "tối đa 1 lần); (c) Cuốn sách hiện không có bất kỳ độc giả nào khác đang đặt trước trong hàng đợi. Khi hợp lệ, hệ thống "
        "cộng thêm 7 ngày vào ngày hẹn trả (due_date) và cập nhật renew_count = 1."
    )
    builder.add_bullet(
        "4. Quy trình Xếp hàng Đặt trước Sách (Reservation Queue): ",
        "Khi một cuốn sách hết sạch bản khả dụng trên kệ (available_quantity = 0), độc giả có thể gửi yêu cầu đặt trước trên hệ thống. "
        "Hệ thống kiểm tra độc giả chưa có đơn đặt trước nào đang chờ cho cuốn sách này, sau đó tạo bản ghi Reservation với trạng thái PENDING. "
        "Khi có độc giả khác mang sách đến trả, hệ thống tự động chuyển đơn đặt trước có thời gian tạo sớm nhất (FIFO - First In First Out) "
        "sang trạng thái READY và thiết lập thời hạn giữ chỗ ưu tiên trong vòng 7 ngày. Nếu sau 7 ngày độc giả không đến nhận, "
        "hệ thống tự động hủy đơn và chuyển quyền ưu tiên cho người tiếp theo trong hàng đợi."
    )
    builder.add_bullet(
        "5. Quy trình Tra cứu Thông minh & Tương tác Trợ lý AI: ",
        "Độc giả nhập các câu hỏi tự nhiên bằng tiếng Việt vào khung chat (ví dụ: 'Tôi muốn tìm sách hướng dẫn lập trình Web với FastAPI'). "
        "Hệ thống tự động trích xuất danh mục sách thực tế từ CSDL, đóng gói vào Context Prompt có chứa các chỉ thị ràng buộc nghiêm ngặt "
        "(Zero-Hallucination Guardrails) và gửi tới Google Gemini 1.5 Flash. AI phân tích ngữ cảnh, lựa chọn sách phù hợp và trả lời "
        "bằng tiếng Việt thân thiện kèm thẻ Card sách tương tác trực tiếp."
    )

    # 2.2. Danh sách Actor & Ma trận RBAC
    builder.add_heading_2("2.2. Danh sách Actor và Ma trận phân quyền (RBAC)")
    builder.add_paragraph(
        "Hệ thống áp dụng mô hình kiểm soát truy cập dựa trên vai trò (Role-Based Access Control - RBAC) "
        "để bảo vệ dữ liệu và phân định quyền hạn rõ ràng giữa 3 nhóm Actor:",
        bold_prefix="Mô hình phân quyền: "
    )

    rbac_headers = ["Chức năng / Phân hệ", "Quản trị viên (ADMIN)", "Thủ thư (LIBRARIAN)", "Độc giả (READER)"]
    rbac_rows = [
        ["Đăng nhập / Đổi mật khẩu", "✅ Toàn quyền", "✅ Toàn quyền", "✅ Toàn quyền"],
        ["Quản lý Tài khoản Users (Tạo/Khóa)", "✅ Toàn quyền", "❌ Không có quyền", "❌ Không có quyền"],
        ["Quản lý Kho Sách (CRUD Sách, Thể loại)", "✅ Toàn quyền", "✅ Toàn quyền", "👁️ Chỉ xem / Tra cứu"],
        ["Quản lý Hồ sơ Độc giả & Cấp thẻ", "✅ Toàn quyền", "✅ Toàn quyền", "👁️ Chỉ xem hồ sơ cá nhân"],
        ["Lập Phiếu Mượn & Nhận Trả Sách", "✅ Toàn quyền", "✅ Toàn quyền", "👁️ Xem lịch sử mượn cá nhân"],
        ["Xử lý Gia hạn Sách", "✅ Toàn quyền", "✅ Toàn quyền", "✅ Được yêu cầu gia hạn"],
        ["Thu tiền phạt & Miễn giảm phạt", "✅ Toàn quyền", "✅ Toàn quyền", "👁️ Xem thông tin nợ phạt"],
        ["Đặt trước sách khi hết bản", "✅ Toàn quyền", "✅ Toàn quyền", "✅ Được tạo đơn đặt trước"],
        ["Xem Thống kê Dashboard & Xuất CSV", "✅ Toàn quyền", "✅ Toàn quyền", "❌ Không có quyền"],
        ["Sử dụng Chatbot AI & Tóm tắt sách", "✅ Toàn quyền", "✅ Toàn quyền", "✅ Toàn quyền"],
    ]
    builder.add_styled_table(
        "Ma trận phân quyền chi tiết RBAC trong hệ thống Quản lý Thư viện AI",
        rbac_headers,
        rbac_rows,
        col_widths=[2.8, 1.4, 1.4, 1.4]
    )

    # 2.3. Yêu cầu chức năng (FR01 - FR12)
    builder.add_heading_2("2.3. Bảng Yêu cầu Chức năng Hệ thống (Functional Requirements)")
    fr_headers = ["Mã YC", "Tên chức năng", "Mô tả đầu vào (Input)", "Quy trình xử lý (Processing)", "Đầu ra (Output)"]
    fr_rows = [
        ["FR01", "Đăng nhập & Xác thực", "Username, Password", "Bcrypt verify hash, tạo JWT Token HS256 có payload role & user_id", "Access Token, Chuyển hướng Dashboard"],
        ["FR02", "Quản lý Kho Sách", "Mã sách, Tên, Tác giả, Thể loại, NXB, Năm, Số lượng", "Validation Pydantic, kiểm tra trùng mã sách/ISBN, lưu CSDL", "Bản ghi sách mới, Cập nhật danh mục"],
        ["FR03", "Quản lý Độc giả", "Mã thẻ, Tên, SĐT, Loại độc giả, Hạn thẻ", "Kiểm tra định dạng SĐT, tạo hồ sơ Reader gắn với User", "Hồ sơ độc giả ACTIVE, Thẻ thư viện"],
        ["FR04", "Lập Phiếu Mượn", "reader_id, book_id", "Kiểm tra thẻ ACTIVE, nợ phạt, số lượng còn; giảm available -1, hẹn trả +14 ngày", "Phiếu mượn trạng thái BORROWING"],
        ["FR05", "Xử lý Trả Sách", "borrow_id, ghi chú tình trạng", "Đổi status RETURNED, tăng available +1; tính phạt nếu quá hạn (2.000đ/ngày)", "Phiếu trả, Bản ghi phạt PENDING (nếu có)"],
        ["FR06", "Gia hạn Sách", "borrow_id", "Kiểm tra chưa quá hạn, renew_count < 1, không ai đặt trước; cộng +7 ngày due_date", "Hạn trả mới, renew_count = 1"],
        ["FR07", "Quản lý & Thu Phạt", "fine_id, hình thức (PAID/WAIVED)", "Ghi nhận thanh toán tiền phạt, mở khóa quyền mượn sách cho độc giả", "Phiếu phạt status PAID / WAIVED"],
        ["FR08", "Đặt trước Sách", "reader_id, book_id (hết bản)", "Kiểm tra available == 0, tạo Reservation PENDING, giữ chỗ khi sách về kho", "Đơn đặt trước status PENDING / READY"],
        ["FR09", "Chatbot Tra cứu AI", "Câu hỏi tự nhiên tiếng Việt", "Trích xuất sách từ DB, Grounded Prompting, gọi Gemini 1.5, lọc thực thể", "Câu trả lời AI + Danh thiếp sách"],
        ["FR10", "AI Tóm tắt Sách", "book_id", "Lấy mô tả, mục lục sách, gọi Gemini tóm tắt 3 phần (nội dung, độc giả, giá trị)", "Đoạn tóm tắt súc tích 100-200 từ"],
        ["FR11", "AI Gợi ý Cá nhân hóa", "reader_id (lấy từ JWT token)", "Lấy lịch sử mượn ẩn danh, phân tích gu đọc qua Gemini, tìm sách phù hợp", "Danh sách 3-5 cuốn sách gợi ý"],
        ["FR12", "Thống kê & Xuất CSV", "Khoảng thời gian, tiêu chí lọc", "Tổng hợp số liệu thời gian thực, tính tỷ lệ mượn, encode UTF-8-BOM", "Dashboard Chart.js, File CSV tải về"],
    ]
    builder.add_styled_table(
        "Bảng tổng hợp 12 Yêu cầu Chức năng Cốt lõi của Hệ thống (FR01 - FR12)",
        fr_headers,
        fr_rows,
        col_widths=[0.8, 1.6, 1.4, 2.2, 1.4]
    )

    # 2.4. Yêu cầu phi chức năng (NFR01 - NFR08)
    builder.add_heading_2("2.4. Bảng Yêu cầu Phi chức năng (Non-Functional Requirements)")
    nfr_headers = ["Mã YC", "Nhóm yêu cầu", "Tiêu chí kỹ thuật chi tiết", "Phương pháp kiểm chứng"]
    nfr_rows = [
        ["NFR01", "Bảo mật Xác thực", "Mật khẩu mã hóa Bcrypt với salt round chuẩn; JWT Token có thời hạn 60 phút, thuật toán HS256", "Kiểm thử mã hóa, chặn request khi token hết hạn"],
        ["NFR02", "Quyền riêng tư AI", "Tuyệt đối không gửi thông tin cá nhân độc giả (Họ tên, SĐT, Email) sang Google Gemini API", "Code review middleware, bắt gói tin HTTP payload"],
        ["NFR03", "Hiệu năng API", "Thời gian phản hồi (Response Time) cho các API nghiệp vụ CRUD < 150ms dưới tải 50 req/s", "Benchmark tải Apache Bench / Pytest execution time"],
        ["NFR04", "Độ tin cậy & Chịu lỗi AI", "Hệ thống tự động kích hoạt Mock Fallback khi mất mạng hoặc hết quota AI, timeout tối đa 15 giây", "Unit test giả lập timeout và mất kết nối Gemini"],
        ["NFR05", "Tính toàn vẹn CSDL", "Sử dụng Foreign Keys, Unique Constraints và Database Transactions đảm bảo ACID tuyệt đối", "Pytest kiểm thử ràng buộc trùng lặp và race condition"],
        ["NFR06", "Trải nghiệm UX", "Giao diện Web tương thích đa màn hình (Responsive), bố cục chuẩn White Theme Glassmorphism", "Kiểm thử Playwright trên các độ phân giải khác nhau"],
        ["NFR07", "Định dạng Dữ liệu", "Xuất file CSV hỗ trợ UTF-8-BOM để mở bằng Microsoft Excel tiếng Việt không bị lỗi font", "Mở file CSV xuất ra trên Excel và kiểm tra hiển thị"],
        ["NFR08", "Đóng gói & Khả chuyển", "Dễ dàng triển khai trên mọi hệ điều hành (Windows, Linux, macOS) thông qua Docker Compose", "Build và chạy docker-compose up trên máy chủ mới"],
    ]
    builder.add_styled_table(
        "Bảng 8 Yêu cầu Phi chức năng của Hệ thống (NFR01 - NFR08)",
        nfr_headers,
        nfr_rows,
        col_widths=[0.8, 1.4, 3.4, 1.8]
    )

    # 2.5. Sơ đồ Use Case
    builder.add_heading_2("2.5. Sơ đồ Use Case Tổng quan & Phân rã Hệ thống")
    builder.add_paragraph(
        "Mô hình Use Case của hệ thống được tổ chức thành 3 sơ đồ phân cấp: Sơ đồ Use Case tổng quát toàn hệ thống, "
        "Sơ đồ Use Case phân hệ nghiệp vụ quản lý thư viện, và Sơ đồ Use Case phân hệ Trợ lý AI thông minh."
    )

    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "02_usecase_general.png"),
        "Sơ đồ Use Case Tổng quan Toàn Hệ thống Quản lý Thư viện AI"
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "03_usecase_library.png"),
        "Sơ đồ Use Case Phân hệ Nghiệp vụ Thư viện (Thủ thư & Độc giả)"
    )
    builder.add_image_with_caption(
        os.path.join(diagrams_dir, "04_usecase_ai.png"),
        "Sơ đồ Use Case Phân hệ Trợ lý AI Thông minh (Generative AI)"
    )

    # 2.6. 10 Bảng đặc tả Use Case chi tiết
    builder.add_heading_2("2.6. Đặc tả Chi tiết 10 Use Case Trọng yếu (Use Case Specifications)")
    builder.add_paragraph(
        "Dưới đây là bảng đặc tả cấu trúc chuẩn học thuật cho 10 Use Case nghiệp vụ và AI quan trọng nhất của hệ thống:"
    )

    # Helper function for UC Spec
    def add_uc_spec(uc_id, uc_title, actor, pre_cond, main_flow, alt_flow, post_cond, business_rules):
        uc_h = ["Thuộc tính Use Case", "Nội dung đặc tả chi tiết"]
        uc_r = [
            ["Mã & Tên Use Case", f"{uc_id}: {uc_title}"],
            ["Tác nhân chính (Actor)", actor],
            ["Tiền điều kiện (Pre-conditions)", pre_cond],
            ["Luồng sự kiện chính (Main Flow)", main_flow],
            ["Luồng phụ / Ngoại lệ (Alternative Flows)", alt_flow],
            ["Hậu điều kiện (Post-conditions)", post_cond],
            ["Quy tắc nghiệp vụ (Business Rules)", business_rules],
        ]
        builder.add_styled_table(f"Đặc tả Use Case {uc_id}: {uc_title}", uc_h, uc_r, col_widths=[2.0, 5.2])

    # UC01
    add_uc_spec(
        "UC01", "Đăng nhập & Xác thực Hệ thống",
        "Quản trị viên (Admin), Thủ thư (Librarian), Độc giả (Reader)",
        "Người dùng đã có tài khoản hợp lệ trong bảng `users` và đang ở trạng thái `is_active = True`.",
        "1. Người dùng truy cập trang /login.\n2. Nhập tên đăng nhập (username) và mật khẩu (password).\n3. Bấm nút 'Đăng nhập'.\n4. Hệ thống mã hóa kiểm tra mật khẩu qua Bcrypt.\n5. Hệ thống sinh JWT Token chứa user_id và role, lưu vào LocalStorage và chuyển hướng tới /dashboard.",
        "4a. Sai tên đăng nhập hoặc mật khẩu: Hệ thống trả về mã lỗi 401 Unauthorized kèm thông báo 'Tên đăng nhập hoặc mật khẩu không chính xác'.\n4b. Tài khoản bị vô hiệu hóa (is_active = False): Báo lỗi 403 Forbidden kèm thông báo 'Tài khoản đã bị khóa, vui lòng liên hệ Admin'.",
        "Người dùng đăng nhập thành công, phiên làm việc được lưu trong JWT Token.",
        "BR01: Mật khẩu tối thiểu 6 ký tự; Token JWT hết hạn sau 60 phút; Khóa tài khoản sau 5 lần nhập sai liên tiếp."
    )

    # UC02
    add_uc_spec(
        "UC02", "Quản lý Danh mục Kho Sách (CRUD & Bộ lọc)",
        "Thủ thư (Librarian), Quản trị viên (Admin)",
        "Thủ thư đã đăng nhập hệ thống với quyền LIBRARIAN hoặc ADMIN.",
        "1. Thủ thư truy cập trang Quản lý Sách (/books).\n2. Hệ thống hiển thị danh sách sách dạng bảng phân trang kèm bộ lọc.\n3. Thủ thư bấm 'Thêm sách mới', điền mã sách, tên sách, tác giả, thể loại, NXB, năm, số lượng.\n4. Bấm 'Lưu lại'.\n5. Hệ thống kiểm tra dữ liệu và lưu vào bảng `books`.",
        "5a. Mã sách hoặc ISBN bị trùng: Hệ thống hiển thị cảnh báo lỗi trùng lặp dữ liệu.\n5b. Số lượng sách nhập <= 0: Hệ thống hiển thị thông báo yêu cầu số lượng phải lớn hơn 0.",
        "Bản ghi sách mới được thêm vào CSDL, số lượng khả dụng ban đầu bằng tổng số lượng.",
        "BR02: Mã sách định dạng BKxxxx; Không cho phép xóa sách đang có phiếu mượn BORROWING."
    )

    # UC03
    add_uc_spec(
        "UC03", "Quản lý Hồ sơ Độc giả & Cấp / Khóa Thẻ",
        "Thủ thư (Librarian), Quản trị viên (Admin)",
        "Thủ thư đã đăng nhập vào hệ thống.",
        "1. Thủ thư mở danh mục Quản lý Độc giả (/readers).\n2. Xem danh sách độc giả, mã thẻ, số điện thoại, hạn thẻ và trạng thái.\n3. Chọn thao tác: Cấp thẻ mới, Chỉnh sửa thông tin, hoặc Đổi trạng thái thẻ (ACTIVE / EXPIRED / SUSPENDED).\n4. Hệ thống cập nhật bảng `readers`.",
        "3a. Số điện thoại không đúng định dạng 10 số: Báo lỗi validation.\n3b. Khóa thẻ độc giả đang có nợ phạt: Hệ thống hiển thị cảnh báo nhưng vẫn cho phép khóa để ngăn mượn thêm.",
        "Trạng thái thẻ và hồ sơ độc giả được cập nhật tức thì trong CSDL.",
        "BR03: Thẻ sinh viên có hạn 365 ngày kể từ ngày cấp; Độc giả bị SUSPENDED bị vô hiệu hóa quyền mượn sách."
    )

    # UC04
    add_uc_spec(
        "UC04", "Lập Phiếu Mượn Sách tại Quầy",
        "Thủ thư (Librarian)",
        "Độc giả có mặt tại quầy với thẻ thư viện hợp lệ; sách cần mượn có sẵn trong kho.",
        "1. Thủ thư chọn menu Mượn / Trả Sách (/borrows) -> Bấm 'Tạo phiếu mượn'.\n2. Nhập mã/ID độc giả và mã/ID cuốn sách cần mượn.\n3. Hệ thống kiểm tra: Thẻ ACTIVE, hạn thẻ > ngày hiện tại, số sách đang mượn < 5, không nợ phạt, và sách có `available_quantity > 0`.\n4. Hệ thống tạo bản ghi `borrow_records` với due_date = today + 14 ngày.\n5. Giảm `available_quantity` của sách đi 1 đơn vị.\n6. Chuyển Reservation của độc giả này sang COMPLETED nếu có.",
        "3a. Thẻ hết hạn hoặc bị khóa: Báo lỗi 'Thẻ không hợp lệ'.\n3b. Độc giả đang giữ >= 5 cuốn: Báo lỗi 'Vượt quá hạn mức mượn'.\n3c. Độc giả có phiếu phạt PENDING: Báo lỗi 'Độc giả phải thanh toán nợ phạt trước khi mượn'.\n3d. Sách đã hết (available = 0): Báo lỗi 'Sách đã hết bản khả dụng' và gợi ý đặt trước.",
        "Phiếu mượn được tạo thành công, tồn kho sách giảm 1, in/lưu phiếu mượn.",
        "BR04: Thời hạn mượn mặc định 14 ngày; Không cho phép mượn vượt quá hạn mức 5 cuốn."
    )

    # UC05
    add_uc_spec(
        "UC05", "Tiếp nhận Trả Sách & Tự động Tính Tiền Phạt",
        "Thủ thư (Librarian)",
        "Phiếu mượn đang ở trạng thái BORROWING.",
        "1. Thủ thư tìm kiếm phiếu mượn của độc giả hoặc bấm nút 'Trả sách' trên danh sách.\n2. Hệ thống ghi nhận return_date = ngày hiện tại, đổi trạng thái phiếu sang RETURNED.\n3. Tăng `available_quantity` của cuốn sách lên 1 đơn vị.\n4. Hệ thống kiểm tra ngày trả: nếu today > due_date, tính số ngày quá hạn và tạo bản ghi `fines` với số tiền = overdue_days * 2.000 VNĐ (status = PENDING).\n5. Kiểm tra bảng `reservations`, nếu có độc giả đang chờ cuốn này, chuyển đơn sớm nhất sang READY.",
        "1a. Phiếu mượn đã có trạng thái RETURNED: Báo lỗi 'Phiếu mượn này đã được trả trước đó'.",
        "Sách được hoàn trả về kho, tăng số lượng khả dụng, tạo phiếu phạt nếu trễ hạn.",
        "BR05: Đơn giá phạt trễ hạn cố định 2.000 VNĐ/ngày; Tiền phạt được ghi nhận tự động vào bảng `fines`."
    )

    # UC06
    add_uc_spec(
        "UC06", "Xử lý Gia hạn Mượn Sách (+7 ngày)",
        "Thủ thư (Librarian), Độc giả (Reader)",
        "Phiếu mượn đang ở trạng thái BORROWING và chưa bị quá hạn.",
        "1. Người dùng bấm nút 'Gia hạn' trên phiếu mượn.\n2. Hệ thống kiểm tra: phiếu chưa quá hạn, `renew_count < 1`, và không có độc giả nào đặt trước cuốn sách này.\n3. Hệ thống cộng thêm 7 ngày vào `due_date`, cập nhật `renew_count = 1`.\n4. Hiển thị thông báo gia hạn thành công kèm hạn trả mới.",
        "2a. Phiếu mượn đã bị quá hạn: Báo lỗi 'Không thể gia hạn phiếu mượn đã quá hạn'.\n2b. Đã gia hạn 1 lần trước đó: Báo lỗi 'Mỗi phiếu mượn chỉ được gia hạn tối đa 1 lần'.\n2c. Sách đã có người đặt trước: Báo lỗi 'Sách đã có người chờ trong hàng đợi, không thể gia hạn'.",
        "Hạn trả sách được gia hạn thêm 7 ngày thành công.",
        "BR06: Số lần gia hạn tối đa là 1 lần (+7 ngày); Không gia hạn cho sách có đơn đặt trước READY/PENDING."
    )

    # UC07
    add_uc_spec(
        "UC07", "Thu Tiền Phạt & Miễn Giảm Phạt Quá Hạn",
        "Thủ thư (Librarian), Quản trị viên (Admin)",
        "Độc giả có bản ghi phạt ở trạng thái PENDING trong bảng `fines`.",
        "1. Thủ thư vào tab Quản lý Phạt (/borrows#fines).\n2. Chọn phiếu phạt cần xử lý.\n3. Chọn hình thức: 'Thu tiền phạt' (PAID) hoặc 'Miễn giảm phạt' (WAIVED kèm lý do).\n4. Hệ thống cập nhật trạng thái phiếu phạt và ngày thanh toán.\n5. Độc giả được mở khóa quyền mượn sách nếu đã thanh toán hết nợ phạt.",
        "3a. Phiếu phạt đã ở trạng thái PAID: Hệ thống vô hiệu hóa nút thanh toán.",
        "Phiếu phạt chuyển sang trạng thái hoàn tất, quyền mượn của độc giả được phục hồi.",
        "BR07: Mọi khoản miễn giảm phạt phải có lý do giải trình hợp lệ (lý do chính đáng, sự cố bất khả kháng)."
    )

    # UC08
    add_uc_spec(
        "UC08", "Đặt Trước Sách Khi Hết Bản Khả Dụng",
        "Độc giả (Reader), Thủ thư (Librarian)",
        "Cuốn sách có số lượng khả dụng `available_quantity = 0`.",
        "1. Độc giả tìm cuốn sách mong muốn trên hệ thống, thấy trạng thái 'Hết sách'.\n2. Bấm nút 'Đặt trước sách'.\n3. Hệ thống kiểm tra độc giả chưa có đơn đặt trước đang chờ cho cuốn này.\n4. Hệ thống tạo bản ghi `reservations` với trạng thái PENDING, hạn giữ chỗ 7 ngày.\n5. Khi sách được trả về kho, hệ thống tự động đổi trạng thái sang READY.",
        "3a. Sách vẫn còn bản khả dụng (> 0): Hệ thống thông báo 'Sách còn sẵn trên kệ, vui lòng mượn trực tiếp'.\n3b. Độc giả đã đặt trước cuốn này rồi: Báo lỗi 'Bạn đã có đơn đặt trước đang chờ cho sách này'.",
        "Đơn đặt trước được ghi nhận vào hàng đợi ưu tiên của hệ thống.",
        "BR08: Thứ tự ưu tiên theo hàng đợi FIFO (First In First Out); Thời gian giữ chỗ ưu tiên là 7 ngày."
    )

    # UC09
    add_uc_spec(
        "UC09", "Chatbot AI Tra cứu Sách bằng Ngôn ngữ Tự nhiên",
        "Độc giả (Reader), Thủ thư (Librarian)",
        "Người dùng đã đăng nhập hệ thống và truy cập trang /ai-chat.",
        "1. Người dùng nhập câu hỏi tự nhiên tiếng Việt vào khung chat (ví dụ: 'Tìm sách lập trình Python cho người mới').\n2. Hệ thống lấy danh mục sách thực tế từ CSDL, đóng gói vào Context Prompt có ràng buộc Zero-Hallucination.\n3. Gửi Prompt sang Google Gemini 1.5 Flash API.\n4. Nhận phản hồi văn bản, trích xuất thực thể sách khớp với DB.\n5. Hiển thị tin nhắn trả lời của AI kèm các Card thông tin sách có thể bấm xem chi tiết/mượn ngay.",
        "2a. Câu hỏi rỗng hoặc quá 500 ký tự: Báo lỗi validation 422.\n3a. Mất mạng hoặc hết quota Gemini: Hệ thống tự động chuyển sang Mock AI Fallback, hiển thị phản hồi mô phỏng thông minh mà không gây gián đoạn trải nghiệm.",
        "Độc giả nhận được câu trả lời chính xác, đáng tin cậy 100% về kho sách thực tế.",
        "BR09: AI chỉ trả lời dựa trên context kho sách thực tế; Tuyệt đối không bịa sách không có trong DB."
    )

    # UC10
    add_uc_spec(
        "UC10", "AI Tóm Tắt Nội Dung & Gợi Ý Sách Cá Nhân Hóa",
        "Độc giả (Reader)",
        "Độc giả đã đăng nhập vào hệ thống.",
        "1. Tóm tắt sách: Độc giả mở Modal chi tiết sách -> Bấm 'AI Tóm tắt'. Hệ thống gọi endpoint POST /api/ai/summarize/{id}, AI sinh đoạn tóm tắt 3 phần súc tích.\n2. Gợi ý sách: Độc giả truy cập trang AI Chatbot hoặc Khám phá. Hệ thống gọi GET /api/ai/suggest, lấy lịch sử mượn đã ẩn danh, phân tích gu đọc và đề xuất 3-5 cuốn sách phù hợp nhất.",
        "1a. Sách chưa có mô tả chi tiết: AI tự động sinh tóm tắt dựa trên tiêu đề, tác giả và thể loại chuyên ngành.\n2a. Độc giả mới chưa có lịch sử mượn: AI tự động gợi ý các đầu sách nổi bật, được mượn nhiều nhất theo các thể loại chính.",
        "Độc giả nắm bắt nhanh nội dung sách và nhận được danh mục gợi ý cá nhân hóa hữu ích.",
        "BR10: Dữ liệu gửi sang AI phải được ẩn danh hóa hoàn toàn theo nguyên tắc Privacy-by-Design."
    )

    builder.doc.add_page_break()
