from sqlalchemy import create_engine, text, func, DateTime, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from config import host, port, db_name, user, password

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Формируем URI подключения
url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"

# Создаём движок (engine)
engine = create_engine(url)

# Создаём сессию
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Выполняем SQL-запрос через ORM (аналог вашего SELECT version())
    result = session.execute(text("SELECT version();"))
    version = result.fetchone()
    print(f"[INFO] Server version: {version[0]}")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    # Закрываем сессию и соединение
    session.close()
    engine.dispose()
    print("[INFO] PostgreSQL connection closed")

Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    title = Column(String(), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

# User(Base):
 #    __tablename__ = 'user'
 #    id = Column(Integer, primary_key=True)
 #    username = Column(String(20), nullable=False, unique=True)
 #    password = Column(String(10), nullable=False, unique=True)

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    #user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    text = Column(String(), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    chat = relationship("Chat", back_populates="messages")

#User.__table__.drop(engine, checkfirst=True) #Drop table
#Base.metadata.create_all(engine) #Create table


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
db = SQLAlchemy(app)

@app.route('/chats/', methods=['POST'])
def create_chat():
    data = request.get_json()
    chat = Chat(title=data['title'])
    db.session.add(chat)
    db.session.commit()
    return jsonify(chat.__dict__), 201

@app.route('/chats/<int:chat_id>/messages/', methods=['POST'])
def create_message(chat_id):
    data = request.get_json()
    message = Message(chat_id=chat_id, text=data['text'])
    db.session.add(message)
    db.session.commit()
    return jsonify(message.__dict__), 201

@app.route('/chats/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    db.session.delete(chat)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():  # Создаём контекст приложения
        db.create_all()  # Теперь это работает!
    app.run(debug=True)

