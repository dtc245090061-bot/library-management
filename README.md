# 📚 HỆ THỐNG QUẢN LÝ THƯ VIỆN TÍCH HỢP TRÍ TUỆ NHÂN TẠO (AI)
### Smart Library Management System with Generative AI Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy%202.0-red)](https://www.sqlalchemy.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-orange?logo=sqlite)](https://sqlite.org)
[![AI](https://img.shields.io/badge/Generative%20AI-Google%20Gemini%201.5%20Flash-4285F4?logo=google)](https://ai.google.dev)
[![FTS5](https://img.shields.io/badge/Search-SQLite%20FTS5%20BM25-blueviolet)](https://sqlite.org/fts5.html)
[![Frontend](https://img.shields.io/badge/Frontend-Vanilla%20JS%20%26%20Glassmorphism-brightgreen)](https://developer.mozilla.org)
[![Tests](https://img.shields.io/badge/Tests-26%2F26%20PASSED-success?logo=pytest)](https://pytest.org)

---

## 📖 1. Giới Thiệu Đề Tài

Hệ thống **Quản Lý Thư Viện Tích Hợp Trí Tuệ Nhân Tạo (Smart Library Management System)** là giải pháp phần mềm hiện đại nhằm số hóa toàn diện quy trình vận hành thư viện học thuật truyền thống, đồng thời ứng dụng công nghệ **AI Tạo sinh (Generative AI - Google Gemini 1.5 Flash)** và **Tìm kiếm toàn văn (FTS5 BM25)** để nâng tầm trải nghiệm tra cứu và nghiên cứu của bạn đọc.

Dự án được xây dựng dựa trên kiến trúc phân tầng chuẩn mực (**Layered Architecture**), tuân thủ các nguyên tắc bảo mật **RBAC (Role-Based Access Control)**, cơ chế bảo vệ quyền riêng tư **Privacy-by-Design**, và kỹ thuật **Grounded In-Context Retrieval** nhằm triệt tiêu hoàn toàn hiện tượng ảo giác (Zero-Hallucination) của mô hình ngôn ngữ lớn.

---

## 🏛️ 2. Kiến Trúc Hệ Thống & Cơ Sở Dữ Liệu

### 2.1. Kiến Trúc Phân Tầng 4 Lớp (Layered Architecture)

Hệ thống phân tách trách nhiệm độc lập theo 4 tầng (Separation of Concerns):
1. **Tầng Trình diễn (Presentation Layer - Web Client):** Xây dựng bằng HTML5, Vanilla CSS Glassmorphism/White Theme trang nhã và JavaScript modules bất đồng bộ (Fetch REST API). Tích hợp Chart.js trực quan hóa KPI thời gian thực.
2. **Tầng Điều khiển & Bảo mật (API Gateway & Controller Layer):** Phát triển trên framework FastAPI hiệu năng cao, kiểm thực dữ liệu qua Pydantic v2 Schemas, xác thực bảo mật JWT Token (HS256) và phân quyền RBAC qua Dependency Injection.
3. **Tầng Dịch vụ Nghiệp vụ (Core Business Service Layer):** 
   - `BorrowService`: Điều phối toàn bộ quy tắc mượn, trả, tự động phạt quá hạn, gia hạn và hàng đợi đặt trước.
   - `AIService`: Điều phối vòng đời tương tác với Google Gemini Cloud API (Timeout 15s, Max Retries 2, Exponential Backoff) và kích hoạt Mock Fallback Engine nội bộ khi mất mạng.
   - `Prompt Engine`: Quản lý các mẫu Prompt có cấu trúc ngữ cảnh và khử định danh dữ liệu nhạy cảm.
   - `FTSService`: Đồng bộ và tìm kiếm toàn văn BM25 tiếng Việt qua SQLite FTS5.
4. **Tầng Dữ liệu & Dịch vụ Ngoài (Data & External Cloud Layer):** SQLAlchemy 2.0 ORM kết nối CSDL SQLite/PostgreSQL (giao dịch ACID toàn vẹn 8 bảng 3NF) và kết nối HTTPS an toàn ra Google Gemini API.

```
+-------------------------------------------------------------------------+
|                1. PRESENTATION LAYER (Web Client UI)                   |
|  - HTML5, Vanilla CSS Glassmorphism, Micro-animations                   |
|  - Chart.js Dashboard Visualizations & Async Fetch REST API             |
+------------------------------------+------------------------------------+
                                     |  HTTP REST / JSON
+------------------------------------v------------------------------------+
|             2. API CONTROLLER & SECURITY LAYER (FastAPI)                |
|  - 7 Routers: Auth, Books, Readers, Borrows, Reservations, Stats, AI    |
|  - JWT Bearer Middleware, RBAC Dependency Injection, Pydantic v2        |
+------------------------------------+------------------------------------+
                                     |  Function Calls
+------------------------------------v------------------------------------+
|                  3. CORE SERVICE LAYER (Business Logic)                 |
|  - BorrowService (Mượn/Trả/Phạt/Gia hạn/FIFO Queue)                     |
|  - AIService (Gemini Orchestrator, Timeout 15s, Mock Fallback)          |
|  - Prompt Engine (Grounded Templates, Privacy Scrubbing)                |
|  - FTSService (SQLite FTS5 BM25 Vietnamese Full-Text Search)            |
+-------------------+---------------------------------+-------------------+
                    | ACID Session                    | HTTPS TLS 1.3
+-------------------v---------------+ +---------------v-------------------+
| 4a. DATABASE LAYER (SQLAlchemy)   | | 4b. EXTERNAL CLOUD SERVICE        |
| - SQLite / PostgreSQL (8 Bảng 3NF)| | - Google Gemini 1.5 Flash Cloud   |
| - users, readers, books, borrows, | |   (Context Window: 1M tokens)     |
|   categories, authors, fines, res | |                                   |
+-----------------------------------+ +-----------------------------------+
```

### 2.2. Mô Hình Cơ Sở Dữ Liệu Quan Hệ (ERD 8 Bảng Chuẩn 3NF)

Hệ thống thiết kế chuẩn hóa 3NF gồm 8 thực thể quan hệ chặt chẽ:
- `users`: Tài khoản người dùng (id, username, email, hashed_password, full_name, role: ADMIN/LIBRARIAN/READER, is_active).
- `readers`: Hồ sơ độc giả (user_id FK, reader_code UQ, reader_type: STUDENT/TEACHER/STAFF/EXTERNAL, card_status: ACTIVE/EXPIRED/SUSPENDED, card_issued_date, card_expire_date, max_borrow_books).
- `categories`: Thể loại sách (id, name, description).
- `authors`: Tác giả sách (id, name, bio).
- `books`: Danh mục sách (code UQ, title, author_id FK, category_id FK, publisher, publish_year, isbn, total_quantity, available_quantity, description, is_active).
- `borrow_records`: Phiếu mượn lưu thông (borrow_code UQ, reader_id FK, book_id FK, borrow_date, due_date, return_date, renew_count, status: BORROWING/RETURNED/OVERDUE).
- `fines`: Khoản phạt vi phạm quá hạn (borrow_record_id FK, reader_id FK, overdue_days, fine_per_day, total_amount, status: PENDING/PAID/WAIVED, paid_date).
- `reservations`: Hàng đợi đặt trước sách (reader_id FK, book_id FK, reservation_date, expire_date, status: PENDING/READY/COMPLETED).

---

## ⚡ 3. Nghiệp Vụ Cốt Lõi Hệ Thống (Business Rules)

### 3.1. Nghiệp Vụ Mượn Sách (Borrowing Workflow)
Thủ thư quét mã thẻ độc giả và mã sách. Hệ thống kiểm tra tuần tự 4 điều kiện nghiêm ngặt:
1. **Trạng thái thẻ:** Thẻ độc giả phải ở trạng thái `ACTIVE` và còn thời hạn sử dụng.
2. **Hạn mức mượn:** Tổng số sách đang mượn hiện tại phải nhỏ hơn hạn mức (Sinh viên: 5 cuốn, Giảng viên: 8 cuốn, Bên ngoài: 3 cuốn).
3. **Nợ phạt:** Độc giả không có bất kỳ khoản nợ phạt trễ hạn nào ở trạng thái `PENDING`.
4. **Tồn kho khả dụng:** Sách yêu cầu phải còn bản khả dụng trên kệ (`available_quantity > 0`).

*Khi thỏa mãn cả 4 điều kiện:* Hệ thống tạo bản ghi `BorrowRecord` mới với hạn trả tiêu chuẩn **14 ngày**, giảm tồn kho `available_quantity` đi 1 đơn vị, và tự động hoàn tất đơn đặt trước tương ứng (nếu có).

### 3.2. Nghiệp Vụ Trả Sách & Tự Động Tính Phạt (Return & Penalty Workflow)
Khi tiếp nhận trả sách:
- Cập nhật ngày trả thực tế (`return_date = today`) và chuyển trạng thái phiếu sang `RETURNED`.
- Tăng số lượng sách khả dụng trong kho lên 1 đơn vị (`available_quantity += 1`).
- **Tự động tính tiền phạt trễ hạn:** Nếu `today > due_date`, hệ thống tự động tính:
  $$\text{Tổng tiền phạt} = (\text{today} - \text{due\_date}) \times 2.000\text{ VNĐ}$$
  và tạo bản ghi phạt `Fine` ở trạng thái `PENDING`.
- **Kích hoạt hàng đợi đặt trước:** Kiểm tra nếu có độc giả khác đang xếp hàng `PENDING` đặt trước sách này, hệ thống tự động chuyển đơn sớm nhất sang trạng thái `READY` và giữ chỗ ưu tiên trong **7 ngày**.

### 3.3. Nghiệp Vụ Gia Hạn Sách (Renewal Workflow)
Độc giả hoặc thủ thư có thể yêu cầu gia hạn thời gian mượn sách thêm **7 ngày** nếu đáp ứng đủ 3 quy tắc:
1. Phiếu mượn đang ở trạng thái `BORROWING` và chưa bị quá hạn (`today <= due_date`).
2. Phiếu mượn chưa từng gia hạn trước đó (`renew_count == 0` - mỗi phiếu chỉ được gia hạn tối đa 01 lần).
3. Cuốn sách hiện không có bất kỳ độc giả nào khác đang đặt trước trong hàng đợi.

### 3.4. Nghiệp Vụ Xếp Hàng Đặt Trước Sách (Reservation FIFO Queue)
- Khi một cuốn sách hết sạch bản khả dụng trên giá (`available_quantity == 0`), độc giả có thể bấm "Đặt trước sách".
- Hệ thống tạo bản ghi `Reservation` với trạng thái `PENDING` và đưa vào hàng đợi FIFO.
- Khi có sách trả về, đơn đặt trước có thời gian tạo sớm nhất được chuyển sang `READY` và khóa giữ chỗ trong vòng 7 ngày.

### 3.5. Nghiệp Vụ Cấp Thẻ Độc Giả Thông Minh
Hỗ trợ 2 phương thức linh hoạt:
- **Tạo độc giả mới hoàn toàn:** Nhập Họ tên, Email, Mã thẻ, Phân loại độc giả, SĐT, Địa chỉ, Hạn thẻ -> Hệ thống tự động sinh tài khoản User (mặc định password `123456`) và cấp thẻ độc giả cùng lúc.
- **Liên kết tài khoản có sẵn:** Cho phép chọn từ danh sách người dùng đã đăng ký nhưng chưa có thẻ.
- **Tự động gợi ý mã thẻ:** API `/api/readers/next-code` tự động phân tích và sinh mã thẻ tiếp theo (ví dụ `DG2026009`).

---

## 🤖 4. Phân Hệ Trợ Lý Trí Tuệ Nhân Tạo (Generative AI)

Hệ thống tích hợp mô hình ngôn ngữ lớn **Google Gemini 1.5 Flash Cloud API** thông qua kiến trúc **Grounded In-Context Prompting** giải quyết triệt để bài toán Hallucination:

1. **Chatbot Tra cứu Ngôn ngữ Tự nhiên (`POST /api/ai/search`):**
   - Tiếp nhận câu hỏi tự nhiên bằng tiếng Việt (ví dụ: *"Tìm cho tôi sách lập trình Web FastAPI dễ học cho người mới bắt đầu"*).
   - Hệ thống tự động truy vấn danh mục sách từ CSDL, ẩn danh thông tin cá nhân (Privacy-by-Design), đóng gói vào Context Prompt kèm các chỉ thị ràng buộc nghiêm ngặt (Zero-Hallucination Guardrails).
   - AI phân tích ngữ cảnh, lựa chọn sách phù hợp và trả về phản hồi tự nhiên kèm các thẻ (Card) sách tương tác trực tiếp (có nút xem chi tiết và mượn ngay).
2. **AI Tóm tắt Nội dung & Mục lục Sách (`POST /api/ai/summarize/{id}`):**
   - Trích xuất thông tin tác phẩm và sinh ra bản tóm tắt hấp dẫn 100 - 200 từ gồm: Tổng quan, Điểm nổi bật, và Đối tượng phù hợp.
3. **AI Gợi ý Sách Cá nhân hóa (`GET /api/ai/suggest`):**
   - Phân tích lịch sử đọc sách của độc giả (đã khử định danh cá nhân) để suy luận gu đọc và đề xuất 3-5 cuốn sách phù hợp nhất kèm lý giải chi tiết.
4. **Cơ chế Chịu lỗi Đa tầng (Resilience & Mock Fallback Engine):**
   - Cấu hình Timeout 15s với thuật toán Retry x2 và Exponential Backoff.
   - Nếu ngắt kết nối mạng hoặc hết quota API Key, hệ thống **tự động chuyển đổi liền mạch sang Mock Fallback Engine nội bộ**, đảm bảo trải nghiệm người dùng không bị gián đoạn.
5. **Tìm kiếm Toàn văn SQLite FTS5:**
   - Hỗ trợ đánh chỉ mục toàn văn BM25 tiếng Việt có dấu cho tiêu đề, tác giả, thể loại và nội dung mô tả sách.

---

## 📁 5. Cấu Trúc Thư Mục Dự Án

```
library-management/
├── backend/                        # Toàn bộ mã nguồn Backend FastAPI
│   ├── main.py                     # Entry point FastAPI, lifespan & routes mounting
│   ├── database.py                 # SQLAlchemy engine, SessionLocal & get_db dependency
│   ├── config.py                   # Pydantic BaseSettings cấu hình biến môi trường
│   ├── schemas.py                  # Pydantic v2 validation models cho Request/Response
│   ├── auth_utils.py               # Bcrypt password hashing & JWT token generation (HS256)
│   ├── dependencies.py             # HTTPBearer & RBAC authorization dependencies
│   ├── seed_data.py                # Script nạp dữ liệu mẫu phong phú 8 bảng
│   ├── backup_cli.py               # Công cụ CLI sao lưu và phục hồi CSDL tự động
│   ├── render_ultra_hd_diagrams.py # Script tự động render 18 sơ đồ kỹ thuật Ultra-HD
│   ├── replace_docx_diagrams.py    # Script tự động cập nhật sơ đồ mới vào file Word báo cáo
│   ├── generate_full_100p_word_report.py # Script xây dựng báo cáo đồ án Word 100 trang
│   ├── requirements.txt            # Danh sách thư viện Python
│   ├── .env.example                # File mẫu cấu hình biến môi trường
│   ├── models/                     # Các mô hình thực thể CSDL (SQLAlchemy ORM)
│   │   ├── __init__.py
│   │   ├── user.py                 # Thực thể User & UserRole (ADMIN, LIBRARIAN, READER)
│   │   ├── reader.py               # Thực thể Reader, ReaderType & CardStatus
│   │   ├── book.py                 # Thực thể Book, Category, Author
│   │   ├── borrow.py               # Thực thể BorrowRecord & Reservation
│   │   └── fine.py                 # Thực thể Fine & FineStatus
│   ├── routers/                    # 7 API Routers độc lập
│   │   ├── auth.py                 # Xác thực, đăng ký, đăng nhập & quản lý Users
│   │   ├── books.py                # Quản lý kho sách, danh mục, tác giả, export CSV
│   │   ├── readers.py              # Quản lý độc giả, cấp thẻ, next-code, available-users
│   │   ├── borrows.py              # Lập phiếu mượn, trả sách, gia hạn, thu phạt
│   │   ├── reservations.py         # Quản lý hàng đợi đặt trước sách FIFO
│   │   ├── statistics.py           # Dashboard KPI, báo cáo quá hạn, xuất CSV UTF-8
│   │   ├── ai.py                   # Chatbot tra cứu, tóm tắt sách, gợi ý cá nhân hóa
│   │   └── backup.py               # API tạo và tải bản sao lưu CSDL (.sql/.db)
│   ├── services/                   # Business Logic & Dịch vụ chuyên biệt
│   │   ├── borrow_service.py       # Nghiệp vụ lưu thông mượn trả & tính phạt
│   │   ├── ai_service.py           # Điều phối Gemini 1.5 Flash Cloud & Mock Fallback
│   │   └── fts_service.py          # Đồng bộ và tìm kiếm toàn văn SQLite FTS5 BM25
│   ├── prompts/                    # Bộ Prompt Templates chuẩn hóa
│   │   ├── search_prompt.py        # Template tra cứu sách có ràng buộc Zero-Hallucination
│   │   ├── summary_prompt.py       # Template tóm tắt nội dung & mục lục tác phẩm
│   │   └── suggest_prompt.py       # Template phân tích sở thích & gợi ý theo gu đọc
│   └── report_sections/            # Các module nội dung báo cáo đồ án chuyên sâu 100 trang
├── frontend/                       # Mã nguồn Giao diện Người dùng (Presentation Layer)
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css            # Toàn bộ Design System Modern Glassmorphism & White theme
│   │   └── js/
│   │       ├── api.js              # Module quản lý gọi Fetch RESTful API
│   │       └── ui.js               # Tiện ích UI (Toast notifications, Modal, Badge, Formatters)
│   └── templates/                  # Giao diện HTML5 cho các phân hệ
│       ├── login.html              # Trang đăng nhập 2 cột hiện đại kèm Demo Accounts
│       ├── dashboard.html          # Trang Dashboard tổng quan KPI & biểu đồ Chart.js
│       ├── books/
│       │   └── index.html          # Quản lý kho sách, thêm/sửa/xóa, bộ lọc đa năng, xuất CSV
│       ├── readers/
│       │   └── index.html          # Quản lý độc giả & cấp thẻ thông minh (modal tạo mới/chọn user)
│       ├── borrows/
│       │   └── index.html          # Quản lý mượn/trả, gia hạn +7 ngày, thu/miễn phạt quá hạn
│       ├── reservations/
│       │   └── index.html          # Quản lý hàng đợi đặt trước sách FIFO
│       ├── statistics/
│       │   └── index.html          # Báo cáo thống kê chuyên sâu & xuất dữ liệu UTF-8
│       ├── users/
│       │   └── index.html          # Quản trị tài khoản & phân quyền RBAC (dành cho Admin)
│       └── ai/
│           └── chatbot.html        # Khung Chatbot AI thông minh với Thẻ sách tương tác
├── docs/                           # Tài liệu kỹ thuật, sơ đồ UML & Báo cáo đồ án
│   ├── diagrams/                   # Bộ 18 sơ đồ kỹ thuật UML & Architecture chất lượng cao
│   ├── screenshots/                # Ảnh chụp màn hình giao diện web thực tế
│   └── Bao_Cao_Do_An_Quan_Ly_Thu_Vien_AI_100Trang.docx # Báo cáo đồ án toàn diện 100 trang
├── tests/                          # Bộ kiểm thử tự động 26+ Test Cases Pytest
│   ├── test_borrow.py              # Kiểm thử nghiệp vụ mượn, trả, phạt trễ hạn, gia hạn
│   ├── test_ai.py                  # Kiểm thử phân hệ AI, Prompting, Guardrails & Fallback
│   └── conftest.py                 # Cấu hình test fixtures & CSDL in-memory test
├── Dockerfile                      # Dockerfile đóng gói ứng dụng
├── docker-compose.yml              # Cấu hình khởi chạy nhanh đa container
├── pytest.ini                      # Cấu hình thực thi Pytest
└── README.md                       # Tài liệu hướng dẫn toàn diện dự án
```

---

## 🚀 6. Hướng Dẫn Cài Đặt & Khởi Chạy Dự Án

### 6.1. Yêu Cầu Môi Trường
- **Python:** Phiên bản 3.10 trở lên.
- **Hệ điều hành:** Windows 10/11, macOS hoặc Linux.
- **Trình duyệt:** Chrome, Edge, Firefox, Safari phiên bản mới nhất.

### 6.2. Các Bước Cài Đặt & Chạy Trực Tiếp (Khuyến Nghị)

#### Bước 1: Clone kho lưu trữ về máy tính
```bash
git clone https://github.com/dtc245090061-bot/library-management.git
cd library-management
```

#### Bước 2: Tạo môi trường ảo và cài đặt thư viện
```bash
# Tạo môi trường ảo Python
python -m venv venv

# Kích hoạt môi trường ảo:
# Trên Windows:
.\venv\Scripts\activate
# Trên macOS / Linux:
source venv/bin/activate

# Cài đặt toàn bộ dependencies
cd backend
pip install -r requirements.txt
```

#### Bước 3: Cấu hình biến môi trường
Tạo file `.env` từ file mẫu `.env.example`:
```bash
# Trên Windows:
copy .env.example .env

# Trên macOS / Linux:
cp .env.example .env
```

Nội dung cấu hình trong file `backend/.env`:
```ini
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./library.db

# API Key Google Gemini (Tùy chọn - Hệ thống tự động chuyển sang Mock AI nếu không có Key)
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash

# Cấu hình nghiệp vụ thư viện
FINE_PER_DAY=2000
DEFAULT_BORROW_DAYS=14
RENEW_DAYS=7
MAX_RENEW_COUNT=1
DEBUG=True
```

*(Lưu ý: Bạn có thể lấy Gemini API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/). Nếu để trống, hệ thống sẽ tự động dùng Mock AI Engine nội bộ rất mượt mà).*

#### Bước 4: Khởi tạo Cơ sở Dữ liệu & Nạp Dữ liệu Mẫu (Seed Data)
```bash
# Đang đứng tại thư mục backend/
python seed_data.py --reset
```
*Lệnh này sẽ tự động khởi tạo 8 bảng CSDL và nạp đầy đủ dữ liệu mẫu gồm 11 Users, 10 Thể loại, 18 Tác giả, 27 Đầu sách, 8 Thẻ độc giả, 15 Phiếu mượn/trả và 3 Đơn đặt trước.*

#### Bước 5: Khởi động Máy chủ FastAPI
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

#### Bước 6: Truy cập và Trải nghiệm
- 🌐 **Giao diện Web:** [http://localhost:8000](http://localhost:8000)
- 📖 **Tài liệu Swagger API:** [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- 📋 **Tài liệu ReDoc:** [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

---

### 6.3. Khởi Chạy Nhanh Bằng Docker & Docker Compose

Nếu máy tính của bạn đã cài đặt Docker Desktop:
```bash
# Tại thư mục gốc library-management/
docker-compose up -d --build

# Kiểm tra log ứng dụng:
docker-compose logs -f

# Truy cập tại: http://localhost:8000
# Dừng ứng dụng:
docker-compose down
```

---

## 🎮 7. Danh Mục Tài Khoản Thử Nghiệm (Demo Accounts)

Hệ thống đã nạp sẵn các tài khoản demo đại diện cho 3 nhóm vai trò người dùng trong hệ thống (Tất cả mật khẩu mặc định là `123456`):

| Nhóm Vai Trò | Tên Đăng Nhập (Username) | Mật Khẩu | Họ và Tên | Quyền Hạn Trong Hệ Thống |
|---|---|---|---|---|
| 🛡️ **Quản Trị Viên (Admin)** | `admin` | `123456` | Nguyễn Hoàng Admin | Toàn quyền hệ thống: Quản lý Users RBAC, phân quyền, cấu hình hệ thống, xem thống kê |
| 👩‍💼 **Thủ Thư (Librarian)** | `thuhu01`<br/>`thuhu02` | `123456` | Nguyễn Thị Hoa<br/>Trần Văn Nam | Quản lý kho sách, quản lý độc giả, lập phiếu mượn/trả, gia hạn, thu phạt, đặt trước, xuất CSV |
| 🎓 **Độc Giả (Reader)** | `docgia01`<br/>`docgia02`<br/>`docgia03` | `123456` | Lê Thị Mai<br/>Phạm Văn Hùng<br/>Hoàng Bích Lan | Tra cứu sách NLU, Chatbot AI, xem gợi ý sách cá nhân hóa, đặt trước sách, xem lịch sử mượn |

---

## 🧪 8. Kiểm Thử Hệ Thống (Automated Testing)

Dự án tích hợp bộ kiểm thử tự động toàn diện với **26 Test Cases** sử dụng Pytest và HTTPX AsyncClient, kiểm chứng 100% các kịch bản nghiệp vụ và phân hệ AI:

```bash
# Tại thư mục gốc library-management/
pytest tests/ -v
```

Kết quả kiểm thử đạt chuẩn:
```text
tests/test_borrow.py::TestBorrow::test_borrow_book_success PASSED               [  4%]
tests/test_borrow.py::TestBorrow::test_borrow_card_expired PASSED               [  8%]
tests/test_borrow.py::TestBorrow::test_borrow_limit_exceeded PASSED             [ 12%]
tests/test_borrow.py::TestBorrow::test_borrow_has_pending_fine PASSED           [ 15%]
tests/test_borrow.py::TestBorrow::test_borrow_out_of_stock PASSED               [ 19%]
tests/test_borrow.py::TestReturn::test_return_on_time PASSED                    [ 23%]
tests/test_borrow.py::TestReturn::test_return_overdue_with_fine PASSED          [ 27%]
tests/test_borrow.py::TestRenew::test_renew_success PASSED                      [ 31%]
tests/test_borrow.py::TestRenew::test_renew_already_renewed PASSED              [ 35%]
tests/test_borrow.py::TestRenew::test_renew_overdue_blocked PASSED              [ 38%]
tests/test_borrow.py::TestReservation::test_reserve_out_of_stock PASSED        [ 42%]
tests/test_ai.py::TestAISearch::test_search_with_valid_query PASSED             [ 46%]
tests/test_ai.py::TestAISearch::test_search_zero_hallucination PASSED           [ 50%]
tests/test_ai.py::TestAISummary::test_summarize_book PASSED                     [ 54%]
tests/test_ai.py::TestAISuggest::test_suggest_personalized PASSED               [ 58%]
tests/test_ai.py::TestAIFallback::test_mock_fallback_on_network_error PASSED   [ 62%]
...
============================= 26 passed in 3.42s =============================
```

Chạy kiểm thử theo từng phân hệ:
```bash
# Chỉ kiểm thử phân hệ Nghiệp vụ Mượn/Trả/Phạt:
pytest tests/test_borrow.py -v

# Chỉ kiểm thử phân hệ Trí tuệ Nhân tạo AI:
pytest tests/test_ai.py -v
```

---

## 📊 9. Danh Mục API Endpoints Chính

| Phân Hệ | Phương Thức | Endpoint URL | Phân Quyền | Mô Tả Chức Năng |
|---|:---:|---|:---:|---|
| **Xác thực** | `POST` | `/api/auth/login` | Công khai | Đăng nhập hệ thống, trả về JWT Access Token |
| | `POST` | `/api/auth/register` | Công khai | Đăng ký tài khoản người dùng mới |
| | `GET` | `/api/auth/me` | Mọi User | Lấy thông tin tài khoản hiện tại đang đăng nhập |
| | `GET` | `/api/auth/users` | Admin | Lấy danh sách tất cả người dùng trong hệ thống |
| **Kho Sách** | `GET` | `/api/books/` | Mọi User | Tra cứu danh sách sách (hỗ trợ phân trang, lọc theo thể loại, tác giả, FTS5) |
| | `POST` | `/api/books/` | Thủ thư / Admin | Thêm mới một cuốn sách vào kho |
| | `PUT` | `/api/books/{id}` | Thủ thư / Admin | Cập nhật thông tin cuốn sách |
| | `DELETE`| `/api/books/{id}` | Thủ thư / Admin | Xóa bỏ một cuốn sách khỏi kho |
| | `GET` | `/api/books/export/csv`| Thủ thư / Admin | Xuất danh mục toàn bộ kho sách ra file CSV chuẩn UTF-8 |
| **Độc Giả** | `GET` | `/api/readers/` | Thủ thư / Admin | Danh sách hồ sơ độc giả và thẻ thư viện |
| | `POST` | `/api/readers/` | Thủ thư / Admin | Cấp thẻ độc giả mới (hỗ trợ tạo User hoặc chọn User có sẵn) |
| | `GET` | `/api/readers/next-code` | Thủ thư / Admin | Tự động sinh mã thẻ độc giả tiếp theo chưa sử dụng |
| | `GET` | `/api/readers/available-users` | Thủ thư / Admin | Danh sách tài khoản người dùng chưa được cấp thẻ |
| **Mượn / Trả**| `POST` | `/api/borrows/` | Thủ thư / Admin | Lập phiếu mượn sách (kiểm tra 4 điều kiện nghiệp vụ) |
| | `PUT` | `/api/borrows/{id}/return` | Thủ thư / Admin | Tiếp nhận trả sách, hoàn kho và tự động tính tiền phạt trễ hạn |
| | `PUT` | `/api/borrows/{id}/renew` | Độc giả / Thủ thư | Gia hạn thêm 7 ngày (tối đa 1 lần mỗi phiếu) |
| | `GET` | `/api/borrows/export/csv` | Thủ thư / Admin | Xuất danh sách phiếu mượn/trả ra file CSV |
| **Tiền Phạt** | `GET` | `/api/fines/` | Thủ thư / Admin | Danh sách các khoản nợ phạt vi phạm quá hạn |
| | `PUT` | `/api/fines/{id}/pay` | Thủ thư / Admin | Ghi nhận thanh toán đủ tiền phạt (chuyển sang PAID) |
| | `PUT` | `/api/fines/{id}/waive` | Thủ thư / Admin | Miễn giảm khoản phạt chính đáng kèm lý do (WAIVED) |
| **Đặt Trước** | `POST` | `/api/reservations/` | Độc giả / Thủ thư | Tạo yêu cầu đặt trước khi sách hết bản khả dụng (FIFO) |
| | `GET` | `/api/reservations/` | Thủ thư / Admin | Danh sách các yêu cầu xếp hàng đặt trước |
| **Trợ Lý AI** | `POST` | `/api/ai/search` | Mọi User | Chatbot tra cứu sách bằng ngôn ngữ tự nhiên tiếng Việt |
| | `POST` | `/api/ai/summarize/{id}` | Mọi User | AI tóm tắt nội dung và mục lục cuốn sách |
| | `GET` | `/api/ai/suggest` | Độc giả / Thủ thư | AI phân tích gu đọc và gợi ý bộ sưu tập sách cá nhân hóa |
| **Thống Kê** | `GET` | `/api/statistics/dashboard` | Thủ thư / Admin | Thống kê số liệu KPI tổng quan thời gian thực |
| | `GET` | `/api/statistics/export/csv` | Thủ thư / Admin | Xuất báo cáo tổng kết thống kê ra file CSV UTF-8 |

---

## 🔒 10. Tiêu Chuẩn Bảo Mật & Đạo Đức AI

1. **Bảo mật Dữ liệu & Danh tính:**
   - Sử dụng thuật toán băm mật khẩu chuẩn công nghiệp **Bcrypt** với Salt ngẫu nhiên.
   - Cơ chế ủy quyền phiên làm việc bằng **JWT Access Token (HS256)** có thời hạn hết hạn 60 phút.
   - Phân định quyền hạn chặt chẽ theo mô hình **RBAC (Role-Based Access Control)** tại tầng API Dependency.
2. **Nguyên tắc Privacy-by-Design trong AI:**
   - 100% thông tin định danh cá nhân của bạn đọc (Họ tên, Email, SĐT, Địa chỉ) được **khử định danh (Scrubbed)** trước khi chuyển tiếp dữ liệu đến Cloud AI Model.
   - Dịch vụ AI chỉ tiếp nhận dữ liệu kỹ thuật về danh mục sách (Tiêu đề, Thể loại, Tác giả).
3. **Kiểm soát Ảo giác (Zero-Hallucination Guardrails):**
   - Áp dụng kỹ thuật Grounded In-Context Prompting buộc mô hình chỉ được phép đưa ra lời giải thích và gợi ý dựa trên tập sách đang thực sự có sẵn trong CSDL thư viện.

---

## 👥 11. Thông Tin Tác Giả & Đồ Án

- **Học phần:** Ứng dụng Trí tuệ Nhân tạo trong Phát triển Phần mềm
- **Đề tài:** Hệ thống Quản lý Thư viện có Tích hợp Trí tuệ Nhân tạo (Smart Library Management System)
- **Công nghệ chính:** Python, FastAPI, SQLAlchemy, SQLite FTS5, Google Gemini AI, Vanilla HTML5/CSS/JS Glassmorphism.
- **Năm thực hiện:** 2026 - 2027

---
*Phát triển với sự tâm huyết và chỉn chu vì một nền tảng thư viện đại học số thông minh, an toàn và tiện ích.*
