# Используем официальный образ Python
FROM python:3.11-slim

# Установка зависимостей
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Запуск миграций и сервера по умолчанию (можно переопределить в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
