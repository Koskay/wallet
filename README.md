## Быстрый старт

1. Клонируйте репозиторий `https://github.com/Koskay/wallet.git`
2. Скопируйте `wallet_billing/.env_example` в `wallet_billing/.env` и настройте переменные окружения
3. Запустите проект:
```bash
make app
```

Миграции и загрузка фикстур происходят автоматически при запуске.

id кошельков для тестов будут в описании эндпоинтов.

## API Documentation

OpenAPI документация доступна по адресу: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

## Make команды

```bash
make app   # Запустить контейнеры
make app-down     # Остановить контейнеры
make app-logs     # Посмотреть логи
make run-test     # Запустить тесты
```