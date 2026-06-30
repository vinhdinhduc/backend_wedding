# 🎉 Hệ Thống Quản Lý & Tra Cứu Tiền Mừng Dịch Vụ

Backend API được xây dựng với **FastAPI** + **MySQL** + **SQLAlchemy**.

## 📋 Yêu Cầu

- Python 3.12+
- MySQL 8.0+ (hoặc MariaDB)
- Virtual environment

## 🚀 Cài Đặt & Chạy

### 1. Tạo Virtual Environment

```bash
cd backend_wedding
python -m venv .venv
.\.venv\Scripts\activate  # Windows
```

### 2. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### 3. Tạo Database & Dữ Liệu Mẫu

#### Cách 1: Dùng SQL Script (Nhanh nhất)

```bash
# Mở MySQL CLI
mysql -u root -p

# Trong MySQL:
SOURCE setup.sql;
```

#### Cách 2: Dùng Alembic Migration (Recommended)

```bash
# Tạo database rỗng trước
mysql -u root -e "CREATE DATABASE IF NOT EXISTS tienmung_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Chạy migration
alembic upgrade head
```

### 4. Cấu Hình `.env`

```bash
cp .env.example .env
```

Cập nhật nếu cần:

```env
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/tienmung_db
SECRET_KEY=your-secret-key-here
APP_ENV=development
```

### 5. Chạy Server

```bash
uvicorn src.main.app:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: `http://localhost:8000`

- API Docs: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 📊 Cấu Trúc Dữ Liệu

### 8 Bảng Chính:

1. **ho_gia_dinh** — Tài khoản hộ gia đình
2. **loai_su_kien** — Danh mục loại sự kiện (Cưới, Tân gia, v.v.)
3. **nguoi** — Danh sách người quen
4. **su_kien** — Các sự kiện phát sinh (cưới, tang, sinh nhật...)
5. **lan_mung** — Chiều VÀO (ai đến mừng mình)
6. **lan_di_mung** — Chiều RA (mình đi mừng ai)
7. **trang_thai_mung_lai** — Trạng thái mừng lại
8. **lich_su_chinh_sua** — Log lịch sử thay đổi dữ liệu

### Dữ Liệu Mẫu:

- 2 hộ gia đình
- 6 người quen (3 người/hộ)
- 6 sự kiện
- 7 lần mừng (chiều vào)
- 3 lần đi mừng (chiều ra)

## 🔧 Các Lệnh Hữu Ích

### Chạy Migration

```bash
# Tạo migration mới
alembic revision --autogenerate -m "Description"

# Áp dụng migration
alembic upgrade head

# Revert migration
alembic downgrade -1
```

### Chạy Tests (Nếu có)

```bash
pytest
```

### Format Code

```bash
black src/
```

## 📝 API Endpoints (Ready)

- `POST /auth/register` — Đăng ký tài khoản
- `POST /auth/login` — Đăng nhập
- `POST /auth/logout` — Đăng xuất

(Thêm các endpoint khác sau)

## 🐛 Troubleshooting

### Error: `No module named 'aiomysql'`

```bash
pip install aiomysql pymysql
```

### Error: `(1045, "Access denied for user 'root'@'localhost'`"

Kiểm tra DATABASE_URL trong `.env`:

```env
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/tienmung_db
```

### Error: `Unknown database 'tienmung_db'`

Tạo database trước:

```bash
mysql -u root -p -e "CREATE DATABASE tienmung_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

## 📚 Tài Liệu Tham Khảo

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
