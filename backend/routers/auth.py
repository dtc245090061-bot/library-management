"""
Router: Authentication - Đăng nhập, đăng ký, thông tin user
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date, timedelta
from database import get_db
from models.user import User, UserRole
from models.reader import Reader, ReaderType, CardStatus
from schemas import Token, UserCreate, UserOut, UserUpdate
from auth_utils import verify_password, get_password_hash, create_access_token
from dependencies import get_current_user, require_admin, require_librarian

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Đăng nhập - trả về JWT token"""
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không đúng"
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Tài khoản đã bị vô hiệu hóa")

    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới (mặc định role reader)"""
    # Kiểm tra username và email đã tồn tại chưa
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Tự động khởi tạo thẻ độc giả nếu role là reader
    if user.role == UserRole.READER:
        reader = Reader(
            user_id=user.id,
            reader_code=f"DG{user.id:04d}",
            reader_type=ReaderType.STUDENT,
            card_status=CardStatus.ACTIVE,
            card_issued_date=date.today(),
            card_expire_date=date.today() + timedelta(days=365),
            max_borrow_books=5
        )
        db.add(reader)
        db.commit()

    return user


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """Lấy thông tin user đang đăng nhập"""
    return current_user


@router.put("/me", response_model=UserOut)
async def update_me(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cập nhật thông tin cá nhân"""
    for field, value in update_data.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


# ===== ADMIN: Quản lý Users =====
@router.get("/users", response_model=dict)
async def list_users(
    keyword: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    """[Admin] Danh sách toàn bộ users"""
    query = db.query(User)
    if keyword:
        query = query.filter(
            (User.full_name.ilike(f"%{keyword}%")) |
            (User.username.ilike(f"%{keyword}%")) |
            (User.email.ilike(f"%{keyword}%"))
        )
    if role:
        try:
            query = query.filter(User.role == UserRole(role))
        except ValueError:
            pass
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    total = query.count()
    users = query.order_by(User.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    return {"total": total, "page": page, "page_size": page_size, "items": [UserOut.model_validate(u) for u in users]}


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user_by_admin(
    user_id: int,
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """[Admin] Cập nhật thông tin user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Không tìm thấy người dùng")
    if user.id == current_admin.id:
        raise HTTPException(400, "Không thể tự chỉnh sửa tài khoản của chính mình qua API này")
    for field, value in update_data.model_dump(exclude_none=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.post("/users/{user_id}/toggle-active", response_model=UserOut)
async def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """[Admin] Kích hoạt hoặc vô hiệu hóa tài khoản user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Không tìm thấy người dùng")
    if user.id == current_admin.id:
        raise HTTPException(400, "Không thể vô hiệu hóa tài khoản của chính mình")
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    return user


@router.post("/users", response_model=UserOut, status_code=201)
async def create_user_by_admin(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    """[Admin] Tạo tài khoản mới (có thể chọn role)"""
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(400, "Tên đăng nhập đã tồn tại")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(400, "Email đã tồn tại")
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Tự động tạo thẻ nếu là độc giả
    if user.role == UserRole.READER:
        reader = Reader(
            user_id=user.id,
            reader_code=f"DG{user.id:04d}",
            reader_type=ReaderType.STUDENT,
            card_status=CardStatus.ACTIVE,
            card_issued_date=date.today(),
            card_expire_date=date.today() + timedelta(days=365),
            max_borrow_books=5
        )
        db.add(reader)
        db.commit()

    return user
