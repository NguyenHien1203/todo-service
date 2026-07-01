from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import httpx

import models
import schemas
from database import SessionLocal, engine

# ----------------------------------------------------------------
# 1. Tạo bảng trong database (nếu chưa có)
# ----------------------------------------------------------------
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo Service",
    description="Microservice co ban - goi sang User Service",
    version="3.0.0",
)

USER_SERVICE_URL = "http://127.0.0.1:8001"

# ----------------------------------------------------------------
# 2. Dependency: mở session DB cho mỗi request, tự đóng khi xong
# ----------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        # ----------------------------------------------------------------
# 3. Các endpoint
# ----------------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Todo Service dang chay!", "status": "ok"}


@app.post("/todos", response_model=schemas.Todo, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    # Gọi sang user-service để kiểm tra user có tồn tại không
    try:
        response = httpx.get(f"{USER_SERVICE_URL}/users/{todo.user_id}", timeout=5.0)
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Khong the ket noi toi User Service"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=400,
            detail=f"User id {todo.user_id} khong ton tai"
        )

    # User hợp lệ -> tạo todo
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        user_id=todo.user_id,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/todos", response_model=list[schemas.Todo])
def list_todos(completed: bool | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Todo)
    if completed is not None:
        query = query.filter(models.Todo.completed == completed)
    return query.all()


@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Khong tim thay todo")
    return todo


@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, update: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Khong tim thay todo")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Khong tim thay todo")
    db.delete(todo)
    db.commit()
    return None