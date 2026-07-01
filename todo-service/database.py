from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Đường dẫn tới file database SQLite (sẽ tự tạo file todo.db nếu chưa có)
SQLALCHERY_DATABASE_URL = "sqlite:///./todo.db"

# "engine" là đối tượng quản lý kết nối tới database
engine = create_engine(
    SQLALCHERY_DATABASE_URL,
    connect_args={"check_same_thread" : False}
)

# SessionLocal là "nhà máy" tạo ra các session (phiên làm việc với DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base là class gốc mà mọi model (bảng) sẽ kế thừa
Base = declarative_base()