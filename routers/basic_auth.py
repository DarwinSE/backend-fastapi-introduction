from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl = 'login')

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
        'password': '123456'
    },
    'lawi2': {
        'username': 'lawi2',
        'fullname': 'Darwin Melian',
        'email': 'lawi2@gmail.com',
        'disabled': True,
        'password': '654321'
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserBD(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
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
    if not form.password == user.password:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'La contraseña no es correcta')
    
    return {'access_token': user.username, 'toker_type': 'bearer'}

@router.get('/user/me')
async def get_me(user: User = Depends(current_user)):
    return user