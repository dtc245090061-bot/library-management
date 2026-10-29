import os
import sys
import asyncio

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from playwright.async_api import async_playwright
from PIL import Image
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DIAGRAMS_DIR = os.path.join(DOCS_DIR, "diagrams")
MAIN_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "Hinh_Anh_Va_So_Do_Do_An", "1_So_Do_Ky_Thuat_UML_Architecture")

os.makedirs(DIAGRAMS_DIR, exist_ok=True)
os.makedirs(MAIN_OUTPUT_DIR, exist_ok=True)

# 18 SƠ ĐỒ KỸ THUẬT ĐƯỢC THIẾT KẾ LẠI TOÀN DIỆN:
# ĐÚNG CHUẨN ĐỊNH DẠNG UML (USE CASE, SWIMLANE ACTIVITY, SEQUENCE, ERD, ARCHITECTURE)
# ĐÚNG 100% NGHIỆP VỤ THỰC TẾ CỦA DỰ ÁN WEB VÀ ĐỀ BÀI ĐỒ ÁN
ULTRA_HD_DIAGRAMS = {
    # -------------------------------------------------------------
    # 01. Context Diagram (Sơ đồ Bối cảnh Hệ thống - DFD Mức 0 Chuẩn)
    # -------------------------------------------------------------
    "01_context_diagram.png": """
flowchart TB
    Admin["👨‍💼 QUẢN TRỊ VIÊN (ADMIN)<br/>• Quản trị tài khoản & phân quyền RBAC<br/>• Giám sát cấu hình & thống kê hệ thống"]
    Librarian["👩‍💼 THỦ THƯ (LIBRARIAN)<br/>• Quản lý danh mục sách & độc giả<br/>• Lập phiếu mượn, trả, gia hạn, thu phạt"]
    Reader["🎓 ĐỘC GIẢ (READER)<br/>• Tra cứu sách NLU & Chatbot AI<br/>• Xem gợi ý, đặt trước & gia hạn"]

    System(["🏛️ TIẾN TRÌNH TRUNG TÂM [0.0]<br/>HỆ THỐNG QUẢN LÝ THƯ VIỆN TÍCH HỢP TRÍ TUỆ NHÂN TẠO (AI)<br/>(FastAPI Backend, SQLAlchemy ORM & Modern Web UI)"])

    Gemini["🤖 DỊCH VỤ GOOGLE GEMINI AI<br/>(Gemini 1.5 Flash Cloud API)<br/>• Timeout 15s, Retry x2, Mock Fallback"]
    Database[("🗄️ CƠ SỞ DỮ LIỆU THƯ VIỆN<br/>(SQLite / PostgreSQL via SQLAlchemy)<br/>• Lưu trữ 8 bảng chuẩn 3NF")]

    Admin <-->|Quản trị Users, phân quyền & báo cáo KPI| System
    Librarian <-->|Thực thi mượn, trả, gia hạn, thu phạt, đặt trước| System
    Reader <-->|Truy vấn ngôn ngữ tự nhiên, yêu cầu gia hạn, đặt trước| System

    System <-->|Giao dịch đọc/ghi dữ liệu ACID toàn vẹn| Database
    System <-->|Gửi Grounded Context Prompt & Nhận phản hồi tự nhiên| Gemini
""",

    # -------------------------------------------------------------
    # 02. General Use Case Diagram (Chuẩn UML Use Case Tổng quan)
    # -------------------------------------------------------------
    "02_usecase_general.png": """
flowchart LR
    subgraph ACTORS ["👥 CÁC TÁC NHÂN HỆ THỐNG (ACTORS)"]
        direction TB
        Admin["👨‍💼 Quản trị viên<br/>(Admin)"]
        Librarian["👩‍💼 Thủ thư<br/>(Librarian)"]
        Reader["🎓 Độc giả<br/>(Reader)"]
    end

    subgraph SYS ["🏛️ HỆ THỐNG QUẢN LÝ THƯ VIỆN TÍCH HỢP AI"]
        subgraph SUB_AUTH ["1. Phân hệ Quản trị & Xác thực"]
            direction TB
            UC_Login(["Đăng nhập & Đổi mật khẩu"])
            UC_Users(["Quản lý Người dùng & RBAC"])
            UC_Stats(["Dashboard Thống kê & Báo cáo CSV"])
        end

        subgraph SUB_LIB ["2. Phân hệ Quản lý Nghiệp vụ Thư viện"]
            direction TB
            UC_Books(["Quản lý Kho Sách & Danh mục"])
            UC_Readers(["Quản lý Độc giả & Thẻ Thư viện"])
            UC_Borrow(["Lập Phiếu Mượn Sách"])
            UC_Return(["Xử lý Trả Sách & Phạt Quá Hạn"])
            UC_Renew(["Xử lý Gia hạn Thời hạn Mượn"])
            UC_Reserve(["Xếp hàng Đặt trước Sách"])
            UC_Fine(["Quản lý & Thu Tiền Phạt"])
        end

        subgraph SUB_AI ["3. Phân hệ Trợ lý AI Thông minh (Generative AI)"]
            direction TB
            UC_AIChat(["Chatbot AI Tra cứu Ngôn ngữ Tự nhiên"])
            UC_AISummary(["AI Tóm tắt Nội dung & Mục lục Sách"])
            UC_AISuggest(["AI Gợi ý Sách Cá nhân hóa theo Gu đọc"])
        end

        SUB_AUTH ~~~ SUB_LIB ~~~ SUB_AI
    end

    %% Phân quyền Quản trị viên
    Admin --> UC_Login
    Admin --> UC_Users
    Admin --> UC_Stats

    %% Phân quyền Thủ thư
    Librarian --> UC_Login
    Librarian --> UC_Books
    Librarian --> UC_Readers
    Librarian --> UC_Borrow
    Librarian --> UC_Return
    Librarian --> UC_Renew
    Librarian --> UC_Reserve
    Librarian --> UC_Fine
    Librarian --> UC_Stats
    Librarian --> UC_AISummary

    %% Phân quyền Độc giả
    Reader --> UC_Login
    Reader --> UC_AIChat
    Reader --> UC_AISummary
    Reader --> UC_AISuggest
    Reader --> UC_Reserve
    Reader --> UC_Renew
""",

    # -------------------------------------------------------------
    # 03. Library Use Case Diagram (Chuẩn UML Nghiệp vụ Thư viện)
    # -------------------------------------------------------------
    "03_usecase_library.png": """
flowchart LR
    actorLib["👩‍💼 Thủ thư (Librarian)"]
    actorReader["🎓 Độc giả (Reader)"]

    subgraph SYS_LIB ["🏛️ PHÂN HỆ QUẢN LÝ NGHIỆP VỤ THƯ VIỆN"]
        subgraph COL1 ["1. Quản lý Danh mục & Bạn đọc"]
            direction TB
            UC_Books(["Quản lý Sách (CRUD, Lọc, Xuất CSV)"])
            UC_Readers(["Quản lý Độc giả & Thẻ Thư viện"])
            UC_Stats(["Dashboard KPI & Báo cáo CSV UTF-8"])
        end

        subgraph COL2 ["2. Lưu thông Mượn / Trả / Gia hạn"]
            direction TB
            UC_Borrow(["Lập Phiếu Mượn Sách (Hạn 14 ngày, max 5 cuốn)"])
            UC_CheckCond(["Kiểm tra 4 Điều kiện Mượn Sách"])
            UC_Return(["Xử lý Trả Sách & Hoàn kho"])
            UC_CalcFine(["Tự động Tính Tiền Phạt (2.000đ/ngày)"])
            UC_Renew(["Xử lý Gia hạn Sách (+7 ngày, tối đa 1 lần)"])
        end

        subgraph COL3 ["3. Đặt trước & Thu phạt Tài chính"]
            direction TB
            UC_Reserve(["Đặt trước Sách khi Hết Bản Khả dụng"])
            UC_TriggerReady(["Kích hoạt Giữ chỗ 7 ngày khi có Sách về"])
            UC_Fine(["Thu Phạt / Miễn Giảm Phạt (PAID/WAIVED)"])
        end

        COL1 ~~~ COL2 ~~~ COL3
    end

    %% Quan hệ include và extend chuẩn UML
    UC_Borrow -.->|«include»| UC_CheckCond
    UC_Return -.->|«extend»| UC_CalcFine
    UC_Return -.->|«extend»| UC_TriggerReady

    %% Tác nhân Thủ thư
    actorLib --> UC_Books
    actorLib --> UC_Readers
    actorLib --> UC_Borrow
    actorLib --> UC_Return
    actorLib --> UC_Renew
    actorLib --> UC_Reserve
    actorLib --> UC_Fine
    actorLib --> UC_Stats

    %% Tác nhân Độc giả
    actorReader --> UC_Reserve
    actorReader --> UC_Renew
""",

    # -------------------------------------------------------------
    # 04. AI Use Case Diagram (Chuẩn UML Phân hệ Trợ lý AI)
    # -------------------------------------------------------------
    "04_usecase_ai.png": """
flowchart LR
    actorReader["🎓 Độc giả (Reader)"]
    actorLib["👩‍💼 Thủ thư (Librarian)"]
    actorGemini["🤖 Google Gemini 1.5 Flash API<br/>(Dịch vụ Đám mây Ngoài)"]

    subgraph SYS_AI ["🏛️ PHÂN HỆ TRỢ LÝ AI THÔNG MINH (GENERATIVE AI)"]
        subgraph COL_A ["1. Dịch vụ AI Trực tiếp cho Người dùng"]
            direction TB
            AI_Search(["Chatbot Tra cứu Sách Ngôn ngữ Tự nhiên"])
            AI_Suggest(["AI Gợi ý Sách Cá nhân hóa theo Gu đọc"])
            AI_Summary(["AI Tóm tắt Nội dung & Mục lục Sách"])
        end

        subgraph COL_B ["2. Cơ chế Kỹ thuật Nền tảng (AI Engine)"]
            direction TB
            AI_Prompt(["Đóng gói Grounded Context Prompt"])
            AI_Privacy(["Khử định danh Cá nhân (Privacy-by-Design)"])
            AI_Extract(["Trích xuất Thực thể Khớp Database"])
            AI_Fallback(["Kích hoạt Mock Fallback Engine"])
        end

        COL_A ~~~ COL_B
    end

    %% Quan hệ include và extend chuẩn UML
    AI_Search -.->|«include»| AI_Prompt
    AI_Search -.->|«include»| AI_Extract
    AI_Suggest -.->|«include»| AI_Privacy
    AI_Suggest -.->|«include»| AI_Prompt
    AI_Prompt -.->|«extend»| AI_Fallback

    %% Tác nhân kết nối
    actorReader --> AI_Search
    actorReader --> AI_Suggest
    actorReader --> AI_Summary

    actorLib --> AI_Search
    actorLib --> AI_Summary

    AI_Prompt ==>|Gửi Prompt & Nhận kết quả| actorGemini
    AI_Summary ==>|Gửi nội dung tóm tắt| actorGemini
""",

    # -------------------------------------------------------------
    # 05. Activity Borrow (Swimlane Chuẩn UML 4 Làn Nghiệp Vụ)
    # -------------------------------------------------------------
    "05_activity_borrow.png": """
flowchart TD
    subgraph Lane1 ["👤 1. ĐỘC GIẢ / THỦ THƯ"]
        Start([🟢 Bắt đầu mượn sách]) --> Input[Thủ thư quét Mã Thẻ & Mã Sách]
        ShowSuccess[Nhận sách và Biên lai mượn (Hạn 14 ngày)] --> EndOk([🎉 Kết thúc thành công])
        ShowErr1[Nhận thông báo: Thẻ hết hạn / không hợp lệ] --> EndErr1([🔴 Kết thúc])
        ShowErr2[Nhận thông báo: Đã mượn tối đa 5 cuốn] --> EndErr2([🔴 Kết thúc])
        ShowErr3[Nhận thông báo: Phải nộp phạt trước khi mượn] --> EndErr3([🔴 Kết thúc])
        ShowErr4[Nhận thông báo: Sách hết -> Chuyển Đặt trước] --> EndErr4([🔴 Kết thúc])
    end

    subgraph Lane2 ["🖥️ 2. GIAO DIỆN WEB CLIENT"]
        Input --> Submit[Gửi yêu cầu POST /api/borrows/<br/>kèm reader_id & book_id]
        ToastErr1[Hiển thị Toast lỗi 400: Thẻ không hợp lệ] --> ShowErr1
        ToastErr2[Hiển thị Toast lỗi 400: Vượt hạn mức 5 cuốn] --> ShowErr2
        ToastErr3[Hiển thị Toast lỗi 400: Còn nợ phạt PENDING] --> ShowErr3
        ToastErr4[Hiển thị Toast lỗi 400: Sách hết bản khả dụng] --> ShowErr4
        ToastOk[Hiển thị thông báo Mượn thành công 201 Created] --> ShowSuccess
    end

    subgraph Lane3 ["⚡ 3. FASTAPI BACKEND & BORROWSERVICE"]
        Submit --> CheckCard{1. Thẻ Độc giả ACTIVE<br/>& Chưa hết hạn?}
        CheckCard -- ❌ Sai --> ToastErr1
        CheckCard --  Đúng --> CheckLimit{2. Số sách đang mượn<br/>hiện tại < 5 cuốn?}
        CheckLimit -- ❌ Sai --> ToastErr2
        CheckLimit --  Đúng --> CheckFine{3. Có nợ phạt trễ hạn<br/>PENDING chưa nộp?}
        CheckFine -- ❌ Có nợ --> ToastErr3
        CheckFine --  Không nợ --> CheckStock{4. Số lượng khả dụng<br/>available_quantity > 0?}
        CheckStock -- ❌ Hết sách --> ToastErr4
        CheckStock --  Còn sách --> ExecBorrow[Thực thi nghiệp vụ Lập phiếu mượn:<br/>due_date = today + 14 ngày, status = BORROWING]
    end

    subgraph Lane4 ["🗄️ 4. CƠ SỞ DỮ LIỆU (DATABASE)"]
        ExecBorrow --> DB1[(Lưu bản ghi BorrowRecord mới)]
        DB1 --> DB2[(Giảm available_quantity = available_quantity - 1)]
        DB2 --> DB3[(Đổi trạng thái Reservation của độc giả sang COMPLETED nếu có)]
        DB3 --> DB4[(Commit giao dịch ACID bảo toàn dữ liệu)]
        DB4 --> ToastOk
    end
""",

    # -------------------------------------------------------------
    # 06. Activity Return (Swimlane Chuẩn UML 4 Làn Nghiệp Vụ)
    # -------------------------------------------------------------
    "06_activity_return.png": """
flowchart TD
    subgraph Lane1 ["👤 1. ĐỘC GIẢ / THỦ THƯ"]
        Start([🟢 Bắt đầu nhận trả sách]) --> Scan[Thủ thư quét hoặc nhập Mã Phiếu Mượn]
        PayFinePrompt[Độc giả nộp tiền phạt trễ hạn tại quầy] --> Finish([🎉 Hoàn tất nhận trả sách])
        NoFineFinish[Nhận lại thẻ & hoàn tất thủ tục] --> Finish
        EndRet([🔴 Kết thúc])
    end

    subgraph Lane2 ["🖥️ 2. GIAO DIỆN WEB CLIENT"]
        Scan --> SubmitRet[Gửi yêu cầu PUT /api/borrows/{record_id}/return]
        ToastAlready[Hiển thị lỗi 400: Phiếu đã trả trước đó] --> EndRet
        PopupFine[Hiển thị Popup Cảnh báo Quá Hạn & Số tiền phạt] --> PayFinePrompt
        ToastSuccess[Hiển thị Toast: Trả sách thành công 200 OK] --> NoFineFinish
    end

    subgraph Lane3 ["⚡ 3. FASTAPI BACKEND & BORROWSERVICE"]
        SubmitRet --> CheckAlready{Phiếu mượn đã có<br/>return_date chưa?}
        CheckAlready -- Đã trả rồi --> ToastAlready
        CheckAlready -- Chưa trả --> UpdateRet[Cập nhật phiếu mượn:<br/>status = RETURNED, return_date = today]
        UpdateRet --> CheckOverdue{Kiểm tra quá hạn:<br/>today > due_date?}
        CheckOverdue --  Có quá hạn --> CalcFine["Tính phạt: overdue_days = today - due_date<br/>total_amount = overdue_days * 2.000 VNĐ"]
        CheckOverdue -- ❌ Đúng hạn --> CheckRes
        CalcFine --> CheckRes{Có độc giả xếp hàng<br/>PENDING đặt trước sách này?}
        CheckRes --  Có người chờ --> SetReady[Chuyển đơn đặt trước sớm nhất sang READY<br/>Khóa giữ chỗ sách trong 7 ngày]
        CheckRes -- ❌ Không có --> EndService[Hoàn tất xử lý dịch vụ]
    end

    subgraph Lane4 ["🗄️ 4. CƠ SỞ DỮ LIỆU (DATABASE)"]
        UpdateRet --> DB_Stock[(Tăng available_quantity = available_quantity + 1)]
        CalcFine --> DB_Fine[(Tạo bản ghi Fine: status = PENDING)]
        SetReady --> DB_Res[(Cập nhật status Reservation = READY, expire_date = today + 7)]
        DB_Stock --> DB_Commit[(Commit giao dịch ACID)]
        DB_Fine --> DB_Commit
        DB_Res --> DB_Commit
        DB_Commit --> PopupDecision{Có phát sinh phạt?}
        PopupDecision -- Có phạt --> PopupFine
        PopupDecision -- Không phạt --> ToastSuccess
    end
""",

    # -------------------------------------------------------------
    # 07. Activity Renew (Swimlane Chuẩn UML 3 Làn Gia Hạn Sách)
    # -------------------------------------------------------------
    "07_activity_renew.png": """
flowchart TD
    subgraph Lane1 ["👤 1. ĐỘC GIẢ / THỦ THƯ"]
        Start([🟢 Bắt đầu yêu cầu gia hạn]) --> SelectRecord[Chọn Phiếu Mượn cần gia hạn trên màn hình]
        SuccessNotice[Nhận thông báo: Gia hạn thành công thêm 7 ngày] --> EndOk([🎉 Hoàn tất gia hạn])
        ErrNotice[Nhận thông báo từ chối gia hạn kèm lý do] --> EndErr([🔴 Kết thúc])
    end

    subgraph Lane2 ["🖥️ 2. GIAO DIỆN WEB CLIENT"]
        SelectRecord --> SubmitRenew[Gửi yêu cầu POST /api/borrows/{record_id}/renew]
        ToastErr[Hiển thị thông báo lỗi chi tiết theo mã 400] --> ErrNotice
        ToastOk[Cập nhật ngày hạn trả mới trên bảng dữ liệu] --> SuccessNotice
    end

    subgraph Lane3 ["⚡ 3. FASTAPI BACKEND & SERVICE & CSDL"]
        SubmitRenew --> Check1{1. Trạng thái phiếu<br/>status == BORROWING?}
        Check1 -- ❌ Sai --> ToastErr
        Check1 --  Đúng --> Check2{2. Đã quá hạn chưa?<br/>today > due_date?}
        Check2 -- ❌ Đã quá hạn --> ToastErr
        Check2 --  Chưa quá hạn --> Check3{3. Số lần gia hạn<br/>renew_count < 1?}
        Check3 -- ❌ Đã gia hạn rồi --> ToastErr
        Check3 --  Chưa gia hạn --> Check4{4. Có người khác đang<br/>đặt trước cuốn sách này?}
        Check4 -- ❌ Có người chờ --> ToastErr
        Check4 --  Không ai đặt --> ApplyRenew["Cập nhật CSDL:<br/>• due_date = due_date + 7 ngày<br/>• renew_count = 1<br/>• Commit giao dịch ACID"]
        ApplyRenew --> ToastOk
    end
""",

    # -------------------------------------------------------------
    # 08. Activity Reservation (Swimlane Chuẩn Hàng Đợi FIFO)
    # -------------------------------------------------------------
    "08_activity_reservation.png": """
flowchart TD
    subgraph Lane1 ["🎓 1. ĐỘC GIẢ (READER)"]
        Start([🟢 Tra cứu sách]) --> CheckZero[Thấy sách yêu thích hết bản: available = 0]
        CheckZero --> ClickRes[Bấm nút 'Đặt trước sách' trên Web]
        ReceiveNotify[Nhận thông báo Sách đã về kho qua hệ thống] --> GoToLibrary[Đến thư viện trong vòng 7 ngày]
        GoToLibrary --> BorrowDirect[Lập phiếu mượn chính thức tại quầy] --> EndOk([🎉 Nhận sách thành công])
    end

    subgraph Lane2 ["🖥️ 2. GIAO DIỆN WEB CLIENT"]
        ClickRes --> PostRes[Gửi POST /api/reservations/ {reader_id, book_id}]
        ToastPending[Hiển thị Toast: Bạn đã vào hàng đợi FIFO đặt trước]
        ToastReady[Hiển thị Huy hiệu READY: Sách đang được giữ chỗ 7 ngày] --> ReceiveNotify
    end

    subgraph Lane3 ["⚡ 3. FASTAPI & CƠ CHẾ ĐIỀU PHỐI HÀNG ĐỢI"]
        PostRes --> ValCheck{available == 0 &<br/>chưa có đơn PENDING?}
        ValCheck -- Hợp lệ --> CreateRes[Tạo đơn Reservation mới: status = PENDING]
        CreateRes --> ToastPending
        EventReturn[Sự kiện: Có độc giả mang sách này đến trả] --> TriggerFIFO[Quét tìm đơn Reservation PENDING có thời gian tạo sớm nhất]
        TriggerFIFO --> UpdateReady["Đổi status = READY<br/>Thiết lập expire_date = today + 7 ngày<br/>Khóa 1 bản sách giữ chỗ"]
        UpdateReady --> ToastReady
    end

    subgraph Lane4 ["🗄️ 4. CƠ SỞ DỮ LIỆU (DATABASE)"]
        CreateRes --> DB_Save[(Lưu vào bảng RESERVATIONS)]
        UpdateReady --> DB_Lock[(Cập nhật trạng thái READY)]
        BorrowDirect --> DB_Done[(Đổi trạng thái sang COMPLETED & Lập phiếu mượn)]
    end
""",

    # -------------------------------------------------------------
    # 09. Activity Fine (Swimlane Chuẩn UML Quản Lý & Thu Phạt)
    # -------------------------------------------------------------
    "09_activity_fine.png": """
flowchart TD
    subgraph Lane1 ["👩‍💼 1. THỦ THƯ (LIBRARIAN)"]
        Start([🟢 Bắt đầu xử lý nợ phạt]) --> ViewFines[Mở Danh sách Phạt & Lọc status = PENDING]
        ViewFines --> SelectFine[Chọn khoản phạt của độc giả cần giải quyết]
        SelectFine --> ChoiceAction{Chọn phương án<br/>giải quyết}
        ChoiceAction -- Thu tiền --> CollectCash[Thu tiền mặt / Quét mã QR chuyển khoản]
        ChoiceAction -- Miễn phạt --> WaivePrompt[Nhập lý do miễn giảm chính đáng]
        EndNotice[Nhận thông báo: Độc giả đã sạch nợ phạt & Thẻ mở khóa] --> Finish([🎉 Hoàn tất xử lý phạt])
    end

    subgraph Lane2 ["🖥️ 2. GIAO DIỆN WEB CLIENT"]
        CollectCash --> ApiPay[Gửi PUT /api/fines/{id}/pay]
        WaivePrompt --> ApiWaive[Gửi PUT /api/fines/{id}/waive kèm reason]
        ToastFinish[Hiển thị Toast thành công 200 OK & Cập nhật bảng] --> EndNotice
    end

    subgraph Lane3 ["⚡ 3. FASTAPI BACKEND & FINESERVICE"]
        ApiPay --> ExecPay[Ghi nhận thanh toán: status = PAID, paid_date = today]
        ApiWaive --> ExecWaive[Ghi nhận miễn giảm: status = WAIVED, lưu notes]
        ExecPay --> CheckRemain
        ExecWaive --> CheckRemain{Độc giả còn khoản phạt<br/>PENDING nào khác không?}
        CheckRemain --  Hết nợ --> UnlockCard[Tự động mở khóa toàn diện quyền mượn sách]
        CheckRemain -- ❌ Còn nợ --> KeepLock[Duy trì tạm khóa quyền mượn sách]
        UnlockCard --> ToastFinish
        KeepLock --> ToastFinish
    end

    subgraph Lane4 ["🗄️ 4. CƠ SỞ DỮ LIỆU (DATABASE)"]
        ExecPay --> DB_Pay[(Cập nhật bảng FINES: status = PAID)]
        ExecWaive --> DB_Waive[(Cập nhật bảng FINES: status = WAIVED)]
        UnlockCard --> DB_Reader[(Bảo đảm hồ sơ Readers sẵn sàng mượn sách)]
    end
""",

    # -------------------------------------------------------------
    # 10. Activity AI Chat (Swimlane Chuẩn Pipeline Trợ Lý AI)
    # -------------------------------------------------------------
    "10_activity_ai_chat.png": """
flowchart TD
    subgraph Lane1 ["🎓 1. ĐỘC GIẢ (READER)"]
        Start([🟢 Độc giả mở khung Chatbot AI]) --> InputQ[Nhập câu hỏi tự nhiên bằng tiếng Việt]
        ShowUI[Đọc câu trả lời thông minh kèm Bộ Thẻ Sách tương tác] --> ActionCard[Bấm nút 'Mượn ngay' hoặc 'Xem chi tiết'] --> Finish([🎉 Trải nghiệm AI hoàn tất])
    end

    subgraph Lane2 ["🖥️ 2. GIAO DIỆN WEB CHATBOT"]
        InputQ --> SubmitQ[Gửi POST /api/ai/search {query: '...'}]
        ShowLoading[Hiển thị hiệu ứng AI đang suy nghĩ...]
        SubmitQ --> ShowLoading
        RenderResponse[Render Markdown tiếng Việt & Component Book Cards] --> ShowUI
    end

    subgraph Lane3 ["⚡ 3. FASTAPI BACKEND & AISERVICE"]
        SubmitQ --> ValidateLen{1 <= Độ dài câu hỏi <= 500 ký tự?}
        ValidateLen -- ❌ Vi phạm --> Err422[Báo lỗi Validation 422]
        ValidateLen --  Hợp lệ --> QueryDB[Truy vấn CSDL: Lấy danh mục sách đang lưu hành]
        QueryDB --> Sanitize[Privacy-by-Design: Khử toàn bộ định danh cá nhân độc giả]
        Sanitize --> InjectPrompt[Đóng gói Grounded System Prompt với Zero-Hallucination Guardrails]
        InjectPrompt --> CallEngine{Kiểm tra kết nối<br/>Google Gemini API}
        CallEngine -- Có mạng & Key --> InvokeCloud[Gọi Gemini 1.5 Flash API - Timeout 15s, Retry x2]
        CallEngine -- Lỗi mạng/Hết quota --> InvokeMock[Kích hoạt Mock Fallback Engine cục bộ]
        InvokeCloud --> ExtractEntity[Thuật toán Entity Matching: So khớp mã và tiêu đề sách thực tế]
        InvokeMock --> ExtractEntity
        ExtractEntity --> PackResult[Đóng gói JSON: answer, suggested_books, source]
        PackResult --> RenderResponse
    end

    subgraph Lane4 ["🌐 4. DỊCH VỤ GOOGLE GEMINI CLOUD"]
        InvokeCloud --> LLMRun[Thực thi suy luận ngôn ngữ trên nền tảng Gemini 1.5 Flash]
        LLMRun --> ReturnText[Trả về phản hồi văn bản phân tích chuyên sâu]
        ReturnText --> ExtractEntity
    end
""",

    # -------------------------------------------------------------
    # 11. Sequence Borrow (Chuẩn UML Sequence Diagram Mượn Sách)
    # -------------------------------------------------------------
    "11_sequence_borrow.png": """
sequenceDiagram
    autonumber
    actor Reader as 🎓 Độc giả
    actor Librarian as 👩‍💼 Thủ thư
    participant UI as 🖥️ Giao diện Web
    participant Router as ⚡ Borrows Router (/api/borrows)
    participant Service as 💼 BorrowService
    participant DB as 🗄️ CSDL (SQLite / PostgreSQL)

    Reader->>Librarian: Xuất trình thẻ thư viện & sách cần mượn
    Librarian->>UI: Quét mã thẻ & mã sách -> Bấm "Lập phiếu mượn"
    activate UI
    UI->>Router: POST /api/borrows/ {reader_id, book_id}
    activate Router
    Router->>Service: borrow_book(db, reader_id, book_id)
    activate Service

    Service->>DB: Truy vấn Reader & kiểm tra: thẻ ACTIVE, hạn dùng, số sách đang mượn < 5
    Service->>DB: Truy vấn Fines: kiểm tra không có nợ phạt PENDING
    Service->>DB: Truy vấn Book: kiểm tra available_quantity > 0

    alt Trường hợp Dữ liệu Không Hợp Lệ (Thẻ khóa / Quá 5 cuốn / Nợ phạt / Hết sách)
        Service-->>Router: Ném ngoại lệ HTTPException 400 Bad Request
        Router-->>UI: 400 Bad Request {"detail": "Mô tả lỗi vi phạm nghiệp vụ"}
        UI-->>Librarian: Hiển thị Toast cảnh báo từ chối lập phiếu mượn
    else Trường hợp Thỏa Mãn Đầy Đủ 4 Điều Kiện
        Service->>DB: Giảm tồn kho: available_quantity = available_quantity - 1
        Service->>DB: Tạo bản ghi BorrowRecord mới (due_date = today + 14 ngày, status = BORROWING)
        Service->>DB: Cập nhật Reservation của độc giả sang COMPLETED (nếu có)
        Service->>DB: Commit giao dịch ACID thành công
        DB-->>Service: Xác nhận lưu dữ liệu thành công
        Service-->>Router: Trả về đối tượng BorrowRecord hoàn chỉnh
        Router-->>UI: 201 Created (JSON dữ liệu phiếu mượn)
        UI-->>Librarian: Hiển thị Toast mượn thành công & In phiếu mượn
        Librarian-->>Reader: Bàn giao sách và phiếu hẹn trả 14 ngày
    end
    deactivate Service
    deactivate Router
    deactivate UI
""",

    # -------------------------------------------------------------
    # 12. Sequence Return (Chuẩn UML Sequence Trả Sách & Phạt)
    # -------------------------------------------------------------
    "12_sequence_return.png": """
sequenceDiagram
    autonumber
    actor Librarian as 👩‍💼 Thủ thư
    participant UI as 🖥️ Giao diện Quản lý Mượn / Trả
    participant Router as ⚡ Borrows Router (/api/borrows)
    participant Service as 💼 BorrowService
    participant DB as 🗄️ CSDL (SQLite / PostgreSQL)

    Librarian->>UI: Bấm nút "Xác nhận Trả sách" trên dòng phiếu mượn
    activate UI
    UI->>Router: PUT /api/borrows/{record_id}/return
    activate Router
    Router->>Service: return_book(db, record_id)
    activate Service

    Service->>DB: Truy vấn BorrowRecord theo record_id
    Service->>DB: Cập nhật status = RETURNED, ghi nhận return_date = today
    Service->>DB: Hoàn trả tồn kho: available_quantity = available_quantity + 1

    alt Trường hợp Trả Quá Hạn (today > due_date)
        Service->>Service: Tính số ngày trễ hạn = today - due_date
        Service->>Service: Tính tổng tiền phạt = overdue_days * 2.000 VNĐ
        Service->>DB: Tạo bản ghi Fine mới (status = PENDING)
    end

    opt Trường hợp Có Đơn Đặt Trước (Reservation) Đang Chờ
        Service->>DB: Tìm đơn Reservation PENDING có thời gian tạo sớm nhất
        Service->>DB: Cập nhật status = READY, thiết lập expire_date = today + 7 ngày
    end

    Service->>DB: Commit giao dịch ACID thành công
    DB-->>Service: Xác nhận giao dịch hoàn tất
    Service-->>Router: Trả về kết quả trả sách kèm thông tin phạt (nếu có)
    deactivate Service
    Router-->>UI: 200 OK {status: "RETURNED", fine: {...}}
    deactivate Router
    UI-->>Librarian: Hiển thị Toast trả sách thành công & Popup thu tiền phạt (nếu trễ hạn)
    deactivate UI
""",

    # -------------------------------------------------------------
    # 13. Sequence AI Chat (Chuẩn UML Sequence Pipeline Chatbot AI)
    # -------------------------------------------------------------
    "13_sequence_ai_chat.png": """
sequenceDiagram
    autonumber
    actor Reader as 🎓 Độc giả
    participant UI as 💬 Khung Chatbot Web UI
    participant Router as ⚡ AI Router (/api/ai/search)
    participant Engine as 📝 Prompt Engine
    participant Service as 🤖 AIService
    participant Gemini as 🌐 Google Gemini 1.5 Flash Cloud
    participant DB as 🗄️ CSDL Thư viện

    Reader->>UI: Nhập câu hỏi: "Tìm cho tôi sách AI dễ hiểu cho người mới bắt đầu"
    activate UI
    UI->>Router: POST /api/ai/search {query: "..."}
    activate Router

    Router->>DB: Lấy danh mục sách đang hoạt động (mã, tên, tác giả, thể loại)
    DB-->>Router: Trả về danh sách sách hiện có trong kho
    Router->>Engine: Đóng gói Prompt (Loại bỏ danh tính độc giả + Zero-Hallucination Guardrails)
    Engine-->>Router: Trả về Grounded Context Prompt hoàn chỉnh

    Router->>Service: generate(SystemPrompt, UserPrompt)
    activate Service

    alt Có API Key hợp lệ và Kết nối Internet ổn định
        Service->>Gemini: Gửi HTTPS Request (Timeout 15s, Max Retries 2)
        activate Gemini
        Gemini-->>Service: Trả về văn bản gợi ý và phân tích chuyên môn
        deactivate Gemini
    else Mất kết nối Internet hoặc Lỗi Google API Quota
        Service->>Service: Kích hoạt Mock Fallback Engine sinh phản hồi cục bộ an toàn
    end

    Service-->>Router: Trả về văn bản phản hồi thông minh
    deactivate Service

    Router->>Router: Trích xuất thực thể sách khớp với Database (Entity Matching)
    Router-->>UI: 200 OK {answer: "...", suggested_books: [...], source: "gemini|mock"}
    deactivate Router

    UI-->>Reader: Hiển thị tin nhắn AI thân thiện kèm các Bộ Thẻ Sách tương tác
    deactivate UI
""",

    # -------------------------------------------------------------
    # 14. Sequence AI Suggest (Chuẩn UML Sequence Gợi Ý Sách)
    # -------------------------------------------------------------
    "14_sequence_ai_suggest.png": """
sequenceDiagram
    autonumber
    actor Reader as 🎓 Độc giả
    participant UI as 🖥️ Trang Khám Phá Sách
    participant Router as ⚡ AI Router (/api/ai/suggest)
    participant Service as 🤖 AIService
    participant Gemini as 🌐 Google Gemini 1.5 Flash Cloud
    participant DB as 🗄️ CSDL Thư viện

    Reader->>UI: Truy cập trang Gợi ý Sách Cá nhân hóa
    activate UI
    UI->>Router: GET /api/ai/suggest
    activate Router

    Router->>DB: Truy vấn lịch sử các đầu sách độc giả từng mượn (Ẩn danh hóa thông tin)
    Router->>DB: Truy vấn toàn bộ danh mục sách hiện có sẵn trong thư viện
    DB-->>Router: Trả về lịch sử đọc & danh mục kho sách

    Router->>Service: Gửi Prompt phân tích sở thích đọc theo thể loại và tác giả
    activate Service
    Service->>Gemini: Phân tích gu đọc và suy luận các tựa sách phù hợp nhất
    activate Gemini
    Gemini-->>Service: Danh sách 3-5 cuốn sách đề xuất kèm lý do chi tiết
    deactivate Gemini
    Service-->>Router: Kết quả gợi ý hoàn chỉnh
    deactivate Service

    Router-->>UI: 200 OK {suggestions: [...], source: "gemini"}
    deactivate Router
    UI-->>Reader: Hiển thị bộ sưu tập sách đề xuất riêng biệt theo hồ sơ học tập
    deactivate UI
""",

    # -------------------------------------------------------------
    # 15. ERD Database (Sơ đồ Thực Thể Quan Hệ 8 Bảng Chuẩn 3NF)
    # -------------------------------------------------------------
    "15_erd_database.png": """
erDiagram
    USERS ||--o| READERS : "có hồ sơ 1:1"
    READERS ||--o{ BORROW_RECORDS : "lập phiếu 1:N"
    BOOKS ||--o{ BORROW_RECORDS : "được mượn 1:N"
    BORROW_RECORDS ||--o| FINES : "phát sinh phạt 1:1"
    READERS ||--o{ RESERVATIONS : "đặt trước 1:N"
    BOOKS ||--o{ RESERVATIONS : "được đặt 1:N"
    CATEGORIES ||--o{ BOOKS : "phân loại 1:N"
    AUTHORS ||--o{ BOOKS : "sáng tác 1:N"

    USERS {
        int id PK "Khóa chính tự tăng"
        string username "Tên đăng nhập duy nhất (UQ)"
        string email "Địa chỉ email duy nhất (UQ)"
        string hashed_password "Mật khẩu băm chuẩn Bcrypt"
        string full_name "Họ và tên người dùng"
        string role "Vai trò: ADMIN, LIBRARIAN, READER"
        boolean is_active "Trạng thái tài khoản"
    }

    READERS {
        int id PK "Khóa chính tự tăng"
        int user_id FK "Khóa ngoại liên kết USERS"
        string reader_code "Mã độc giả duy nhất (UQ)"
        string phone "Số điện thoại liên hệ"
        string reader_type "Loại: SINH_VIEN, GIANG_VIEN"
        string card_status "Trạng thái thẻ: ACTIVE, EXPIRED"
        date card_issued_date "Ngày cấp thẻ thư viện"
        date card_expire_date "Ngày hết hạn thẻ"
        int max_borrow_books "Hạn mức mượn tối đa: 5 cuốn"
    }

    CATEGORIES {
        int id PK "Khóa chính tự tăng"
        string name "Tên thể loại duy nhất (UQ)"
        string description "Mô tả thể loại sách"
    }

    AUTHORS {
        int id PK "Khóa chính tự tăng"
        string name "Họ và tên tác giả"
        string bio "Tiểu sử và chuyên môn tác giả"
    }

    BOOKS {
        int id PK "Khóa chính tự tăng"
        string code "Mã sách duy nhất (UQ)"
        string title "Tựa đề cuốn sách"
        int author_id FK "Khóa ngoại liên kết AUTHORS"
        int category_id FK "Khóa ngoại liên kết CATEGORIES"
        string publisher "Nhà xuất bản"
        int publish_year "Năm xuất bản"
        string isbn "Mã ISBN quốc tế duy nhất"
        int total_quantity "Tổng số bản sách nhập kho"
        int available_quantity "Số bản sách còn sẵn trên kệ"
        string description "Tóm tắt nội dung cuốn sách"
        boolean is_active "Trạng thái lưu hành"
    }

    BORROW_RECORDS {
        int id PK "Khóa chính tự tăng"
        string borrow_code "Mã phiếu mượn duy nhất (UQ)"
        int reader_id FK "Khóa ngoại liên kết READERS"
        int book_id FK "Khóa ngoại liên kết BOOKS"
        date borrow_date "Ngày mượn sách"
        date due_date "Hạn trả sách (tiêu chuẩn 14 ngày)"
        date return_date "Ngày thực tế mang sách trả"
        int renew_count "Số lần đã gia hạn (tối đa 1)"
        string status "Trạng thái: BORROWING, RETURNED, OVERDUE"
        string notes "Ghi chú tình trạng sách"
    }

    FINES {
        int id PK "Khóa chính tự tăng"
        int borrow_record_id FK "Khóa ngoại liên kết BORROW_RECORDS"
        int reader_id FK "Khóa ngoại liên kết READERS"
        int overdue_days "Số ngày trễ hạn thực tế"
        float fine_per_day "Đơn giá phạt: 2.000 VNĐ/ngày"
        float total_amount "Tổng tiền phạt phải nộp"
        string status "Trạng thái: PENDING, PAID, WAIVED"
        date paid_date "Ngày thanh toán tiền phạt"
    }

    RESERVATIONS {
        int id PK "Khóa chính tự tăng"
        int reader_id FK "Khóa ngoại liên kết READERS"
        int book_id FK "Khóa ngoại liên kết BOOKS"
        datetime reservation_date "Thời điểm tạo đơn đặt trước"
        date expire_date "Thời hạn giữ chỗ ưu tiên (7 ngày)"
        string status "Trạng thái: PENDING, READY, COMPLETED"
        string notes "Ghi chú đặt trước"
    }
""",

    # -------------------------------------------------------------
    # 16. System Architecture (Kiến Trúc Phân Tầng 4 Lớp Chuẩn Mực)
    # -------------------------------------------------------------
    "16_system_architecture.png": """
flowchart TB
    subgraph ClientLayer ["1. TẦNG GIAO DIỆN NGƯỜI DÙNG (PRESENTATION LAYER - CLIENT)"]
        direction LR
        UI1["🖥️ Web Client Hiện Đại<br/>(HTML5, Vanilla CSS Glassmorphism)"]
        UI2["📊 Trực Quan Hóa Dữ Liệu<br/>(Chart.js KPI Dashboard)"]
        UI3["⚡ Module JavaScript Bất Đồng Bộ<br/>(Fetch JSON REST API)"]
    end

    subgraph APILayer ["2. TẦNG ĐIỀU KHIỂN & BẢO MẬT API (FASTAPI BACKEND CONTROLLER)"]
        direction LR
        Router["🛣️ 7 API Routers Độc Lập:<br/>• Auth, Books, Readers, Borrows<br/>• Reservations, Statistics, AI"]
        Guards["🛡️ Cơ Chế Bảo Mật & Phân Quyền:<br/>• JWT Bearer HS256 Token<br/>• RBAC Dependency Injection"]
        Schemas["📋 Kiểm Thực Dữ Liệu Chặt Chẽ:<br/>• Pydantic v2 Models Validation"]
    end

    subgraph ServiceLayer ["3. TẦNG NGHIỆP VỤ CỐT LÕI (CORE BUSINESS SERVICE LAYER)"]
        direction LR
        BorrowSvc["💼 BorrowService (Quản lý Lưu thông):<br/>• Kiểm tra 4 điều kiện mượn<br/>• Tính phạt 2.000đ/ngày & giữ chỗ 7 ngày"]
        AISvc["🤖 AIService (Điều phối AI):<br/>• Quản lý Gemini 1.5 Flash Cloud<br/>• Timeout 15s & Mock Fallback Engine"]
        Prompts["📝 Prompt Engine:<br/>• Zero-Hallucination Guardrails<br/>• Privacy-by-Design Scrubbing"]
    end

    subgraph DataLayer ["4. TẦNG DỮ LIỆU & DỊCH VỤ NGOÀI (DATA & EXTERNAL SERVICES LAYER)"]
        direction LR
        DB[("🗄️ CSDL Quan Hệ (SQLite / PostgreSQL)<br/>SQLAlchemy 2.0 ORM (8 Bảng chuẩn 3NF)<br/>Bảo đảm giao dịch toàn vẹn ACID")]
        Gemini["🌐 Google Gemini 1.5 Flash API<br/>(Cửa sổ ngữ cảnh 1.000.000 tokens)<br/>Kết nối an toàn bảo mật qua HTTPS TLS 1.3"]
    end

    ClientLayer ==>|Giao thức HTTP / JSON RESTful Requests| APILayer
    APILayer ==>|Gọi hàm nghiệp vụ & Chuyển giao Dependency Context| ServiceLayer
    BorrowSvc ==>|Thực thi giao dịch ACID đọc/ghi dữ liệu| DB
    AISvc ==>|Gọi HTTPS API an toàn đám mây| Gemini
    AISvc -.->|Đối soát thực thể sách| DB
    BorrowSvc -.->|Tích hợp khuôn mẫu| Prompts
""",

    # -------------------------------------------------------------
    # 17. AI Pipeline Flow (Quy Trình Grounded Prompting 2 Giai Đoạn)
    # -------------------------------------------------------------
    "17_ai_pipeline_flow.png": """
flowchart TD
    subgraph Stage1 ["GIAI ĐOẠN 1: TIẾP NHẬN YÊU CẦU & CHUẨN BỊ NGỮ CẢNH (PRIVACY-BY-DESIGN)"]
        Step1["1. Độc giả gửi câu hỏi tự nhiên bằng tiếng Việt<br/>(Ví dụ: 'Tôi muốn tìm sách học lập trình Python cơ bản')"]
        Step2["2. Truy vấn CSDL Thư viện nội bộ<br/>(Lấy danh mục sách khả dụng: Mã, Tên, Tác giả, Thể loại)"]
        Step3["3. Khử định danh dữ liệu nhạy cảm (Privacy Scrubbing)<br/>(Loại bỏ 100% thông tin cá nhân của độc giả trước khi gửi lên Cloud)"]
        Step4["4. Đóng gói Grounded Context Prompt với Zero-Hallucination Guardrails<br/>(Ràng buộc nghiêm ngặt: Chỉ gợi ý và phân tích dựa trên sách có trong DB)"]
        
        Step1 --> Step2 --> Step3 --> Step4
    end

    subgraph Stage2 ["GIAI ĐOẠN 2: THỰC THI SUY LUẬN AI & TRÍCH XUẤT THỰC THỂ SÁCH"]
        Step5{"5. Gọi Mô hình Ngôn ngữ Lớn (LLM)<br/>Google Gemini 1.5 Flash API<br/>(Cửa sổ 1M tokens - Tiêu thụ ~15K-35K tokens)"}
        Step5_Mock["Kích hoạt Mock Fallback Engine an toàn nội bộ<br/>(Tự động phản hồi khi ngắt mạng hoặc hết quota API)"]
        Step6["6. Phân tích Văn bản & Khớp Thực thể Thông minh (Smart Entity Extraction)<br/>(Thuật toán quét trích xuất mã sách và tựa sách thực tế trong DB)"]
        Step7["7. Trả về Giao diện Người dùng<br/>(Đoạn hội thoại tự nhiên tiếng Việt + Bộ Thẻ Sách có nút Mượn trực tiếp)"]
        
        Step4 --> Step5
        Step5 -- Kết nối Internet ổn định --> Step6
        Step5 -- Lỗi mạng / Quá thời gian Timeout 15s --> Step5_Mock --> Step6
        Step6 --> Step7
    end
""",

    # -------------------------------------------------------------
    # 18. RAG Architecture (Kiến Trúc Hiện Tại vs Định Hướng RAG)
    # -------------------------------------------------------------
    "18_rag_architecture.png": """
flowchart TD
    subgraph HienTai ["GIAI ĐOẠN HIỆN TẠI: Grounded In-Context Retrieval (Đã Hiện Thực Hoàn Chỉnh)"]
        Q1["Câu hỏi người dùng"] --> DB1[("SQLite / PostgreSQL Database")]
        DB1 --> P1["Ghép toàn bộ Sách khả dụng vào Context Prompt<br/>(Tận dụng cửa sổ ngữ cảnh 1.000.000 tokens của Gemini 1.5 Flash)"]
        P1 --> G1["Google Gemini 1.5 Flash Engine"]
        G1 --> Out1["Kết quả chính xác tuyệt đối, Zero-Hallucination, Trả lời kèm Card Sách"]
    end

    subgraph TuongLai ["ĐỊNH HƯỚNG MỞ RỘNG: Retrieval-Augmented Generation (RAG) với Vector Database"]
        PDF["Tài liệu, Mục lục, Toàn văn Sách PDF"] --> Chunker["Text Chunking & Preprocessing (Cắt đoạn ngữ nghĩa)"]
        Chunker --> EmbedModel["Embedding Model (text-embedding-004)"]
        EmbedModel --> VectorDB[("Vector Database (ChromaDB / FAISS)")]
        Q2["Câu hỏi chuyên sâu"] --> QEmbed["Embed Query Vector"]
        QEmbed --> SimSearch["Vector Similarity Search (Tìm top-k Chunks tương đồng nhất)"]
        VectorDB --> SimSearch
        SimSearch --> RAGPrompt["RAG Context Prompt (Trích đoạn liên quan)"]
        RAGPrompt --> LLM2["Gemini LLM Engine"]
        LLM2 --> Out2["Trả lời chuyên sâu, trích dẫn rõ nguồn trang và chương sách"]
    end
"""
}

# HTML Template kết xuất đồ họa cao cấp, font chữ sắc nét chuẩn academic
HTML_RENDER_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            padding: 40px;
            background: #FFFFFF;
            display: inline-block;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }}
        #diagram-card {{
            background: #FFFFFF;
            padding: 35px;
            border: 1.5px solid #CBD5E1;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            display: inline-block;
        }}
        svg {{
            font-family: 'Segoe UI', Roboto, Arial, sans-serif !important;
            letter-spacing: 0.2px;
        }}
        .node rect, .node circle, .node ellipse, .node polygon {{
            stroke-width: 2px !important;
        }}
        .edgeLabel {{
            background-color: #FFFFFF !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
        }}
        /* ERD Specific Styling */
        .er.entityBox {{
            fill: #F8FAFC !important;
            stroke: #4F46E5 !important;
            stroke-width: 2px !important;
        }}
        .er.attributeBoxOdd {{
            fill: #FFFFFF !important;
        }}
        .er.attributeBoxEven {{
            fill: #F1F5F9 !important;
        }}
    </style>
</head>
<body>
    <div id="diagram-card">
        <pre class="mermaid">
{mermaid_code}
        </pre>
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            themeVariables: {{
                primaryColor: '#EEF2FF',
                primaryTextColor: '#0F172A',
                primaryBorderColor: '#4F46E5',
                lineColor: '#3B82F6',
                secondaryColor: '#F0FDFA',
                secondaryBorderColor: '#0D9488',
                tertiaryColor: '#FFFFFF',
                tertiaryBorderColor: '#CBD5E1',
                fontFamily: 'Segoe UI, Roboto, sans-serif',
                fontSize: '15px'
            }}
        }});
    </script>
</body>
</html>
"""

# Bảng ánh xạ mã hình ảnh theo mục lục đồ án
MAPPING_NAMES = {
    "01_context_diagram.png": "Hinh_3_1_So_Do_Boi_Canh_Context_Diagram.png",
    "02_usecase_general.png": "Hinh_2_1_So_Do_Use_Case_Tong_Quan.png",
    "03_usecase_library.png": "Hinh_2_2_So_Do_Use_Case_Nghiep_Vu_Thu_Vien.png",
    "04_usecase_ai.png": "Hinh_2_3_So_Do_Use_Case_Tro_Ly_AI.png",
    "05_activity_borrow.png": "Hinh_3_3_So_Do_Hoat_Dong_Muon_Sach.png",
    "06_activity_return.png": "Hinh_3_4_So_Do_Hoat_Dong_Tra_Sach_Tinh_Phat.png",
    "07_activity_renew.png": "Hinh_3_5_So_Do_Hoat_Dong_Gia_Han_Sach.png",
    "08_activity_reservation.png": "Hinh_3_6_So_Do_Hoat_Dong_Dat_Truoc_Sach.png",
    "09_activity_fine.png": "Hinh_3_7_So_Do_Hoat_Dong_Xu_Ly_Phat.png",
    "10_activity_ai_chat.png": "Hinh_3_8_So_Do_Hoat_Dong_Chatbot_AI.png",
    "11_sequence_borrow.png": "Hinh_3_9_So_Do_Tuan_Tu_Muon_Sach.png",
    "12_sequence_return.png": "Hinh_3_10_So_Do_Tuan_Tu_Tra_Sach_Xu_Ly_Phat.png",
    "13_sequence_ai_chat.png": "Hinh_3_11_So_Do_Tuan_Tu_Chatbot_AI_Tra_Cuu.png",
    "14_sequence_ai_suggest.png": "Hinh_3_12_So_Do_Tuan_Tu_AI_Goi_Y_Sach.png",
    "15_erd_database.png": "Hinh_4_1_So_Do_Thuc_The_Quan_He_ERD_8_Bang.png",
    "16_system_architecture.png": "Hinh_3_2_So_Do_Kien_Truc_Phan_Tang_Layered.png",
    "17_ai_pipeline_flow.png": "Hinh_5_1_So_Do_Pipeline_Grounded_Prompting_AI.png",
    "18_rag_architecture.png": "Hinh_5_2_So_Do_Kien_Truc_Mo_Rong_RAG_VectorDB.png",
}

async def render_all_ultra_hd():
    print("🚀 Bắt đầu Render toàn bộ 18 sơ đồ ở độ phân giải siêu nét Ultra-HD (2K/Retina)...")
    print(f"📁 Thư mục lưu trữ chính: {MAIN_OUTPUT_DIR}")
    print(f"📁 Thư mục tài liệu báo cáo: {DIAGRAMS_DIR}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 3000, "height": 2200}, device_scale_factor=2)
        
        for idx, (filename, mermaid_code) in enumerate(ULTRA_HD_DIAGRAMS.items(), 1):
            html_content = HTML_RENDER_TEMPLATE.format(mermaid_code=mermaid_code.strip())
            temp_file = os.path.join(DIAGRAMS_DIR, "temp_render.html")
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            await page.goto(f"file://{temp_file}")
            await page.wait_for_selector("#diagram-card svg", timeout=25000)
            
            # Tự động co giãn theo viewBox chuẩn, nét căng
            dimensions = await page.evaluate("""() => {
                const s = document.querySelector('#diagram-card svg');
                s.style.maxWidth = 'none';
                const vb = s.getAttribute('viewBox');
                let targetW = 1600;
                let targetH = 1000;
                
                if (vb) {
                    const parts = vb.trim().split(/[ ,]+/);
                    if (parts.length === 4) {
                        const vbW = parseFloat(parts[2]);
                        const vbH = parseFloat(parts[3]);
                        
                        targetW = vbW;
                        if (targetW < 1300) {
                            targetW = 1400;
                        }
                        const scale = targetW / vbW;
                        targetH = vbH * scale;
                    }
                }
                
                s.setAttribute('width', `${targetW}px`);
                s.setAttribute('height', `${targetH}px`);
                s.style.width = `${targetW}px`;
                s.style.height = `${targetH}px`;
                
                return { targetW, targetH };
            }""")
            
            await page.wait_for_timeout(500)
            
            card_el = await page.query_selector("#diagram-card")
            output_png_docs = os.path.join(DIAGRAMS_DIR, filename)
            await card_el.screenshot(path=output_png_docs)
            
            # Đồng bộ sang thư mục đồ án chính
            main_copy_1 = os.path.join(MAIN_OUTPUT_DIR, filename)
            shutil.copy(output_png_docs, main_copy_1)
            
            mapped_name = MAPPING_NAMES.get(filename)
            if mapped_name:
                main_copy_2 = os.path.join(MAIN_OUTPUT_DIR, mapped_name)
                shutil.copy(output_png_docs, main_copy_2)
                
            im = Image.open(output_png_docs)
            file_kb = os.path.getsize(output_png_docs) / 1024
            print(f"  [{idx:2d}/18] ✅ [ĐÃ XUẤT] {filename:26} -> {im.size[0]}x{im.size[1]} px ({file_kb:.1f} KB)")
            
        await browser.close()
        
    print("\n🎉 HOÀN TẤT RENDER 18 SƠ ĐỒ ĐẠT CHUẨN KỸ THUẬT & ĐÚNG ĐỊNH DẠNG UML TOÀN DIỆN!")

if __name__ == "__main__":
    asyncio.run(render_all_ultra_hd())
