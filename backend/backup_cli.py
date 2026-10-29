"""
CLI Script: Quản lý Sao lưu & Khôi phục CSDL Thư viện
Sử dụng:
    python backend/backup_cli.py --action create [--label my_backup]
    python backend/backup_cli.py --action list
    python backend/backup_cli.py --action restore --filename <backup_file.db>
"""
import argparse
import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))
from services.backup_service import backup_service


def main():
    parser = argparse.ArgumentParser(description="CLI Quản lý Sao lưu & Khôi phục CSDL")
    parser.add_argument("--action", choices=["create", "list", "restore", "delete"], required=True,
                        help="Hành động cần thực hiện")
    parser.add_argument("--label", type=str, default=None, help="Nhãn đính kèm khi sao lưu")
    parser.add_argument("--filename", type=str, default=None, help="Tên file sao lưu khi khôi phục hoặc xóa")

    args = parser.parse_args()

    if args.action == "create":
        print("📦 Đang tiến hành tạo bản sao lưu CSDL...")
        res = backup_service.create_backup(label=args.label)
        print("✅ Sao lưu thành công!")
        print(f" - Tên file: {res['filename']}")
        print(f" - Dung lượng: {res['size_bytes'] / 1024:.1f} KB")
        print(f" - Số bảng: {res['tables_count']} | Tổng bản ghi: {res['total_records']}")

    elif args.action == "list":
        backups = backup_service.list_backups()
        print(f"📋 Danh sách các bản sao lưu ({len(backups)} bản):")
        print(f"{'Tên file':<38} | {'Thời gian tạo (UTC)':<22} | {'Dung lượng':<10} | {'Bản ghi'}")
        print("-" * 85)
        for b in backups:
            size_kb = f"{b['size_bytes'] / 1024:.1f} KB"
            print(f"{b['filename']:<38} | {b['created_at'][:19]:<22} | {size_kb:<10} | {b['total_records']}")

    elif args.action == "restore":
        if not args.filename:
            print("❌ Lỗi: Cần cung cấp --filename khi thực hiện khôi phục.")
            sys.exit(1)
        print(f"⚠️ Đang tiến hành khôi phục từ file '{args.filename}'...")
        res = backup_service.restore_backup(args.filename)
        print("✅ Khôi phục thành công!")
        print(f" - Đã khôi phục: {res['restored_tables']} bảng | {res['restored_records']} bản ghi.")
        print(f" - Đã tự động tạo bản lưu an toàn trước đó: {res['safety_backup']}")

    elif args.action == "delete":
        if not args.filename:
            print("❌ Lỗi: Cần cung cấp --filename khi thực hiện xóa.")
            sys.exit(1)
        if backup_service.delete_backup(args.filename):
            print(f"🗑️ Đã xóa bản sao lưu '{args.filename}'.")
        else:
            print(f"❌ Không tìm thấy file '{args.filename}'.")


if __name__ == "__main__":
    main()
