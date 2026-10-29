"""
Seed data - Tạo dữ liệu mẫu phong phú và toàn diện cho Thư viện thông minh
Bao gồm:
- Users & Readers (Admin, Thủ thư, Độc giả Sinh viên/Giảng viên/Nhân viên)
- Categories (Đa dạng 10 thể loại)
- Authors (15 tác giả nổi tiếng trong và ngoài nước)
- Books (30+ cuốn sách thực tế với mô tả chi tiết, đầy đủ mã sách, NXB, ISBN)
- BorrowRecords (Đang mượn, đã trả, quá hạn, đã gia hạn)
- Fines (Phiếu phạt quá hạn đã trả và chưa trả)
- Reservations (Đặt trước sách đang chờ và hoàn tất)
"""
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import random
import string
from datetime import date, datetime, timedelta, timezone
from sqlalchemy.orm import Session

# Thêm backend vào path nếu chạy độc lập
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine, Base
from auth_utils import get_password_hash as _gph
from models import (
    User, UserRole,
    Category, Author, Book,
    Reader, ReaderType, CardStatus,
    BorrowRecord, BorrowStatus,
    Reservation, ReservationStatus,
    Fine, FineStatus
)


def get_password_hash(pwd: str) -> str:
    return _gph(pwd[:72])


def seed_database(force_reset: bool = False):
    """Tạo toàn bộ dữ liệu mẫu"""
    db = SessionLocal()
    try:
        # Nếu force_reset, xóa hết dữ liệu cũ
        if force_reset:
            print("🔄 Đang làm mới cơ sở dữ liệu...")
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
        elif db.query(User).count() > 0:
            print("✅ Dữ liệu đã tồn tại trong CSDL. Chạy với --reset nếu muốn nạp lại.")
            return

        print("🌱 Đang khởi tạo dữ liệu mẫu thư viện...")

        # =========================================================================
        # 1. USERS & ACCOUNTS
        # =========================================================================
        users_data = [
            # Quản trị viên
            {"username": "admin", "email": "admin@library.edu.vn", "password": "Admin@123",
             "full_name": "Nguyễn Hoàng Admin", "role": UserRole.ADMIN},
            # Thủ thư
            {"username": "thuhu01", "email": "thuhu01@library.edu.vn", "password": "Thuhu@123",
             "full_name": "Nguyễn Thị Hoa (Thủ thư chính)", "role": UserRole.LIBRARIAN},
            {"username": "thuhu02", "email": "thuhu02@library.edu.vn", "password": "Thuhu@123",
             "full_name": "Trần Văn Nam (Thủ thư ca 2)", "role": UserRole.LIBRARIAN},
            # Độc giả sinh viên
            {"username": "docgia01", "email": "maile@student.edu.vn", "password": "Docgia@123",
             "full_name": "Lê Thị Mai", "role": UserRole.READER},
            {"username": "docgia02", "email": "hungpham@student.edu.vn", "password": "Docgia@123",
             "full_name": "Phạm Văn Hùng", "role": UserRole.READER},
            {"username": "docgia03", "email": "lanhoang@student.edu.vn", "password": "Docgia@123",
             "full_name": "Hoàng Thị Lan", "role": UserRole.READER},
            {"username": "docgia04", "email": "tuanvu@student.edu.vn", "password": "Docgia@123",
             "full_name": "Vũ Minh Tuấn", "role": UserRole.READER},
            {"username": "docgia05", "email": "hangdo@student.edu.vn", "password": "Docgia@123",
             "full_name": "Đỗ Thanh Hằng", "role": UserRole.READER},
            # Độc giả giảng viên & nhân viên
            {"username": "docgia06", "email": "nguyenvana@teacher.edu.vn", "password": "Docgia@123",
             "full_name": "PGS.TS Nguyễn Văn An", "role": UserRole.READER},
            {"username": "docgia07", "email": "tranthib@teacher.edu.vn", "password": "Docgia@123",
             "full_name": "TS. Trần Thị Bình", "role": UserRole.READER},
            {"username": "docgia08", "email": "buiquochung@staff.edu.vn", "password": "Docgia@123",
             "full_name": "Bùi Quốc Hùng (Nghiên cứu viên)", "role": UserRole.READER},
        ]

        user_objects = []
        for ud in users_data:
            u = User(
                username=ud["username"],
                email=ud["email"],
                hashed_password=get_password_hash(ud["password"]),
                full_name=ud["full_name"],
                role=ud["role"],
                is_active=True
            )
            db.add(u)
            user_objects.append(u)
        db.commit()
        for u in user_objects:
            db.refresh(u)

        user_map = {u.username: u for u in user_objects}

        # =========================================================================
        # 2. CATEGORIES
        # =========================================================================
        categories_data = [
            {"name": "Trí tuệ nhân tạo & Học máy", "description": "Machine Learning, Deep Learning, Generative AI, LLMs, NLP, Computer Vision"},
            {"name": "Công nghệ thông tin & Lập trình", "description": "Python, JavaScript, Go, Rust, Web Fullstack, DevOps, Microservices"},
            {"name": "Khoa học Dữ liệu & Toán ứng dụng", "description": "Data Analytics, Big Data, Đại số tuyến tính, Xác suất thống kê"},
            {"name": "An toàn thông tin & Mạng máy tính", "description": "Cybersecurity, Mạng viễn thông, Mã hóa mật mã học, Penetration Testing"},
            {"name": "Kinh tế & Khởi nghiệp", "description": "Kinh tế học, Quản trị kinh doanh, Tài chính doanh nghiệp, Đầu tư, Khởi nghiệp tinh gọn"},
            {"name": "Văn học Việt Nam & Thế giới", "description": "Tiểu thuyết, tác phẩm kinh điển, thơ ca, văn học hiện đại và kinh điển"},
            {"name": "Kỹ năng sống & Phát triển bản thân", "description": "Tư duy phản biện, giao tiếp đắc nhân tâm, quản lý thời gian, lãnh đạo"},
            {"name": "Lịch sử & Triết học", "description": "Lịch sử thế giới, lịch sử Việt Nam, triết học ứng dụng, văn minh nhân loại"},
            {"name": "Ngoại ngữ & Luyện thi", "description": "Tiếng Anh IELTS/TOEIC, Tiếng Nhật JLPT, Tiếng Trung HSK"},
            {"name": "Khoa học Tự nhiên & Vũ trụ", "description": "Vật lý thiên văn, sinh học hiện đại, khoa học vũ trụ, cơ học lượng tử"},
        ]

        cat_objects = []
        for cd in categories_data:
            c = Category(**cd)
            db.add(c)
            cat_objects.append(c)
        db.commit()
        for c in cat_objects:
            db.refresh(c)

        cat_map = {c.name: c for c in cat_objects}

        # =========================================================================
        # 3. AUTHORS
        # =========================================================================
        authors_data = [
            {"name": "Stuart Russell & Peter Norvig", "bio": "Các giáo sư hàng đầu thế giới về Trí tuệ nhân tạo tại UC Berkeley và Stanford"},
            {"name": "Andrew Ng", "bio": "Đồng sáng lập Coursera, Giáo sư Đại học Stanford, người tiên phong trong giáo dục AI"},
            {"name": "Robert C. Martin (Uncle Bob)", "bio": "Huyền thoại ngành công nghệ phần mềm, tác giả nguyên lý Clean Code và SOLID"},
            {"name": "Martin Fowler", "bio": "Chuyên gia kiến trúc phần mềm, tác giả sách Refactoring và Microservices"},
            {"name": "François Chollet", "bio": "Tác giả thư viện Keras, chuyên gia nghiên cứu AI tại Google"},
            {"name": "Nguyễn Văn An", "bio": "Giảng viên CNTT & Khoa học Máy tính, ĐH Bách Khoa"},
            {"name": "Trần Thị Bình", "bio": "Tiến sĩ Khoa học Dữ liệu và Trí tuệ Nhân tạo"},
            {"name": "Stephen R. Covey", "bio": "Tác giả nổi tiếng thế giới về phát triển kỹ năng lãnh đạo cá nhân"},
            {"name": "Yuval Noah Harari", "bio": "Nhà sử học, triết gia, tác giả bộ ba Sapiens - Homo Deus - 21 bài học"},
            {"name": "Dale Carnegie", "bio": "Bậc thầy về nghệ thuật giao tiếp và đắc nhân tâm"},
            {"name": "Nguyễn Du", "bio": "Đại thi hào dân tộc Việt Nam, Danh nhân văn hóa thế giới"},
            {"name": "Nam Cao", "bio": "Nhà văn hiện thực xuất sắc của văn học Việt Nam thế kỷ 20"},
            {"name": "Vũ Trọng Phụng", "bio": "Nhà văn trào phúng bậc thầy của nền văn học hiện thực Việt Nam"},
            {"name": "Eric Ries", "bio": "Doanh nhân và tác giả phương pháp Khởi nghiệp Tinh gọn (The Lean Startup)"},
            {"name": "Stephen Hawking", "bio": "Nhà vật lý lý thuyết, vũ trụ học thiên tài người Anh"},
            {"name": "Phạm Minh Đức", "bio": "Tiến sĩ Toán học ứng dụng và Thống kê giải tích"},
            {"name": "Bùi Quốc Hùng", "bio": "Giảng viên Kinh tế, ĐH Kinh tế Quốc dân"},
            {"name": "Ngô Thị Hà", "bio": "Chuyên gia đào tạo kỹ năng mềm và tâm lý học ứng dụng"},
        ]

        author_objects = []
        for ad in authors_data:
            a = Author(**ad)
            db.add(a)
            author_objects.append(a)
        db.commit()
        for a in author_objects:
            db.refresh(a)

        author_map = {a.name: a for a in author_objects}

        # =========================================================================
        # 4. BOOKS (30+ Cuốn sách phong phú)
        # =========================================================================
        books_data = [
            # --- AI & Học máy ---
            {
                "code": "AI001",
                "title": "Artificial Intelligence: A Modern Approach (4th Edition)",
                "author": "Stuart Russell & Peter Norvig",
                "category": "Trí tuệ nhân tạo & Học máy",
                "publisher": "Pearson",
                "year": 2021,
                "qty": 5,
                "isbn": "978-0134685991",
                "desc": "Cuốn giáo trình kinh điển và toàn diện nhất về Trí tuệ Nhân tạo trên thế giới. Nội dung bao quát từ thuật toán tìm kiếm A*, Logic mờ, Mạng Bayes, Học máy, Học sâu (Deep Learning), Xử lý ngôn ngữ tự nhiên (NLP) cho đến Đạo đức và Tương lai của AI."
            },
            {
                "code": "AI002",
                "title": "Machine Learning Yearning: Cẩm nang triển khai Học máy",
                "author": "Andrew Ng",
                "category": "Trí tuệ nhân tạo & Học máy",
                "publisher": "NXB Thông tin và Truyền thông",
                "year": 2022,
                "qty": 6,
                "isbn": "978-6048041231",
                "desc": "Hướng dẫn thực chiến từ Giáo sư Andrew Ng về cách xây dựng, đánh giá và tối ưu hóa hệ thống Machine Learning trong thực tế. Giúp giải quyết các bài toán về Train/Dev/Test set, chẩn đoán Overfitting/Underfitting và chuyển giao tri thức."
            },
            {
                "code": "AI003",
                "title": "Deep Learning với Python và Keras",
                "author": "François Chollet",
                "category": "Trí tuệ nhân tạo & Học máy",
                "publisher": "NXB Khoa học Kỹ thuật",
                "year": 2023,
                "qty": 4,
                "isbn": "978-6046718902",
                "desc": "Được viết bởi chính tác giả thư viện Keras, cuốn sách hướng dẫn chi tiết cách xây dựng các mô hình Học sâu: CNN cho thị giác máy tính, RNN & Transformer cho xử lý văn bản, GANs và Diffusion models cho tạo sinh hình ảnh."
            },
            {
                "code": "AI004",
                "title": "Kỹ thuật Prompt Engineering và Generative AI",
                "author": "Trần Thị Bình",
                "category": "Trí tuệ nhân tạo & Học máy",
                "publisher": "NXB Khoa học Kỹ thuật",
                "year": 2024,
                "qty": 7,
                "isbn": "978-6046723451",
                "desc": "Nắm vững nghệ thuật và khoa học điều khiển các mô hình ngôn ngữ lớn (LLMs như Gemini, GPT, Claude). Bao gồm Zero-shot, Few-shot, Chain-of-Thought, ReAct framework, RAG (Retrieval Augmented Generation) và AI Agents tự động."
            },
            {
                "code": "AI005",
                "title": "Nhập môn Thị giác Máy tính và Xử lý Ảnh",
                "author": "Nguyễn Văn An",
                "category": "Trí tuệ nhân tạo & Học máy",
                "publisher": "NXB Đại học Quốc gia",
                "year": 2023,
                "qty": 4,
                "isbn": "978-6046728893",
                "desc": "Lý thuyết và thực hành xử lý ảnh số với OpenCV, nhận diện khuôn mặt, phân vùng ảnh (Segmentation), phát hiện đối tượng với YOLO và mô hình thị giác hiện đại."
            },

            # --- Lập trình & CNTT ---
            {
                "code": "CS001",
                "title": "Clean Code: Mã sạch - Nghệ thuật viết mã chuyên nghiệp",
                "author": "Robert C. Martin (Uncle Bob)",
                "category": "Công nghệ thông tin & Lập trình",
                "publisher": "NXB Lao động",
                "year": 2020,
                "qty": 8,
                "isbn": "978-0132350884",
                "desc": "Cuốn sách gối đầu giường của mọi lập trình viên. Hướng dẫn các quy tắc vàng trong đặt tên biến, viết hàm đơn nhiệm, xử lý lỗi, viết unit test và kỹ thuật tái cấu trúc mã nguồn (Refactoring) để biến code xấu thành code đẹp."
            },
            {
                "code": "CS002",
                "title": "Clean Architecture: Kiến trúc phần mềm chuẩn mực",
                "author": "Robert C. Martin (Uncle Bob)",
                "category": "Công nghệ thông tin & Lập trình",
                "publisher": "NXB Lao động",
                "year": 2021,
                "qty": 5,
                "isbn": "978-0134494166",
                "desc": "Bộ quy tắc thiết kế hệ thống phần mềm độc lập với UI, CSDL và framework bên ngoài. Phân tích sâu sắc các nguyên lý SOLID, ranh giới kiến trúc và thiết kế hướng đối tượng."
            },
            {
                "code": "CS003",
                "title": "Refactoring: Cải tiến cấu trúc mã nguồn hiện có",
                "author": "Martin Fowler",
                "category": "Công nghệ thông tin & Lập trình",
                "publisher": "NXB Thông tin và Truyền thông",
                "year": 2021,
                "qty": 4,
                "isbn": "978-0134757599",
                "desc": "Phương pháp từng bước cải tiến thiết kế của mã nguồn cũ mà không thay đổi hành vi bên ngoài, giúp hệ thống luôn dễ bảo trì, mở rộng và giảm nợ kỹ thuật (Technical Debt)."
            },
            {
                "code": "CS004",
                "title": "Lập trình Python từ Cơ bản đến Nâng cao",
                "author": "Nguyễn Văn An",
                "category": "Công nghệ thông tin & Lập trình",
                "publisher": "NXB Thanh niên",
                "year": 2023,
                "qty": 10,
                "isbn": "978-6046714562",
                "desc": "Giáo trình toàn diện về Python: cú pháp cơ bản, OOP, decorators, generators, lập trình bất đồng bộ (asyncio), làm việc với CSDL và xây dựng RESTful API với FastAPI."
            },
            {
                "code": "CS005",
                "title": "Cấu trúc Dữ liệu và Giải thuật Kinh điển",
                "author": "Phạm Minh Đức",
                "category": "Công nghệ thông tin & Lập trình",
                "publisher": "NXB Giáo dục",
                "year": 2022,
                "qty": 8,
                "isbn": "978-6046719876",
                "desc": "Phân tích độ phức tạp thuật toán O(n), cấu trúc dữ liệu mảng, danh sách liên kết, ngăn xếp (Stack), hàng đợi (Queue), Cây nhị phân (Binary Trees), Đồ thị (Graphs) và Quy hoạch động."
            },
            {
                "code": "CS006",
                "title": "Xây dựng Web hiện đại với FastAPI và React",
                "author": "Trần Thị Bình",
                "category": "Công nghệ thông tin & Lập trình",
                "publisher": "NXB Khoa học Kỹ thuật",
                "year": 2024,
                "qty": 6,
                "isbn": "978-6046726789",
                "desc": "Hướng dẫn thực chiến xây dựng ứng dụng web Fullstack hiện đại. Backend sử dụng Python FastAPI, Pydantic, SQLAlchemy; Frontend sử dụng React/Vue, TailwindCSS và Docker containerization."
            },

            # --- Khoa học Dữ liệu & Toán ---
            {
                "code": "DS001",
                "title": "Python for Data Analysis & Pandas",
                "author": "Trần Thị Bình",
                "category": "Khoa học Dữ liệu & Toán ứng dụng",
                "publisher": "NXB Thanh niên",
                "year": 2022,
                "qty": 6,
                "isbn": "978-1491957660",
                "desc": "Hướng dẫn toàn diện về xử lý, làm sạch và phân tích dữ liệu dạng bảng với NumPy, Pandas, Matplotlib và Seaborn."
            },
            {
                "code": "MA001",
                "title": "Đại số Tuyến tính cho Trí tuệ Nhân tạo",
                "author": "Phạm Minh Đức",
                "category": "Khoa học Dữ liệu & Toán ứng dụng",
                "publisher": "NXB Đại học Quốc gia",
                "year": 2021,
                "qty": 5,
                "isbn": "978-6046721112",
                "desc": "Không gian vector, ma trận, định thức, phép phân rã SVD (Singular Value Decomposition), PCA và ứng dụng trực tiếp trong giải thuật Machine Learning."
            },
            {
                "code": "MA002",
                "title": "Xác suất Thống kê ứng dụng trong Khoa học Máy tính",
                "author": "Phạm Minh Đức",
                "category": "Khoa học Dữ liệu & Toán ứng dụng",
                "publisher": "NXB Giáo dục",
                "year": 2022,
                "qty": 7,
                "isbn": "978-6046722223",
                "desc": "Lý thuyết xác suất, biến ngẫu nhiên, các hàm phân phối phổ biến (Gaussian, Poisson, Bernoulli), kiểm định giả thuyết và ước lượng tham số."
            },

            # --- An toàn thông tin & Mạng ---
            {
                "code": "SEC001",
                "title": "An toàn Thông tin và Phòng thủ Mạng",
                "author": "Nguyễn Văn An",
                "category": "An toàn thông tin & Mạng máy tính",
                "publisher": "NXB Thông tin và Truyền thông",
                "year": 2023,
                "qty": 4,
                "isbn": "978-6046733334",
                "desc": "Nguyên lý bảo mật mạng, mật mã học cổ điển và hiện đại (RSA, AES, ECC), chữ ký số, chứng chỉ SSL/TLS, tường lửa và phát hiện xâm nhập IDS/IPS."
            },

            # --- Kinh tế & Khởi nghiệp ---
            {
                "code": "EC001",
                "title": "The Lean Startup: Khởi nghiệp Tinh gọn",
                "author": "Eric Ries",
                "category": "Kinh tế & Khởi nghiệp",
                "publisher": "NXB Trẻ",
                "year": 2020,
                "qty": 6,
                "isbn": "978-0307887894",
                "desc": "Mô hình khởi nghiệp đột phá dựa trên chu trình Xây dựng - Đo lường - Học hỏi (Build - Measure - Learn) và sản phẩm khả dụng tối thiểu (MVP) giúp giảm thiểu rủi ro."
            },
            {
                "code": "EC002",
                "title": "Kinh tế học Vi mô và Vĩ mô Căn bản",
                "author": "Bùi Quốc Hùng",
                "category": "Kinh tế & Khởi nghiệp",
                "publisher": "NXB Kinh tế Quốc dân",
                "year": 2022,
                "qty": 5,
                "isbn": "978-6046744445",
                "desc": "Phân tích các quy luật cung cầu, hành vi người tiêu dùng, cấu trúc thị trường cạnh tranh, lạm phát, lãi suất và chính sách tiền tệ tài khóa."
            },

            # --- Văn học Việt Nam & Thế giới ---
            {
                "code": "LT001",
                "title": "Truyện Kiều (Khảo cứu và Chú giải)",
                "author": "Nguyễn Du",
                "category": "Văn học Việt Nam & Thế giới",
                "publisher": "NXB Văn học",
                "year": 2019,
                "qty": 10,
                "isbn": "978-6046755556",
                "desc": "Kiệt tác bất hủ của đại thi hào Nguyễn Du viết bằng thể thơ lục bát, phản ánh số phận đau thương của nàng Thúy Kiều và bức tranh xã hội phong kiến đầy biến động."
            },
            {
                "code": "LT002",
                "title": "Chí Phèo và Tuyển tập Truyện ngắn Hiện thực",
                "author": "Nam Cao",
                "category": "Văn học Việt Nam & Thế giới",
                "publisher": "NXB Văn học",
                "year": 2020,
                "qty": 7,
                "isbn": "978-6046766667",
                "desc": "Tuyển tập những tác phẩm đỉnh cao của Nam Cao: Chí Phèo, Lão Hạc, Đời Thừa, Giăng Sáng... khắc họa sâu sắc bi kịch bị tha hóa của người nông dân và nỗi đau của người trí thức nghèo."
            },
            {
                "code": "LT003",
                "title": "Số Đỏ (Tiểu thuyết Trào phúng)",
                "author": "Vũ Trọng Phụng",
                "category": "Văn học Việt Nam & Thế giới",
                "publisher": "NXB Văn học",
                "year": 2019,
                "qty": 6,
                "isbn": "978-6046777778",
                "desc": "Tác phẩm trào phúng kinh điển với nhân vật trung tâm Xuân Tóc Đỏ, vạch trần thói học đòi âu hóa lố lăng và sự suy đồi đạo đức của xã hội thành thị đương thời."
            },

            # --- Kỹ năng sống & Phát triển bản thân ---
            {
                "code": "SK001",
                "title": "Đắc Nhân Tâm (How to Win Friends and Influence People)",
                "author": "Dale Carnegie",
                "category": "Kỹ năng sống & Phát triển bản thân",
                "publisher": "NXB Tổng hợp TP.HCM",
                "year": 2022,
                "qty": 12,
                "isbn": "978-6046788889",
                "desc": "Cuốn sách nghệ thuật giao tiếp và thu phục lòng người bán chạy nhất mọi thời đại. Đưa ra các nguyên tắc đối nhân xử thế tinh tế, chân thành để gặt hái thành công và hạnh phúc."
            },
            {
                "code": "SK002",
                "title": "7 Thói quen để Thành đạt (The 7 Habits of Highly Effective People)",
                "author": "Stephen R. Covey",
                "category": "Kỹ năng sống & Phát triển bản thân",
                "publisher": "NXB Trẻ",
                "year": 2021,
                "qty": 8,
                "isbn": "978-0743269513",
                "desc": "Khung tư duy phát triển bản thân từ gốc rễ nhân cách: Luôn chủ động, Bắt đầu bằng đích đến, Ưu tiên điều quan trọng nhất, Tư duy cùng thắng và Rèn giũa bản thân."
            },
            {
                "code": "SK003",
                "title": "Tư duy Nhanh và Chậm (Thinking, Fast and Slow)",
                "author": "Dale Carnegie",
                "category": "Kỹ năng sống & Phát triển bản thân",
                "publisher": "NXB Thế giới",
                "year": 2021,
                "qty": 5,
                "isbn": "978-6046799990",
                "desc": "Khám phá hai hệ thống chi phối tư duy con người: Hệ thống 1 (nhanh, trực giác, cảm tính) và Hệ thống 2 (chậm, logic, cân nhắc), giúp bạn đưa ra những quyết định sáng suốt hơn."
            },

            # --- Lịch sử & Triết học ---
            {
                "code": "HI001",
                "title": "Sapiens: Lược sử Loài người",
                "author": "Yuval Noah Harari",
                "category": "Lịch sử & Triết học",
                "publisher": "NXB Thế giới",
                "year": 2020,
                "qty": 8,
                "isbn": "978-6047743210",
                "desc": "Tác phẩm lịch sử chấn động thế giới khám phá 70.000 năm tiến hóa của loài người qua ba cuộc cách mạng lớn: Cách mạng Nhận thức, Cách mạng Nông nghiệp và Cách mạng Khoa học."
            },
            {
                "code": "HI002",
                "title": "Homo Deus: Lược sử Tương lai",
                "author": "Yuval Noah Harari",
                "category": "Lịch sử & Triết học",
                "publisher": "NXB Thế giới",
                "year": 2021,
                "qty": 6,
                "isbn": "978-6047743227",
                "desc": "Cái nhìn đầy thách thức về thế kỷ 21 khi nhân loại đối mặt với Trí tuệ Nhân tạo, Công nghệ Sinh học và nguy cơ biến đổi thành giống loài thần thánh hoặc bị thay thế."
            },

            # --- Khoa học Tự nhiên & Vũ trụ ---
            {
                "code": "SCI001",
                "title": "Lược sử Thời gian (A Brief History of Time)",
                "author": "Stephen Hawking",
                "category": "Khoa học Tự nhiên & Vũ trụ",
                "publisher": "NXB Trẻ",
                "year": 2020,
                "qty": 6,
                "isbn": "978-6041123456",
                "desc": "Cuốn sách vật lý thiên văn kinh điển giải thích những bí ẩn lớn nhất của vũ trụ: Vụ nổ Big Bang, Lỗ đen vũ trụ, Thuyết tương đối của Einstein và Bản chất của thời gian."
            },
            {
                "code": "SCI002",
                "title": "Vũ trụ trong Vỏ hạt dẻ",
                "author": "Stephen Hawking",
                "category": "Khoa học Tự nhiên & Vũ trụ",
                "publisher": "NXB Trẻ",
                "year": 2021,
                "qty": 4,
                "isbn": "978-6041123470",
                "desc": "Khám phá các biên giới mới nhất của vật lý lý thuyết: Thuyết M, không gian 11 chiều, du hành thời gian và sự hòa hợp giữa Cơ học lượng tử và Thuyết tương đối rộng."
            }
        ]

        book_objects = []
        for bd in books_data:
            b = Book(
                code=bd["code"],
                title=bd["title"],
                author_id=author_map[bd["author"]].id,
                category_id=cat_map[bd["category"]].id,
                publisher=bd["publisher"],
                publish_year=bd["year"],
                total_quantity=bd["qty"],
                available_quantity=bd["qty"],
                isbn=bd.get("isbn"),
                description=bd.get("desc")
            )
            db.add(b)
            book_objects.append(b)
        db.commit()
        for b in book_objects:
            db.refresh(b)

        book_map = {b.code: b for b in book_objects}

        # =========================================================================
        # 5. READERS (Thẻ độc giả)
        # =========================================================================
        reader_configs = [
            {"username": "docgia01", "code": "DG2024001", "type": ReaderType.STUDENT, "phone": "0981234561", "address": "KTX Khu A, ĐHQG"},
            {"username": "docgia02", "code": "DG2024002", "type": ReaderType.STUDENT, "phone": "0981234562", "address": "KTX Khu B, ĐHQG"},
            {"username": "docgia03", "code": "DG2024003", "type": ReaderType.STUDENT, "phone": "0981234563", "address": "123 Cầu Giấy, Hà Nội"},
            {"username": "docgia04", "code": "DG2024004", "type": ReaderType.STUDENT, "phone": "0981234564", "address": "456 Hai Bà Trưng, Hà Nội"},
            {"username": "docgia05", "code": "DG2024005", "type": ReaderType.STUDENT, "phone": "0981234565", "address": "789 Nguyễn Trãi, Thanh Xuân"},
            {"username": "docgia06", "code": "DG2024006", "type": ReaderType.TEACHER, "phone": "0912345671", "address": "Khoa CNTT, ĐH Bách Khoa"},
            {"username": "docgia07", "code": "DG2024007", "type": ReaderType.TEACHER, "phone": "0912345672", "address": "Viện Toán học & AI"},
            {"username": "docgia08", "code": "DG2024008", "type": ReaderType.STAFF,   "phone": "0912345673", "address": "Phòng Nghiên cứu Đào tạo"},
        ]

        reader_objects = []
        for rc in reader_configs:
            u = user_map[rc["username"]]
            r = Reader(
                user_id=u.id,
                reader_code=rc["code"],
                phone=rc["phone"],
                address=rc["address"],
                date_of_birth=date(1995 if rc["type"] != ReaderType.STUDENT else 2003, 5, 15),
                reader_type=rc["type"],
                card_status=CardStatus.ACTIVE,
                card_issued_date=date(2024, 1, 1),
                card_expire_date=date(2026, 12, 31),
                max_borrow_books=8 if rc["type"] == ReaderType.TEACHER else 5
            )
            db.add(r)
            reader_objects.append(r)
        db.commit()
        for r in reader_objects:
            db.refresh(r)

        reader_map = {r.reader_code: r for r in reader_objects}
        librarian_id = user_map["thuhu01"].id

        # =========================================================================
        # 6. BORROW RECORDS & FINES (Thực tế, đa dạng)
        # =========================================================================
        # Các kịch bản mượn trả
        borrow_scenarios = [
            # 1. Độc giả 01 (Mai Lê) - Học AI & Lập trình
            {"reader": "DG2024001", "book": "AI001", "days_ago": 25, "duration": 14, "returned": True,  "ret_days": 10}, # Trả đúng hạn
            {"reader": "DG2024001", "book": "CS001", "days_ago": 18, "duration": 14, "returned": True,  "ret_days": 12}, # Trả đúng hạn
            {"reader": "DG2024001", "book": "AI004", "days_ago": 8,  "duration": 14, "returned": False, "renew": 1},      # Đang mượn (đã gia hạn 1 lần)
            {"reader": "DG2024001", "book": "CS004", "days_ago": 3,  "duration": 14, "returned": False, "renew": 0},      # Mới mượn

            # 2. Độc giả 02 (Phạm Hùng) - Quá hạn có phạt
            {"reader": "DG2024002", "book": "CS006", "days_ago": 22, "duration": 14, "returned": False, "renew": 0},     # ĐANG QUÁ HẠN (trễ 8 ngày)
            {"reader": "DG2024002", "book": "AI003", "days_ago": 30, "duration": 14, "returned": True,  "ret_days": 20}, # Đã trả trễ 6 ngày (có tiền phạt)

            # 3. Độc giả 03 (Hoàng Lan) - Kinh tế & Kỹ năng
            {"reader": "DG2024003", "book": "EC001", "days_ago": 15, "duration": 14, "returned": True,  "ret_days": 13}, # Trả đúng hạn
            {"reader": "DG2024003", "book": "SK001", "days_ago": 6,  "duration": 14, "returned": False, "renew": 0},      # Đang mượn
            {"reader": "DG2024003", "book": "SK002", "days_ago": 5,  "duration": 14, "returned": False, "renew": 0},      # Đang mượn

            # 4. Độc giả 04 (Vũ Tuấn) - Lịch sử & Khoa học
            {"reader": "DG2024004", "book": "HI001", "days_ago": 28, "duration": 14, "returned": True,  "ret_days": 14}, # Trả đúng hạn
            {"reader": "DG2024004", "book": "SCI001", "days_ago": 12, "duration": 14, "returned": False, "renew": 0},    # Đang mượn
            {"reader": "DG2024004", "book": "HI002", "days_ago": 20, "duration": 14, "returned": False, "renew": 0},    # ĐANG QUÁ HẠN (trễ 6 ngày)

            # 5. Độc giả 06 (Thầy An) - Giảng viên
            {"reader": "DG2024006", "book": "AI001", "days_ago": 10, "duration": 30, "returned": False, "renew": 0},     # Đang mượn
            {"reader": "DG2024006", "book": "CS002", "days_ago": 40, "duration": 30, "returned": True,  "ret_days": 25}, # Trả đúng hạn
            {"reader": "DG2024006", "book": "DS001", "days_ago": 5,  "duration": 30, "returned": False, "renew": 0},     # Đang mượn
        ]

        for i, sc in enumerate(borrow_scenarios):
            reader = reader_map[sc["reader"]]
            book = book_map[sc["book"]]

            borrow_date = date.today() - timedelta(days=sc["days_ago"])
            due_date = borrow_date + timedelta(days=sc["duration"])

            if sc["returned"]:
                status = BorrowStatus.RETURNED
                return_date = borrow_date + timedelta(days=sc.get("ret_days", sc["duration"]))
            else:
                return_date = None
                if date.today() > due_date:
                    status = BorrowStatus.OVERDUE
                else:
                    status = BorrowStatus.BORROWING

                # Trừ số lượng khả dụng
                if book.available_quantity > 0:
                    book.available_quantity -= 1

            code_suffix = f"{i+1:04d}"
            borrow_code = f"PM{borrow_date.strftime('%Y%m%d')}{code_suffix}"

            rec = BorrowRecord(
                borrow_code=borrow_code,
                reader_id=reader.id,
                book_id=book.id,
                borrow_date=borrow_date,
                due_date=due_date,
                return_date=return_date,
                renew_count=sc.get("renew", 0),
                status=status,
                librarian_id=librarian_id
            )
            db.add(rec)
            db.flush()

            # Nếu trả trễ -> Tạo phiếu phạt (Đã thanh toán hoặc Chưa thanh toán)
            if sc["returned"] and return_date and return_date > due_date:
                overdue_days = (return_date - due_date).days
                fine = Fine(
                    borrow_record_id=rec.id,
                    reader_id=reader.id,
                    overdue_days=overdue_days,
                    fine_per_day=2000.0,
                    total_amount=overdue_days * 2000.0,
                    status=FineStatus.PAID,
                    paid_date=return_date
                )
                db.add(fine)

            # Nếu đang quá hạn -> Tạo phiếu phạt PENDING
            elif not sc["returned"] and date.today() > due_date:
                overdue_days = (date.today() - due_date).days
                fine = Fine(
                    borrow_record_id=rec.id,
                    reader_id=reader.id,
                    overdue_days=overdue_days,
                    fine_per_day=2000.0,
                    total_amount=overdue_days * 2000.0,
                    status=FineStatus.PENDING
                )
                db.add(fine)

        db.commit()

        # =========================================================================
        # 7. RESERVATIONS (Đặt trước sách)
        # =========================================================================
        reservations_data = [
            {"reader": "DG2024005", "book": "AI001", "status": ReservationStatus.PENDING, "notes": "Đặt trước khi có bản trả lại"},
            {"reader": "DG2024003", "book": "CS001", "status": ReservationStatus.READY,   "notes": "Đã có sách sẵn sàng ở quầy mượn"},
            {"reader": "DG2024002", "book": "AI004", "status": ReservationStatus.COMPLETED, "notes": "Đã nhận sách thành công"},
        ]

        for res in reservations_data:
            r = Reservation(
                reader_id=reader_map[res["reader"]].id,
                book_id=book_map[res["book"]].id,
                reservation_date=datetime.now(timezone.utc) - timedelta(days=2),
                expire_date=date.today() + timedelta(days=5),
                status=res["status"],
                notes=res["notes"]
            )
            db.add(r)
        db.commit()

        print("="*60)
        print("🎉 SEED DỮ LIỆU THÀNH CÔNG RỰC RỠ!")
        print(f"   👥 Người dùng : {len(user_objects)} tài khoản (Admin, Thủ thư, Độc giả)")
        print(f"   📚 Danh mục    : {len(cat_objects)} thể loại sách")
        print(f"   ✍️ Tác giả     : {len(author_objects)} tác giả nổi tiếng")
        print(f"   📖 Sách        : {len(book_objects)} cuốn sách chi tiết phong phú")
        print(f"   🎫 Độc giả     : {len(reader_objects)} thẻ độc giả hoạt động")
        print(f"   🔄 Phiếu mượn  : {len(borrow_scenarios)} phiếu (Đang mượn, đã trả, quá hạn)")
        print(f"   📌 Đặt trước   : {len(reservations_data)} phiếu đặt trước")
        print("="*60)

    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi khi seed dữ liệu: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    force_reset = "--reset" in sys.argv
    Base.metadata.create_all(bind=engine)
    seed_database(force_reset=force_reset)
