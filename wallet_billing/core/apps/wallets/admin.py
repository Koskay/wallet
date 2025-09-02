from django.contrib import admin

from core.apps.wallets.models.transaction import WalletTransaction
from core.apps.wallets.models.wallets import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance')


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance_after')

