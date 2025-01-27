from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# run del server uvicorn main:app --reload

@app.get('/', tags = ['root'])
async def root():
    return 'Hola FastAPI'

@app.get('/url', tags = ['root'])
async def url():
    return {'url_generica': 'https://youtube.com'}

# Routers

app.include_router(products.router)
app.include_router(users.router)
app.mount('/static', StaticFiles(directory = 'static'), name = 'static')

# Documentacion propia de FastAPI http://127.0.0.1:8000/docs
# Documentacion propia de FastAPI http://127.0.0.1:8000/redoc