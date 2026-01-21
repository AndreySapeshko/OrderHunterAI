# OrderHunterAI — автоматизированный сбор заказов

**Order Hunter AI** — это backend-сервис, который автоматически собирает, фильтрует и оценивает заказы с разных источников (биржи, Telegram-каналы), используя интеллектуальную оценку на основе нейросетей.

### 📌 Подходит для стартапов, агентств и автоматизаторов, которым нужно:

- непрерывно мониторить фриланс-биржи и Telegram

- отсеивать нерелевантные заказы

- получать качественные лиды для обработки

Перейти к [Setup & Run](#Setup-&-Run)

### 🧠 Что делает продукт

**Order Hunter AI:**

- ✔ собирает заказы и объявления с разных источников
- ✔ фильтрует по ключевым параметрам
- ✔ оценивает релевантность и качество каждого лида
- ✔ классифицирует запросы по категориям
- ✔ готов к интеграции в ваши системы CRM / Dashboard

## 🚀 Преимущества для бизнеса
### 🔎 Автоматизация анализа заказов

Не нужно вручную мониторить Telegram-каналы, биржи, сообщения — система делает это за вас.

### 📈 Интеллектуальная оценка лидов

Каждому заказу присваивается релевантность, категория и оценка качества, что экономит часы человеческой аналитики.

### ⚙️ Гибкая интеграция

Можно подключить к собственной воронке продаж, CRM или службе рассылок.

### 💡 Подходит для:

- агентств, которые ищут клиентов

- стартапов с автоматическими воронками

- сервисов лид-генерации

- аналитических платформ

## 🧩 Как использовать

1. Собрать источники заказов

2. Настроить фильтры

3. Интегрировать вывод в вашу систему

4. Анализ и дальнейшая обработка лидов

## 📞 Интеграция и поддержка

Если вы хотите внедрить этот сервис под ваши задачи — пиши в andrdd17@gmail.com или напрямую в профиль автора.

## 📌 GitHub URL

https://github.com/AndreySapeshko/OrderHunterAI

## Setup & Run

### git clone https://github.com/AndreySapeshko/OrderHunterAI

### Файл .env

- Создать в директории OrderHunterAI файл .env
- Из имеющемуся в репозитории файлу .env.example скопировать все 
и вставить в .env
- Значения переменных помеченных комментарием "# указать свой", изменить.

### Docker
```
cd OrderHunterAI
docker compose up --build
```
### Node.js

```
cd frontend
npm run dev
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

### Регистрация пользователей
- Администратор создается с всеми правами.
- Обычный пользователь после регистрации ждет одобрения от администратора.
- Администратор может одобрить подключение нового пользователя в admin-панели.

### Telegram bot

- В файле .env в переменную TELEGRAM_BOT_TOKEN указать токен подключаемого бота.
- В подключенном боте отправить команду c email указанным при регистрации:
```
/link my_email@example.com
```

### создать tg_session.session
1. Установить Telegram Desktop и войти в аккаунт

- Скачать Telegram Desktop:
👉 https://desktop.telegram.org/

- Войти в нужный Telegram-аккаунт обычным способом

- Закрыть Telegram Desktop

2. Найти папку tdata
- Windows
`C:\Users\<USERNAME>\AppData\Roaming\Telegram Desktop\tdata`

- macOS
`~/Library/Application Support/Telegram Desktop/tdata`

- Linux
`~/.local/share/TelegramDesktop/tdata`


- Скопировать всю папку tdata целиком.

3. Конвертировать tdata в Telethon session

Используется библиотека opentele.

Установка
`pip install opentele`

Скрипт конвертации
```
from opentele.tl import TelegramClient
from opentele.api import API

API_ID = <YOUR_TELEGRAM_API_ID>
API_HASH = "<YOUR_TELEGRAM_API_HASH>"

api = API(API_ID, API_HASH)

with TelegramClient.from_tdata(
    tdata_dir="/path/to/tdata",
    api=api,
    session="tg_session",
):
    print("tg_session.session created")

```
После выполнения в текущей директории появится файл:

tg_session.session

4. Поместить сессию в проект

- Скопировать файл в:

`backend/.sessions/tg_session.session`


- Убедиться, что .sessions/ добавлена в .gitignore.

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
