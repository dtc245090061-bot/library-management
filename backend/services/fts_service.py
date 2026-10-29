"""
Service: Full-Text Search (FTS5) for Books
Cung cấp khả năng tìm kiếm toàn văn siêu tốc và xếp hạng độ khớp (BM25)
bằng SQLite FTS5 theo đề xuất nâng cao ở Mục 4 của Đề tài.
"""
import sqlite3
import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "library.db"))


class FTSService:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_fts_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_fts_table(self):
        """Khởi tạo bảng ảo FTS5 nếu chưa có"""
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS books_fts USING fts5(
                    book_id UNINDEXED,
                    code,
                    title,
                    author_name,
                    category_name,
                    publisher,
                    description,
                    tokenize='unicode61 remove_diacritics 1'
                );
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.warning(f"Không thể tạo bảng books_fts: {e}")

    def sync_fts_index(self):
        """Đồng bộ toàn bộ sách từ bảng books vào books_fts"""
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            
            # Xóa chỉ mục cũ và nạp mới
            cur.execute("DELETE FROM books_fts;")
            cur.execute("""
                INSERT INTO books_fts (book_id, code, title, author_name, category_name, publisher, description)
                SELECT 
                    b.id,
                    b.code,
                    b.title,
                    COALESCE(a.name, ''),
                    COALESCE(c.name, ''),
                    COALESCE(b.publisher, ''),
                    COALESCE(b.description, '')
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.id
                LEFT JOIN categories c ON b.category_id = c.id
                WHERE b.is_active = 1;
            """)
            conn.commit()
            total_indexed = cur.rowcount
            conn.close()
            logger.info(f"✅ Đã đồng bộ {total_indexed} cuốn sách vào SQLite FTS5 index.")
            return total_indexed
        except Exception as e:
            logger.warning(f"Lỗi đồng bộ FTS: {e}")
            return 0

    def search_fts(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Tìm kiếm toàn văn FTS5 với xếp hạng độ liên quan BM25 (rank).
        Hỗ trợ tìm kiếm từ khóa ghép, tiền tố (prefix) và lọc tiếng Việt.
        """
        if not query or not query.strip():
            return []

        clean_query = query.strip().replace('"', '""').replace("'", "''")
        # Thêm prefix search cho từ cuối cùng
        words = clean_query.split()
        if words:
            fts_expression = " ".join(f'"{w}"*' for w in words)
        else:
            fts_expression = f'"{clean_query}"*'

        try:
            conn = self._get_connection()
            cur = conn.cursor()
            
            sql = """
                SELECT 
                    book_id,
                    code,
                    title,
                    author_name,
                    category_name,
                    publisher,
                    bm25(books_fts) AS rank_score
                FROM books_fts
                WHERE books_fts MATCH ?
                ORDER BY rank_score ASC
                LIMIT ?;
            """
            cur.execute(sql, (fts_expression, limit))
            rows = cur.fetchall()
            conn.close()

            results = []
            for r in rows:
                results.append({
                    "book_id": r[0],
                    "code": r[1],
                    "title": r[2],
                    "author": r[3],
                    "category": r[4],
                    "publisher": r[5],
                    "relevance_score": float(-r[6])  # BM25 số âm càng nhỏ càng khớp, đảo dấu để trực quan
                })
            return results
        except Exception as e:
            logger.warning(f"FTS query error '{query}': {e}. Fallback sang rỗng.")
            return []


fts_service = FTSService()
