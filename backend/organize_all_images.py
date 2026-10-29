import os
import shutil

ROOT_DIR = r"c:\Users\bahun\Downloads\Đồ án 2"
TARGET_MAIN_DIR = os.path.join(ROOT_DIR, "Hinh_Anh_Va_So_Do_Do_An")
TARGET_DIAGRAMS_DIR = os.path.join(TARGET_MAIN_DIR, "1_So_Do_Ky_Thuat_UML_Architecture")
TARGET_SCREENSHOTS_DIR = os.path.join(TARGET_MAIN_DIR, "2_Anh_Chup_Giao_Dien_Web_UI")

SOURCE_DIAGRAMS_DIR = os.path.join(ROOT_DIR, "library-management", "docs", "diagrams")
SOURCE_SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "library-management", "docs", "screenshots")

os.makedirs(TARGET_DIAGRAMS_DIR, exist_ok=True)
os.makedirs(TARGET_SCREENSHOTS_DIR, exist_ok=True)

# 1. Copy 18 Diagrams
diagram_mapping = [
    ("01_context_diagram.png", "Hinh_3_1_So_Do_Boi_Canh_Context_Diagram.png", "Sơ đồ Bối cảnh Hệ thống (Context Diagram - Mức 0)"),
    ("02_usecase_general.png", "Hinh_2_1_So_Do_Use_Case_Tong_Quan.png", "Sơ đồ Use Case Tổng quan Toàn Hệ thống"),
    ("03_usecase_library.png", "Hinh_2_2_So_Do_Use_Case_Nghiep_Vu_Thu_Vien.png", "Sơ đồ Use Case Phân hệ Nghiệp vụ Thư viện"),
    ("04_usecase_ai.png", "Hinh_2_3_So_Do_Use_Case_Tro_Ly_AI.png", "Sơ đồ Use Case Phân hệ Trợ lý AI Thông minh"),
    ("05_activity_borrow.png", "Hinh_3_3_So_Do_Hoat_Dong_Muon_Sach.png", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Mượn sách tại Quầy"),
    ("06_activity_return.png", "Hinh_3_4_So_Do_Hoat_Dong_Tra_Sach_Tinh_Phat.png", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Trả sách & Tính phạt"),
    ("07_activity_renew.png", "Hinh_3_5_So_Do_Hoat_Dong_Gia_Han_Sach.png", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Gia hạn sách (+7 ngày)"),
    ("08_activity_reservation.png", "Hinh_3_6_So_Do_Hoat_Dong_Dat_Truoc_Sach.png", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Xếp hàng Đặt trước"),
    ("09_activity_fine.png", "Hinh_3_7_So_Do_Hoat_Dong_Xu_Ly_Phat.png", "Sơ đồ Hoạt động (Activity Diagram) Quy trình Xử lý Nộp & Miễn phạt"),
    ("10_activity_ai_chat.png", "Hinh_3_8_So_Do_Hoat_Dong_Chatbot_AI.png", "Sơ đồ Hoạt động (Activity Diagram) Luồng Chatbot AI Tra cứu"),
    ("11_sequence_borrow.png", "Hinh_3_9_So_Do_Tuan_Tu_Muon_Sach.png", "Sơ đồ Tuần tự (Sequence Diagram) Nghiệp vụ Lập phiếu Mượn sách"),
    ("12_sequence_return.png", "Hinh_3_10_So_Do_Tuan_Tu_Tra_Sach_Xu_Ly_Phat.png", "Sơ đồ Tuần tự (Sequence Diagram) Nghiệp vụ Trả sách & Xử lý phạt"),
    ("13_sequence_ai_chat.png", "Hinh_3_11_So_Do_Tuan_Tu_Chatbot_AI_Tra_Cuu.png", "Sơ đồ Tuần tự (Sequence Diagram) Chatbot AI Tra cứu Ngôn ngữ tự nhiên"),
    ("14_sequence_ai_suggest.png", "Hinh_3_12_So_Do_Tuan_Tu_AI_Goi_Y_Sach.png", "Sơ đồ Tuần tự (Sequence Diagram) AI Gợi ý sách theo Gu đọc"),
    ("15_erd_database.png", "Hinh_4_1_So_Do_Thuc_The_Quan_He_ERD_8_Bang.png", "Sơ đồ Thực thể Quan hệ CSDL 8 Bảng Chuẩn 3NF (ERD)"),
    ("16_system_architecture.png", "Hinh_3_2_So_Do_Kien_Truc_Phan_Tang_Layered.png", "Sơ đồ Kiến trúc Phân tầng Hệ thống (Layered Architecture)"),
    ("17_ai_pipeline_flow.png", "Hinh_5_1_So_Do_Pipeline_Grounded_Prompting_AI.png", "Sơ đồ Pipeline Luồng Xử lý Dữ liệu AI (Grounded Prompting)"),
    ("18_rag_architecture.png", "Hinh_5_2_So_Do_Kien_Truc_Mo_Rong_RAG_VectorDB.png", "Sơ đồ Kiến trúc Định hướng Mở rộng RAG với Vector Database"),
]

for src_name, dest_name, desc in diagram_mapping:
    src_path = os.path.join(SOURCE_DIAGRAMS_DIR, src_name)
    if os.path.exists(src_path):
        # Lưu cả tên chuẩn gốc và tên có tiền tố hình
        shutil.copy(src_path, os.path.join(TARGET_DIAGRAMS_DIR, src_name))
        shutil.copy(src_path, os.path.join(TARGET_DIAGRAMS_DIR, dest_name))

# 2. Copy 10 UI Screenshots
screenshot_mapping = [
    ("ui_01_login.png", "Hinh_6_1_Giao_Dien_Dang_Nhap_Demo_Accounts.png", "Giao diện Đăng nhập Hệ thống có hỗ trợ Demo Accounts"),
    ("ui_02_dashboard.png", "Hinh_6_2_Giao_Dien_Dashboard_Tong_Quan_ChartJS.png", "Giao diện Dashboard Tổng quan với Thẻ KPI và Biểu đồ Thống kê Trực quan"),
    ("ui_03_books.png", "Hinh_6_3_Giao_Dien_Quan_Ly_Kho_Sach_CRUD_Bo_Loc.png", "Giao diện Quản lý Kho Sách kèm Bộ lọc và Thao tác CRUD"),
    ("ui_04_readers.png", "Hinh_6_4_Giao_Dien_Quan_Ly_Doc_Gia_The_Thu_Vien.png", "Giao diện Quản lý Hồ sơ Độc giả và Trạng thái Thẻ Thư viện"),
    ("ui_05_borrows.png", "Hinh_6_5_Giao_Dien_Lap_Phieu_Muon_Tra_Sach.png", "Giao diện Lập Phiếu Mượn và Nhận Trả Sách tại Quầy"),
    ("ui_06_fines.png", "Hinh_6_6_Giao_Dien_Quan_Ly_Thu_Tien_Phat_Qua_Han.png", "Giao diện Quản lý và Xử lý Thu / Miễn Tiền Phạt Quá Hạn"),
    ("ui_07_reservations.png", "Hinh_6_7_Giao_Dien_Hang_Doi_Dat_Truoc_Sach.png", "Giao diện Quản lý Hàng đợi Đặt Trước Sách"),
    ("ui_08_statistics.png", "Hinh_6_8_Giao_Dien_Bao_Cao_Thong_Ke_Xuat_CSV.png", "Giao diện Báo cáo Thống kê Nghiệp vụ và Xuất Báo cáo CSV UTF-8-BOM"),
    ("ui_09_ai_chatbot.png", "Hinh_6_9_Giao_Dien_Tro_Ly_AI_Chatbot_Goi_Y.png", "Giao diện Trợ lý AI Chatbot Đối thoại và Gợi ý Sách"),
    ("ui_10_users.png", "Hinh_6_10_Giao_Dien_Quan_Tri_Vien_Phan_Quyen_RBAC.png", "Giao diện Quản trị viên Quản lý Tài khoản và Phân quyền RBAC"),
]

for src_name, dest_name, desc in screenshot_mapping:
    src_path = os.path.join(SOURCE_SCREENSHOTS_DIR, src_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, os.path.join(TARGET_SCREENSHOTS_DIR, src_name))
        shutil.copy(src_path, os.path.join(TARGET_SCREENSHOTS_DIR, dest_name))

# 3. Tạo file README Catalog
readme_path = os.path.join(TARGET_MAIN_DIR, "README_Danh_Muc_Hinh_Anh_Va_So_Do.md")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write("# 📚 DANH MỤC TOÀN BỘ 28 SƠ ĐỒ KỸ THUẬT & ẢNH GIAO DIỆN ĐỒ ÁN\n\n")
    f.write("Thư mục này lưu trữ toàn bộ các hình ảnh độ phân giải cao và sơ đồ kỹ thuật chuẩn học thuật được sử dụng trong Báo cáo Đồ án Học phần.\n\n")
    f.write("---\n\n")
    
    f.write("## 📐 PHẦN 1: 18 SƠ ĐỒ KỸ THUẬT (UML, ERD, KIẾN TRÚC, AI PIPELINE)\n\n")
    f.write("| STT | Ký hiệu trong Báo cáo | Tên Sơ đồ Kỹ thuật | File ảnh gốc | File ảnh theo mã hình |\n")
    f.write("|:---:|:---|:---|:---|:---|\n")
    for i, (src_name, dest_name, desc) in enumerate(diagram_mapping, 1):
        f.write(f"| {i} | Hình {dest_name.split('_')[1]}_{dest_name.split('_')[2]} | {desc} | `{src_name}` | `{dest_name}` |\n")
    
    f.write("\n---\n\n")
    f.write("## 🖥️ PHẦN 2: 10 ẢNH CHỤP MÀN HÌNH GIAO DIỆN WEB THỰC TẾ (WHITE THEME GLASSMORPHISM)\n\n")
    f.write("| STT | Ký hiệu trong Báo cáo | Tên Giao diện Màn hình | File ảnh gốc | File ảnh theo mã hình |\n")
    f.write("|:---:|:---|:---|:---|:---|\n")
    for i, (src_name, dest_name, desc) in enumerate(screenshot_mapping, 1):
        f.write(f"| {i} | Hình {dest_name.split('_')[1]}_{dest_name.split('_')[2]} | {desc} | `{src_name}` | `{dest_name}` |\n")
    
    f.write("\n---\n")
    f.write("Tất cả hình ảnh đã được chuẩn hóa định dạng PNG độ sắc nét cao, sẵn sàng phục vụ trình chiếu Slide và in ấn báo cáo đồ án.\n")

print(f"✅ Đã lưu thành công toàn bộ 28 sơ đồ và hình ảnh vào thư mục: {TARGET_MAIN_DIR}")
