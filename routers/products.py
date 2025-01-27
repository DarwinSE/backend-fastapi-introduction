from fastapi import APIRouter

router = APIRouter()

@router.get('/products')
def products():
    return ['Producto 1', 'Producto 2', 'Producto 3', 'Producto 4', 'Producto 5']