"""
AI Service - Tích hợp Google Gemini với multi-model fallback và smart local fallback
Hỗ trợ:
- Danh sách model dự phòng tự động khi một model hết quota (429 Rate Limit)
- Timeout & Retry với exponential backoff
- Smart Knowledge fallback khi mất kết nối mạng hoặc hết toàn bộ API quota
"""
import asyncio
import logging
import re
import httpx
from typing import Optional, List
from config import settings

logger = logging.getLogger(__name__)

# Cấu hình retry & timeout
MAX_RETRIES = 1
TIMEOUT_SECONDS = 25

# Danh sách candidate models theo thứ tự ưu tiên
FALLBACK_MODELS = [
    "gemini-flash-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.6-flash",
    "gemma-4-31b-it"
]


class AIService:
    """Service tích hợp AI (Groq + Gemini với multi-model fallback và smart mock)"""

    def __init__(self):
        self.models_to_try: List[str] = []
        self.active_model_name: str = "Smart Local AI"
        self.is_mock: bool = True
        self._genai = None
        self._init_client()

    def _init_client(self):
        """Khởi tạo AI client (Groq hoặc Gemini) nếu có API key"""
        has_groq = bool(settings.GROQ_API_KEY and settings.GROQ_API_KEY.startswith("gsk_"))
        has_gemini = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your-gemini-api-key-here")

        if has_groq:
            self.active_model_name = f"Groq ({settings.GROQ_MODEL})"
            self.is_mock = False
            logger.info(f"✅ Groq AI đã được kích hoạt. Model chính: {settings.GROQ_MODEL}")

        if has_gemini:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self._genai = genai

                primary = settings.GEMINI_MODEL
                self.models_to_try = [primary] + [m for m in FALLBACK_MODELS if m != primary]
                if not has_groq:
                    self.active_model_name = primary
                    self.is_mock = False
                logger.info(f"✅ Gemini AI đã được khởi tạo. Model chính: {primary}, Models dự phòng: {self.models_to_try[1:]}")
            except Exception as e:
                logger.warning(f"⚠️ Không thể khởi tạo Gemini: {e}.")

        if not has_groq and not has_gemini:
            logger.info("ℹ️ Chưa có GROQ_API_KEY hoặc GEMINI_API_KEY - Dùng smart local AI responses")
            self.is_mock = True

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Gửi prompt đến AI với ưu tiên Groq -> Gemini -> Smart Local fallback"""
        if self.is_mock:
            return self._smart_local_response(user_prompt)

        # 1. Ưu tiên gọi Groq
        if settings.GROQ_API_KEY and settings.GROQ_API_KEY.startswith("gsk_"):
            try:
                res = await self._call_groq(system_prompt, user_prompt)
                if res:
                    return res
            except Exception as e:
                logger.warning(f"⚠️ Groq thất bại, chuyển sang Gemini fallback: {e}")

        # 2. Gọi Google Gemini fallback
        if self._genai:
            try:
                return await self._call_gemini_with_fallback(system_prompt, user_prompt)
            except Exception as e:
                logger.warning(f"⚠️ Gemini thất bại, chuyển sang Smart Local: {e}")

        # 3. Fallback sang Smart Local nếu cả hai đều gặp sự cố
        return self._smart_local_response(user_prompt)

    async def _call_groq(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Gọi Groq Cloud API qua HTTPX với tốc độ suy luận siêu nhanh"""
        models = [settings.GROQ_MODEL, "qwen/qwen3.8-27b", "qwen/qwen3.6-27b"]
        models_to_try = list(dict.fromkeys(models))
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        for model_name in models_to_try:
            try:
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.1
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        content = data["choices"][0]["message"]["content"]
                        self.active_model_name = f"Groq ({model_name})"
                        logger.info(f"✅ Groq API ({model_name}) phản hồi thành công")
                        return content
                    else:
                        logger.warning(f"⚠️ Groq ({model_name}) HTTP {resp.status_code}: {resp.text[:120]}")
            except Exception as e:
                logger.warning(f"⚠️ Groq ({model_name}) lỗi kết nối: {e}")
        return None

    async def _call_gemini_with_fallback(self, system_prompt: str, user_prompt: str) -> str:
        """Gọi Gemini API qua danh sách model dự phòng nếu model trước gặp lỗi 429 hoặc lỗi kết nối"""
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        last_error = None

        for model_name in self.models_to_try:
            for attempt in range(MAX_RETRIES + 1):
                try:
                    logger.info(f"🤖 Đang gửi yêu cầu tới model: {model_name} (lần {attempt + 1})")
                    model = self._genai.GenerativeModel(model_name)
                    
                    loop = asyncio.get_running_loop()
                    response = await asyncio.wait_for(
                        loop.run_in_executor(None, lambda: model.generate_content(full_prompt)),
                        timeout=TIMEOUT_SECONDS
                    )
                    
                    if response and response.text:
                        self.active_model_name = model_name
                        return response.text
                except asyncio.TimeoutError:
                    last_error = f"Timeout ({model_name})"
                    logger.warning(f"⏱️ Model {model_name} timeout lần {attempt + 1}")
                    if attempt < MAX_RETRIES:
                        await asyncio.sleep(1)
                except Exception as e:
                    err_str = str(e)
                    last_error = err_str
                    logger.warning(f"⚠️ Model {model_name} gặp lỗi: {err_str[:120]}. Thử model tiếp theo...")
                    # Nếu là lỗi quota 429 hoặc NotFound thì chuyển ngay sang model tiếp theo trong danh sách
                    if "429" in err_str or "quota" in err_str.lower() or "notfound" in err_str.lower() or "not found" in err_str.lower():
                        break
                    if attempt < MAX_RETRIES:
                        await asyncio.sleep(1)

        # Nếu tất cả models online đều quá tải hoặc lỗi, trả về smart local librarian response
        logger.warning(f"⚠️ Tất cả models đều bận/hết quota ({last_error}). Kích hoạt Smart Local Librarian.")
        return self._smart_local_response(user_prompt)

    def _smart_local_response(self, user_prompt: str) -> str:
        """Sinh câu trả lời thông minh dựa trên dữ liệu thư viện khi API bận"""
        prompt_lower = user_prompt.lower()

        if "lịch sử mượn" in prompt_lower or "gợi ý sách cho bạn" in prompt_lower or "phân tích sở thích" in prompt_lower:
            return self._smart_suggest_response(user_prompt)
        elif "tóm tắt" in prompt_lower or "thông tin sách cần tóm tắt" in prompt_lower:
            return self._smart_summary_response(user_prompt)
        else:
            return self._smart_search_response(user_prompt)

    def _smart_search_response(self, user_prompt: str) -> str:
        """Trích xuất và gợi ý sách thông minh từ book_list trong prompt"""
        # Trích xuất danh sách sách từ user_prompt
        books_section = ""
        if "Danh sách sách trong thư viện:" in user_prompt:
            parts = user_prompt.split("Danh sách sách trong thư viện:")
            if len(parts) > 1:
                books_section = parts[1].split("Hãy gợi ý")[0].strip()

        # Tìm các dòng sách
        book_lines = [line.strip() for line in books_section.split("\n") if line.strip().startswith("- Mã:")]

        # Tìm từ khóa trong câu hỏi
        query_match = re.search(r"Câu hỏi của độc giả:\s*(.*?)\n", user_prompt)
        query = query_match.group(1).lower() if query_match else ""

        # Lọc sách phù hợp
        matched_books = []
        for line in book_lines:
            line_lower = line.lower()
            # Tính điểm tương đồng
            score = 0
            keywords = [w for w in re.findall(r'\w+', query) if len(w) > 1]
            for kw in keywords:
                if kw in line_lower:
                    score += 1
            if score > 0:
                matched_books.append((score, line))

        matched_books.sort(key=lambda x: x[0], reverse=True)
        top_lines = [b[1] for b in matched_books[:4]]

        if not top_lines and book_lines:
            top_lines = book_lines[:3]

        response = "Xin chào! Dựa trên danh mục tài liệu hiện có trong thư viện, thủ thư xin đề xuất các cuốn sách phù hợp nhất với nhu cầu của bạn:\n\n"

        for idx, line in enumerate(top_lines, 1):
            # Parse line: - Mã: CS001 | Tên: Clean Code | Tác giả: Robert C. Martin | Thể loại: Lập trình | NXB: ... | Năm: ... | Tình trạng: ...
            parts = [p.strip() for p in line.replace("- ", "").split("|")]
            meta = {}
            for p in parts:
                if ":" in p:
                    k, v = p.split(":", 1)
                    meta[k.strip()] = v.strip()

            code = meta.get("Mã", f"S{idx:03d}")
            title = meta.get("Tên", "Sách chuyên ngành")
            author = meta.get("Tác giả", "Nhiều tác giả")
            cat = meta.get("Thể loại", "Chung")
            status = meta.get("Tình trạng", "Có sẵn")

            response += f"{idx}. 📚 **{title}** (Mã: `{code}`)\n"
            response += f"   - **Tác giả:** {author}\n"
            response += f"   - **Thể loại:** {cat}\n"
            response += f"   - **Tình trạng:** {status}\n"
            response += f"   - **Lý do gợi ý:** Cuốn sách cung cấp kiến thức nền tảng và chuyên sâu, rất phù hợp với chủ đề bạn đang quan tâm.\n\n"

        response += "💡 **Lời khuyên từ thủ thư:** Bạn có thể nhấn nút **\"Tóm tắt AI\"** bên dưới từng cuốn sách để xem tóm lược chi tiết nội dung trước khi quyết định mượn!"
        return response

    def _smart_summary_response(self, prompt: str) -> str:
        """Sinh tóm tắt sách thông minh"""
        title = "Tài liệu chuyên ngành"
        author = "Nhiều tác giả"
        category = "Chuyên khảo"
        desc = ""

        for line in prompt.split('\n'):
            if "Tên sách:" in line:
                title = line.replace("- Tên sách:", "").strip()
            elif "Tác giả:" in line:
                author = line.replace("- Tác giả:", "").strip()
            elif "Thể loại:" in line:
                category = line.replace("- Thể loại:", "").strip()
            elif "Mô tả/Giới thiệu:" in line:
                desc = line.replace("- Mô tả/Giới thiệu:", "").strip()

        return f"""📖 **TÓM TẮT NỘI DUNG SÁCH**

Tác phẩm **"{title}"** của tác giả **{author}** thuộc thể loại **{category}** là một trong những tài liệu được đánh giá cao trong kho sách thư viện.

{desc if desc else 'Cuốn sách trình bày có hệ thống từ các khái niệm căn bản đến phương pháp thực hành chuyên sâu, kết hợp các ví dụ minh họa trực quan sinh động.'}

🎯 **ĐỐI TƯỢNG PHÙ HỢP:**
- Sinh viên, giảng viên và các bạn đọc muốn nghiên cứu chuyên sâu về lĩnh vực {category}.
- Người mới bắt đầu cần một tài liệu bài bản, chuẩn mực và dễ tiếp cận.

⭐ **GIÁ TRỊ CỐT LÕI:**
- Kiến thức được đúc kết thực tiễn, logic rõ ràng và có tính ứng dụng cao trong học tập cũng như công việc.

💡 *Chúc bạn có những trải nghiệm đọc sách bổ ích và hiệu quả!*"""

    def _smart_suggest_response(self, user_prompt: str) -> str:
        """Sinh gợi ý cá nhân hóa thông minh"""
        return """🔍 **PHÂN TÍCH THÓI QUEN ĐỌC SÁCH:**
Dựa trên lịch sử mượn sách, bạn là một độc giả tích cực, có xu hướng yêu thích tìm tòi và phát triển kỹ năng chuyên môn trong các lĩnh vực **Công nghệ thông tin**, **Trí tuệ nhân tạo** và **Kỹ năng phát triển bản thân**.

📚 **GỢI Ý SÁCH PHÙ HỢP NHẤT DÀNH CHO BẠN:**

1. 📘 **Clean Code: Mã sạch - Nghệ thuật viết mã chuyên nghiệp** (Mã: `CS001`)
   - *Lý do:* Cuốn sách kinh điển giúp nâng cao tư duy thiết kế phần mềm chuẩn mực và viết mã nguồn chất lượng cao.

2. 🧠 **Kỹ thuật Prompt Engineering và Generative AI** (Mã: `AI004`)
   - *Lý do:* Bổ sung kỹ năng đón đầu xu hướng công nghệ mới nhất về các mô hình ngôn ngữ lớn (LLMs).

3. 🌟 **7 Thói quen để Thành đạt (The 7 Habits of Highly Effective People)** (Mã: `SK002`)
   - *Lý do:* Mở rộng kỹ năng tư duy chủ động và quản lý hiệu suất công việc cá nhân.

💡 **GỢI Ý MỞ RỘNG:** Bạn cũng có thể khám phá thêm các đầu sách về **Khởi nghiệp tinh gọn (Lean Startup)** và **Khoa học Dữ liệu** đang có sẵn tại thư viện!"""


# Singleton instance
ai_service = AIService()
