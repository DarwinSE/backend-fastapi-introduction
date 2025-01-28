from fastapi import APIRouter, HTTPException, status

from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema

router = APIRouter(prefix = '/userdb', tags = ['users'])

user_list = []

def search_users(id: int):
    user_id = filter(lambda user: user.id == id, user_list)
    try:
        return list(user_id)[0]
    except:
        return {'error': 'No se ha encontrado el usuario'}
    
@router.get('/')
async def users():
    return user_list

@router.get('/{id}')
async def user(id: int):
    return search_users(id)

@router.get('/')
async def user(id: int):
    return search_users(id)

@router.post('/', response_model = User, status_code = status.HTTP_201_CREATED)
async def post_user(user: User):
    #if type(search_users(user.id)) == User:
    #    raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = 'El usuario ya existe')
    
    user_dict = dict(user)
    del user_dict['id']

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({'_id': id}))

    return User(**new_user)

@router.put('/')
async def update_user(user: User):
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            return {'message': 'Usuario actualizado con éxito'}
        
    return {'error': 'El usuario no existe'}

@router.delete('/{id}')
async def delete_user(id: int):
    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            return {'message': 'Usuario eliminado con éxito'}
        
    return {'error': 'No se ha podido eliminar el usuario'}