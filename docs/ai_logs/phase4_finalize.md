# Nhật Ký Sử Dụng AI - Giai Đoạn 4: Hoàn Thiện, Triển Khai & Báo Cáo

## Thông tin chung
- **Giai đoạn**: Hoàn thiện hệ thống, triển khai và tổng hợp báo cáo
- **AI sử dụng**: Google Gemini / Antigravity IDE (AI coding assistant)
- **Mục tiêu**: Sinh hướng dẫn sử dụng, review bảo mật, tạo báo cáo kỹ thuật, đóng gói Docker

---

## Prompt 4.1: Sinh hướng dẫn sử dụng cho thủ thư

**Prompt gửi cho AI:**
```
Dựa trên hệ thống quản lý thư viện có các chức năng: đăng nhập, quản lý sách,
quản lý độc giả, mượn/trả/gia hạn sách, quản lý đặt trước, xem thống kê và
xuất CSV. Hãy viết hướng dẫn sử dụng chi tiết cho vai trò Thủ thư (Librarian),
bao gồm các bước thao tác cho từng chức năng, kèm lưu ý quan trọng.
```

**Kết quả AI:**
- Sinh hướng dẫn đầy đủ 8 chức năng với từng bước thao tác
- Bao gồm lưu ý về nghiệp vụ (ví dụ: gia hạn tối đa 1 lần, phạt tự động)
- Đề xuất thêm mục "Câu hỏi thường gặp" → ✅ Đã bổ sung

**Phần chỉnh sửa thủ công:**
- Điều chỉnh số ngày gia hạn từ "14 ngày" → "7 ngày" (AI gợi ý sai)
- Bổ sung hướng dẫn sử dụng AI Chatbot (AI không tự sinh vì không biết UI)
- Cập nhật đường dẫn URL thực tế: `http://localhost:8000`

**File kết quả:** [`docs/user_guide/librarian_guide.md`](../user_guide/librarian_guide.md)

---

## Prompt 4.2: Sinh hướng dẫn sử dụng cho độc giả

**Prompt gửi cho AI:**
```
Viết hướng dẫn sử dụng cho Độc giả của hệ thống thư viện online.
Các chức năng độc giả có: xem danh sách sách, tìm kiếm, đặt trước sách,
xem phiếu mượn cá nhân, sử dụng AI Chatbot tra cứu, xem tóm tắt sách,
nhận gợi ý đọc sách. Viết ngắn gọn, thân thiện, dễ hiểu.
```

**Kết quả AI:**
- Hướng dẫn 6 chức năng với ngôn ngữ thân thiện cho người dùng phổ thông
- Thêm phần "Mẹo sử dụng AI Chatbot hiệu quả" → ✅ Rất hữu ích

**Phần chỉnh sửa thủ công:**
- Cập nhật thông tin tài khoản demo (admin/admin123)
- Bổ sung hướng dẫn đặt trước sách khi hết hàng

**File kết quả:** [`docs/user_guide/reader_guide.md`](../user_guide/reader_guide.md)

---

## Prompt 4.3: Review luồng bảo mật dữ liệu độc giả

**Prompt gửi cho AI:**
```
Review luồng xử lý dữ liệu trong hệ thống thư viện có tích hợp AI này.
Tập trung vào bảo mật dữ liệu độc giả khi gọi AI Gemini:

[Paste code backend/routers/ai.py và backend/services/ai_service.py]

Kiểm tra:
1. Dữ liệu cá nhân nào được gửi sang AI?
2. API key có bị lộ không?
3. Có lỗ hổng bảo mật nào không?
4. Đề xuất cải thiện.
```

**Kết quả AI:**
```
✅ ĐIỂM TỐT:
1. Không lộ API key - dùng biến môi trường .env ✅
2. Endpoint /suggest chỉ gửi book_titles và borrow_history (không có reader_id, email, phone)
3. JWT authentication bảo vệ tất cả AI endpoints
4. Pydantic validation giới hạn độ dài query (max 500 chars)

⚠️ CẦN CẢI THIỆN:
1. Thiếu rate limiting cho AI endpoints (ai spam 1000 request)
2. Nên log AI request để audit
3. Timeout chưa được set (có thể treo nếu Gemini chậm)

🔧 ĐỀ XUẤT CODE:
- Thêm asyncio.wait_for(timeout=15) cho Gemini call
- Thêm retry với exponential backoff cho rate limit 429
```

**Đã áp dụng:**
- ✅ Thêm `timeout=15s` trong `ai_service.py`
- ✅ Thêm retry 2 lần với exponential backoff
- ✅ Xử lý lỗi 429 Rate Limit
- ⏳ Rate limiting endpoint: ghi nhận, phạm vi ngoài đề tài cơ bản

---

## Prompt 4.4: Tạo báo cáo kỹ thuật

**Prompt gửi cho AI:**
```
Tạo báo cáo kỹ thuật cho dự án "Hệ thống Quản lý Thư viện có tích hợp AI" bao gồm:
1. Tổng quan và bối cảnh đề tài
2. Yêu cầu hệ thống (chức năng + phi chức năng + AI)
3. Thiết kế kiến trúc và CSDL (ERD)
4. Thiết kế và tối ưu Prompt AI (3 vòng)
5. Kết quả kiểm thử (24 test cases)
6. Bảo mật và đạo đức AI
7. Hướng dẫn cài đặt và chạy

Stack: FastAPI + SQLite + Jinja2 + Google Gemini
```

**Kết quả AI:**
- Sinh cấu trúc báo cáo 7 phần với nội dung chi tiết
- Có sơ đồ kiến trúc ASCII
- Có bảng phân bổ test cases

**Phần chỉnh sửa thủ công:**
- Cập nhật số lượng test cases thực tế (24)
- Điều chỉnh mô tả ERD cho đúng với model thực
- Thêm phần "Tối ưu 3 vòng prompt" cụ thể hơn

**File kết quả:** [`docs/technical_report.md`](../technical_report.md)

---

## Prompt 4.5: Đóng gói ứng dụng với Docker

**Prompt gửi cho AI:**
```
Tạo Dockerfile và docker-compose.yml cho ứng dụng FastAPI với:
- Python 3.11
- SQLite database persist trong volume
- Environment variables từ .env
- Multi-stage build để tối ưu image size
- Healthcheck endpoint /health
```

**Kết quả AI:**
- Sinh Dockerfile multi-stage build đúng cấu trúc
- docker-compose.yml với volume và env vars
- Đề xuất thêm .dockerignore → ✅ Đã ghi nhận

**Phần chỉnh sửa thủ công:**
- Điều chỉnh WORKDIR vì backend nằm trong subfolder
- Sửa PYTHONPATH để import đúng các module

**File kết quả:** [`Dockerfile`](../../Dockerfile), [`docker-compose.yml`](../../docker-compose.yml)

---

## Prompt 4.6: Tạo và tối ưu dữ liệu mẫu

**Prompt gửi cho AI:**
```
Tạo seed data cho hệ thống thư viện bao gồm:
- 5 thể loại sách (CNTT, Văn học, Kinh tế, Khoa học, Kỹ năng sống)
- 8 tác giả
- 20 đầu sách đa dạng, thực tế
- 3 tài khoản mẫu (admin, librarian, reader)
- 5 phiếu mượn mẫu (đang mượn, đã trả, quá hạn)
Dùng SQLAlchemy, Python.
```

**Kết quả AI:**
- Sinh file seed_data.py với đủ các entity
- Dữ liệu tên sách thực tế, phù hợp từng thể loại
- Đề xuất seed cả Fine records để demo phạt → ✅ Đã bổ sung

**Phần chỉnh sửa thủ công:**
- Điều chỉnh ngày mượn để có cả phiếu quá hạn thực tế
- Thêm ISBN thực tế cho sách

**File kết quả:** [`backend/seed_data.py`](../../backend/seed_data.py)

---

## Tổng kết vai trò AI trong toàn bộ SDLC

| Giai đoạn | AI hỗ trợ gì | Kết quả |
|-----------|-------------|---------|
| **GĐ1 - Phân tích** | Phân tích nghiệp vụ, thiết kế ERD, use case | Tiết kiệm 60% thời gian phân tích |
| **GĐ2 - Phát triển** | Sinh model, API, giao diện, logic nghiệp vụ | Code skeleton nhanh, debug hiệu quả |
| **GĐ3 - Tích hợp AI** | Thiết kế prompt, tối ưu 3 vòng, sinh test case | Zero hallucination, 24 test PASSED |
| **GĐ4 - Hoàn thiện** | Tài liệu, bảo mật review, Docker, seed data | Báo cáo đầy đủ, sẵn sàng deploy |

**Bài học quan trọng:**
- AI tăng tốc phát triển nhưng luôn cần kiểm tra và điều chỉnh thủ công
- Prompt engineering là kỹ năng quan trọng: ràng buộc rõ ràng → kết quả tốt hơn
- AI không thay thế được tư duy nghiệp vụ nhưng là công cụ cực kỳ hiệu quả
