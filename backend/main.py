"""
Main FastAPI Application - Hệ thống Quản lý Thư viện
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

# Import database và models
from database import engine, Base
import models  # noqa - trigger model registration

# Import routers
from routers.auth import router as auth_router
from routers.books import router as books_router, category_router, author_router
from routers.readers import router as readers_router
from routers.borrows import router as borrows_router, fine_router
from routers.reservations import router as reservations_router
from routers.statistics import router as statistics_router
from routers.ai import router as ai_router
from routers.backup import router as backup_router


# ===== LIFESPAN =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup và shutdown events"""
    # Tạo bảng CSDL
    Base.metadata.create_all(bind=engine)
    # Tạo dữ liệu mẫu khi khởi động lần đầu
    from seed_data import seed_database
    seed_database()
    # Đồng bộ chỉ mục tìm kiếm toàn văn FTS5
    from services.fts_service import fts_service
    fts_service.sync_fts_index()
    print("🚀 Ứng dụng thư viện đã khởi động!")
    print("📖 Truy cập: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/api/docs")
    yield
    # Shutdown: dọn dẹp nếu cần


app = FastAPI(
    title="📚 Hệ thống Quản lý Thư viện",
    description="Library Management System với tích hợp AI - FastAPI + SQLite + Gemini",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files và templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ===== API ROUTERS =====
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(category_router)
app.include_router(author_router)
app.include_router(readers_router)
app.include_router(borrows_router)
app.include_router(fine_router)
app.include_router(reservations_router)
app.include_router(statistics_router)
app.include_router(ai_router)
app.include_router(backup_router)


# ===== FRONTEND ROUTES =====
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/books", response_class=HTMLResponse)
async def books_page(request: Request):
    return templates.TemplateResponse("books/index.html", {"request": request})


@app.get("/readers", response_class=HTMLResponse)
async def readers_page(request: Request):
    return templates.TemplateResponse("readers/index.html", {"request": request})


@app.get("/borrows", response_class=HTMLResponse)
async def borrows_page(request: Request):
    return templates.TemplateResponse("borrows/index.html", {"request": request})


@app.get("/statistics", response_class=HTMLResponse)
async def statistics_page(request: Request):
    return templates.TemplateResponse("statistics/index.html", {"request": request})


@app.get("/ai-chat", response_class=HTMLResponse)
async def ai_chat_page(request: Request):
    return templates.TemplateResponse("ai/chatbot.html", {"request": request})


@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    """Trang quản lý tài khoản (chỉ Admin)"""
    return templates.TemplateResponse("users/index.html", {"request": request})


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": "Library Management System"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
