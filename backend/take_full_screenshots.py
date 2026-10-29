import os
import sys
import time
import subprocess
import asyncio
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SCREENSHOTS_DIR = os.path.join(DOCS_DIR, "screenshots")
IMAGES_DIR = os.path.join(DOCS_DIR, "images")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

async def capture():
    print("🚀 Bắt đầu khởi chạy Playwright để chụp ảnh giao diện...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
        page = await context.new_page()

        base_url = "http://127.0.0.1:8000"

        # 1. Login Page
        print("📸 1. Chụp trang Đăng nhập...")
        await page.goto(f"{base_url}/login", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        img1 = os.path.join(SCREENSHOTS_DIR, "ui_01_login.png")
        await page.screenshot(path=img1)
        await page.screenshot(path=os.path.join(IMAGES_DIR, "01_login_page.png"))
        print("  ✅ ui_01_login.png")

        # Đăng nhập Admin
        print("🔑 Đăng nhập tài khoản Admin...")
        try:
            demo_btn = await page.query_selector('.demo-account[data-user="admin"]')
            if demo_btn:
                await demo_btn.click()
            else:
                await page.fill("#username", "admin")
                await page.fill("#password", "admin123")
            await page.click("#login-btn")
            await page.wait_for_url(f"{base_url}/dashboard", timeout=10000)
        except Exception as e:
            print("  Fallback login fill:", e)
            await page.fill("#username", "admin")
            await page.fill("#password", "admin123")
            await page.click("#login-btn")
            await page.wait_for_url(f"{base_url}/dashboard", timeout=10000)

        await page.wait_for_timeout(1500)

        # 2. Dashboard
        print("📸 2. Chụp trang Dashboard...")
        img2 = os.path.join(SCREENSHOTS_DIR, "ui_02_dashboard.png")
        await page.screenshot(path=img2)
        await page.screenshot(path=os.path.join(IMAGES_DIR, "02_dashboard_page.png"))
        print("  ✅ ui_02_dashboard.png")

        # 3. Books Management
        print("📸 3. Chụp trang Quản lý Sách...")
        await page.goto(f"{base_url}/books", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        img3 = os.path.join(SCREENSHOTS_DIR, "ui_03_books.png")
        await page.screenshot(path=img3)
        await page.screenshot(path=os.path.join(IMAGES_DIR, "03_books_page.png"))
        print("  ✅ ui_03_books.png")

        # 4. Readers Management
        print("📸 4. Chụp trang Quản lý Độc giả...")
        await page.goto(f"{base_url}/readers", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        img4 = os.path.join(SCREENSHOTS_DIR, "ui_04_readers.png")
        await page.screenshot(path=img4)
        await page.screenshot(path=os.path.join(IMAGES_DIR, "08_readers_page.png"))
        print("  ✅ ui_04_readers.png")

        # 5. Borrows Management
        print("📸 5. Chụp trang Mượn / Trả Sách...")
        await page.goto(f"{base_url}/borrows", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        img5 = os.path.join(SCREENSHOTS_DIR, "ui_05_borrows.png")
        await page.screenshot(path=img5)
        await page.screenshot(path=os.path.join(IMAGES_DIR, "05_borrows_page.png"))
        print("  ✅ ui_05_borrows.png")

        # 6. Fines Tab
        print("📸 6. Chụp Tab Quản lý Phạt...")
        try:
            fines_tab = await page.query_selector("#tab-fines, button[data-tab='fines'], a[href='#fines']")
            if fines_tab:
                await fines_tab.click()
                await page.wait_for_timeout(800)
            img6 = os.path.join(SCREENSHOTS_DIR, "ui_06_fines.png")
            await page.screenshot(path=img6)
            await page.screenshot(path=os.path.join(IMAGES_DIR, "06_fines_tab.png"))
            print("  ✅ ui_06_fines.png")
        except Exception as e:
            print("  Lỗi chụp tab fines:", e)

        # 7. Reservations Tab
        print("📸 7. Chụp Tab Đặt trước...")
        try:
            res_tab = await page.query_selector("#tab-reservations, button[data-tab='reservations'], a[href='#reservations']")
            if res_tab:
                await res_tab.click()
                await page.wait_for_timeout(800)
            img7 = os.path.join(SCREENSHOTS_DIR, "ui_07_reservations.png")
            await page.screenshot(path=img7)
            await page.screenshot(path=os.path.join(IMAGES_DIR, "07_reservations_tab.png"))
            print("  ✅ ui_07_reservations.png")
        except Exception as e:
            print("  Lỗi chụp tab reservations:", e)

        # 8. Statistics Page
        print("📸 8. Chụp trang Thống kê & Báo cáo...")
        await page.goto(f"{base_url}/statistics", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        img8 = os.path.join(SCREENSHOTS_DIR, "ui_08_statistics.png")
        await page.screenshot(path=img8)
        await page.screenshot(path=os.path.join(IMAGES_DIR, "09_statistics_page.png"))
        print("  ✅ ui_08_statistics.png")

        # 9. AI Chatbot Page
        print("📸 9. Chụp trang Trợ lý AI Chatbot...")
        await page.goto(f"{base_url}/ai-chat", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        img9 = os.path.join(SCREENSHOTS_DIR, "ui_09_ai_chatbot.png")
        await page.screenshot(path=img9)
        await page.screenshot(path=os.path.join(IMAGES_DIR, "10_ai_chatbot_page.png"))
        print("  ✅ ui_09_ai_chatbot.png")

        # 10. Users Management
        print("📸 10. Chụp trang Quản lý Tài khoản...")
        await page.goto(f"{base_url}/users", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        img10 = os.path.join(SCREENSHOTS_DIR, "ui_10_users.png")
        await page.screenshot(path=img10)
        await page.screenshot(path=os.path.join(IMAGES_DIR, "11_users_page.png"))
        print("  ✅ ui_10_users.png")

        await browser.close()
        print("🎉 Hoàn tất chụp toàn bộ 10 ảnh giao diện Web!")

if __name__ == "__main__":
    asyncio.run(capture())
