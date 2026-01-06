# OrderHunterAI

## Overview
Система решает следующие задачи:

- автоматический сбор заказов из внешних источников

- дедупликация и нормализация данных

- фильтрация по ключевым словам и эвристикам

- персонализация под каждого пользователя

- опциональный LLM-анализ заказов

- уведомления в Telegram

- web-интерфейс для управления и анализа

Архитектура ориентирована на асинхронность, отказоустойчивость и расширяемость.

## Features
- 🔌 Модульные коннекторы источников (Telegram, Kwork, Reddit)

- 🧠 Эвристический Rule Engine

- 🤖 Опциональный LLM-анализ (OpenAI, OpenRouter)

- 🧩 Гибкие пользовательские правила фильтрации

- 🔔 Telegram-уведомления

- 🌐 Web UI (FastAPI + React)

- 🔐 JWT-аутентификация и роли (user / admin)

- 🧪 Покрытие тестами и CI

- 🐳 Docker-first deployment

## Architecture
Основные компоненты системы:

- Ingestion Pipeline — сбор и нормализация данных

- Raw Items — сырые данные из источников

- Leads — нормализованные потенциальные заказы

- User Leads — персонализированные лиды под пользователя

- Rule Engine — фильтрация и скоринг

- LLM Layer — дополнительный анализ (опционально)

- Notification Layer — Telegram

Web API & UI

Поток данных:

`Source → RawItem → RuleEngine → Lead → UserLead → Notification
`
## Tech Stack
### Backend

- Python 3.13

- FastAPI

- SQLAlchemy (async)

- PostgreSQL

- APScheduler

- JWT (Auth)

- Pydantic

- Pytest

### Frontend

- React

- React Router

- Fetch API

- Minimal UI (MVP-oriented)

### Infrastructure

- Docker / Docker Compose

- CI (lint + tests)

## Data Model

- RawItem — сырые данные заказа

- Lead — нормализованный заказ

- UserLead — связь лида и пользователя

- UserRule — пользовательские правила

- LeadAI — результат LLM-анализа (опционально)

- User — пользователь системы
- SystemState - состояния для управления работой LLM
- SourceStat - состояния источников 
- LeadNotification - отслеживание отправленных уведомлений

## Ingestion Pipeline

### Каждый источник реализует интерфейс коннектора:

- fetch() — получение данных

- get_cursor() / mark_success() — состояние источника

- state — хранение прогресса

### Pipeline:

- фильтрация по длине текста

- дедупликация по content_hash

- сохранение RawItem

- передача в Rule Engine

## Rule Engine

### Rule Engine реализует:

- include / exclude keywords

- минимальную длину текста

- эвристический скоринг

- отдельные правила для уведомлений

- фильтрацию по источникам

Правила настраиваются через Web UI.

## LLM Analysis (Optional)

### LLM используется не как основной фильтр, а как дополнительный аналитический слой:

- классификация

- релевантность

- дополнительный скоринг

### При превышении лимитов или ошибках система:

- автоматически отключает LLM

- продолжает работу на эвристиках

## Authentication & Authorization

- JWT-токены

- роли: user / admin

- регистрация с подтверждением администратором

- admin UI для управления пользователями

## Web UI

### Доступные страницы:

- Raw Items — сырые данные

- User Leads — персонализированные лиды

- Lead Details — подробный просмотр

- Rules Editor — настройка фильтрации

- Admin Panel — управление пользователями

## Telegram Bot

### Telegram используется для:

- подключение к боту

- уведомлений о новых лидах

- быстрого доступа к заказам

## API Documentation

### Swagger UI доступен по адресу:

http://localhost:8000/docs

## Setup & Run

### git clone https://github.com/AndreySapeshko/OrderHunterAI

```
cd OrderHunterAI
docker compose up --build
```
### Frontend:

```
http://localhost:5173
```
### Backend:

```
http://localhost:8000
```
### Создание администратора
```
docker exec -it backend python -m backend.app.api.auth.create_admin
```

## Testing

### Проект покрыт тестами:

`pytest`

### Покрытие тестами:

`OrderHunterAI/htmlcov/index.html`

### CI автоматически проверяет:

- линтинг

- тесты

## Limitations

- LLM ограничен rate limits

- фильтрация требует тонкой настройки под источник

- не реализована очередь высокой нагрузки (осознанно)

## Future Improvements

- подключение альтернативных LLM (Claude, Gemini, local models)

- приоритетная очередь лидов

- полнотекстовый поиск

- статистика и аналитика

- multi-tenant deployment
