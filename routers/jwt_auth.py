from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt

from passlib.context import CryptContext

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl = 'login')

ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 60
SECRET = '7bb5a14b532b2c114566143462dd7f107acd84e1b5d95216ce090a0cd6b47c3c'

crypt = CryptContext(schemes = ['bcrypt'])

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserBD(User):
    password: str

users_db = {
    'lawi': {
        'username': 'lawi',
        'fullname': 'Darwin Guerra',
        'email': 'lawi@gmail.com',
        'disabled': False,
        'password': '$2a$12$An9CadrCO4Vp2F5xEIYSvuV1uutMX5oSaAbHCI7XbPK8XU7nh4nsm'
    },
    'lawi2': {
        'username': 'lawi2',
        'fullname': 'Darwin Melian',
        'email': 'lawi2@gmail.com',
        'disabled': True,
        'password': '$2a$12$0v2F7CrYyPFQALbOVZYZTuc8A7Pw3RS4sNxJV5VxVz2ldFyq6V7Ve'
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserBD(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'Credenciales de autentificacion invalidas', headers = {'www-authenticate' : 'Bearer'})

    try:
        username = jwt.decode(token, SECRET, algorithms = [ALGORITHM]).get('sub')
        if username is None:
            raise exception

    except jwt.JWTError:
        raise exception
    
    return search_user(username)
    
async def current_user(user: str = Depends(auth_user)):
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'Credenciales de autentificacion invalidas', headers = {'www-authenticate' : 'Bearer'})
    
    if user.disabled:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Usuario Inactivo')
    
    return user

@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'El usuario no es correcto')

    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'La contraseña no es correcta')

    expire = datetime.utcnow() + timedelta(seconds = ACCESS_TOKEN_DURATION)
    access_token = {'sub': user.username, 'exp': expire}
    
    return {'access_token': jwt.encode(access_token, SECRET, algorithm = ALGORITHM), 'toker_type': 'bearer'}

@router.get('/user/me')
async def get_me(user: User = Depends(current_user)):
    return user