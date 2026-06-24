# ESG Parser Backend

This project is a Django backend for collecting ESG-related content and serving it through REST API endpoints.

It currently supports:
- news parsing
- course parsing
- project parsing
- event parsing
- saving parsed data into PostgreSQL
- filtering and pagination for API endpoints
- manual and async parser execution through Django + Celery

## Stack

- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis-compatible broker
- Selenium + requests-based parsers

## Project Structure

- `ESGBack/` - Django project root
- `ESGBack/ESGBack/` - Django settings and project config
- `ESGBack/v1/` - main API app
- `ESGBack/v1/parsers/` - parser implementations
- `ESGBack/v1/parsers/GroupedParsers/` - grouped parser entrypoints

## Main Features

### Content models

The backend exposes these main entities:
- `News`
- `Course`
- `Project`
- `Event`

### Parser flow

Parser flow is:

1. parser fetches data from source websites
2. parsed objects are normalized into parser classes
3. `AddNews`, `AddCourse`, `AddProject`, `AddEvent` save them to DB
4. frontend reads stored data from API

### API endpoints

Main endpoints:

- `GET /api/v1/News/`
- `GET /api/v1/Courses/`
- `GET /api/v1/Projects/`
- `GET /api/v1/Events/`

Parser trigger endpoint:

- `POST /api/v1/parsers/run/`

Subscription endpoint:

- `POST /api/v1/subscribe/`

## Setup

### 1. Create and activate virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r ESGBack/requirements.txt
```

### 3. Configure PostgreSQL

Current database settings are in `ESGBack/ESGBack/settings.py`.

Default local config:

- database: `esgdb`
- user: `postgres`
- password: `pa55word`
- host: `localhost`
- port: `5432`

### 4. Run migrations

```powershell
cd ESGBack
python manage.py migrate
```

### 5. Start Django

```powershell
python manage.py runserver
```

## Tests

Run Django checks and tests from the backend directory:

```powershell
cd ESGBack
python manage.py check
python manage.py test
```

The test suite includes:

- auth flow tests for registration, email activation, login, admin login, and password reset
- subscription and admin moderation tests
- security regression tests that verify parser execution and content writes require admin access
- syntax regression tests that compile the live `ESGBack`, `v1`, and `user` Python source trees

## Filtering and Pagination

Global pagination is enabled with DRF `LimitOffsetPagination`.

Example:

```text
/api/v1/News/?limit=20&offset=0
```

Search and ordering are also enabled on list endpoints.

Examples:

```text
/api/v1/News/?search=climate
/api/v1/Events/?ordering=-event_date
/api/v1/Courses/?lang=en
/api/v1/Projects/?isActive=true
```

## Parser Execution

### Run parsers synchronously

Useful for development and local manual refresh:

```http
POST /api/v1/parsers/run/
{
  "mode": "sync"
}
```

### Run parsers asynchronously with Celery

Useful for background execution:

```http
POST /api/v1/parsers/run/
{
  "mode": "async"
}
```

## Celery and Redis

Celery uses:

```python
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
```

To run async tasks:

1. start Redis-compatible broker
2. start Celery worker

Worker command:

```powershell
python -m celery -A ESGBack worker -l info --pool=solo
```

If using Docker Redis:

```powershell
docker run -d --name esg-redis -p 6379:6379 redis:7
```

## Notes

- Some parser sources support all `ru`, `kk`, `en` variants, but not every external site provides all three languages.
- Selenium-based parsers may take longer than request-based parsers.
- Local parser trigger testing was enabled in debug mode for localhost requests.

## Recommended Run Flow

For local development:

1. start PostgreSQL
2. start Django
3. start Redis
4. start Celery worker
5. trigger parsers through `/api/v1/parsers/run/`
6. read parsed data through `/api/v1/News/`, `/Courses/`, `/Projects/`, `/Events/`
