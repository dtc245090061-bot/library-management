"""
Router: Readers (Độc giả)
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import List, Optional
import random
import re
from datetime import date, timedelta
from database import get_db
from models.reader import Reader, ReaderType, CardStatus
from models.user import User, UserRole
from schemas import ReaderCreate, ReaderUpdate, ReaderOut
from dependencies import require_librarian, require_any, get_current_user
from auth_utils import get_password_hash

router = APIRouter(prefix="/api/readers", tags=["Readers"])


@router.get("/next-code")
async def get_next_reader_code(
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Gợi ý mã thẻ độc giả tiếp theo tự động"""
    readers = db.query(Reader.reader_code).all()
    current_year = date.today().year
    prefix = f"DG{current_year}"

    max_seq = 0
    for (code,) in readers:
        # Kiểm tra mã dạng DG + 4 số năm + số thứ tự (VD: DG2024008 -> 8)
        m = re.match(r'^DG(?:\d{4})?(\d+)$', code)
        if m:
            try:
                max_seq = max(max_seq, int(m.group(1)))
            except ValueError:
                pass

    next_num = max_seq + 1
    next_code = f"{prefix}{next_num:03d}"

    # Đảm bảo mã chưa từng bị trùng
    while db.query(Reader).filter(Reader.reader_code == next_code).first():
        next_num += 1
        next_code = f"{prefix}{next_num:03d}"

    return {"next_code": next_code}


@router.get("/available-users")
async def list_available_users_without_card(
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Danh sách các tài khoản người dùng chưa được cấp thẻ độc giả"""
    existing_user_ids = db.query(Reader.user_id).all()
    used_ids = [uid for (uid,) in existing_user_ids]

    users = db.query(User).filter(
        User.id.notin_(used_ids) if used_ids else True,
        User.is_active == True
    ).all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "full_name": u.full_name,
            "email": u.email,
            "role": u.role.value
        }
        for u in users
    ]


@router.get("/", response_model=dict)
async def list_readers(
    keyword: Optional[str] = Query(None, description="Tìm theo mã thẻ hoặc tên"),
    reader_type: Optional[str] = None,
    card_status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Danh sách độc giả"""
    query = db.query(Reader).join(User)

    if keyword:
        query = query.filter(
            or_(
                Reader.reader_code.ilike(f"%{keyword}%"),
                User.full_name.ilike(f"%{keyword}%"),
                User.email.ilike(f"%{keyword}%"),
            )
        )
    if reader_type:
        query = query.filter(Reader.reader_type == reader_type)
    if card_status:
        query = query.filter(Reader.card_status == card_status)

    total = query.count()
    readers = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [ReaderOut.model_validate(r) for r in readers]
    }


@router.get("/me", response_model=ReaderOut)
async def get_my_reader_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lấy thông tin thẻ độc giả của user đang đăng nhập"""
    reader = db.query(Reader).filter(Reader.user_id == current_user.id).first()
    if not reader:
        raise HTTPException(404, "Bạn chưa có thẻ độc giả")
    return reader


@router.get("/{reader_id}", response_model=ReaderOut)
async def get_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(404, "Không tìm thấy độc giả")
    return reader


@router.post("/", response_model=ReaderOut, status_code=201)
async def create_reader(
    data: ReaderCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Tạo thẻ độc giả mới (hỗ trợ tạo tài khoản user mới hoặc liên kết user có sẵn)"""
    # 1. Kiểm tra mã thẻ đã tồn tại chưa
    if db.query(Reader).filter(Reader.reader_code == data.reader_code).first():
        raise HTTPException(400, f"Mã thẻ '{data.reader_code}' đã tồn tại")

    user_id = data.user_id

    # 2. Xử lý User
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(404, f"Không tìm thấy người dùng với ID={user_id}")
        if db.query(Reader).filter(Reader.user_id == user_id).first():
            raise HTTPException(400, f"Người dùng '{user.full_name}' (ID: {user_id}) đã có thẻ độc giả")
    else:
        # Nếu không truyền user_id, tạo luôn tài khoản User mới
        if not data.full_name:
            raise HTTPException(400, "Vui lòng nhập Họ tên độc giả hoặc chọn User ID có sẵn")

        username = data.username
        if not username:
            # Tạo username từ reader_code hoặc sinh ngẫu nhiên
            clean_code = re.sub(r'[^a-zA-Z0-9]', '', data.reader_code).lower()
            username = clean_code if clean_code else f"user_{random.randint(1000, 9999)}"

        # Đảm bảo username không trùng
        base_username = username
        counter = 1
        while db.query(User).filter(User.username == username).first():
            username = f"{base_username}_{counter}"
            counter += 1

        email = data.email
        if not email:
            email = f"{username}@library.local"
        else:
            if db.query(User).filter(User.email == email).first():
                raise HTTPException(400, f"Email '{email}' đã được sử dụng bởi tài khoản khác")

        new_user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(data.password or "123456"),
            full_name=data.full_name.strip(),
            role=UserRole.READER,
            is_active=True
        )
        db.add(new_user)
        db.flush()
        user_id = new_user.id

    # 3. Tính hạn thẻ mặc định (2 năm kể từ ngày cấp nếu không truyền)
    expire_date = data.card_expire_date
    if not expire_date:
        today = date.today()
        try:
            expire_date = today.replace(year=today.year + 2)
        except ValueError:
            expire_date = today + timedelta(days=730)

    # 4. Xác định hạn mức mượn sách theo loại độc giả
    max_books = data.max_borrow_books
    if not max_books or max_books == 5:
        if data.reader_type == ReaderType.TEACHER:
            max_books = 8
        elif data.reader_type == ReaderType.EXTERNAL:
            max_books = 3
        else:
            max_books = 5

    # 5. Tạo thẻ độc giả
    reader = Reader(
        user_id=user_id,
        reader_code=data.reader_code.strip(),
        phone=data.phone.strip() if data.phone else None,
        address=data.address.strip() if data.address else None,
        date_of_birth=data.date_of_birth,
        reader_type=data.reader_type,
        card_status=CardStatus.ACTIVE,
        card_issued_date=date.today(),
        card_expire_date=expire_date,
        max_borrow_books=max_books
    )
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


@router.put("/{reader_id}", response_model=ReaderOut)
async def update_reader(
    reader_id: int,
    data: ReaderUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    """Cập nhật thông tin độc giả"""
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(404, "Không tìm thấy độc giả")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(reader, field, value)
    db.commit()
    db.refresh(reader)
    return reader


@router.delete("/{reader_id}", status_code=204)
async def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_librarian)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(404, "Không tìm thấy độc giả")
    db.delete(reader)
    db.commit()
