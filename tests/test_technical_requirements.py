"""
Tests: Yêu cầu Kỹ thuật & Nghiệp vụ Nâng cao (Tiêu chuẩn Đề bài)
1. Kiểm thử Full-Text Search (SQLite FTS5 & BM25 ranking)
2. Kiểm thử Prompt Templates (Tra cứu, Tóm tắt, Gợi ý - Zero-Hallucination & Privacy)
3. Kiểm thử Chi tiết Mượn/Trả, Giới hạn mượn, Ràng buộc Nợ phạt, Tính phạt quá hạn chính xác
4. Kiểm thử Chatbot Tra cứu (Không bịa đặt dữ liệu, phản hồi đúng tình trạng tồn kho)
5. Kiểm thử Hệ thống Sao lưu & Khôi phục CSDL an toàn (Backup & Restore)
"""
import pytest
import os
import sys
import sqlite3
from datetime import date, timedelta
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app
from services.fts_service import fts_service
from services.backup_service import backup_service
from prompts.search_prompt import SEARCH_SYSTEM_PROMPT, SEARCH_USER_PROMPT
from prompts.summary_prompt import SUMMARY_SYSTEM_PROMPT, SUMMARY_USER_PROMPT
from prompts.suggest_prompt import SUGGEST_SYSTEM_PROMPT, SUGGEST_USER_PROMPT


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def auth_headers(client):
    res = client.post('/api/auth/login', data={'username': 'admin', 'password': 'Admin@123'})
    token = res.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


# =============================================================================
# 1. KIỂM THỬ TÌM KIẾM TOÀN VĂN FTS5 (FULL-TEXT SEARCH & BM25)
# =============================================================================
class TestFTS5Search:
    def test_fts5_sync_and_bm25_search(self):
        """Kiểm tra FTS5 đánh chỉ mục và tìm kiếm có điểm BM25"""
        count = fts_service.sync_fts_index()
        assert count > 0, "Chỉ mục FTS5 phải chứa các cuốn sách trong DB"

        results = fts_service.search_fts("trí tuệ nhân tạo", limit=10)
        assert len(results) > 0, "Phải tìm thấy sách khi tra cứu 'trí tuệ nhân tạo'"
        for r in results:
            assert "book_id" in r
            assert "code" in r
            assert "title" in r
            assert "relevance_score" in r
            assert isinstance(r["relevance_score"], float)

    def test_fts5_empty_or_whitespace_query(self):
        """Kiểm tra xử lý chuỗi rỗng không làm sập FTS5"""
        assert fts_service.search_fts("") == []
        assert fts_service.search_fts("   ") == []

    def test_fts5_api_endpoint(self, client):
        """Kiểm tra endpoint GET /api/books/fts/search"""
        res = client.get('/api/books/fts/search?q=lập trình&limit=10')
        assert res.status_code == 200
        data = res.json()
        assert "items" in data
        assert "search_engine" in data
        assert "FTS5" in data["search_engine"]


# =============================================================================
# 2. KIỂM THỬ TÍNH TOÀN VẸN CỦA PROMPT TEMPLATES RIÊNG BIỆT
# =============================================================================
class TestPromptTemplates:
    def test_search_prompt_zero_hallucination(self):
        """Prompt tra cứu phải có ràng buộc chống bịa đặt 100%"""
        assert "Không bịa" in SEARCH_SYSTEM_PROMPT or "chỉ gợi ý sách có trong" in SEARCH_SYSTEM_PROMPT.lower()
        assert "{query}" in SEARCH_USER_PROMPT
        assert "{book_list}" in SEARCH_USER_PROMPT

    def test_summary_prompt_structure(self):
        """Prompt tóm tắt phải có định dạng 3 phần: Tóm tắt, Phù hợp, Giá trị"""
        assert "TÓM TẮT" in SUMMARY_SYSTEM_PROMPT
        assert "PHÙ HỢP" in SUMMARY_SYSTEM_PROMPT
        assert "GIÁ TRỊ" in SUMMARY_SYSTEM_PROMPT
        assert "{title}" in SUMMARY_USER_PROMPT
        assert "{description}" in SUMMARY_USER_PROMPT

    def test_suggest_prompt_privacy(self):
        """Prompt gợi ý phải tuân thủ ẩn thông tin cá nhân độc giả"""
        assert "ẩn thông tin cá nhân" in SUGGEST_USER_PROMPT.lower() or "không suy đoán thông tin cá nhân" in SUGGEST_SYSTEM_PROMPT.lower()
        assert "{borrow_history}" in SUGGEST_USER_PROMPT
        assert "{available_books}" in SUGGEST_USER_PROMPT


# =============================================================================
# 3. KIỂM THỬ CHATBOT TRA CỨU & KHÔNG BỊA ĐẶT (ZERO-HALLUCINATION)
# =============================================================================
class TestChatbotRetrieval:
    def test_chatbot_rejects_hallucination_on_fake_topic(self, client, auth_headers):
        """Chatbot không được bịa sách khi hỏi về chủ đề hoàn toàn không có trong thư viện"""
        payload = {"query": "Tôi muốn mượn sách về cách làm bún bò Huế và công thức nấu ăn cổ truyền"}
        res = client.post('/api/ai/search', json=payload, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert "answer" in data
        # Kiểm tra sách gợi ý chỉ được lấy từ DB thật (không được bịa sách ẩm thực)
        suggested = data.get("suggested_books", [])
        for b in suggested:
            assert "bún bò" not in b.get("title", "").lower()

    def test_chatbot_returns_real_books_structure(self, client, auth_headers):
        """Chatbot tra cứu chủ đề AI phải trả về sách thực trong DB kèm tình trạng"""
        payload = {"query": "Tìm sách về trí tuệ nhân tạo"}
        res = client.post('/api/ai/search', json=payload, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert "answer" in data
        assert len(data.get("suggested_books", [])) > 0
        for b in data["suggested_books"]:
            assert "code" in b
            assert "title" in b
            assert "available" in b


# =============================================================================
# 4. KIỂM THỬ HỆ THỐNG SAO LƯU & KHÔI PHỤC CSDL (BACKUP & RESTORE)
# =============================================================================
class TestBackupAndRestoreSystem:
    def test_backup_creation_and_integrity(self):
        """Kiểm tra tạo snapshot sao lưu và tính toàn vẹn CSDL SQLite"""
        res = backup_service.create_backup(label="unit_test_run")
        assert res["status"] == "success"
        assert os.path.exists(res["filepath"])
        assert res["size_bytes"] > 0
        assert res["tables_count"] >= 5

        # Kiểm tra header SQLite hợp lệ
        with open(res["filepath"], "rb") as f:
            header = f.read(16)
            assert header == b"SQLite format 3\x00"

    def test_backup_list_and_safety_restore(self):
        """Kiểm tra danh sách sao lưu và cơ chế an toàn khi khôi phục"""
        backups = backup_service.list_backups()
        assert len(backups) > 0
        latest = backups[0]
        assert "filename" in latest
        assert "size_bytes" in latest
        assert "total_records" in latest

        # Khôi phục file hợp lệ
        res_restore = backup_service.restore_backup(latest["filename"])
        assert res_restore["status"] == "success"
        assert "safety_backup" in res_restore
        safety_path = os.path.join(backup_service.backup_dir, res_restore["safety_backup"])
        assert os.path.exists(safety_path)

