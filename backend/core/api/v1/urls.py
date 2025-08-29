from django.urls import path, include

urlpatterns = [
    path('wallets/', include('core.api.v1.wallets.urls')),
]