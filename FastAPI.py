from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text, func, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager


# Импорт из config (как в вашем коде)
from config import host, port, db_name, user, password

# URI подключения
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"

# Создаём движок
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаём сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# База для моделей
Base = declarative_base()

# Модели (как в вашем коде)
class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    title = Column(String(), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    text = Column(String(), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    chat = relationship("Chat", back_populates="messages")

# Pydantic модели для валидации
class ChatCreate(BaseModel):
    title: str

class MessageCreate(BaseModel):
    text: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при запуске приложения
    try:
        with SessionLocal() as session:
            result = session.execute(text("SELECT version();"))
            version = result.fetchone()
            print(f"[INFO] Server version: {version[0]}")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)

    yield  # Здесь приложение работает (основная логика)

    # Код, выполняемый при завершении работы (опционально)
    # Например:
    # print("[INFO] Application shutting down...")

app = FastAPI(lifespan=lifespan)


# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/chats/", response_model=list[ChatCreate])
def get_chats(db: Session = Depends(get_db)):
    chats = db.query(Chat).all()
    return chats


# Создание чата
@app.post("/chats/", response_model=ChatCreate)
def create_chat(chat_create: ChatCreate, db: Session = Depends(get_db)):
    chat = Chat(title=chat_create.title)
    db.add(chat)
    db.commit()
    db.refresh(chat)  # чтобы вернуть актуальный объект с id
    return chat

# Создание сообщения
@app.post("/chats/{chat_id}/messages/", response_model=MessageCreate)
def create_message(chat_id: int, message_create: MessageCreate, db: Session = Depends(get_db)):
    message = Message(chat_id=chat_id, text=message_create.text)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

# Удаление чата
@app.delete("/chats/{chat_id}", status_code=204)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(chat)
    db.commit()
    return

# Запуск сервера (только для разработки)
if __name__ == "__main__":
    # Создаём таблицы (если их нет)
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
