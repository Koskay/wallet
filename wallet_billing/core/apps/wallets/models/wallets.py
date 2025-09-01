import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from core.apps.common.models import TimedBaseModel


class Wallet(TimedBaseModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Идентификатор'
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_wallet',
        verbose_name='Пользователь'
    )

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(Decimal('999999999'))],
        verbose_name='Баланс'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Статус кошелька'
    )

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'


    def __str__(self) -> str:
        return f"Кошелек пользователя {self.user.username}"

    def deposit(self, amount: Decimal):
        self.balance += amount
        self.full_clean()

    def withdrawal(self, amount: Decimal):
        self.balance -= amount
        self.full_clean()
