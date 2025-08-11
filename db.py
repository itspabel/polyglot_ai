import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, User, UserAIKey
from cryptography.fernet import Fernet
from config import FERNET_KEY, DB_PATH

fernet = Fernet(FERNET_KEY)
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
Session = scoped_session(sessionmaker(bind=engine))

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    Base.metadata.create_all(engine)

def encrypt_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_key(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()

def get_or_create_user(telegram_user_id):
    session = Session()
    user = session.query(User).filter_by(telegram_user_id=telegram_user_id).first()
    if not user:
        user = User(telegram_user_id=telegram_user_id, stars=0)
        session.add(user)
        session.commit()
    return user

def get_user(user_id):
    session = Session()
    return session.query(User).filter_by(telegram_user_id=user_id).first()

def set_active_ai(user_id, provider, model, api_key):
    session = Session()
    user = get_or_create_user(user_id)
    enc_key = encrypt_key(api_key)
    key = session.query(UserAIKey).filter_by(user_id=user.id, provider_name=provider).first()
    if key:
        key.encrypted_api_key = enc_key
        key.selected_model = model
    else:
        key = UserAIKey(user_id=user.id, provider_name=provider, encrypted_api_key=enc_key, selected_model=model)
        session.add(key)
    session.commit()

def get_user_keys(user_id):
    session = Session()
    user = get_or_create_user(user_id)
    return session.query(UserAIKey).filter_by(user_id=user.id).all()

def remove_ai(user_id, provider):
    session = Session()
    user = get_or_create_user(user_id)
    session.query(UserAIKey).filter_by(user_id=user.id, provider_name=provider).delete()
    session.commit()

def increment_stars(user):
    session = Session()
    user.stars += 1
    session.commit()

def get_top_donors(limit=10):
    session = Session()
    users = session.query(User).order_by(User.stars.desc()).limit(limit).all()
    return [(str(u.telegram_user_id), u.stars) for u in users]
