# Hướng Dẫn Sử Dụng - Dành cho Thủ Thư

## 🎯 Tổng quan

Hệ thống Quản lý Thư viện giúp thủ thư quản lý toàn bộ hoạt động mượn/trả sách, theo dõi độc giả và xem báo cáo thống kê.

---

## 🔐 Đăng nhập

1. Truy cập `http://localhost:8000`
2. Nhập tài khoản thủ thư: `thuhu01` / `Thuhu@123`
3. Nhấn **Đăng nhập**

---

## 📖 Quản lý Sách

### Xem danh sách sách
1. Nhấn **Quản lý Sách** trên sidebar
2. Dùng ô tìm kiếm để lọc theo tên, tác giả, mã sách
3. Chọn **Thể loại** để lọc
4. Tích **Còn sách** để chỉ hiện sách có sẵn

### Thêm sách mới
1. Nhấn **➕ Thêm sách**
2. Điền thông tin: mã sách (bắt buộc, duy nhất), tên, tác giả, thể loại
3. Nhập số lượng
4. Nhấn **💾 Lưu**

### Sửa/Xóa sách
- Nhấn ✏️ để chỉnh sửa thông tin
- Nhấn 🗑️ để xóa mềm (sách không hiển thị nhưng lịch sử vẫn giữ)

---

## 🔄 Quản lý Mượn/Trả

### Lập phiếu mượn
1. Nhấn **Mượn/Trả** → **📝 Lập phiếu mượn**
2. Nhập **ID độc giả** và **ID sách**
3. Nhấn **Tạo phiếu mượn**

> ⚠️ Hệ thống tự kiểm tra:
> - Thẻ độc giả còn hạn
> - Số sách đang mượn chưa vượt giới hạn
> - Không còn nợ phạt

### Trả sách
1. Tìm phiếu mượn cần trả
2. Nhấn **↩️ Trả**
3. Xác nhận
4. Nếu quá hạn → phiếu phạt tự động được tạo

### Gia hạn sách
1. Tìm phiếu mượn (trạng thái "Đang mượn")
2. Nhấn **🔄 Gia hạn** (chỉ hiện nếu chưa gia hạn)
3. Xác nhận → hạn trả tăng thêm 7 ngày

> ℹ️ Không thể gia hạn nếu:
> - Đã quá hạn
> - Có người đặt trước cuốn sách đó
> - Đã gia hạn 1 lần rồi

### Xử lý phiếu phạt
1. Chọn tab **💰 Phiếu phạt**
2. Tìm phiếu cần xử lý
3. Nhấn **💳 Thu phạt** để ghi nhận thanh toán
4. Hoặc **🎁 Miễn** để miễn phạt (có lý do)

---

## 👥 Quản lý Độc giả

### Tạo thẻ độc giả
1. Nhấn **Độc giả** → **➕ Tạo thẻ độc giả**
2. Nhập User ID (người dùng phải đăng ký tài khoản trước)
3. Điền mã thẻ (VD: DG2024001), loại độc giả, hạn thẻ
4. Nhấn **💾 Tạo thẻ**

### Cập nhật trạng thái thẻ
- Nhấn ✏️ → thay đổi `card_status`: Active/Expired/Suspended

---

## 📊 Báo cáo & Thống kê

Truy cập **Thống kê** để xem:
- 📈 Biểu đồ lượt mượn 6 tháng
- 🗂️ Phân bổ sách theo thể loại
- 🔥 Top 10 sách mượn nhiều nhất
- ⭐ Top 10 độc giả tích cực
- ⚠️ Danh sách sách quá hạn và tiền phạt ước tính

---

## ⚠️ Lưu ý quan trọng

1. **Không thể xóa hoàn toàn sách** đã có lịch sử mượn (chỉ ẩn)
2. **Phiếu phạt tự động** tạo khi trả sách quá hạn
3. **Gia hạn** phải làm trước khi sách quá hạn
4. **Đặt trước** tự hủy sau 7 ngày nếu độc giả không đến lấy
