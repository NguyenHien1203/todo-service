# Todo Service - Bước 1: Microservice cơ bản

## Cài đặt

```bash
# 1. Tạo môi trường ảo (khuyên dùng để không làm rối Python hệ thống)
python -m venv venv

# 2. Kích hoạt môi trường ảo
# Trên macOS/Linux:
source venv/bin/activate
# Trên Windows:
venv\Scripts\activate

# 3. Cài thư viện
pip install -r requirements.txt
```

## Chạy service

```bash
uvicorn main:app --reload
```

Sau đó mở trình duyệt:
- API: http://127.0.0.1:8000
- **Tài liệu tương tác (Swagger UI)**: http://127.0.0.1:8000/docs ← Vào đây để thử API trực tiếp!

## Thử nghiệm bằng curl

```bash
# Tạo todo mới
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Học FastAPI", "description": "Đọc docs"}'

# Xem danh sách todo
curl http://127.0.0.1:8000/todos

# Xem 1 todo theo id
curl http://127.0.0.1:8000/todos/1

# Cập nhật todo (đánh dấu hoàn thành)
curl -X PUT http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Xoá todo
curl -X DELETE http://127.0.0.1:8000/todos/1
```

## Giải thích các khái niệm quan trọng

| Khái niệm | Giải thích |
|---|---|
| `FastAPI()` | Khởi tạo 1 ứng dụng web. Đây là "trái tim" của service. |
| `BaseModel` (Pydantic) | Định nghĩa hình dạng dữ liệu. FastAPI tự động validate: nếu client gửi sai kiểu dữ liệu (VD: title là số thay vì chữ), API tự trả lỗi 422 mà bạn không cần code gì thêm. |
| `@app.get`, `@app.post`... | Decorator gắn 1 hàm Python với 1 URL + HTTP method. Đây chính là "route". |
| `response_model` | Khai báo dữ liệu trả về đúng hình dạng nào, giúp tự sinh docs và lọc field thừa. |
| `HTTPException` | Cách chuẩn để trả lỗi HTTP (404, 400...) từ trong logic Python. |
| `todos_db: dict` | "Database" giả bằng dictionary. Khi tắt server, dữ liệu mất — đây là lý do bước tiếp theo ta sẽ thêm SQLite. |
| `--reload` (uvicorn) | Tự động restart server mỗi khi bạn sửa code, tiện khi phát triển. |

## Vì sao gọi đây là 1 "microservice"?

Ở bước này nó chỉ là 1 service đơn lẻ — nhưng nó đã có đủ đặc điểm nền tảng của microservice:
- Có ranh giới rõ ràng (chỉ lo về "Todo", không lo việc khác)
- Giao tiếp qua HTTP/REST theo chuẩn
- Có thể chạy độc lập, đóng gói riêng (bước sau sẽ Docker hoá)

Bước tiếp theo: thêm **database thật (SQLite + SQLAlchemy)** để dữ liệu không mất khi restart, sau đó tách thêm 1 service thứ hai để 2 service giao tiếp với nhau — đúng chất "micro-services" (số nhiều).