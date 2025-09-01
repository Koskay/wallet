import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from core.apps.common.enums import OperationType, TransactionStatus
from core.apps.common.models import TimedBaseModel
from core.apps.wallets.dto.transaction import TransactionDTO


class WalletTransaction(TimedBaseModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Идентификатор'
    )

    wallet = models.ForeignKey(
        'Wallet',
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

    @classmethod
    def from_dto(cls, dto: TransactionDTO):
        return cls(
            id=dto.id,
            wallet_id=dto.wallet_id,
            operation_type=dto.operation_type.value,
            amount=dto.amount,
            balance_after=dto.balance_after,
            balance_before=dto.balance_before,
            status=dto.status.value
        )

    def to_dto(self):
        return TransactionDTO(
            id=self.id,
            wallet_id=self.wallet_id,
            operation_type=OperationType(self.operation_type),
            amount=self.amount,
            balance_after=self.balance_after,
            balance_before=self.balance_before,
            status=TransactionStatus(self.status)
        )