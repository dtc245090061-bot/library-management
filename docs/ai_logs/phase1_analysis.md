# Nhật Ký Sử Dụng AI - Giai Đoạn 1: Phân Tích & Thiết Kế

## Thông tin chung
- **Giai đoạn**: Phân tích yêu cầu và thiết kế hệ thống
- **AI sử dụng**: Google Gemini / Claude
- **Mục tiêu**: Phân tích nghiệp vụ, thiết kế ERD, use case, kiến trúc

---

## Prompt 1: Phân tích nghiệp vụ thư viện

**Prompt gửi cho AI:**
```
Hệ thống quản lý thư viện trường học cần xử lý các nghiệp vụ sau:
1. Mượn sách: độc giả có thẻ mượn sách nếu còn sẵn
2. Trả sách: tính phạt nếu quá hạn
3. Gia hạn: tối đa 1 lần, thêm 7 ngày
4. Đặt trước: khi sách đang được mượn hết

Hãy phân tích chi tiết từng nghiệp vụ, xác định các ràng buộc và điều kiện ngoại lệ.
```

**Kết quả AI trả về:**
- Nghiệp vụ Mượn: kiểm tra thẻ còn hạn, số sách đang mượn < giới hạn, không nợ phạt
- Nghiệp vụ Trả: tính ngày quá hạn, tạo phiếu phạt, tăng số lượng sách
- Nghiệp vụ Gia hạn: kiểm tra chưa quá hạn, chưa có người đặt trước, chưa gia hạn lần nào
- Nghiệp vụ Đặt trước: chỉ khi sách hết, hủy sau 7 ngày nếu không lấy

**Đánh giá & điều chỉnh:**
✅ Kết quả AI phù hợp với yêu cầu đề tài
✅ Đã thêm: kiểm tra "còn nợ phạt" trước khi mượn (AI chưa đề cập)
✅ Đã điều chỉnh: thời gian gia hạn từ 14 ngày xuống 7 ngày theo yêu cầu đề

---

## Prompt 2: Thiết kế ERD

**Prompt gửi cho AI:**
```
Thiết kế ERD cho hệ thống quản lý thư viện với các thực thể:
- Sách (Book): mã, tên, tác giả, thể loại, NXB, năm, số lượng
- Độc giả (Reader): mã thẻ, thông tin cá nhân, loại, trạng thái
- Phiếu mượn (BorrowRecord): mã phiếu, ngày mượn, ngày hẹn trả, trạng thái
- Phiếu phạt (Fine): số ngày quá hạn, tiền phạt, trạng thái
Chỉ rõ quan hệ, khóa chính, khóa ngoại và ràng buộc.
```

**Kết quả AI trả về:**
```
Entities và Relations:
- User (1) — (1) Reader
- Reader (1) — (N) BorrowRecord
- Book (1) — (N) BorrowRecord
- BorrowRecord (1) — (0..1) Fine
- Book (N) — (1) Author
- Book (N) — (1) Category
- Reader (1) — (N) Reservation
- Book (1) — (N) Reservation
```

**Đánh giá & điều chỉnh:**
✅ Quan hệ đúng và đầy đủ
✅ Đã tách `User` và `Reader` để hỗ trợ nhiều vai trò (admin, librarian)
⚠️ AI đề xuất dùng JSONB cho lịch sử - đã đổi sang bảng riêng `Fine` để dễ query

---

## Prompt 3: Xác định chức năng AI phù hợp

**Prompt gửi cho AI:**
```
Với hệ thống quản lý thư viện, AI có thể hỗ trợ những chức năng gì?
Đánh giá độ khó và độ hữu ích của mỗi chức năng.
```

**Kết quả AI trả về:**
| Chức năng | Độ hữu ích | Độ phức tạp |
|-----------|-----------|-------------|
| Chatbot tra cứu sách | Cao | Trung bình |
| Tóm tắt nội dung sách | Cao | Thấp |
| Gợi ý sách cá nhân | Cao | Trung bình |
| Phát hiện sách quá hạn | Thấp | Rất thấp (đã có logic) |
| Phân tích xu hướng đọc | Trung bình | Cao |

**Quyết định:**
✅ Chọn 3 chức năng: Chatbot + Tóm tắt + Gợi ý
❌ Loại bỏ: Phân tích xu hướng (phức tạp, ít giá trị cho đề tài cơ bản)

---

## Prompt 4: Thiết kế Prompt Template

**Prompt gửi cho AI:**
```
Thiết kế system prompt cho chatbot tra cứu sách thư viện.
Yêu cầu: AI chỉ gợi ý sách có trong danh sách, không bịa thêm.
Input: câu hỏi người dùng + danh sách sách từ DB
Output: danh sách tối đa 5 sách + lý do gợi ý
```

**Kết quả AI trả về:**
```
SYSTEM: Bạn là trợ lý tra cứu thư viện. Chỉ gợi ý sách có trong dữ liệu được cung cấp...
```

**Đánh giá & điều chỉnh:**
✅ Prompt rõ ràng, có ràng buộc tốt
✅ Đã thêm: "Không thêm thông tin không có trong dữ liệu"
✅ Đã thêm: Format output cụ thể với emoji dễ đọc
⚠️ Thêm giới hạn độ dài câu hỏi (500 ký tự) để tránh prompt injection
