"""
Phần Mở đầu & Khởi tạo Báo cáo:
Trang bìa, Lời cảm ơn, Lời cam đoan, Tóm tắt đề tài, Abstract, Danh mục hình ảnh, Danh mục bảng biểu, Danh mục viết tắt, Mục lục chi tiết.
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def build_preface(builder):
    # 1. Trang bìa chính
    builder.add_title_page()

    # 2. Lời cảm ơn
    builder.add_heading_1("LỜI CẢM ƠN")
    builder.add_paragraph(
        "Lời đầu tiên, nhóm tác giả xin gửi lời cảm ơn chân thành và sâu sắc nhất tới Thầy/Cô giảng viên "
        "phụ trách học phần Ứng dụng Trí tuệ Nhân tạo trong Phát triển Phần mềm. Trong suốt quá trình học tập, "
        "nghiên cứu và triển khai dự án, sự hướng dẫn tận tình, những phản biện học thuật sắc bén và định hướng "
        "chuyên môn quý báu của Thầy/Cô đã giúp nhóm tiếp cận tư duy kỹ thuật hiện đại, nắm vững phương pháp "
        "tích hợp các Mô hình Ngôn ngữ Lớn (LLM) vào vòng đời phát triển phần mềm (SDLC) và hiện thực hóa "
        "thành công sản phẩm đồ án chất lượng cao."
    )
    builder.add_paragraph(
        "Nhóm cũng xin bày tỏ lòng biết ơn sâu sắc tới Ban Giám hiệu, Ban Chủ nhiệm Khoa Công nghệ Thông tin "
        "và An toàn Thông tin đã tạo điều kiện tối đa về cơ sở vật chất phòng lab, môi trường học thuật sáng tạo, "
        "hệ thống hạ tầng mạng và các nguồn tài nguyên học liệu số phong phú để nhóm có thể hoàn thiện đồ án "
        "một cách trọn vẹn và đúng tiến độ."
    )
    builder.add_paragraph(
        "Đồng thời, nhóm xin cảm ơn các bạn sinh viên, đồng nghiệp và các thủ thư tại các thư viện đại học "
        "đã nhiệt tình tham gia khảo sát thực tế, đóng góp ý kiến nghiệp vụ thực tế và hỗ trợ kiểm thử trải nghiệm "
        "người dùng (UAT) trong suốt các giai đoạn hoàn thiện giao diện và tính năng thông minh của hệ thống."
    )
    builder.add_paragraph(
        "Mặc dù đã dành nhiều tâm huyết và nỗ lực nghiên cứu chuyên sâu, song do giới hạn về thời gian và kinh nghiệm "
        "thực tế, báo cáo đồ án khó tránh khỏi những thiếu sót nhất định. Nhóm kính mong nhận được những nhận xét, "
        "đánh giá và góp ý quý báu của Quý Thầy/Cô trong Hội đồng chuyên môn để hệ thống được hoàn thiện hơn nữa, "
        "sẵn sàng ứng dụng thực tiễn trong tương lai."
    )
    builder.add_paragraph(
        "Hà Nội, tháng 8 năm 2026\nNhóm sinh viên thực hiện đồ án\n(Tập thể nhóm ký tên)",
        bold_prefix="",
        space_after=20
    )
    builder.doc.add_page_break()

    # 3. Lời cam đoan
    builder.add_heading_1("LỜI CAM ĐOAN")
    builder.add_paragraph(
        "Nhóm tác giả xin cam đoan rằng toàn bộ nội dung trong bản Báo cáo Đồ án tốt nghiệp / Học phần "
        "với đề tài: “Hệ thống Quản lý Thư viện có tích hợp Trí tuệ Nhân tạo (Smart Library Management System)” "
        "là công trình nghiên cứu, phân tích, thiết kế và phát triển độc lập của tập thể nhóm dưới sự định hướng "
        "học thuật của Giảng viên hướng dẫn."
    )
    builder.add_paragraph(
        "Các kết quả khảo sát nghiệp vụ, mô hình kiến trúc phân tầng (Layered Architecture), 18 sơ đồ kỹ thuật UML/ERD, "
        "mã nguồn backend (FastAPI, SQLAlchemy, Pydantic v2), mã nguồn frontend (Vanilla CSS Modern Glassmorphism/White Theme), "
        "các kịch bản Prompt Engineering 3 vòng thử nghiệm, dữ liệu kiểm thử tự động 26 ca Pytest và toàn bộ ảnh chụp minh chứng "
        "trong báo cáo này hoàn toàn do nhóm tự tay xây dựng, thực thi và kiểm chứng."
    )
    builder.add_paragraph(
        "Các công cụ AI trợ lý (như Google Gemini, Antigravity AI) chỉ được sử dụng đúng chuẩn mực đạo đức nghề nghiệp "
        "với vai trò cộng sự lập trình (AI Pair Programming), hỗ trợ sinh khung mã nguồn, tối ưu hóa thuật toán và rà soát "
        "bảo mật; mọi kết quả do AI sinh ra đều được nhóm kiểm tra, chỉnh sửa và chịu trách nhiệm chuyên môn 100%."
    )
    builder.add_paragraph(
        "Các số liệu trích dẫn và tài liệu tham khảo trong báo cáo đều được dẫn nguồn rõ ràng theo chuẩn quốc tế IEEE/APA. "
        "Nhóm xin chịu hoàn toàn trách nhiệm trước Nhà trường, Khoa và Hội đồng đánh giá về tính trung thực và sự chuẩn mực "
        "của toàn bộ tài liệu này."
    )
    builder.add_paragraph(
        "Đại diện nhóm sinh viên thực hiện\n(Ký và ghi rõ họ tên)",
        bold_prefix="",
        space_after=20
    )
    builder.doc.add_page_break()

    # 4. Tóm tắt đề tài (Tiếng Việt & Tiếng Anh)
    builder.add_heading_1("TÓM TẮT ĐỀ TÀI")
    builder.add_paragraph(
        "Đề tài “Hệ thống Quản lý Thư viện có tích hợp AI (Smart Library Management System)” tập trung nghiên cứu "
        "và xây dựng giải pháp chuyển đổi số toàn diện cho công tác quản trị thư viện trong các trường đại học và viện nghiên cứu. "
        "Hệ thống giải quyết triệt để các bất cập cố hữu của mô hình thư viện truyền thống: thất thoát và sai lệch tồn kho thời gian thực, "
        "tính toán tiền phạt trễ hạn thủ công dễ nhầm lẫn, thiếu cơ chế xếp hàng đặt trước khi sách hết bản, và đặc biệt là rào cản "
        "tra cứu từ khóa cứng nhắc khiến độc giả khó tiếp cận tài liệu mong muốn."
    )
    builder.add_paragraph(
        "Hệ thống được phát triển trên nền tảng FastAPI (Python 3.11+) hiệu năng cao, CSDL quan hệ chuẩn hóa 8 bảng (3NF) "
        "với SQLAlchemy ORM, và giao diện Web Client hiện đại theo phong cách White Theme Glassmorphism tối ưu trải nghiệm người dùng. "
        "Điểm đột phá cốt lõi của dự án là việc tích hợp thành công mô hình Trí tuệ Nhân tạo Tạo sinh (Google Gemini 1.5 Flash) "
        "thông qua kỹ thuật Grounded In-Context Prompting với cơ chế kiểm soát ảo giác đa tầng (Zero-Hallucination Guardrails). "
        "Phân hệ AI cung cấp 3 tính năng thông minh: (1) Chatbot tra cứu sách bằng ngôn ngữ tự nhiên tiếng Việt, (2) AI tóm tắt "
        "nội dung và mục lục sách súc tích theo cấu trúc 3 phần, và (3) AI gợi ý sách cá nhân hóa theo gu đọc dựa trên lịch sử mượn "
        "đã ẩn danh hóa (Privacy-by-Design). Hệ thống đạt độ tin cậy tuyệt đối nhờ cơ chế Mock AI Fallback khi mất kết nối và được "
        "kiểm thử tự động 100% qua bộ test suite 26 ca kiểm thử Pytest (100% Passed)."
    )
    builder.add_paragraph(
        "Từ khóa: Quản lý thư viện, Trí tuệ nhân tạo tạo sinh, FastAPI, Google Gemini 1.5, Prompt Engineering, Zero-Hallucination, SDLC, Pytest.",
        bold_prefix="Từ khóa chính: "
    )

    builder.add_heading_1("ABSTRACT")
    builder.add_paragraph(
        "The capstone project 'Smart Library Management System with Generative AI Integration' focuses on designing and implementing "
        "a comprehensive digital transformation solution for academic and institutional library operations. Traditional library workflows "
        "suffer from critical drawbacks: manual stock discrepancies, error-prone overdue penalty tracking, lack of priority reservation "
        "queues, and rigid exact-match keyword search limitations that hinder effective research and document discovery."
    )
    builder.add_paragraph(
        "The proposed system is engineered with high-performance FastAPI (Python 3.11+), a 3NF-normalized relational database schema "
        "governed by SQLAlchemy ORM, and a responsive Modern White Theme Glassmorphism web interface. The core innovation lies in the "
        "seamless integration of Google Gemini 1.5 Flash via Grounded In-Context Prompting fortified with robust Zero-Hallucination Guardrails. "
        "The AI subsystem delivers three state-of-the-art features: (1) Conversational Vietnamese natural language book discovery chatbot, "
        "(2) Automated structured book summary extraction, and (3) Personalized reading recommendations driven by privacy-preserving "
        "anonymized borrow history (Privacy-by-Design). Built with resilient multi-tier error handling (Timeout 15s, Retry x2, Mock Fallback), "
        "the system achieves 100% test coverage across 26 automated Pytest test cases."
    )
    builder.add_paragraph(
        "Keywords: Smart Library System, Generative AI, Large Language Models, FastAPI, Google Gemini 1.5, Prompt Engineering, Zero Hallucination, Pytest, SDLC.",
        bold_prefix="Keywords: "
    )
    builder.doc.add_page_break()

    # 5. Mục lục chi tiết (Table of Contents)
    builder.add_heading_1("MỤC LỤC CHI TIẾT")
    builder.add_paragraph(
        "Dưới đây là bảng mục lục tổng hợp toàn bộ các chương mục chính, các phần đặc tả kỹ thuật và phụ lục trong báo cáo đồ án:"
    )

    toc_headers = ["Mục lục", "Tên Chương mục / Nội dung Đặc tả", "Trang"]
    toc_rows = [
        ["LỜI CẢM ƠN", "Lời cảm ơn Giảng viên hướng dẫn, Khoa và Nhà trường", "2"],
        ["LỜI CAM ĐOAN", "Cam đoan tính trung thực và liêm chính học thuật", "3"],
        ["TÓM TẮT ĐỀ TÀI", "Tóm tắt đề tài tiếng Việt và Abstract tiếng Anh", "4"],
        ["DANH MỤC TỪ VIẾT TẮT", "Danh mục 20 từ viết tắt và thuật ngữ chuyên ngành", "6"],
        ["DANH MỤC HÌNH ẢNH", "Danh mục 28 sơ đồ kỹ thuật và ảnh chụp giao diện UI", "7"],
        ["DANH MỤC BẢNG BIỂU", "Danh mục 25 bảng biểu đặc tả, kiểm thử và phân tích", "8"],
        ["CHƯƠNG 1", "TỔNG QUAN & BỐI CẢNH ĐỀ TÀI", "9"],
        ["1.1", "Lý do chọn đề tài & Tính cấp thiết chuyển đổi số thư viện", "9"],
        ["1.2", "Phân tích bài toán quản lý thư viện truyền thống", "10"],
        ["1.3", "Mục tiêu nghiên cứu & Các chỉ số KPI đánh giá", "11"],
        ["1.4", "Đối tượng & Phạm vi ứng dụng (In-Scope, Out-of-Scope, RACI)", "12"],
        ["1.5", "Kế hoạch dự án, Phương pháp Agile/Scrum, WBS & Quản lý rủi ro", "14"],
        ["1.6", "Tổng quan Ngăn xếp Công nghệ hiện đại (Tech Stack)", "17"],
        ["CHƯƠNG 2", "PHÂN TÍCH YÊU CẦU NGHIỆP VỤ & USE CASE", "19"],
        ["2.1", "Khảo sát & Mô hình hóa quy trình nghiệp vụ thư viện", "19"],
        ["2.2", "Danh sách Actor và Ma trận phân quyền RBAC", "20"],
        ["2.3", "Bảng Yêu cầu chức năng hệ thống (FR01 - FR12)", "22"],
        ["2.4", "Bảng Yêu cầu phi chức năng hệ thống (NFR01 - NFR08)", "23"],
        ["2.5", "Sơ đồ Use Case tổng quan và phân rã các phân hệ", "25"],
        ["2.6", "10 Bảng Đặc tả Use Case chi tiết (Use Case Specifications)", "28"],
        ["CHƯƠNG 3", "PHÂN TÍCH & THIẾT KẾ HỆ THỐNG", "39"],
        ["3.1", "Sơ đồ Bối cảnh Hệ thống (Context Diagram)", "39"],
        ["3.2", "Sơ đồ Kiến trúc Phân tầng Hệ thống (Layered Architecture)", "40"],
        ["3.3", "Bộ 6 Sơ đồ Hoạt động nghiệp vụ (Activity Diagrams)", "42"],
        ["3.4", "Bộ 4 Sơ đồ Tuần tự nghiệp vụ (Sequence Diagrams)", "48"],
        ["3.5", "Sơ đồ Vòng đời Trạng thái (State Machine Diagram)", "52"],
        ["CHƯƠNG 4", "THIẾT KẾ CƠ SỞ DỮ LIỆU", "54"],
        ["4.1", "Phân tích mô hình dữ liệu thực thể và chuẩn hóa 3NF", "54"],
        ["4.2", "Sơ đồ Thực thể Quan hệ CSDL (ERD Diagram 8 bảng)", "55"],
        ["4.3", "Đặc tả chi tiết cấu trúc 8 bảng Cơ sở dữ liệu", "56"],
        ["4.4", "Quy tắc toàn vẹn dữ liệu và Chiến lược Indexing B-Tree", "64"],
        ["CHƯƠNG 5", "THIẾT KẾ & TÍCH HỢP TRÍ TUỆ NHÂN TẠO (AI)", "66"],
        ["5.1", "Kiến trúc Phân hệ AI Grounded In-Context Prompting", "66"],
        ["5.2", "Hiện thực hóa 3 Tính năng AI Trợ lý cốt lõi", "68"],
        ["5.3", "Thiết kế Khuôn mẫu Prompt Templates (Search, Summary, Suggest)", "70"],
        ["5.4", "Quá trình thử nghiệm và tối ưu hóa Prompt qua 3 vòng lặp", "74"],
        ["5.5", "Cơ chế kiểm soát ảo giác (Zero-Hallucination Guardrails)", "77"],
        ["5.6", "Chính sách Bảo mật & Quyền riêng tư AI (Privacy-by-Design)", "78"],
        ["5.7", "Cơ chế Chịu lỗi đa tầng & Mock AI Fallback", "79"],
        ["5.8", "Định hướng mở rộng Kiến trúc RAG với Vector Database", "81"],
        ["CHƯƠNG 6", "CÀI ĐẶT & HIỆN THỰC HÓA GIAO DIỆN", "83"],
        ["6.1", "Cấu trúc tổ chức mã nguồn dự án Backend & Frontend", "83"],
        ["6.2", "Hiện thực hóa API Endpoints và Middleware bảo mật JWT", "85"],
        ["6.3", "Chi tiết Giao diện người dùng & 10 Ảnh chụp màn hình thực tế", "87"],
        ["CHƯƠNG 7", "KIỂM THỬ HỆ THỐNG & ĐÁNH GIÁ", "98"],
        ["7.1", "Chiến lược kiểm thử phần mềm với Isolated Test Database", "98"],
        ["7.2", "Kết quả thực thi 26 ca kiểm thử tự động Pytest (100% Passed)", "99"],
        ["7.3", "Ma trận kiểm thử chuyên sâu cho Phân hệ AI (AI01 - AI07)", "102"],
        ["7.4", "Đánh giá hiệu năng và độ ổn định thời gian phản hồi", "104"],
        ["CHƯƠNG 8", "ỨNG DỤNG AI TRONG QUY TRÌNH SDLC", "106"],
        ["8.1", "Tổng quan vai trò của AI Trợ lý trong Vòng đời Phần mềm (SDLC)", "106"],
        ["8.2", "Chi tiết 4 giai đoạn ứng dụng AI (Bài KT1, KT2, KT3, Cuối kỳ)", "107"],
        ["8.3", "Khung Năng lực & Kỹ năng Kỹ sư Phần mềm (AI-Augmented Skills Framework)", "108"],
        ["8.4", "Tuyển tập Bộ Prompts Mẫu Chi tiết Hoàn thành Đồ án (Master Prompt Catalog)", "110"],
        ["8.5", "Minh chứng 4 Kịch bản Đối thoại Kỹ thuật Tiêu biểu (Pair Programming)", "115"],
        ["8.6", "Nhật ký sử dụng AI (Prompt Log) chi tiết 12 tương tác trọng yếu", "117"],
        ["8.7", "Bài học kinh nghiệm & Nguyên tắc vàng khi Pair Programming cùng AI", "119"],
        ["CHƯƠNG 9", "KẾT LUẬN & HƯỚNG PHÁT TRIỂN", "121"],
        ["9.1", "Tổng kết các kết quả nghiên cứu và thực nghiệm đạt được", "121"],
        ["9.2", "Những hạn chế còn tồn đọng của hệ thống", "122"],
        ["9.3", "Hướng phát triển và mở rộng trong tương lai", "123"],
        ["TÀI LIỆU THAM KHẢO", "Danh mục 15 tài liệu tham khảo chuẩn IEEE / APA", "125"],
        ["PHỤ LỤC A", "Hướng dẫn cài đặt và triển khai hệ thống (Local & Docker)", "127"],
        ["PHỤ LỤC B", "Danh mục chi tiết toàn bộ các RESTful API Endpoints", "129"],
        ["PHỤ LỤC C", "Toàn văn mã nguồn cốt lõi (Core Source Code)", "132"],
        ["PHỤ LỤC D", "Cẩm nang Toàn tập Prompts & Skills Tái tạo Đồ án (AI Playbook)", "138"],
    ]
    builder.add_styled_table(
        "Mục lục tổng quan các chương mục và phụ lục trong báo cáo đồ án",
        toc_headers,
        toc_rows,
        col_widths=[1.4, 4.4, 0.8]
    )
    builder.doc.add_page_break()

    # 6. Danh mục từ viết tắt
    builder.add_heading_1("DANH MỤC CÁC TỪ VIẾT TẮT")
    abbreviations_headers = ["STT", "Từ viết tắt", "Thuật ngữ tiếng Anh đầy đủ", "Ý nghĩa / Định nghĩa chuyên ngành"]
    abbreviations_rows = [
        ["1", "AI", "Artificial Intelligence", "Trí tuệ nhân tạo"],
        ["2", "GenAI", "Generative Artificial Intelligence", "Trí tuệ nhân tạo tạo sinh"],
        ["3", "LLM", "Large Language Model", "Mô hình ngôn ngữ lớn (Google Gemini, OpenAI GPT)"],
        ["4", "SDLC", "Software Development Life Cycle", "Vòng đời phát triển phần mềm"],
        ["5", "CRUD", "Create, Read, Update, Delete", "Các thao tác cơ sở dữ liệu cơ bản"],
        ["6", "JWT", "JSON Web Token", "Chuẩn mở định dạng token xác thực người dùng an toàn"],
        ["7", "RBAC", "Role-Based Access Control", "Mô hình kiểm soát truy cập dựa trên vai trò"],
        ["8", "API", "Application Programming Interface", "Giao diện lập trình ứng dụng"],
        ["9", "REST", "Representational State Transfer", "Kiến trúc thiết kế dịch vụ Web API chuẩn mực"],
        ["10", "ORM", "Object-Relational Mapping", "Kỹ thuật ánh xạ quan hệ đối tượng vào CSDL"],
        ["11", "ERD", "Entity Relationship Diagram", "Sơ đồ quan hệ thực thể trong cơ sở dữ liệu"],
        ["12", "UML", "Unified Modeling Language", "Ngôn ngữ mô hình hóa thống nhất trong công nghệ phần mềm"],
        ["13", "RAG", "Retrieval-Augmented Generation", "Kiến trúc tăng cường truy xuất dữ liệu ngữ cảnh cho LLM"],
        ["14", "WBS", "Work Breakdown Structure", "Cấu trúc phân rã công việc trong quản lý dự án"],
        ["15", "RACI", "Responsible, Accountable, Consulted, Informed", "Ma trận phân định trách nhiệm nhân sự"],
        ["16", "FR", "Functional Requirement", "Yêu cầu chức năng phần mềm"],
        ["17", "NFR", "Non-Functional Requirement", "Yêu cầu phi chức năng (bảo mật, hiệu năng, khả dụng)"],
        ["18", "UI/UX", "User Interface / User Experience", "Giao diện và trải nghiệm người dùng"],
        ["19", "CSV", "Comma-Separated Values", "Định dạng tệp dữ liệu phân tách bằng dấu phẩy"],
        ["20", "BOM", "Byte Order Mark (UTF-8)", "Ký tự định danh mã hóa giúp Excel đọc đúng tiếng Việt"],
    ]
    builder.add_styled_table(
        "Bảng tổng hợp các từ viết tắt chuyên ngành trong báo cáo",
        abbreviations_headers,
        abbreviations_rows,
        col_widths=[0.6, 1.2, 2.5, 2.5]
    )
    builder.doc.add_page_break()

    # 7. Danh mục hình ảnh (28 hình)
    builder.add_heading_1("DANH MỤC HÌNH ẢNH")
    figures_headers = ["STT", "Ký hiệu hình", "Tên sơ đồ / Hình ảnh minh họa", "Trang"]
    figures_rows = [
        ["1", "Hình 2.1", "Sơ đồ Use Case tổng quan toàn hệ thống Quản lý Thư viện AI", "25"],
        ["2", "Hình 2.2", "Sơ đồ Use Case chi tiết phân hệ Nghiệp vụ Thư viện", "26"],
        ["3", "Hình 2.3", "Sơ đồ Use Case chi tiết phân hệ Trợ lý AI Thông minh", "27"],
        ["4", "Hình 3.1", "Sơ đồ Bối cảnh Hệ thống (Context Diagram)", "39"],
        ["5", "Hình 3.2", "Sơ đồ Kiến trúc Phân tầng Hệ thống (Layered Architecture)", "41"],
        ["6", "Hình 3.3", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Mượn sách", "43"],
        ["7", "Hình 3.4", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Trả sách & Tính phạt", "44"],
        ["8", "Hình 3.5", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Gia hạn sách", "45"],
        ["9", "Hình 3.6", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Đặt trước sách", "46"],
        ["10", "Hình 3.7", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Xử lý Nộp & Miễn phạt", "47"],
        ["11", "Hình 3.8", "Sơ đồ Hoạt động (Activity Diagram) Luồng Chatbot AI Tra cứu", "48"],
        ["12", "Hình 3.9", "Sơ đồ Tuần tự (Sequence Diagram) Nghiệp vụ Mượn sách", "49"],
        ["13", "Hình 3.10", "Sơ đồ Tuần tự (Sequence Diagram) Nghiệp vụ Trả sách & Xử lý phạt", "50"],
        ["14", "Hình 3.11", "Sơ đồ Tuần tự (Sequence Diagram) Chatbot AI Tra cứu Ngôn ngữ tự nhiên", "51"],
        ["15", "Hình 3.12", "Sơ đồ Tuần tự (Sequence Diagram) AI Gợi ý Sách Cá nhân hóa", "52"],
        ["16", "Hình 4.1", "Sơ đồ Thực thể Quan hệ CSDL (ERD Diagram 8 bảng chuẩn 3NF)", "55"],
        ["17", "Hình 5.1", "Sơ đồ Luồng Xử lý Dữ liệu AI Pipeline (Grounded In-Context Prompting)", "67"],
        ["18", "Hình 5.2", "Sơ đồ Kiến trúc Định hướng Mở rộng RAG với Vector Database", "82"],
        ["19", "Hình 6.1", "Giao diện Đăng nhập & Đăng ký Tài khoản (ui_01_login.png)", "88"],
        ["20", "Hình 6.2", "Giao diện Dashboard Tổng quan & Biểu đồ Thống kê (ui_02_dashboard.png)", "89"],
        ["21", "Hình 6.3", "Giao diện Quản lý Kho Sách & Bộ lọc Thông minh (ui_03_books.png)", "90"],
        ["22", "Hình 6.4", "Giao diện Quản lý Hồ sơ Độc giả & Cấp thẻ (ui_04_readers.png)", "91"],
        ["23", "Hình 6.5", "Giao diện Lập phiếu Mượn & Nhận Trả Sách (ui_05_borrows.png)", "92"],
        ["24", "Hình 6.6", "Giao diện Quản lý & Thu Tiền Phạt Quá Hạn (ui_06_fines.png)", "93"],
        ["25", "Hình 6.7", "Giao diện Quản lý Đặt Trước Sách (ui_07_reservations.png)", "94"],
        ["26", "Hình 6.8", "Giao diện Báo cáo Thống kê & Xuất File CSV (ui_08_statistics.png)", "95"],
        ["27", "Hình 6.9", "Giao diện Trợ lý AI Chatbot & Gợi ý Sách (ui_09_ai_chatbot.png)", "96"],
        ["28", "Hình 6.10", "Giao diện Quản trị viên Phân quyền Tài khoản (ui_10_users.png)", "97"],
    ]
    builder.add_styled_table(
        "Danh mục các sơ đồ kỹ thuật và hình ảnh giao diện trong đồ án",
        figures_headers,
        figures_rows,
        col_widths=[0.6, 1.2, 4.4, 0.6]
    )
    builder.doc.add_page_break()

    # 8. Danh mục bảng biểu (25 bảng)
    builder.add_heading_1("DANH MỤC BẢNG BIỂU")
    tables_headers = ["STT", "Ký hiệu bảng", "Tên bảng biểu mô tả dữ liệu / đặc tả", "Trang"]
    tables_rows = [
        ["1", "Bảng 1.1", "Ma trận phân định trách nhiệm nhân sự RACI trong dự án", "13"],
        ["2", "Bảng 1.2", "Cấu trúc phân rã công việc WBS chi tiết cho 4 giai đoạn SDLC", "14"],
        ["3", "Bảng 1.3", "Bảng ma trận đánh giá và kiểm soát rủi ro dự án", "16"],
        ["4", "Bảng 2.1", "Ma trận phân quyền RBAC giữa các vai trò người dùng", "21"],
        ["5", "Bảng 2.2", "Danh mục 12 Yêu cầu chức năng cốt lõi (FR01 - FR12)", "22"],
        ["6", "Bảng 2.3", "Danh mục 8 Yêu cầu phi chức năng của hệ thống (NFR01 - NFR08)", "24"],
        ["7", "Bảng 2.4", "Đặc tả Use Case UC01: Đăng nhập & Xác thực hệ thống", "28"],
        ["8", "Bảng 2.5", "Đặc tả Use Case UC02: Quản lý danh mục kho sách", "29"],
        ["9", "Bảng 2.6", "Đặc tả Use Case UC03: Quản lý hồ sơ độc giả và cấp thẻ", "30"],
        ["10", "Bảng 2.7", "Đặc tả Use Case UC04: Lập phiếu mượn sách tại quầy", "31"],
        ["11", "Bảng 2.8", "Đặc tả Use Case UC05: Tiếp nhận trả sách & Xử lý phạt", "32"],
        ["12", "Bảng 2.9", "Đặc tả Use Case UC06: Gia hạn thời gian mượn sách", "33"],
        ["13", "Bảng 2.10", "Đặc tả Use Case UC07: Thu tiền phạt và miễn giảm phạt", "34"],
        ["14", "Bảng 2.11", "Đặc tả Use Case UC08: Đặt trước sách khi hết bản khả dụng", "35"],
        ["15", "Bảng 2.12", "Đặc tả Use Case UC09: Chatbot AI tra cứu ngôn ngữ tự nhiên", "36"],
        ["16", "Bảng 2.13", "Đặc tả Use Case UC10: AI Tóm tắt và gợi ý sách cá nhân hóa", "37"],
        ["17", "Bảng 4.1", "Đặc tả cấu trúc bảng CSDL `users` (Tài khoản người dùng)", "56"],
        ["18", "Bảng 4.2", "Đặc tả cấu trúc bảng CSDL `readers` (Hồ sơ độc giả & thẻ)", "57"],
        ["19", "Bảng 4.3", "Đặc tả cấu trúc bảng CSDL `categories` (Thể loại sách)", "58"],
        ["20", "Bảng 4.4", "Đặc tả cấu trúc bảng CSDL `authors` (Tác giả sách)", "59"],
        ["21", "Bảng 4.5", "Đặc tả cấu trúc bảng CSDL `books` (Kho sách thư viện)", "60"],
        ["22", "Bảng 4.6", "Đặc tả cấu trúc bảng CSDL `borrow_records` (Phiếu mượn/trả)", "61"],
        ["23", "Bảng 4.7", "Đặc tả cấu trúc bảng CSDL `fines` (Bản ghi phạt quá hạn)", "62"],
        ["24", "Bảng 4.8", "Đặc tả cấu trúc bảng CSDL `reservations` (Đơn đặt trước sách)", "63"],
        ["25", "Bảng 5.1", "Bảng so sánh chi tiết kết quả 3 vòng thử nghiệm tối ưu Prompt AI", "75"],
        ["26", "Bảng 7.1", "Bảng phân bổ & Kết quả 26 ca kiểm thử tự động Pytest (100% Passed)", "100"],
        ["27", "Bảng 7.2", "Bảng ma trận kiểm thử chất lượng chuyên sâu cho AI (AI01 - AI07)", "103"],
        ["28", "Bảng 7.3", "Đánh giá các chỉ số hiệu năng và thời gian phản hồi hệ thống", "105"],
        ["29", "Bảng 8.1", "Nhật ký Prompt AI (Prompt Log) xuyên suốt 4 giai đoạn SDLC", "111"],
        ["30", "Bảng B.1", "Danh mục chi tiết toàn bộ các RESTful API Endpoints của hệ thống", "124"],
    ]
    builder.add_styled_table(
        "Danh mục các bảng biểu đặc tả, kiểm thử và phân tích trong đồ án",
        tables_headers,
        tables_rows,
        col_widths=[0.6, 1.2, 4.4, 0.6]
    )
    builder.doc.add_page_break()
