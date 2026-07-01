"""
Todo Service - Microservice cơ bản đầu tiên
=============================================
Đây là 1 REST API đơn giản quản lý danh sách công việc (Todo).
Dữ liệu lưu trong bộ nhớ (in-memory) - mất khi restart server.
Ở giai đoạn sau ta sẽ thay bằng database thật.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------------------------------------------------------------
# 1. Khởi tạo ứng dụng FastAPI
# ----------------------------------------------------------------
app = FastAPI(
    title="Todo Service",
    description="Microservice cơ bản để học Python",
    version="1.0.0",
)

# ----------------------------------------------------------------
# 2. Định nghĩa "hình dạng" dữ liệu bằng Pydantic model
#    -> Đây gọi là "schema", giúp FastAPI tự validate dữ liệu vào/ra
# ----------------------------------------------------------------
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime


# ----------------------------------------------------------------
# 3. "Database" giả lập bằng dictionary trong bộ nhớ
# ----------------------------------------------------------------
todos_db: dict[int, Todo] = {}
next_id: int = 1


# ----------------------------------------------------------------
# 4. Các endpoint (route) - đây là phần "API" mà client sẽ gọi
# ----------------------------------------------------------------

@app.get("/")
def read_root():
    """Endpoint kiểm tra service còn sống không (health check)."""
    return {"message": "Todo Service đang chạy!", "status": "ok"}


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    """Tạo mới 1 todo."""
    global next_id
    new_todo = Todo(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=False,
        created_at=datetime.now(),
    )
    todos_db[next_id] = new_todo
    next_id += 1
    return new_todo


@app.get("/todos", response_model=list[Todo])
def list_todos(completed: Optional[bool] = None):
    """Lấy danh sách todo, có thể lọc theo trạng thái completed."""
    results = list(todos_db.values())
    if completed is not None:
        results = [t for t in results if t.completed == completed]
    return results


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """Lấy 1 todo theo id."""
    todo = todos_db.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy todo")
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, update: TodoUpdate):
    """Cập nhật 1 todo (title, description, completed)."""
    todo = todos_db.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy todo")

    update_data = update.model_dump(exclude_unset=True)
    updated_todo = todo.model_copy(update=update_data)
    todos_db[todo_id] = updated_todo
    return updated_todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    """Xoá 1 todo."""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Không tìm thấy todo")
    del todos_db[todo_id]
    return None