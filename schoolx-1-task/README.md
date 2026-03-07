
# Severstal Test (FastAPI + Async SQLAlchemy)

Небольшой сервис задач (Tasks) на FastAPI с асинхронным доступом к PostgreSQL через SQLAlchemy 2.0 (async) и миграциями Alembic.

## Стек

- Python 3.13+
- FastAPI + Uvicorn
- SQLAlchemy 2.0 (AsyncEngine/AsyncSession)
- asyncpg (драйвер PostgreSQL)
- Alembic (миграции, async template)
- Pydantic v2 (схемы запросов/ответов)
- Ruff (форматирование)

## Быстрый старт

1) Создать `.env` (можно на основе `example.env`).

Минимально нужны переменные для БД (см. `src/app/config.py`):

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `SECRET_KEY`

2) Установить зависимости (через uv):

```bash
uv sync
```

3) Применить миграции:

```bash
uv run alembic upgrade head
```

4) Запустить приложение:

```bash
uv run main.py
```

После запуска Swagger UI обычно доступен по `/docs`.

## Миграции (Alembic)

- Создать новую миграцию (автогенерация):

```bash
uv run alembic revision --autogenerate -m "Your message"
```

- Применить миграции:

```bash
uv run alembic upgrade head
```

## Логика проекта

Сервис реализует CRUD для сущности `Task`.

- Репозитории (DB слой) лежат в `src/database/repositories/`.
- Сервисы (бизнес-логика) лежат в `src/api/<module>/service.py`.
- Роуты FastAPI — `src/api/<module>/router.py`.
- Валидация/контракты API — Pydantic модели в `src/api/<module>/schema.py` и ответы в `src/api/<module>/response.py`.

### Пагинация и фильтры

Пагинация сделана в «page/size» формате (страница/размер страницы) и вынесена в общий модуль:

- `src/api/pagination.py`: `PaginationParams` и обобщённый ответ `PaginatedResponse[T]`.

Фильтрация реализована на уровне базового репозитория по соглашению:

- `field=value` → точное сравнение (`=`)
- `field_contains=value` → поиск по подстроке (`ILIKE %value%`)

Для задач используются поля фильтрации (см. `TaskFilter`):

- `status`
- `title_contains`
- `description_contains`

Сортировка:

- `sort_by` — поле сортировки (ограничено в `TaskPaginationParams`)
- `order` — `asc` или `desc`

## API (Tasks)

Базовый префикс: `/tasks`

- `GET /tasks` — список задач с фильтрами/пагинацией
- `GET /tasks/{id}` — получить задачу по id
- `POST /tasks` — создать задачу
- `PATCH /tasks/{id}` — обновить задачу (частично: описание/asset/status и т.д.)
- `DELETE /tasks/{id}` — удалить задачу

Пример запроса списка:

`/tasks?page=1&size=10&sort_by=created_at&order=desc&status=PENDING&title_contains=bug`

## Структура папок

```text
src/
	api/
		task/
			router.py      # HTTP endpoints
			service.py     # бизнес-логика
			schema.py      # входные схемы/фильтры/параметры
			response.py    # выходные модели
	app/
		config.py        # настройки через env
		app.py           # создание FastAPI приложения (если используется)
	database/
		database.py      # engine + async_session_maker + Base
		models/          # ORM модели
		repositories/    # базовый репозиторий и репозитории сущностей
		sql_enums.py     # enum-ы для БД/ORM
migration/           # Alembic env.py + versions/
```

## Форматирование

```bash
uv run ruff format .
```

