from django.contrib import admin

from core.apps.wallets.models.wallets import Wallet


@admin.register(Wallet)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance')

