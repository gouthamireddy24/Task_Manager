from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL

# MySQL database details
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="",
    host="127.0.0.1",
    port=3306,
    database="task_manager"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()