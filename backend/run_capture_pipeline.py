import os
import sys
import time
import subprocess
import asyncio

backend_dir = os.path.dirname(os.path.abspath(__file__))

print("🚀 Khởi động máy chủ FastAPI cục bộ...")
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=backend_dir,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(3)

try:
    print("📸 Thực thi script chụp ảnh giao diện Playwright...")
    import take_full_screenshots
    asyncio.run(take_full_screenshots.capture())
    print("✅ Đã chụp thành công tất cả các trang giao diện!")
finally:
    print("🛑 Dừng máy chủ FastAPI...")
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except Exception:
        proc.kill()
    print("✅ Đã dừng máy chủ an toàn.")
