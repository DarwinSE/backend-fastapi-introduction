from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Entidad Users

class User(BaseModel):
    id: int
    name: str
    surname: str
    alias: str
    age: int

user_list = [
    User(id = 1, name = 'Darwin', surname = 'Guerra', alias = 'Lawi', age = 24),
    User(id = 2, name = 'Ashley', surname = 'Garcia', alias = 'Azh', age = 28)
]

@app.get('/usersjson')
async def usersjson():
    return [
        {'name': 'Darwin', 'surname': 'Guerra', 'alias': 'Lawi', 'age': 24},
        {'name': 'Ashley', 'surname': 'Garcia', 'alias': 'Azh', 'age': 28}
        ]

def search_users(id: int):
    user_id = filter(lambda user: user.id == id, user_list)
    try:
        return list(user_id)[0]
    except:
        return {'error': 'No se ha encontrado el usuario'}

# Path
# http://127.0.0.1:8000/user/2
@app.get('/users')
async def users():
    return user_list

@app.get('/user/{id}')
async def user(id: int):
    return search_users(id)
    
# Query
# http://127.0.0.1:8000/user/?id=2
@app.get('/user')
async def user(id: int):
    return search_users(id)

@app.post('/user', response_model = User, status_code = 201)
async def post_user(user: User):
    if type(search_users(user.id)) == User:
        raise HTTPException(status_code = 204, detail = 'El usuario ya existe')
    
    user_list.append(user)
    return {'message': 'Usuario creado con éxito'}

@app.put('/user')
async def update_user(user: User):
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            return {'message': 'Usuario actualizado con éxito'}
        
    return {'error': 'El usuario no existe'}

@app.delete('/user/{id}')
async def delete_user(id: int):
    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            return {'message': 'Usuario eliminado con éxito'}
        
    return {'error': 'No se ha podido eliminar el usuario'}