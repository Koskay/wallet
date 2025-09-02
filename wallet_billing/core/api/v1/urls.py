from django.http import HttpResponse
from django.middleware.csrf import get_token
from ninja import Router

from core.api.v1.wallets.handlers import router as wallets_router

router = Router()

@router.get("get-csrf", include_in_schema=False)
def get_csrf_token(request):
    token = get_token(request)
    response = HttpResponse(token)  # Передаем токен в HttpResponse
    response.set_cookie('csrftoken', token, httponly=True)  # Опционально: установка куки

router.add_router('/wallets', wallets_router)