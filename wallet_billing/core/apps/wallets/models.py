import uuid
from decimal import Decimal

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
        validators=[MinValueValidator(0)],
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


class TransactionStatus(models.TextChoices):
    SUCCESS = 'success', 'Успешно'
    IN_PROCESSING = 'in_processing', 'В обработке'
    CANCELED = 'canceled', 'Отменена'
    FAILED = 'failed', 'Ошибка'


class OperationType(models.TextChoices):
    OPERATION_DEPOSIT = 'deposit', 'Пополнение'
    OPERATION_WITHDRAW = 'withdraw', 'Списание'


class WalletTransaction(TimedBaseModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Идентификатор'
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Кошелек'
    )

    operation_type = models.CharField(
        max_length=32,
        choices=OperationType.choices,
        verbose_name='Тип операции'
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Сумма'
    )

    balance_after = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )

    balance_before = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )

    status = models.CharField(
        max_length=32,
        choices=TransactionStatus.choices,
    )


    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']


    def __str__(self) -> str:
        return f"{self.operation_type} {self.amount} для {self.wallet.id}"