from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from apscheduler.schedulers.background import BackgroundScheduler
import os
from datetime import datetime

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = 5432
DB_NAME = os.getenv("POSTGRES_DB", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_hello_world():
    db = SessionLocal()
    new_log = Log(message="Hello World")
    db.add(new_log)
    db.commit()
    db.close()
    print(f"[{datetime.utcnow()}] Logged Hello World")

scheduler = BackgroundScheduler()
scheduler.add_job(log_hello_world, 'interval', seconds=60)  
scheduler.start()

@app.get("/logs")
def read_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).order_by(Log.timestamp.desc()).all()
    return [{"id": log.id, "message": log.message, "timestamp": log.timestamp.isoformat()} for log in logs]
