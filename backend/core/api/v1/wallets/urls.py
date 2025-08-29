from django.urls import path
from core.api.v1.wallets.handlers import ListUsers

urlpatterns = [
    path('wallet/', ListUsers.as_view()),
]