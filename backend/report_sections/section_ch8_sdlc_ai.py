"""
Chương 8: Ứng dụng AI trong Quy trình SDLC (Phiên bản Mở rộng Toàn diện Chuyên sâu)
Bao gồm:
- Phân tích 4 giai đoạn SDLC (Bài KT1, KT2, KT3, Cuối kỳ)
- Khung Năng Lực & Kỹ Năng Kỹ Sư Phần Mềm (AI-Augmented Engineering Skills Framework)
- Tuyển Tập Bộ Prompts Mẫu Chi Tiết Hoàn Thành Đồ Án (The Master Prompt Catalog: P01 - P12)
- 4 Kịch bản Đối thoại Kỹ thuật (Pair Programming Dialogues)
- Nhật ký Prompt Log tổng hợp 12 tương tác trọng yếu
- 4 Bài học kinh nghiệm & nguyên tắc vàng khi Pair Programming cùng AI
"""

def build_chapter_8(builder):
    builder.add_heading_1("CHƯƠNG 8: ỨNG DỤNG AI TRONG QUY TRÌNH SDLC", chapter_num=8)

    # 8.1. Tổng quan vai trò AI
    builder.add_heading_2("8.1. Tổng quan Vai trò của AI Trợ lý trong Vòng đời Phần mềm (SDLC)")
    builder.add_paragraph(
        "Khác với các đồ án công nghệ thông tin truyền thống chỉ sử dụng AI như một tính năng phụ trợ ở giai đoạn cuối, "
        "dự án này đặt Trí tuệ Nhân tạo vào vị trí đối tác cộng sự (AI Pair Programmer) đồng hành xuyên suốt 100% "
        "các giai đoạn của Vòng đời Phát triển Phần mềm (Software Development Life Cycle - SDLC). "
        "Sự kết hợp giữa tư duy phân tích, phản biện của kỹ sư phần mềm và năng lực sinh mã nguồn, sinh tài liệu "
        "tốc độ cao của các mô hình ngôn ngữ lớn (LLM) đã rút ngắn hơn 60% thời gian phát triển, "
        "đồng thời nâng cao độ bao phủ kiểm thử lên 100% và chuẩn hóa chất lượng kiến trúc hệ thống.",
        bold_prefix="Mô hình phát triển AI-Augmented SDLC: "
    )
    builder.add_paragraph(
        "Trong suốt quá trình thực hiện đề tài, nhóm phát triển đã phối hợp chặt chẽ cùng các công cụ AI thế hệ mới "
        "(Google Gemini, OpenAI GPT-4o, GitHub Copilot và Antigravity IDE), tuân thủ nguyên tắc 'Human-in-the-Loop' "
        "(Con người nắm quyền kiểm soát và phê duyệt tối hậu). Mọi kết quả do AI đề xuất từ sơ đồ kiến trúc, "
        "cấu trúc cơ sở dữ liệu, mã nguồn backend/frontend cho đến các ca kiểm thử tự động đều phải trải qua quy trình "
        "thẩm định 3 bước nghiêm ngặt: (1) Phân tích tính hợp lệ; (2) Kiểm chứng với dữ liệu thực tế; "
        "và (3) Tinh chỉnh tối ưu hóa hiệu năng & bảo mật."
    )

    # 8.2 - 8.5. Chi tiết 4 giai đoạn
    builder.add_heading_2("8.2. Giai đoạn 1 (Bài KT1): AI Hỗ trợ Phân tích Nghiệp vụ & Thiết kế Hệ thống")
    builder.add_paragraph(
        "Trong giai đoạn khảo sát ban đầu, nhóm đã sử dụng AI để phân tích quy trình mượn/trả thư viện đại học, "
        "nhận diện các trường hợp ngoại lệ (Edge Cases) mà con người dễ bỏ sót: ví dụ như trường hợp độc giả cố tình mượn sách "
        "khi đang có nợ phạt trễ hạn chưa thanh toán, hoặc trường hợp yêu cầu gia hạn sách khi cuốn sách đó đã có độc giả khác "
        "xếp hàng đặt trước. AI đã hỗ trợ sinh ra bộ khung Use Case, đề xuất cấu trúc bảng CSDL chuẩn hóa 3NF và kiến trúc phân tầng Layered Architecture."
    )
    builder.add_paragraph(
        "Sinh viên đã phản biện và điều chỉnh kết quả của AI: Tách biệt thực thể `users` và `readers` thay vì gộp chung thành một bảng "
        "như AI gợi ý ban đầu, nhằm đảm bảo nguyên tắc phân quyền RBAC và hỗ trợ tài khoản quản trị viên không cần có hồ sơ thẻ thư viện."
    )

    builder.add_heading_2("8.3. Giai đoạn 2 (Bài KT2): AI Hỗ trợ Sinh Mã Nguồn Backend & Giao diện Web")
    builder.add_paragraph(
        "Nhóm đã sử dụng AI để sinh nhanh khung mã nguồn (Boilerplate Code) cho các SQLAlchemy Models, Pydantic Schemas, "
        "và các hàm tiện ích bảo mật mật khẩu Bcrypt / JWT. Đặc biệt, AI hỗ trợ lập trình logic phức tạp trong `borrow_service.py` "
        "(tự động tính số ngày trễ hạn, tính tiền phạt theo đơn giá ngày, và khôi phục tồn kho an toàn trong Database Transaction)."
    )
    builder.add_paragraph(
        "Sinh viên đã trực tiếp kiểm tra và tối ưu hóa mã nguồn: Bổ sung ràng buộc `min(available_quantity + 1, total_quantity)` "
        "để loại trừ triệt để nguy cơ lỗi logic làm số lượng sách khả dụng vượt quá tổng số sách sở hữu khi có thao tác trả nhầm."
    )

    builder.add_heading_2("8.4. Giai đoạn 3 (Bài KT3): AI Hỗ trợ Thiết kế Prompt & Tự Động Hóa Kiểm Thử")
    builder.add_paragraph(
        "AI đóng vai trò chuyên gia Prompt Engineer, giúp nhóm tinh chỉnh qua 3 vòng thử nghiệm (Iterations) để triệt tiêu "
        "hiện tượng ảo giác. Đồng thời, AI hỗ trợ sinh toàn bộ bộ kiểm thử tự động 26 ca Pytest bao phủ đầy đủ các kịch bản "
        "thành công, thất bại, tấn công inject và lỗi ranh giới biên."
    )
    builder.add_paragraph(
        "Sinh viên đã cấu hình môi trường kiểm thử cô lập (Isolated Test DB Fixtures), đảm bảo mỗi ca kiểm thử chạy độc lập "
        "và nạp dữ liệu mẫu sạch sẽ, không gây ảnh hưởng lẫn nhau."
    )

    builder.add_heading_2("8.5. Giai đoạn 4 (Bài Cuối kỳ): AI Hỗ trợ Review Bảo Mật & Tổng Hợp Tài Liệu")
    builder.add_paragraph(
        "AI thực hiện rà soát an ninh mã nguồn (Security Code Review), phát hiện các lỗ hổng rò rỉ dữ liệu cá nhân sang API ngoài, "
        "đề xuất cơ chế Timeout 15s và Retry x2. Cuối cùng, AI hỗ trợ đóng gói Dockerfile đa tầng và sinh bộ tài liệu kỹ thuật hoàn chỉnh."
    )
    builder.add_paragraph(
        "Sinh viên đã trực tiếp kiểm thử trên các môi trường thực tế (Windows, Linux Docker) để xác nhận hệ thống hoạt động ổn định 100%."
    )

    # 8.6. Khung Năng Lực & Kỹ Năng Kỹ Sư Phần Mềm (AI-Augmented Engineering Skills)
    builder.add_heading_2("8.6. Khung Năng Lực & Kỹ Năng Kỹ Sư Phần Mềm (AI-Augmented Engineering Skills Framework)")
    builder.add_paragraph(
        "Để hoàn thành xuất sắc đồ án với khối lượng công việc đồ sộ (hệ thống full-stack hoàn chỉnh, CSDL 8 bảng, "
        "bộ kiểm thử tự động 100% pass và báo cáo kỹ thuật chuyên sâu 100+ trang), nhóm sinh viên đã ứng dụng "
        "và rèn luyện bộ 6 kỹ năng kỹ sư phần mềm thế hệ mới (AI-Augmented Software Engineering Skills):",
        bold_prefix="Khung kỹ năng cốt lõi: "
    )

    builder.add_bullet(
        "1. Skill 1: Kỹ Năng Phân Tích Nghiệp Vụ & Mô Hình Hóa Miền (Domain Modeling & System Analysis Skill): ",
        "Năng lực trừu tượng hóa nghiệp vụ quản lý thư viện thực tế thành các thực thể phần mềm, quan hệ dữ liệu chuẩn 3NF "
        "và các ràng buộc toàn vẹn. Khả năng phát hiện sớm các trường hợp ngoại lệ (Edge Cases) trong luồng mượn/trả/gia hạn/đặt trước/tính phạt "
        "để cung cấp ngữ cảnh chính xác cho AI."
    )
    builder.add_bullet(
        "2. Skill 2: Kỹ Năng Kỹ Nghệ Câu Lệnh Chuyên Sâu (Advanced Prompt Engineering & Guardrails Skill): ",
        "Làm chủ các kỹ thuật thiết kế câu lệnh đỉnh cao: Role-based Persona (định hình chuyên gia), Context Grounding (cung cấp dữ liệu làm bằng chứng duy nhất), "
        "Few-shot In-Context Learning (đưa mẫu ví dụ mẫu mực), Zero-Hallucination Guardrails (rào chắn phủ định chống bịa đặt dữ liệu) "
        "và Structured Output Enforcement (ép kiểu dữ liệu đầu ra JSON / Pydantic Schemas)."
    )
    builder.add_bullet(
        "3. Skill 3: Kỹ Năng Kiến Trúc Phân Tầng Full-Stack & ORM (Full-Stack Layered Architecture & ACID Database Skill): ",
        "Khả năng định hướng AI thiết kế và tổ chức mã nguồn theo mô hình kiến trúc sạch (Clean Layered Architecture): "
        "FastAPI Asynchronous Routers -> Business Services -> SQLAlchemy 2.0 ORM -> SQLite Database. Năng lực kiểm soát giao dịch CSDL (Transaction Management) "
        "đảm bảo tính toàn vẹn ACID khi xử lý đồng thời tồn kho sách, cùng kỹ năng xây dựng giao diện người dùng hiện đại Glassmorphism bằng Vanilla CSS tokens."
    )
    builder.add_bullet(
        "4. Skill 4: Kỹ Năng Phát Triển Hướng Kiểm Thử & Đánh Giá AI (Test-Driven Development & AI Evaluation Skill): ",
        "Năng lực thiết kế bộ kiểm thử tự động toàn diện bằng Pytest, kỹ thuật cô lập môi trường kiểm thử (Isolated SQLite Test Fixtures), "
        "kỹ thuật Mocking dịch vụ AI bên ngoài (Mock AIService Fallback) để kiểm thử độc lập mà không phụ thuộc Internet hoặc API Key. "
        "Đồng thời, làm chủ phương pháp đánh giá chất lượng phản hồi AI qua các tiêu chí: Độ liên quan (Relevance), Độ trung thực (Faithfulness) và Không ảo giác (Zero-Hallucination)."
    )
    builder.add_bullet(
        "5. Skill 5: Kỹ Năng An Toàn Thông Tin & Quyền Riêng Tư AI (AI Privacy & Security-by-Design Skill): ",
        "Năng lực thẩm định an ninh mã nguồn (Security Audit), phát hiện và ngăn chặn các lỗ hổng OWASP Top 10 (SQL Injection, XSS, Broken Access Control). "
        "Triển khai triệt để nguyên tắc Privacy-by-Design và Thu nhỏ dữ liệu (Data Minimization): bóc tách và ẩn danh hóa hoàn toàn dữ liệu PII (họ tên, email, số điện thoại) "
        "của độc giả trước khi truyền tải sang API Gemini đám mây. Bảo vệ API bằng mã hóa mật khẩu Bcrypt và chữ ký số JWT HS256."
    )
    builder.add_bullet(
        "6. Skill 6: Kỹ Năng Đóng Gói Container & Vận Hành Khôi Phục (DevOps, Containerization & Disaster Recovery Skill): ",
        "Năng lực cấu hình Dockerfile đa tầng (Multi-stage Build) tối ưu hóa dung lượng, phối hợp dịch vụ qua Docker Compose, "
        "tích hợp máy công cụ tìm kiếm toàn văn FTS5 (SQLite Full-Text Search), xây dựng công cụ dòng lệnh sao lưu dữ liệu tự động (`backup_cli.py`) "
        "và lập kế hoạch dự phòng khôi phục thảm họa CSDL."
    )

    skills_matrix_headers = ["Kỹ Năng Kỹ Sư (Skill)", "Mục Tiêu Áp Dụng Trong Đồ Án", "Công Nghệ & Công Cụ Tương Ứng", "Đóng Góp Của AI", "Vai Trò Thẩm Định Của Sinh Viên"]
    skills_matrix_rows = [
        ["Skill 1: Domain Modeling", "Mô hình hóa nghiệp vụ thư viện & CSDL 3NF", "Draw.io, PlantUML, ERD, Relational Schema", "Đề xuất cấu trúc bảng và phát hiện edge cases", "Tách riêng bảng Users và Readers, chuẩn hóa khóa ngoại"],
        ["Skill 2: Prompt Engineering", "Xây dựng Chatbot tra cứu & tóm tắt không bịa đặt", "Google Gemini 1.5 Flash, Prompt Templates", "Sinh cấu trúc Prompt 5 lớp và mẫu từ chối lịch sự", "Thực nghiệm 3 vòng lặp, thêm rào chắn Zero-Hallucination"],
        ["Skill 3: Full-Stack Architecture", "Lập trình Backend FastAPI & Giao diện Vanilla CSS", "Python 3.12, FastAPI, SQLAlchemy 2.0, HTML/CSS/JS", "Sinh nhanh mã nguồn Boilerplate, CRUD endpoints", "Rà soát giao dịch ACID, tối ưu biến CSS Glassmorphism"],
        ["Skill 4: TDD & AI Evaluation", "Kiểm thử tự động 26 ca Pytest bao phủ 100%", "Pytest, Pytest-Asyncio, HTTPX, SQLite In-Memory", "Sinh khung 26 test functions và kịch bản biên", "Tách biệt Isolated Test Fixture, bổ sung Mock Fallback"],
        ["Skill 5: Security & Privacy", "Bảo vệ thông tin độc giả và phân quyền RBAC", "Bcrypt, JWT HS256, OAuth2, Data Minimization", "Cảnh báo nguy cơ rò rỉ PII sang Cloud API", "Ẩn danh hóa lịch sử mượn trước khi gửi sang Gemini"],
        ["Skill 6: DevOps & Recovery", "Đóng gói ứng dụng và sao lưu CSDL tự động", "Docker, Docker Compose, SQLite FTS5, Shell/CLI", "Sinh Dockerfile multi-stage và script backup CLI", "Cấu hình Volume bền vững và kiểm tra khôi phục CSDL thực tế"],
    ]
    builder.add_styled_table(
        "Bảng 8.1: Ma trận Khung Năng lực Kỹ sư Phần mềm (AI Engineering Skills Matrix) áp dụng trong đề tài",
        skills_matrix_headers,
        skills_matrix_rows,
        col_widths=[1.2, 1.5, 1.4, 1.4, 1.5]
    )

    # 8.7. Toàn Bộ Bộ Prompt Mẫu Chi Tiết (Master Prompt Catalog)
    builder.add_heading_2("8.7. Tuyển Tập Bộ Prompts Mẫu Chi Tiết Hoàn Thành Đồ Án (The Master Prompt Catalog)")
    builder.add_paragraph(
        "Dưới đây là tuyển tập 12 bộ câu lệnh (Prompts) tiêu biểu, được thiết kế chuẩn mực theo kỹ nghệ Prompt Engineering nâng cao, "
        "đã được nhóm sinh viên sử dụng tuần tự qua 4 giai đoạn SDLC để hoàn thiện toàn bộ hệ sinh thái đồ án. "
        "Mỗi kịch bản đều bao gồm: Mục tiêu kỹ thuật, Vai trò thiết lập (System Persona), Câu lệnh đầu vào chi tiết (User Prompt), "
        "Kết quả do AI sinh ra, và phần kiểm chứng, phản biện, tinh chỉnh mã nguồn của sinh viên."
    )

    def add_master_prompt_box(p_id, stage, title, persona, user_prompt, ai_response, human_refinement):
        content = (
            f"📌 MÃ SỐ PROMPT: {p_id} | GIAI ĐOẠN: {stage}\n"
            f"🎯 MỤC TIÊU KỸ THUẬT: {title}\n\n"
            f"🎭 SYSTEM PERSONA (THIẾT LẬP VAI TRÒ AI):\n{persona}\n\n"
            f"📝 USER PROMPT (CÂU LỆNH ĐẦU VÀO NGUYÊN VĂN):\n{user_prompt}\n\n"
            f"🤖 PHẢN HỒI CỦA AI (KẾT QUẢ SINH RA):\n{ai_response}\n\n"
            f"🔍 KIỂM CHỨNG & TINH CHỈNH CỦA SINH VIÊN (HUMAN REFINEMENT):\n{human_refinement}"
        )
        builder.add_callout(f"Prompt Chi Tiết {p_id}: {title} ({stage})", content)

    # Prompt P01
    add_master_prompt_box(
        "P01", "Giai đoạn 1 (Bài KT1)",
        "Phân Tích Nghiệp Vụ Thư Viện Đại Học & Nhận Diện Các Trường Hợp Biên (Edge Cases)",
        "Bạn là Chuyên gia Phân tích Nghiệp vụ Phần mềm (Lead Business Analyst) và Kiến trúc sư Hệ thống với hơn 15 năm kinh nghiệm trong ngành quản trị thư viện học thuật.",
        "Tôi đang xây dựng Hệ thống Quản lý Thư viện Đại học tích hợp AI (FastAPI + SQLite). "
        "Hãy phân tích chi tiết quy trình nghiệp vụ cốt lõi gồm: Mượn sách, Trả sách, Gia hạn sách, Đặt trước sách (Reservation) và Xử lý phạt trễ hạn. "
        "Yêu cầu đặc biệt: Liệt kê ít nhất 6 trường hợp ngoại lệ (Edge Cases / Exception Flows) mà hệ thống bắt buộc phải kiểm tra và chặn lỗi logic để đảm bảo không bị thất thoát tài sản thư viện.",
        "AI sinh ra bản đặc tả quy trình 5 bước và chỉ ra 6 Edge Cases trọng yếu: (1) Độc giả đang bị khóa thẻ cố tình mượn sách; (2) Mượn sách khi đã đạt hạn mức tối đa (5 cuốn); (3) Mượn sách có số lượng khả dụng bằng 0; (4) Gia hạn sách khi cuốn sách đó đã có độc giả khác đặt trước; (5) Trả sách quá hạn cần tính tiền phạt tự động 2,000đ/ngày; (6) Hủy đơn đặt trước khi quá thời hạn giữ sách (48 giờ).",
        "✅ Sinh viên kiểm chứng và bổ sung thêm Edge Case số 7: 'Chặn mượn sách mới nếu độc giả đang có khoản phạt quá hạn chưa thanh toán'. Đây là quy định thực tế tại các trường đại học mà AI ban đầu chưa đề cập."
    )

    # Prompt P02
    add_master_prompt_box(
        "P02", "Giai đoạn 1 (Bài KT1)",
        "Thiết Kế Ma Trận Phân Quyền RBAC & Danh Mục Use Case Cho 3 Nhóm Actor",
        "Bạn là Kiến trúc sư Bảo mật Phần mềm (Security Architect) am hiểu sâu sắc về mô hình kiểm soát truy cập dựa trên vai trò (Role-Based Access Control - RBAC).",
        "Hãy thiết kế Ma trận phân quyền chi tiết (RBAC Matrix) cho Hệ thống Quản lý Thư viện với 3 Actor: Admin (Quản trị viên), Librarian (Thủ thư), Reader (Độc giả). "
        "Liệt kê danh sách 10 Use Case trọng yếu, xác định quyền hạn cụ thể (Create, Read, Update, Delete, Execute) của từng Actor trên từng tài nguyên (Users, Readers, Books, Borrows, Fines, Reservations, AI Chatbot, Statistics).",
        "AI sinh bảng ma trận phân quyền 3 cột x 8 nhóm chức năng. Phân định rõ: Admin có toàn quyền quản lý tài khoản; Librarian có quyền tạo phiếu mượn, thu tiền phạt, cập nhật sách; Reader chỉ có quyền tra cứu sách, xem lịch sử cá nhân và sử dụng Chatbot AI.",
        "✅ Sinh viên điều chỉnh: Cho phép Thủ thư có quyền 'Miễn/Giảm phạt' có ghi chú lý do đặc biệt (sách bị lỗi kỹ thuật hoặc sự kiện miễn phí của nhà trường), đồng thời khóa quyền độc giả không được tự ý xóa đơn đặt trước nếu đơn đã chuyển sang trạng thái READY."
    )

    # Prompt P03
    add_master_prompt_box(
        "P03", "Giai đoạn 1 (Bài KT1)",
        "Thiết Kế Mô Hình Cơ Sở Dữ Liệu ERD Chuẩn Hóa 3NF Với 8 Thực Thể",
        "Bạn là Chuyên gia Thiết kế Cơ sở Dữ liệu (Database Architect) chuyên sâu về chuẩn hóa quan hệ 3NF và tối ưu hóa chỉ mục SQL.",
        "Hãy thiết kế lược đồ quan hệ CSDL (Relational Schema) đạt chuẩn 3NF cho 8 thực thể: Users, Readers, Categories, Authors, Books, BorrowRecords, Fines, Reservations. "
        "Yêu cầu: Xác định rõ Khóa chính (PK), Khóa ngoại (FK), kiểu dữ liệu SQLite, các ràng buộc toàn vẹn (Unique, Check, Default) và giải thích mối quan hệ (1:1, 1:N).",
        "AI đề xuất lược đồ 8 bảng với các liên kết khóa ngoại chặt chẽ. AI giải thích tính chuẩn hóa: Loại bỏ phụ thuộc hàm bắc cầu bằng cách tách Authors và Categories ra khỏi Books; tách Fines ra khỏi BorrowRecords để phục vụ thanh toán từng phần.",
        "✅ Sinh viên phát hiện AI ban đầu gộp chung Users và Readers làm một bảng. Sinh viên đã yêu cầu tách riêng `users` (chứa username, password_hash, role) và `readers` (chứa mã thẻ card_number, họ tên, email, phone, hạn thẻ) liên kết 1:1 qua `user_id`. Thiết kế này giúp hệ thống linh hoạt, cho phép Admin và Thủ thư không nhất thiết phải có hồ sơ thẻ độc giả."
    )

    # Prompt P04
    add_master_prompt_box(
        "P04", "Giai đoạn 2 (Bài KT2)",
        "Sinh Bộ Khung SQLAlchemy 2.0 ORM Models & Pydantic Schemas Với Validation",
        "Bạn là Lập trình viên Backend Python cao cấp (Senior Python Engineer) chuyên sâu về FastAPI, SQLAlchemy 2.0 và Pydantic v2.",
        "Hãy viết mã nguồn định nghĩa 8 SQLAlchemy Models trong thư mục `models/` tuân thủ cú pháp SQLAlchemy 2.0 DeclarativeBase, có `relationship()`, `cascade='all, delete-orphan'` phù hợp. "
        "Đồng thời viết các Pydantic Schemas tương ứng (`schemas.py`) bao gồm: Request Schemas (có Field validation: regex kiểm tra email, độ dài mật khẩu >= 6, số lượng sách >= 0) và Response Schemas có `from_attributes = True`.",
        "AI sinh đầy đủ các file models (`user.py`, `book.py`, `reader.py`, `borrow.py`, `fine.py`) và file `schemas.py` hoàn chỉnh với cú pháp hiện đại `Mapped[]` và `mapped_column()`.",
        "✅ Sinh viên kiểm tra và bổ sung ràng buộc kiểm tra chuỗi rỗng cho `title`, `author_id` và bổ sung giá trị mặc định `fine_amount_per_day = 2000` trong `config.py` để dễ dàng cấu hình thay đổi chính sách phạt."
    )

    # Prompt P05
    add_master_prompt_box(
        "P05", "Giai đoạn 2 (Bài KT2)",
        "Lập Trình Lớp Dịch Vụ Mượn/Trả Sách & Tính Phạt Tự Động Trong Database Transaction",
        "Bạn là Chuyên gia Xây dựng Logic Nghiệp vụ Phần mềm (Business Logic Expert).",
        "Hãy viết module `services/borrow_service.py` xử lý 3 nghiệp vụ quan trọng bằng SQLAlchemy Session: "
        "(1) `borrow_book()`: kiểm tra thẻ hoạt động, kiểm tra nợ phạt, trừ `available_quantity`, tạo BorrowRecord; "
        "(2) `return_book()`: cập nhật `return_date`, tăng `available_quantity`, tự động tính tiền phạt trễ hạn `overdue_days * 2000` VNĐ và kích hoạt đơn đặt trước (Reservation) sớm nhất; "
        "(3) `renew_book()`: gia hạn thêm 7 ngày nếu sách chưa quá hạn và chưa có người đặt trước. Đảm bảo toàn bộ thao tác nằm trong Transaction an toàn.",
        "AI sinh mã nguồn lớp `BorrowService` với các khối lệnh try-except, rollback khi lỗi và commit khi thành công.",
        "✅ Sinh viên trực tiếp phản biện và sửa đổi 2 điểm quan trọng: (1) Sửa logic khôi phục tồn kho thành `book.available_quantity = min(book.available_quantity + 1, book.total_quantity)` nhằm loại bỏ triệt để nguy cơ số khả dụng vượt quá tổng số thực có nếu nhân viên bấm trả nhầm 2 lần; (2) Chuyển trạng thái đơn đặt trước thành `READY` và gán thời hạn lấy sách 48 giờ."
    )

    # Prompt P06
    add_master_prompt_box(
        "P06", "Giai đoạn 2 (Bài KT2)",
        "Thiết Kế Hệ Thống Giao Diện Người Dùng Modern Light Glassmorphism Bằng Vanilla CSS",
        "Bạn là Chuyên gia Thiết kế Giao diện UI/UX Frontend (Senior UI/UX & CSS Specialist) với gu thẩm mỹ tinh tế, hiện đại.",
        "Hãy viết file `frontend/static/css/main.css` theo phong cách Modern Light Theme chuyên nghiệp, sang trọng: "
        "- Sử dụng hệ thống biến CSS Design Tokens (:root) cho màu sắc (Deep Indigo #1E1B4B, Indigo #4F46E5, Slate #0F172A), "
        "- Ứng dụng hiệu ứng Glassmorphism (nền mờ nhẹ, backdrop-filter: blur(12px), viền mờ border-color: rgba(...)), "
        "- Thiết kế Card thống kê nổi bật, bảng dữ liệu thanh lịch bo tròn cạnh, badges trạng thái đa màu sắc, modal popup và thanh điều hướng sidebar mượt mà. Tuyệt đối không dùng Bootstrap hay Tailwind.",
        "AI sinh hơn 600 dòng CSS chuẩn mực, phân chia rõ ràng các module: Reset, Typography (Inter/Roboto), Layout, Buttons, Form Inputs, Tables, Cards, Modals, Toasts và Media Queries tương thích di động.",
        "✅ Sinh viên tinh chỉnh: Cải thiện độ tương phản (Contrast Ratio) của chữ trên nền badge để đạt chuẩn WCAG AA cho người khiếm thị, và tối ưu hóa chuyển động hover (`transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1)`)."
    )

    # Prompt P07
    add_master_prompt_box(
        "P07", "Giai đoạn 3 (Bài KT3)",
        "Thiết Kế System Prompt Chatbot Tra Cứu Sách Với Grounded In-Context Retrieval",
        "Bạn là Chuyên gia Kỹ nghệ Câu lệnh (Prompt Engineer Lead) chuyên sâu về xây dựng Chatbot tra cứu thông tin chống ảo giác cho hệ thống dữ liệu đóng.",
        "Hãy viết file `prompts/search_prompt.py` xây dựng System Prompt và hàm `build_search_prompt(query, books_context)`. "
        "Yêu cầu: "
        "- Đóng vai: Thủ thư AI tận tâm của Thư viện Thông minh, "
        "- Grounding: Chỉ được phép tìm kiếm và gợi ý các cuốn sách có mặt trong chuỗi dữ liệu `books_context` được nạp vào, "
        "- Zero-Hallucination Guardrails: Cấm tuyệt đối việc tự bịa tên sách, tác giả hoặc năm xuất bản không có trong dữ liệu, "
        "- Mẫu từ chối: Nếu độc giả hỏi chủ đề mà thư viện không có sách, phải từ chối lịch sự và gợi ý chủ đề gần nhất, "
        "- Định dạng câu trả lời: Dùng Markdown rõ ràng kèm biểu tượng cảm xúc.",
        "AI sinh bản thiết kế Prompt với đầy đủ 5 lớp nguyên tắc bảo vệ, phân tách rõ vai trò System và User.",
        "✅ Sinh viên kiểm nghiệm thực tế: Thêm ràng buộc giới hạn độ dài câu hỏi tối đa 500 ký tự và cơ chế tiền lọc từ khóa (SQL Keyword Pre-filter) trước khi gửi danh mục sách vào Prompt, giúp tiết kiệm 70% lượng token tiêu thụ."
    )

    # Prompt P08
    add_master_prompt_box(
        "P08", "Giai đoạn 3 (Bài KT3)",
        "Thực Nghiệm & Tinh Chỉnh Prompt Qua 3 Vòng Lặp (Iterations) Triệt Tiêu Ảo Giác",
        "Bạn là Nhà nghiên cứu Đánh giá Mô hình AI (AI Evaluation & Benchmarking Researcher).",
        "Hãy phân tích và xây dựng báo cáo thực nghiệm 3 vòng lặp tinh chỉnh Prompt (Prompt Iteration Experiments) cho tính năng gợi ý sách: "
        "- Vòng 1 (Baseline Prompt): Thử nghiệm câu lệnh cơ bản, phân tích hiện tượng ảo giác khi người dùng hỏi sách ngoài danh mục; "
        "- Vòng 2 (Rule-based Guardrails): Thêm các quy tắc phủ định nghiêm ngặt; "
        "- Vòng 3 (Few-shot Grounded Prompt): Cung cấp ví dụ mẫu câu trả lời chuẩn và yêu cầu trích xuất ID sách chính xác. "
        "Lập bảng so sánh tỷ lệ chính xác (Accuracy), tỷ lệ ảo giác (Hallucination Rate) và thời gian phản hồi qua 3 vòng.",
        "AI xây dựng bảng so sánh chi tiết và phân tích sâu nguyên nhân khiến mô hình bị 'lạc đề' ở vòng 1 (do thiếu rào chắn phủ định) và cách khắc phục triệt để ở vòng 3.",
        "✅ Sinh viên thực hiện chạy kiểm thử thực nghiệm trên 20 kịch bản câu hỏi hóc búa, xác nhận tỷ lệ ảo giác giảm từ 35% (ở Vòng 1) xuống 0% (ở Vòng 3)."
    )

    # Prompt P09
    add_master_prompt_box(
        "P09", "Giai đoạn 3 (Bài KT3)",
        "Thiết Kế Prompt Tóm Tắt Sách & Gợi Ý Cá Nhân Hóa Dựa Trên Lịch Sử Mượn",
        "Bạn là Chuyên gia Xây dựng Hệ thống Gợi ý (Recommendation System Engineer) và Chuyên gia Tóm tắt Văn bản NLP.",
        "Hãy viết mã nguồn cho 2 template Prompt: "
        "(1) `summary_prompt.py`: Nhận thông tin mô tả chi tiết của một cuốn sách và sinh đoạn tóm tắt hấp dẫn dài 3-5 câu, làm nổi bật giá trị cốt lõi và đối tượng độc giả phù hợp; "
        "(2) `suggest_prompt.py`: Nhận danh mục lịch sử các thể loại và cuốn sách độc giả đã từng mượn (đã ẩn danh thông tin cá nhân), kết hợp với kho sách hiện có của thư viện để gợi ý 3 cuốn sách tiếp theo kèm lời giải thích thuyết phục.",
        "AI sinh 2 module template hoàn chỉnh, tích hợp biến định dạng Python string format an toàn.",
        "✅ Sinh viên tinh chỉnh: Thêm tham số nhiệt độ `temperature=0.2` cho tóm tắt (để tăng tính chính xác, cô đọng) và `temperature=0.5` cho gợi ý (để tăng sự phong phú, sáng tạo nhưng vẫn bám sát dữ liệu thực tế)."
    )

    # Prompt P10
    add_master_prompt_box(
        "P10", "Giai đoạn 3 (Bài KT3)",
        "Sinh Toàn Bộ Bộ Kiểm Thử Tự Động 26 Ca Pytest & Thiết Lập Isolated Test Fixtures",
        "Bạn là Kỹ sư Tự động hóa Kiểm thử Cấp cao (Senior QA Automation Engineer) chuyên sâu về Pytest, HTTPX và Test-Driven Development (TDD).",
        "Hãy viết bộ kiểm thử tự động toàn diện gồm 2 file trong thư mục `tests/`: "
        "- `test_borrow.py`: 14 test cases kiểm thử độc lập cho nghiệp vụ mượn sách, mượn trùng, mượn sách hết bản, gia hạn, trả sách đúng hạn, trả sách quá hạn tính phạt 2000đ/ngày, thanh toán tiền phạt; "
        "- `test_ai.py`: 12 test cases kiểm thử các endpoint AI (`/api/ai/search`, `/api/ai/summarize/{id}`, `/api/ai/suggest`), kiểm thử trường hợp sách không tồn tại, kiểm thử cơ chế Mock AI Fallback khi không có API key. "
        "Yêu cầu: Thiết kế Pytest Fixture sử dụng SQLite Test Database riêng biệt, tự động seed dữ liệu mẫu trước mỗi test và dọn dẹp sau khi chạy xong.",
        "AI sinh toàn bộ mã nguồn kiểm thử với đầy đủ assertions kiểm tra Status Code, JSON response structure và dữ liệu cập nhật trong CSDL.",
        "✅ Sinh viên kiểm thử và phát hiện lỗi xung đột khóa file SQLite trên hệ điều hành Windows khi nhiều hàm test cùng truy cập 1 file. Sinh viên đã tinh chỉnh fixture để dọn dẹp session triệt để (`session.close()`, `engine.dispose()`) trước khi gỡ file test db."
    )

    # Prompt P11
    add_master_prompt_box(
        "P11", "Giai đoạn 4 (Bài Cuối kỳ)",
        "Rà Soát An Toàn Thông Tin Mã Nguồn & Che Giấu Dữ Liệu Cá Nhân Độc Giả (Privacy-by-Design)",
        "Bạn là Chuyên gia Đánh giá An ninh Ứng dụng (Application Security Auditor) và Chuyên gia Tuân thủ Quyền Riêng tư (Data Privacy Officer).",
        "Hãy rà soát toàn bộ các routers API trong thư mục `backend/routers/` và `services/ai_service.py` để tìm các lỗ hổng an ninh tiềm ẩn: "
        "(1) Có rò rỉ dữ liệu định danh cá nhân độc giả (Họ tên, SĐT, Email, Địa chỉ) sang bên thứ ba (Google Gemini API) không? "
        "(2) Token JWT có được bảo vệ và kiểm tra hết hạn đúng cách không? "
        "(3) Có nguy cơ bị tấn công Prompt Injection không? "
        "Hãy đề xuất giải pháp kỹ thuật cụ thể để khắc phục triệt để.",
        "AI chỉ ra nguy cơ tại endpoint `/api/ai/suggest`: code ban đầu đang truyền toàn bộ object `BorrowRecord` (có chứa thông tin độc giả) vào Prompt. AI đề xuất giải pháp bóc tách chỉ gửi danh sách thể loại và tựa sách đã mượn.",
        "✅ Sinh viên đã hiện thực hóa kỹ thuật Data Minimization: Tạo hàm `anonymize_reader_history()` để lọc sạch 100% PII trước khi đóng gói payload gửi đến LLM. Bổ sung regex kiểm tra sanitize câu hỏi tìm kiếm để ngăn chặn các câu lệnh tiêm nhiễm (Jailbreak / System Override)."
    )

    # Prompt P12
    add_master_prompt_box(
        "P12", "Giai đoạn 4 (Bài Cuối kỳ)",
        "Đóng Gói Ứng Dụng Đa Nền Tảng Với Docker Compose & Viết Công Cụ CLI Sao Lưu CSDL",
        "Bạn là Chuyên gia Kỹ thuật Vận hành DevOps & SRE (Site Reliability Engineer).",
        "Hãy viết các cấu hình triển khai hoàn thiện cho dự án: "
        "- `Dockerfile`: Sử dụng multi-stage build từ `python:3.12-slim`, tối ưu hóa kích thước image, tạo người dùng non-root `appuser` để tăng cường bảo mật; "
        "- `docker-compose.yml`: Định nghĩa service `web`, ánh xạ cổng 8000:8000, thiết lập biến môi trường, cấu hình volume lưu trữ bền vững cho file CSDL `library.db` và thư mục `backups/`; "
        "- `backup_cli.py`: Công cụ dòng lệnh hỗ trợ sao lưu thủ công/tự động CSDL SQLite, nén gzip và khôi phục dữ liệu nhanh chóng khi có sự cố.",
        "AI sinh toàn bộ file Dockerfile, docker-compose.yml và file mã nguồn Python CLI `backup_cli.py` với các lệnh `backup`, `restore`, `list` trực quan.",
        "✅ Sinh viên đã thử nghiệm build và chạy thành công trên cả Docker Desktop Windows và Linux Server, xác nhận dữ liệu trong CSDL vẫn an toàn nguyên vẹn sau khi khởi động lại container."
    )

    # 8.8. Bốn kịch bản đối thoại kỹ thuật tiêu biểu
    builder.add_heading_2("8.8. Minh chứng 4 Kịch bản Đối thoại Kỹ thuật Tiêu Biểu (Pair Programming Dialogues)")
    builder.add_paragraph(
        "Để minh họa sinh động phương pháp làm việc 'Cộng tác Lập trình cùng AI' (Pair Programming), "
        "dưới đây là 4 trích đoạn đối thoại kỹ thuật thực tế giữa sinh viên và AI trợ lý trong quá trình giải quyết các bài toán hóc búa:"
    )

    def add_dialogue_callout(dialogue_id, title, prompt_text, ai_text, review_text):
        full_text = f"👤 PROMPT CỦA SINH VIÊN:\n{prompt_text}\n\n🤖 PHẢN HỒI CỦA AI TRỢ LÝ:\n{ai_text}\n\n🔍 KIỂM CHỨNG & CHỈNH SỬA CỦA SINH VIÊN:\n{review_text}"
        builder.add_callout(f"Kịch bản Đối thoại {dialogue_id}: {title}", full_text)

    add_dialogue_callout(
        "ĐH01", "Thiết kế Thuật toán Tính Phạt & Khôi phục Tồn kho (Bài KT2)",
        "Hãy viết hàm Python SQLAlchemy nhận ID phiếu mượn, cập nhật ngày trả thực tế, tăng tồn kho khả dụng, tính phạt trễ hạn 2000đ/ngày nếu quá hạn, và đổi trạng thái đơn đặt trước sớm nhất sang READY.",
        "AI sinh mã nguồn hàm `return_book()` bao gồm logic trừ ngày `(today - record.due_date).days`, tạo bản ghi `Fine(total_amount=overdue_days * 2000)` và truy vấn đơn `Reservation` sớm nhất.",
        "Sinh viên phát hiện AI thiếu kiểm tra trạng thái phiếu đã trả trước đó và chưa giới hạn `available_quantity <= total_quantity`. Sinh viên đã bổ sung 2 điều kiện này vào mã nguồn chính thức."
    )

    add_dialogue_callout(
        "ĐH02", "Tối ưu hóa System Prompt Chống Ảo Giác (Bài KT3)",
        "Prompt tra cứu sách hiện tại thỉnh thoảng tự bịa ra sách tiếng Anh không có trong thư viện khi độc giả hỏi chủ đề mới. Hãy viết lại System Prompt có các ràng buộc phủ định mạnh mẽ để triệt tiêu 100% lỗi này.",
        "AI sinh ra bộ 5 nguyên tắc Zero-Hallucination Guardrails, ép buộc mô hình CHỈ ĐƯỢC PHÉP trả lời từ danh sách sách cung cấp trong ngữ cảnh, và đưa ra mẫu câu từ chối lịch sự khi không tìm thấy sách.",
        "Sinh viên kiểm thử thực tế với 10 câu hỏi khó và nhận thấy AI hoàn toàn không bịa sách nữa. Sinh viên quyết định đưa Prompt này vào production."
    )

    add_dialogue_callout(
        "ĐH03", "Sinh Bộ Kiểm Thử Tự Động Pytest Cô Lập (Bài KT3)",
        "Hãy viết file test Pytest cho API mượn/trả sách FastAPI sử dụng database SQLite in-memory test fixtures, bao phủ các trường hợp: mượn thành công, mượn sách hết bản, trả sách quá hạn và kiểm tra token auth.",
        "AI sinh bộ fixture `test_client`, `librarian_token`, `reader_token`, `sample_book` và 14 hàm test với assertions đầy đủ.",
        "Sinh viên tinh chỉnh lại fixture để sử dụng SQLite test file riêng biệt và dọn dẹp sau mỗi lượt chạy để tránh xung đột khóa file trên hệ điều hành Windows."
    )

    add_dialogue_callout(
        "ĐH04", "Rà soát An Toàn Thông Tin & Quyền Riêng Tư (Bài Cuối kỳ)",
        "Hãy rà soát toàn bộ các file trong thư mục `routers/ai.py` để tìm các nguy cơ vi phạm an toàn thông tin và rò rỉ dữ liệu cá nhân của người dùng sang Google Gemini API.",
        "AI chỉ ra rằng endpoint `/api/ai/suggest` đang gửi toàn bộ bản ghi `BorrowRecord` (bao gồm `reader_id`, `reader_name`, `phone`) sang prompt. AI đề xuất chỉ gửi `book.title` và `category.name`.",
        "Sinh viên đã tái cấu trúc lại hàm để ẩn danh hóa hoàn toàn dữ liệu trước khi gửi sang Gemini, đảm bảo tuân thủ nguyên tắc Privacy-by-Design."
    )

    # 8.9. Bảng nhật ký Prompt chi tiết
    builder.add_heading_2("8.9. Nhật Ký Sử Dụng AI (Prompt Log) Xuyên Suốt 4 Giai Đoạn")
    builder.add_paragraph(
        "Bảng tổng hợp chi tiết toàn bộ 12 lượt tương tác kỹ thuật quan trọng giữa nhóm phát triển và AI trợ lý trong suốt 4 giai đoạn SDLC:"
    )

    prompt_log_headers = ["Mã & GĐ", "Mục tiêu Kỹ thuật", "Tóm tắt Prompt gửi AI", "Đóng góp của AI", "Phần Sinh viên Kiểm chứng & Tinh chỉnh"]
    prompt_log_rows = [
        ["P01 (KT1)", "Phân tích nghiệp vụ mượn trả", "Phân tích quy trình mượn/trả/gia hạn/đặt trước & edge cases", "Sinh danh sách 5 quy trình và 6 trường hợp ngoại lệ", "✅ Bổ sung Edge Case: 'Chặn mượn sách khi còn nợ phạt trễ hạn'."],
        ["P02 (KT1)", "Thiết kế ma trận RBAC", "Thiết kế ma trận phân quyền 3 roles x 8 tài nguyên", "Sinh ma trận quyền hạn Create/Read/Update/Delete", "✅ Bổ sung quyền miễn giảm phạt cho Thủ thư kèm ghi chú bắt buộc."],
        ["P03 (KT1)", "Thiết kế CSDL chuẩn 3NF", "Thiết kế quan hệ ERD 8 bảng, khóa chính, khóa ngoại", "Sinh lược đồ quan hệ 8 thực thể chuẩn hóa 3NF", "✅ Tách bảng Users và Readers để hỗ trợ tài khoản quản trị viên."],
        ["P04 (KT2)", "Sinh ORM Models & Schemas", "Viết SQLAlchemy 2.0 Models & Pydantic v2 validation", "Sinh mã nguồn models và schemas đầy đủ", "✅ Bổ sung regex kiểm tra email và giá trị mặc định tiền phạt 2000đ/ngày."],
        ["P05 (KT2)", "Lập trình BorrowService", "Tạo hàm mượn/trả/gia hạn an toàn trong Transaction", "Sinh khung hàm nghiệp vụ và tính ngày quá hạn", "✅ Thêm ràng buộc `min(available + 1, total)` tránh tràn tồn kho."],
        ["P06 (KT2)", "Thiết kế giao diện CSS", "Viết Vanilla CSS Glassmorphism hiện đại với biến tokens", "Sinh hơn 600 dòng CSS chuẩn mực, responsive", "✅ Tinh chỉnh độ tương phản text WCAG AA và hiệu ứng hover cards."],
        ["P07 (KT3)", "Thiết kế System Prompt", "Thiết kế System Prompt Chatbot Grounded In-Context", "Sinh 5 nguyên tắc Zero-Hallucination Guardrails", "✅ Giới hạn câu hỏi <= 500 ký tự và tiền lọc SQL trước khi gọi AI."],
        ["P08 (KT3)", "Tối ưu Prompt 3 vòng", "Thử nghiệm 3 vòng lặp tinh chỉnh Prompt gợi ý sách", "Lập bảng so sánh Accuracy, Hallucination qua 3 vòng", "✅ Thực nghiệm 20 kịch bản, xác nhận triệt tiêu ảo giác về 0%."],
        ["P09 (KT3)", "Prompt Tóm tắt & Gợi ý", "Template tóm tắt sách cô đọng và gợi ý theo lịch sử", "Sinh template chuỗi định dạng cho Gemini", "✅ Thiết lập `temperature=0.2` cho tóm tắt và `0.5` cho gợi ý sách."],
        ["P10 (KT3)", "Sinh 26 ca test Pytest", "Viết 14 test nghiệp vụ + 12 test AI với SQLite riêng", "Sinh trọn bộ mã nguồn test suite Pytest", "✅ Khắc phục lỗi Windows file lock bằng Isolated Test Fixtures."],
        ["P11 (Cuối kỳ)", "Review bảo mật Privacy", "Rà soát lỗ hổng PII và nguy cơ Prompt Injection", "Phát hiện gửi thông tin độc giả sang Gemini API", "✅ Tạo hàm `anonymize_reader_history()` lọc sạch 100% PII."],
        ["P12 (Cuối kỳ)", "Docker & Backup CLI", "Viết Dockerfile multi-stage, compose và script backup", "Sinh cấu hình Docker tối ưu và tool CLI backup/restore", "✅ Kiểm tra volume CSDL bền vững và diễn tập khôi phục thành công."],
    ]
    builder.add_styled_table(
        "Bảng 8.2: Bảng nhật ký Prompt (Prompt Log) chi tiết 12 tương tác kỹ thuật trong toàn bộ chu trình SDLC",
        prompt_log_headers,
        prompt_log_rows,
        col_widths=[1.0, 1.4, 1.8, 1.5, 1.5]
    )

    # 8.10. Bài học kinh nghiệm
    builder.add_heading_2("8.10. Bài học Kinh nghiệm & Nguyên Tắc Vàng Khi Pair Programming Cùng AI")
    builder.add_paragraph(
        "Từ quá trình thực tế áp dụng AI vào toàn bộ quy trình phát triển đề tài, nhóm sinh viên đã đúc kết được "
        "4 bài học mang tính phương pháp luận và nguyên tắc thực hành kỹ nghệ phần mềm hiện đại:",
        bold_prefix="Đúc kết kinh nghiệm: "
    )
    builder.add_bullet(
        "1. AI là 'Bộ khuếch đại năng suất', không phải 'Người thay thế tư duy': ",
        "AI có thể sinh ra hàng trăm dòng mã nguồn chỉ trong vài giây, nhưng chỉ có kỹ sư phần mềm con người mới thấu hiểu "
        "trọn vẹn các yêu cầu nghiệp vụ thực tế, các quy tắc bảo mật và phát hiện ra các lỗ hổng logic tinh vi "
        "(như lỗi tràn số lượng sách khả dụng hoặc lỗ hổng rò rỉ dữ liệu cá nhân)."
    )
    builder.add_bullet(
        "2. Kỹ năng Prompt Engineering quyết định 80% chất lượng sản phẩm: ",
        "Một câu lệnh mơ hồ, chung chung sẽ chỉ nhận về kết quả sơ sài và dễ bị ảo giác. "
        "Việc nắm vững các kỹ thuật phân vai (Persona), cung cấp ngữ cảnh nền tảng (Context Grounding), "
        "đưa ra rào chắn phủ định (Negative Guardrails) và ép kiểu đầu ra (Schema Enforcement) là chìa khóa để làm chủ công nghệ AI."
    )
    builder.add_bullet(
        "3. Kiểm thử tự động (Automated Testing) là 'Lưới bảo vệ sinh mệnh': ",
        "Tuyệt đối không bao giờ tin tưởng mã nguồn do AI sinh ra khi chưa có kiểm thử. "
        "Việc xây dựng bộ 26 ca kiểm thử tự động Pytest bao phủ 100% là bằng chứng thép bảo đảm hệ thống hoạt động ổn định, "
        "không phát sinh lỗi hồi quy (Regression Bugs) khi nâng cấp."
    )
    builder.add_bullet(
        "4. Nguyên tắc Privacy-by-Design là tiêu chuẩn đạo đức và an ninh số 1: ",
        "Khi đưa Trí tuệ Nhân tạo vào các hệ thống quản trị đời sống thực, việc bảo vệ quyền riêng tư của người dùng là tối thượng. "
        "Phải luôn ghi nhớ nguyên tắc Thu nhỏ dữ liệu (Data Minimization): Không bao giờ gửi dữ liệu cá nhân nhạy cảm lên các mô hình đám mây "
        "khi tác vụ đó chỉ đơn thuần cần dữ liệu về sách."
    )

    builder.doc.add_page_break()
