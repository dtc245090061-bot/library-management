"""
Router: Backup & Restore Database
Cung cấp API sao lưu và khôi phục CSDL SQLite
"""
import os
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from dependencies import require_admin, require_librarian, get_current_user
from models.user import User
from services.backup_service import backup_service

router = APIRouter(prefix="/api/backup", tags=["Backup & Restore"])


class CreateBackupRequest(BaseModel):
    label: Optional[str] = None


class RestoreBackupRequest(BaseModel):
    filename: str


@router.post("/create", response_model=Dict[str, Any], status_code=201)
async def create_database_backup(
    data: Optional[CreateBackupRequest] = None,
    current_user: User = Depends(require_librarian)
):
    """Tạo bản snapshot sao lưu CSDL hiện tại (Thủ thư & Admin)"""
    try:
        label = data.label if data else None
        result = backup_service.create_backup(label=label)
        return result
    except Exception as e:
        raise HTTPException(500, f"Lỗi tạo bản sao lưu: {str(e)}")


@router.get("/list", response_model=List[Dict[str, Any]])
async def list_database_backups(
    current_user: User = Depends(require_librarian)
):
    """Lấy danh sách các bản sao lưu hiện có (Thủ thư & Admin)"""
    try:
        return backup_service.list_backups()
    except Exception as e:
        raise HTTPException(500, f"Lỗi lấy danh sách sao lưu: {str(e)}")


@router.post("/restore", response_model=Dict[str, Any])
async def restore_database(
    data: RestoreBackupRequest,
    current_user: User = Depends(require_admin)
):
    """Khôi phục CSDL từ bản sao lưu (Chỉ Admin)"""
    try:
        result = backup_service.restore_backup(data.filename)
        return result
    except FileNotFoundError:
        raise HTTPException(404, f"Không tìm thấy file sao lưu '{data.filename}'")
    except ValueError as ve:
        raise HTTPException(400, f"File sao lưu không hợp lệ: {str(ve)}")
    except Exception as e:
        raise HTTPException(500, f"Lỗi khôi phục CSDL: {str(e)}")


@router.get("/download/{filename}")
async def download_backup_file(
    filename: str,
    current_user: User = Depends(require_admin)
):
    """Tải file sao lưu về máy cục bộ (Chỉ Admin)"""
    file_path = os.path.join(backup_service.backup_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "Không tìm thấy file sao lưu")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/x-sqlite3"
    )


@router.delete("/{filename}", status_code=204)
async def delete_backup_file(
    filename: str,
    current_user: User = Depends(require_admin)
):
    """Xóa một bản sao lưu (Chỉ Admin)"""
    success = backup_service.delete_backup(filename)
    if not success:
        raise HTTPException(404, "Không tìm thấy file sao lưu để xóa")
