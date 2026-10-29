import os
import shutil
import asyncio
from playwright.async_api import async_playwright
from PIL import Image

# Import toàn bộ 18 sơ đồ và logic render chuẩn Ultra-HD
from render_ultra_hd_diagrams import (
    ULTRA_HD_DIAGRAMS,
    HTML_RENDER_TEMPLATE,
    MAPPING_NAMES,
    render_all_ultra_hd,
    DIAGRAMS_DIR,
    SCREENSHOTS_DIR,
    MAIN_OUTPUT_DIR
)

async def capture_ui_screenshots():
    print("📸 Đang chụp ảnh màn hình các trang giao diện Web thực tế (Retina 2K)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)

        base_url = "http://localhost:8000"

        try:
            # 1. Login Page
            await page.goto(f"{base_url}/", timeout=10000)
            await page.wait_for_timeout(1000)
            await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_01_login.png"))
            print("  ✅ Chụp: ui_01_login.png")

            # Login as Admin
            await page.fill("#username", "admin")
            await page.fill("#password", "Admin@123")
            await page.click("#login-btn")
            await page.wait_for_url(f"{base_url}/dashboard")
            await page.wait_for_timeout(1500)

            # 2. Dashboard
            await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_02_dashboard.png"))
            print("  ✅ Chụp: ui_02_dashboard.png")

            # 3. Books
            await page.goto(f"{base_url}/books")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_03_books.png"))
            print("  ✅ Chụp: ui_03_books.png")

            # 4. Readers
            await page.goto(f"{base_url}/readers")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_04_readers.png"))
            print("  ✅ Chụp: ui_04_readers.png")

            # 5. Borrows
            await page.goto(f"{base_url}/borrows")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_05_borrows.png"))
            print("  ✅ Chụp: ui_05_borrows.png")

            # 6. Fines
            try:
                await page.click("#tab-fines")
                await page.wait_for_timeout(600)
                await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_06_fines.png"))
                print("  ✅ Chụp: ui_06_fines.png")
            except Exception:
                pass

            # 7. Reservations
            try:
                await page.click("#tab-reservations")
                await page.wait_for_timeout(600)
                await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_07_reservations.png"))
                print("  ✅ Chụp: ui_07_reservations.png")
            except Exception:
                pass

            # 8. Statistics
            await page.goto(f"{base_url}/statistics")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_08_statistics.png"))
            print("  ✅ Chụp: ui_08_statistics.png")

            # 9. AI Chatbot
            await page.goto(f"{base_url}/ai-chat")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_09_ai_chatbot.png"))
            print("  ✅ Chụp: ui_09_ai_chatbot.png")

            # 10. Users
            await page.goto(f"{base_url}/users")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "ui_10_users.png"))
            print("  ✅ Chụp: ui_10_users.png")
        except Exception as e:
            print(f"⚠️ Lưu ý khi chụp UI (Server backend có thể chưa bật): {e}")

        await browser.close()

async def main():
    await render_all_ultra_hd()
    # Chụp UI screenshots nếu server đang chạy
    # await capture_ui_screenshots()
    print("🎉 Toàn bộ sơ đồ Ultra-HD đã được đồng bộ!")

if __name__ == "__main__":
    asyncio.run(main())
