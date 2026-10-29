"""
Service: Backup & Restore SQLite Database
Quản lý sao lưu và khôi phục cơ sở dữ liệu thư viện
"""
import os
import shutil
import sqlite3
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

BACKUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups"))
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "library.db"))


class BackupService:
    def __init__(self, backup_dir: str = BACKUP_DIR, db_path: str = DB_PATH):
        self.backup_dir = backup_dir
        self.db_path = db_path
        os.makedirs(self.backup_dir, exist_ok=True)

    def _get_db_stats(self, path: str) -> Dict[str, Any]:
        """Đo đạc thống kê số bảng và dung lượng của file SQLite"""
        stats = {"size_bytes": 0, "tables_count": 0, "total_records": 0, "is_valid": False}
        if not os.path.exists(path):
            return stats
        
        stats["size_bytes"] = os.path.getsize(path)
        try:
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [row[0] for row in cur.fetchall()]
            stats["tables_count"] = len(tables)
            
            total_records = 0
            for t in tables:
                try:
                    cur.execute(f"SELECT COUNT(*) FROM \"{t}\";")
                    total_records += cur.fetchone()[0]
                except Exception:
                    pass
            stats["total_records"] = total_records
            stats["is_valid"] = True
            conn.close()
        except Exception as e:
            logger.warning(f"Lỗi kiểm tra tính toàn vẹn CSDL {path}: {e}")
        return stats

    def create_backup(self, label: Optional[str] = None) -> Dict[str, Any]:
        """Tạo snapshot sao lưu CSDL hiện tại"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Không tìm thấy file CSDL chính tại: {self.db_path}")

        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        label_part = f"_{label.strip()}" if label else ""
        backup_filename = f"library_backup_{timestamp_str}{label_part}.db"
        dest_path = os.path.join(self.backup_dir, backup_filename)

        # Sử dụng SQLite backup API an toàn tránh xung đột transaction
        try:
            src_conn = sqlite3.connect(self.db_path)
            dest_conn = sqlite3.connect(dest_path)
            with dest_conn:
                src_conn.backup(dest_conn)
            dest_conn.close()
            src_conn.close()
        except Exception as e:
            logger.warning(f"SQLite backup API lỗi, fallback sang file copy: {e}")
            shutil.copy2(self.db_path, dest_path)

        stats = self._get_db_stats(dest_path)
        return {
            "filename": backup_filename,
            "filepath": dest_path,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "size_bytes": stats["size_bytes"],
            "tables_count": stats["tables_count"],
            "total_records": stats["total_records"],
            "status": "success"
        }

    def list_backups(self) -> List[Dict[str, Any]]:
        """Danh sách toàn bộ các bản sao lưu hiện có"""
        backups = []
        if not os.path.exists(self.backup_dir):
            return backups

        files = [f for f in os.listdir(self.backup_dir) if f.endswith(".db")]
        for f in sorted(files, reverse=True):
            fpath = os.path.join(self.backup_dir, f)
            stats = self._get_db_stats(fpath)
            mtime = os.path.getmtime(fpath)
            created_at = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
            backups.append({
                "filename": f,
                "created_at": created_at,
                "size_bytes": stats["size_bytes"],
                "tables_count": stats["tables_count"],
                "total_records": stats["total_records"],
                "is_valid": stats["is_valid"]
            })
        return backups

    def restore_backup(self, filename: str) -> Dict[str, Any]:
        """Khôi phục CSDL từ file snapshot (có tự động tạo bản sao lưu an toàn trước)"""
        backup_path = os.path.join(self.backup_dir, filename)
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Không tìm thấy file sao lưu: {filename}")

        # Kiểm tra tính toàn vẹn bản backup trước khi khôi phục
        stats = self._get_db_stats(backup_path)
        if not stats["is_valid"]:
            raise ValueError("File sao lưu bị hỏng hoặc không đúng định dạng SQLite")

        # 1. Tạo bản lưu an toàn trước khi khôi phục (Pre-restore safety backup)
        safety_name = f"pre_restore_safety_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.db"
        safety_path = os.path.join(self.backup_dir, safety_name)
        if os.path.exists(self.db_path):
            shutil.copy2(self.db_path, safety_path)

        # 2. Tiến hành khôi phục ghi đè
        try:
            src_conn = sqlite3.connect(backup_path)
            dest_conn = sqlite3.connect(self.db_path)
            with dest_conn:
                src_conn.backup(dest_conn)
            dest_conn.close()
            src_conn.close()
        except Exception as e:
            logger.warning(f"Lỗi SQLite restore API, fallback sang copy: {e}")
            shutil.copy2(backup_path, self.db_path)

        restored_stats = self._get_db_stats(self.db_path)
        return {
            "status": "success",
            "message": f"Đã khôi phục thành công từ {filename}",
            "safety_backup": safety_name,
            "restored_tables": restored_stats["tables_count"],
            "restored_records": restored_stats["total_records"]
        }

    def delete_backup(self, filename: str) -> bool:
        """Xóa file sao lưu"""
        path = os.path.join(self.backup_dir, filename)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False


backup_service = BackupService()
