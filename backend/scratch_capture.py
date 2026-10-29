import os
import asyncio
from playwright.async_api import async_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def capture_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        # 1. Login Page
        print("Capturing 1. Login Page...")
        await page.goto("http://127.0.0.1:8000/login", wait_until="networkidle")
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "01_login_page.png"), full_page=False)

        # Log in as librarian
        await page.click('.demo-account[data-user="thuhu01"]')
        await page.click('#login-btn')
        await page.wait_for_url("**/dashboard", timeout=10000)
        await page.wait_for_timeout(1000)

        # 2. Dashboard Page
        print("Capturing 2. Dashboard Page...")
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "02_dashboard_page.png"), full_page=False)

        # 3. Books Page
        print("Capturing 3. Books Page...")
        await page.goto("http://127.0.0.1:8000/books", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "03_books_page.png"), full_page=False)

        # Open Detail Modal & AI Summary
        first_detail_btn = await page.query_selector("button[title='Chi tiết']")
        if first_detail_btn:
            await first_detail_btn.click()
            await page.wait_for_timeout(600)
            # Click AI summary
            await page.click('#btn-ai-summary')
            await page.wait_for_timeout(1500)
            await page.screenshot(path=os.path.join(OUTPUT_DIR, "04_book_detail_ai_summary.png"), full_page=False)
            await page.click(".modal-close")
            await page.wait_for_timeout(400)

        # 4. Borrows Page
        print("Capturing 4. Borrows Page...")
        await page.goto("http://127.0.0.1:8000/borrows", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "05_borrows_page.png"), full_page=False)

        # Borrows - Fines tab
        await page.click('#tab-fines')
        await page.wait_for_timeout(800)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "06_fines_tab.png"), full_page=False)

        # Borrows - Reservations tab
        await page.click('#tab-reservations')
        await page.wait_for_timeout(800)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "07_reservations_tab.png"), full_page=False)

        # 5. Readers Page
        print("Capturing 5. Readers Page...")
        await page.goto("http://127.0.0.1:8000/readers", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "08_readers_page.png"), full_page=False)

        # 6. Statistics Page
        print("Capturing 6. Statistics Page...")
        await page.goto("http://127.0.0.1:8000/statistics", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "09_statistics_page.png"), full_page=False)

        # 7. AI Chatbot Page
        print("Capturing 7. AI Chatbot Page...")
        await page.goto("http://127.0.0.1:8000/ai-chat", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Send a quick question
        chips = await page.query_selector_all(".chip")
        if chips:
            await chips[0].click()
            await page.wait_for_timeout(2000)

        # Click AI suggest
        await page.click("button:has-text('Gợi ý dựa trên lịch sử đọc')")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "10_ai_chatbot_page.png"), full_page=False)

        await browser.close()
        print("All screenshots captured successfully in:", OUTPUT_DIR)

if __name__ == "__main__":
    asyncio.run(capture_all())
