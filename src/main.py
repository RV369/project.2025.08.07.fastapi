from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user,
    get_password_hash,
    verify_password,
)
from src.database import engine, get_db
from src.models import Base, User
from src.schemas import Token
from src.schemas import User as UserSchema
from src.schemas import UserCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post('/register', response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """Регистрация нового пользователя."""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail='Email уже зарегистрирован',
        )
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail='Имя пользователя уже занято',
        )
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """Выдача токена доступа по логину и паролю."""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/users/me', response_model=UserSchema)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> User:
    return current_user


@app.get('/protected')
async def protected_route(
    current_user: User = Depends(get_current_active_user),
) -> dict:
    return {
        'message': f'Привет, {current_user.username}! Это защищённый маршрут.',
    }
