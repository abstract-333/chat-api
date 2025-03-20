DC = docker compose
EXEC = docker exec -t
LOGS = docker logs
ENV = --env-file .env
ENV_PROD = --env-file .env.prod
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
STORAGES_UI_FILE = docker_compose/storages_ui.yaml
SERVER_FILE = docker_compose/server.yaml
LOGGERS_FILE = docker_compose/loggers.yaml
APP_CONTAINER = main-app


.PHONY: all
all:
	${DC} -f ${STORAGES_FILE} -f ${STORAGES_UI_FILE} -f ${APP_FILE} -f ${SERVER_FILE} ${ENV} up --build -d


.PHONY: all-prod
all-prod:
	${DC} -f ${STORAGES_FILE} -f ${STORAGES_UI_FILE} -f ${APP_FILE} -f ${SERVER_FILE} ${ENV_PROD} up --build -d

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-prod
app-prod:
	${DC} -f ${APP_FILE} ${ENV_PROD} up --build -d


.PHONY: server
server:
	${DC} -f ${SERVER_FILE} ${ENV} up --build -d


.PHONY: loggers
loggers:
	${DC} -f ${LOGGERS_FILE} ${ENV} up --build -d


.PHONY: storages-pure
storages-pure:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d


.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} -f ${STORAGES_UI_FILE} ${ENV} up --build -d


.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down


.PHONY: server-down
server-down:
	${DC} -f ${SERVER_FILE} down


.PHONY: loggers-down
loggers-down:
	${DC} -f ${LOGGERS_FILE} down


.PHONY: storages-pure-down
storages-pure-down:
	${DC} -f ${STORAGES_FILE} down


.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} -f ${STORAGES_UI_FILE} down


.PHONY: all-down
all-down:
	${DC} -f ${STORAGES_FILE} -f ${STORAGES_UI_FILE} -f ${APP_FILE} -f ${SERVER_FILE} down


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: server-logs
server-logs:
	${DC} -f ${SERVER_FILE} logs -f


.PHONY: loggers-logs
loggers-logs:
	${DC} -f ${LOGGERS_FILE} logs -f


.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash


.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest
