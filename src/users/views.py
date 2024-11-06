from fastapi import APIRouter
from .valid_customers import Customer
from users import crud

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/')
def create_user(user: Customer):
    """Создание пользователя."""
    return crud.create_user(user_in=user)
