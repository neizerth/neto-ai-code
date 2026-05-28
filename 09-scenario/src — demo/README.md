## Пример проекта (09): структура как в презентации

Сценарий: пользователь пишет блюдо → получает список покупок.

### Структура (как в презентации)

- `api/` — точки входа (валидация запроса, вызов сервисов)
- `services/` — бизнес‑логика
- `llm/` — вызов модели
- `config/` — конфиги и переменные окружения
- `tests/` — тесты

Дополнительно:

- `streamlit_app.py` — простой UI для ручной проверки

### Запуск

0) Перейдите в папку проекта:

```bash
cd 09-scenario/src
```

1) Виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Зависимости:

```bash
pip install -r requirements.txt
```

3) Настройки:

Скопируйте пример и заполните ключ:

```bash
cp config/.env.example config/.env
```

Откройте `config/.env` и заполните `GIGACHAT_CREDENTIALS=...`.

Если нужны сертификаты НУЦ Минцифры, добавьте `GIGACHAT_CA_BUNDLE_FILE=...` или поставьте сертификаты на уровне ОС.

4) Запуск API (FastAPI):

```bash
uvicorn api.main:app --reload
```

API поднимется на `http://127.0.0.1:8000`.

5) Проверка API через curl:

```bash
curl -s -X POST "http://127.0.0.1:8000/api/shopping" \
  -H "Content-Type: application/json" \
  -d '{"dish":"борщ","people":"2","output_format":"Список продуктов"}'
```

6) Запуск UI (Streamlit):

```bash
streamlit run streamlit_app.py
```

### Проверки

- пустой ввод → сообщение, вызова API нет
- очень длинный ввод → сообщение, вызова API нет
- нет ключа → сообщение
- проблема с сертификатами → сообщение

