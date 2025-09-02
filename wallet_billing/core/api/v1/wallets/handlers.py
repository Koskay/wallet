import uuid

from django.http import HttpRequest

from ninja import Router
from ninja.errors import HttpError

from core.api.v1.schemas import ApiResponse
from core.api.v1.wallets.schemas import WalletTransactionInSchema, WalletTransactionOutSchema, WalletDataOutSchema
from core.apps.common.exception.base import ServiceException
from core.apps.wallets.factories import get_billing_use_case, get_wallet_query_service

router = Router(tags=["Wallets"])


@router.post('{wallet_id}/operation',
             response={201: ApiResponse[WalletTransactionOutSchema]},
             description="""Пополнение или списание средств с кошелька.
             
             Данные кошельков:
             - id: 8902108a-6710-4bf2-bf14-e5c1ac8cd291
             - id: 2bf561d7-c3f9-4281-ba7b-d29cf7d6273c
             
             - На обоих начальный баланс: 1000.00

             Операции:
             - deposit: Пополнение кошелька на указанную сумму
             - withdrawal: Списание средств с кошелька (если достаточно баланса)

             Параметры:
             - wallet_id: UUID кошелька для операции
             - amount: Сумма операции (положительное число)
             - operation_type: Тип операции - 'deposit' или 'withdrawal'

             Возвращает:
             - Данные о выполненной транзакции с новым балансом кошелька
             - Статус операции (успех/ошибка)
             - Сообщение об ошибке (в случае неудачи)

             Ошибки:
             - 404: Кошелек не найден
             - 400: Недостаточно средств для списания
             - 400: Неверный тип операции или сумма""")
def create_wallet(request: HttpRequest,
                  wallet_id: uuid.UUID,
                  operation_data: WalletTransactionInSchema) -> ApiResponse[WalletTransactionOutSchema]:
    billing_use_case = get_billing_use_case()
    operation_dto = operation_data.to_dto(wallet_id=wallet_id)
    try:
        transaction_dto = billing_use_case.process_operation(operation=operation_dto)
    except ServiceException as exc:
        raise HttpError(status_code=exc.status_code, message=exc.message)
    return ApiResponse(data=WalletTransactionOutSchema.from_dto(transaction_dto))


@router.get('{wallet_id}',
            response=ApiResponse[WalletDataOutSchema],
            description="""Получение кошелька по его id, вместе с 5 последними транзакциями.
            
            Данные кошельков:
             - id: 8902108a-6710-4bf2-bf14-e5c1ac8cd291
             - id: 2bf561d7-c3f9-4281-ba7b-d29cf7d6273c

             Параметры:
             - wallet_id: UUID кошелька 

             Возвращает:
             - Данные кошелька
             - Список последних транзакций

             Ошибки:
             - 404: Кошелек не найден """)
def get_wallet(request: HttpRequest,
               wallet_id: uuid.UUID) -> ApiResponse[WalletDataOutSchema]:
    try:
        wallet_query_service = get_wallet_query_service()
        wallet_dto = wallet_query_service.get_wallet_by_id(wallet_id=wallet_id)
    except ServiceException as exc:
        raise HttpError(status_code=exc.status_code, message=exc.message)
    return ApiResponse(data=WalletDataOutSchema.from_dto(wallet_dto))



