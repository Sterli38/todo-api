# Todo API

REST API для списка задач на Django + Django REST Framework, хранение в SQLite.

## Требования

- Python 3.13+
- Зависимости: `Django`, `djangorestframework` (см. `requirements.txt`)

## Запуск локально

Linux / macOS:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

Windows (PowerShell):

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

API доступен по адресу **http://localhost:8000/tasks**

## Запуск через Docker (альтернатива)

```bash
docker build -t todo-api .
docker run --rm -p 8000:8000 todo-api
```

Миграции применяются автоматически при старте контейнера. Адрес тот же: http://localhost:8000/tasks

## Тесты

```bash
python manage.py test
```

## API

| Метод    | URL           | Действие                | Ответ                      |
|----------|---------------|-------------------------|----------------------------|
| `POST`   | `/tasks`      | Создать задачу          | `201` + задача             |
| `GET`    | `/tasks`      | Список задач            | `200` + массив (`[]`, если пусто) |
| `GET`    | `/tasks/{id}` | Получить задачу         | `200` + задача             |
| `PUT`    | `/tasks/{id}` | Обновить задачу целиком | `200` + задача             |
| `DELETE` | `/tasks/{id}` | Удалить задачу          | `204` без тела             |

Завершающий `/` допускается: `/tasks/`, `/tasks/{id}/`.

Поля задачи: `id` (генерируется сервером), `title` (обязательное, 1–100 символов, не только пробелы),
`description` (необязательное), `completed` (по умолчанию `false`).
При `PUT` поля `title` и `completed` обязательны, отсутствие `description` очищает описание.

### Ошибки

Все ошибки возвращаются в JSON:

```json
{"error": "Некорректные данные.", "details": {"title": ["Это поле не может быть пустым."]}}
```

```json
{"error": "Задача не найдена."}
```

- `400` — невалидные данные или некорректный JSON
- `404` — задача не найдена
- `405` — метод не поддерживается

## Примеры запросов

Создать задачу:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Подготовиться к собеседованию", "description": "Повторить основы HTTP"}'
```

Получить список:

```bash
curl http://localhost:8000/tasks
```

Обновить задачу целиком:

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Подготовиться к собеседованию", "completed": true}'
```

Удалить задачу:

```bash
curl -X DELETE -i http://localhost:8000/tasks/1
```

## Структура

```
config/              настройки проекта и корневые URL
tasks/
  models.py          модель Task (хранение)
  serializers.py     валидация и преобразование JSON <-> модель
  views.py           HTTP-обработка (ModelViewSet)
  urls.py            роутинг /tasks
  exceptions.py      единый JSON-формат ошибок
  migrations/        миграции БД
  tests/             тесты API
```

## Настройки через переменные окружения (необязательно)

| Переменная             | По умолчанию                      |
|------------------------|-----------------------------------|
| `DJANGO_SECRET_KEY`    | dev-ключ |
| `DJANGO_DEBUG`         | `0`                               |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,0.0.0.0`     |
| `SQLITE_PATH`          | `db.sqlite3` в корне проекта      |
