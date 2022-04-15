from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from .database import get_db
from .models import User
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRES_MINUTES = settings.token_expire_time_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_token(data: dict):
    to_encode = data.copy()

    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expires_at})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id: str = payload.get('user_id')

        if user_id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(user_id=user_id)  
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

    # verify token and fetch user id from it for further manipulations in requests
    token_data = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.id == token_data.user_id).first()

    return user


