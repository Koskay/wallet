import uuid

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
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
        validators=[MinValueValidator(0)], #  в теории, баланс может быть отрицательным, тут зависит от условий бизнеса
        verbose_name='Баланс'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Статус кошелька'
    )

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'


