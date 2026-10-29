# 🧪 Nhật ký Thử nghiệm Prompt AI - Hệ thống Thư viện

> **Mục tiêu**: Cải thiện chất lượng chatbot tra cứu sách thông qua 3 vòng thử nghiệm và tối ưu hóa prompt.

---

## Vòng 1: Prompt cơ bản (Baseline)

**Ngày thử nghiệm**: 2026-08-15  
**Model**: gemini-1.5-flash  

### System Prompt v1 (Đơn giản)
```
Bạn là trợ lý thư viện. Hãy gợi ý sách phù hợp.
```

### User Prompt v1
```
Câu hỏi: {query}
Danh sách sách: {book_list}
```

### Kết quả thử nghiệm

| Câu hỏi | Kết quả | Đánh giá |
|---------|---------|----------|
| "Tôi muốn học AI cho người mới" | Trả về 3 sách đúng nhưng không có lý do | ⚠️ Chấp nhận được |
| "Sách nào hay nhất?" | Bịa ra sách không có trong DB | ❌ Thất bại |
| "Sách về Python" | Liệt kê đúng nhưng không format | ⚠️ Thiếu format |
| "Tìm sách cho trẻ em" | Nói "không có" nhưng không giải thích | ❌ Thiếu thông tin |

**Vấn đề phát hiện**:
- AI bịa sách khi không tìm thấy phù hợp
- Thiếu format output nhất quán
- Không có ràng buộc "chỉ dùng dữ liệu được cung cấp"
- Thiếu giải thích lý do gợi ý

---

## Vòng 2: Thêm ràng buộc và format (Cải thiện)

**Ngày thử nghiệm**: 2026-08-17  
**Model**: gemini-1.5-flash  

### System Prompt v2 (Có ràng buộc)
```
Bạn là trợ lý tra cứu thư viện thông minh.
Nhiệm vụ: Giúp độc giả tìm sách phù hợp từ danh mục thư viện.

QUAN TRỌNG:
- Chỉ gợi ý sách có trong danh sách được cung cấp bên dưới.
- Không bịa thêm sách, mã sách hoặc tình trạng sách.
- Không thêm thông tin không có trong dữ liệu.
- Nếu không tìm thấy sách phù hợp, hãy nói thật với độc giả.
- Trả lời bằng tiếng Việt, thân thiện và dễ hiểu.

Định dạng trả lời:
📚 [Tên sách] (Mã: [mã sách])
- Tác giả: [tên]
- Tình trạng: [còn X bản / hết sách]
- Lý do gợi ý: [giải thích]
```

### User Prompt v2
```
Câu hỏi của độc giả: {query}

Danh sách sách trong thư viện:
{book_list}

Hãy gợi ý tối đa 5 cuốn sách. Chỉ dùng thông tin từ danh sách trên.
```

### Kết quả thử nghiệm

| Câu hỏi | Kết quả | Đánh giá |
|---------|---------|----------|
| "Tôi muốn học AI cho người mới" | 3 sách đúng với lý do rõ ràng | ✅ Tốt |
| "Sách nào hay nhất?" | Hỏi lại để clarify hoặc đề xuất từ DB | ✅ Cải thiện |
| "Sách về Python" | Đúng format, có lý do | ✅ Tốt |
| "Tìm sách cho trẻ em" | Báo không có phù hợp + đề xuất gần nhất | ✅ Tốt hơn |

**Cải thiện đạt được**:
- Không còn bịa sách
- Output có format nhất quán
- Có lý do gợi ý

**Vấn đề còn lại**:
- Chưa có hướng dẫn xử lý câu hỏi mơ hồ
- Thiếu lời mở đầu thân thiện

---

## Vòng 3: Tối ưu cuối cùng (Production)

**Ngày thử nghiệm**: 2026-08-19  
**Model**: gemini-1.5-flash  

### System Prompt v3 (Hoàn thiện - ĐANG DÙNG)
```
Bạn là trợ lý tra cứu thư viện thông minh.
Nhiệm vụ: Giúp độc giả tìm sách phù hợp từ danh mục thư viện.

QUAN TRỌNG:
- Chỉ gợi ý sách có trong danh sách được cung cấp bên dưới.
- Không bịa thêm sách, mã sách hoặc tình trạng sách.
- Không thêm thông tin không có trong dữ liệu.
- Nếu không tìm thấy sách phù hợp, hãy nói thật với độc giả.
- Trả lời bằng tiếng Việt, thân thiện và dễ hiểu.
- Giải thích ngắn gọn lý do gợi ý mỗi cuốn sách.

Định dạng trả lời:
1. Đưa ra lời mở đầu ngắn
2. Liệt kê các sách gợi ý theo định dạng:
   📚 [Tên sách] (Mã: [mã sách])
   - Tác giả: [tên tác giả]
   - Thể loại: [thể loại]
   - Tình trạng: [còn X bản / hết sách]
   - Lý do gợi ý: [giải thích ngắn]
3. Kết thúc bằng lời khuyên thêm nếu cần
```

### User Prompt v3
```
Câu hỏi của độc giả: {query}

Danh sách sách trong thư viện:
{book_list}

Hãy gợi ý tối đa 5 cuốn sách phù hợp nhất với câu hỏi trên. 
Chỉ dùng thông tin từ danh sách trên. Giải thích lý do gợi ý cho từng cuốn.
```

### Kết quả thử nghiệm toàn diện

| Loại câu hỏi | Câu hỏi mẫu | Kết quả | Đánh giá |
|-------------|------------|---------|----------|
| Chủ đề rõ | "Tôi muốn học AI cho người mới" | Gợi ý đúng 3-5 sách với lý do cụ thể | ✅ Xuất sắc |
| Chủ đề mơ hồ | "Sách hay về khoa học" | Hỏi clarify + đề xuất thể loại | ✅ Tốt |
| Sách không tồn tại | "Sách nấu ăn Việt Nam" | Báo không có, đề xuất thể loại gần | ✅ Đúng |
| Sách hết | "Sách Machine Learning" | Hiển thị sách hết + gợi ý tương tự còn | ✅ Hữu ích |
| Câu hỏi cá nhân | "Sách cho sinh viên năm 1" | Gợi ý theo cấp độ phù hợp | ✅ Tốt |
| Câu hỏi ngắn | "Python" | Gợi ý đúng tất cả sách Python | ✅ OK |

**Cải thiện so với v1**:
- ✅ Không bịa sách (0 hallucination)
- ✅ Format nhất quán, dễ đọc
- ✅ Lý do gợi ý rõ ràng
- ✅ Xử lý tốt câu hỏi mơ hồ
- ✅ Hiển thị đúng tình trạng sách (còn/hết)

---

## So sánh 3 phiên bản

| Tiêu chí | v1 (Baseline) | v2 (Cải thiện) | v3 (Production) |
|----------|--------------|----------------|-----------------|
| Không bịa sách | ❌ | ✅ | ✅ |
| Format nhất quán | ❌ | ✅ | ✅ |
| Lý do gợi ý | ❌ | ✅ | ✅ |
| Xử lý mơ hồ | ❌ | ⚠️ | ✅ |
| Xử lý sách hết | ❌ | ⚠️ | ✅ |
| Thân thiện | ⚠️ | ⚠️ | ✅ |
| **Điểm tổng** | **2/6** | **4/6** | **6/6** |

---

## Bài học rút ra

1. **Ràng buộc rõ ràng là quan trọng nhất**: "Chỉ dùng dữ liệu được cung cấp" loại bỏ hoàn toàn hallucination.
2. **Format output trong prompt**: Định nghĩa format trả lời giúp output nhất quán và dễ parse.
3. **Xử lý edge case**: Cần hướng dẫn AI xử lý trường hợp không tìm thấy sách phù hợp.
4. **Giải thích lý do**: Yêu cầu AI giải thích lý do gợi ý giúp độc giả tin tưởng hơn.
5. **Ngôn ngữ thân thiện**: Thêm yêu cầu "thân thiện và dễ hiểu" cải thiện trải nghiệm người dùng.

---

## Giới hạn và rủi ro

- AI có thể hiểu sai từ khóa trong tiếng Việt có dấu
- Khi danh sách sách quá dài (>100 sách), có thể vượt context window → cần filter trước
- Không gửi dữ liệu cá nhân độc giả trong prompt (đã implement)
- Cần test thêm với câu hỏi tiếng Anh/Việt lẫn lộn
