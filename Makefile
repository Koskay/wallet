STORAGES_FILE = docker_compose/storages.yaml
BACK_FILE = docker_compose/web.yaml



DB_CONTAINER = postgres_db
BACK_CONTAINER = web

LOGS = docker logs
ENV = --env-file wallet_billing/.env
DC = docker compose
EXEC = docker exec -it
STOP = docker stop
START = docker start
MANAGE_PY = python manage.py


.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: postgres-exec
postgres-exec:
	${EXEC} ${DB_CONTAINER} psql -U my_user



.PHONY: app
app:
	${DC} -f ${BACK_FILE} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${BACK_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${BACK_FILE} -f ${STORAGES_FILE}  down

.PHONY: app-exec
app-exec:
	${EXEC} ${BACK_CONTAINER} ash

.PHONY: app-migrate
app-migrate:
	${EXEC} ${BACK_CONTAINER} ${MANAGE_PY} migrate

.PHONY: app-migrations
app-migrations:
	${EXEC} ${BACK_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: superuser
superuser:
	${EXEC} ${BACK_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: run-test
run-test:
	${EXEC} ${BACK_CONTAINER} pytest -s

.PHONY: run-unittest
run-unittest:
	${EXEC} ${BACK_CONTAINER} pytest -s tests/services/

.PHONY: run-e2e-test
run-e2e-test:
	${EXEC} ${BACK_CONTAINER} pytest -s tests/e2e/