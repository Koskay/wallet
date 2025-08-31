from django.db import models


class TransactionStatus(models.TextChoices):
    SUCCESS = 'success', 'Успешно'
    IN_PROCESSING = 'in_processing', 'В обработке'
    CANCELED = 'canceled', 'Отменена'
    FAILED = 'failed', 'Ошибка'


class OperationType(models.TextChoices):
    OPERATION_DEPOSIT = 'deposit', 'Пополнение'
    OPERATION_WITHDRAW = 'withdraw', 'Списание'