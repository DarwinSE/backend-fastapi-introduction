from fastapi import APIRouter

router = APIRouter(prefix = '/products', tags = ['products'], responses = {404: {'message': '404 Not Found'}})

products_list = ['Producto 1', 'Producto 2', 'Producto 3', 'Producto 4', 'Producto 5']

@router.get('/')
def products():
    return products_list

@router.get('/{product_id}')
def product(product_id: int):
    return products_list[product_id]