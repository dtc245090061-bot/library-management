# Nhật Ký Sử Dụng AI - Giai Đoạn 2 & 3: Phát Triển & Tích Hợp AI

## Giai đoạn 2: Xây dựng chức năng quản lý

### Prompt 2.1: Sinh model SQLAlchemy

**Prompt:**
```
Tạo SQLAlchemy model cho bảng BorrowRecord (phiếu mượn sách) với các trường:
mã phiếu (unique), reader_id, book_id, ngày mượn, ngày hẹn trả, ngày trả thực tế,
số lần gia hạn, trạng thái (BORROWING/RETURNED/OVERDUE/LOST), ghi chú.
Dùng Enum cho trạng thái.
```

**Kết quả AI:**
- Sinh model đúng cấu trúc với Enum, Foreign Keys, relationships
- Đề xuất thêm `librarian_id` để ghi nhận thủ thư xử lý ✅ Đã dùng

**Phần chỉnh sửa thủ công:**
- Thêm `onupdate=datetime.utcnow` cho `updated_at`
- Đổi tên `return_date` từ `actual_return_date` (AI đặt dài hơn cần)

---

### Prompt 2.2: Sinh logic tính phạt

**Prompt:**
```
Viết hàm Python tính phạt quá hạn khi độc giả trả sách:
- Phạt 2000 VNĐ/ngày quá hạn
- Tự động tạo bản ghi Fine nếu quá hạn
- Cập nhật available_quantity của sách
```

**Kết quả AI:**
```python
def return_book(record_id, notes, db):
    record = db.query(BorrowRecord).filter(BorrowRecord.id == record_id).first()
    today = date.today()
    record.return_date = today
    record.status = BorrowStatus.RETURNED
    
    if today > record.due_date:
        overdue_days = (today - record.due_date).days
        fine = Fine(...)
        db.add(fine)
    ...
```

**Phần chỉnh sửa thủ công:**
- Thêm giới hạn `min(available_quantity + 1, total_quantity)` để tránh số âm
- Thêm validation: sách đã trả không được trả lại

---

### Prompt 2.3: Debug lỗi ràng buộc

**Prompt:**
```
Lỗi: khi gia hạn sách, hệ thống vẫn cho gia hạn dù có người đặt trước.
Code hiện tại: [paste code renew_book]
Tìm lỗi và sửa.
```

**Kết quả AI:**
- Phát hiện thiếu kiểm tra `Reservation.status == PENDING`
- Đề xuất thêm query kiểm tra trước khi gia hạn

**Đã áp dụng:** ✅ Thêm check reservation trong `renew_book()`

---

## Giai đoạn 3: Tích hợp AI và tối ưu Prompt

### Thử nghiệm Prompt - Vòng 1

**Prompt v1 (đơn giản):**
```
Gợi ý sách phù hợp với câu hỏi: {query}
Danh sách sách: {books}
```

**Kết quả:** AI đôi khi bịa thêm sách không có trong danh sách ❌

---

### Thử nghiệm Prompt - Vòng 2

**Prompt v2 (thêm ràng buộc):**
```
SYSTEM: Chỉ gợi ý sách có trong danh sách. Không bịa.
USER: Câu hỏi: {query}. Sách: {books}
```

**Kết quả:** Tốt hơn, nhưng format trả lời không nhất quán ⚠️

---

### Thử nghiệm Prompt - Vòng 3 (Hiện tại)

**Prompt v3 (có format output):**
```
SYSTEM: Bạn là trợ lý tra cứu thư viện. Chỉ gợi ý sách có trong danh sách được cung cấp.
Không bịa mã sách hoặc tình trạng sách. Trả lời tiếng Việt.

Format trả lời:
📚 [Tên sách] (Mã: [mã])
- Tác giả: ...
- Lý do gợi ý: ...
```

**Kết quả:** ✅ Nhất quán, không bịa, format đẹp

**Cải tiến so với v1:**
- Thêm format rõ ràng → output chuẩn hơn
- Thêm "không bịa" → ít hallucination hơn
- Thêm "tiếng Việt" → đảm bảo ngôn ngữ đúng

---

### Prompt 3.1: Tóm tắt sách - Vòng thử nghiệm

**Test case 1:** Sách có mô tả đầy đủ
→ AI tóm tắt tốt, đúng thể loại, có đối tượng độc giả ✅

**Test case 2:** Sách không có mô tả
→ AI tóm tắt dựa trên tên + tác giả → vẫn ra kết quả hữu ích ✅

**Test case 3:** Sách tiếng Anh
→ AI tóm tắt bằng tiếng Việt đúng theo prompt ✅

---

### Xử lý lỗi AI (Error Handling)

| Lỗi | Xử lý |
|-----|-------|
| API key sai/hết quota | Fallback sang mock response |
| Timeout | try/except với HTTPException 500 |
| Response rỗng | Return thông báo lỗi thân thiện |
| Sách hết | Vẫn gợi ý nhưng note "Hết sách" |
| Câu hỏi quá dài | Pydantic validation max_length=500 |

---

### Review Code bằng AI

**Prompt:**
```
Review đoạn code sau về bảo mật:
[paste ai_router.py]
Tìm các vấn đề bảo mật có thể có.
```

**AI phát hiện:**
1. ⚠️ Nên thêm rate limiting cho AI endpoints (tránh spam)
2. ⚠️ Nên log các request AI để audit
3. ✅ Không lộ API key (đã đúng)
4. ✅ Không gửi dữ liệu cá nhân (đã đúng)

**Đã xử lý:**
- Rate limiting: ghi nhận, sẽ implement trong phase 4
- Logging: thêm logger vào ai_service.py ✅
