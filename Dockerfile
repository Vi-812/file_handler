# Используем базовый образ Python 3.10
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера (celery_file_handler)
WORKDIR /celery_file_handler

# Копируем файл с зависимостями (requirements.txt) в контейнер
COPY requirements.txt .

# Устанавливаем зависимости через pip
RUN pip install -r requirements.txt

# Копируем все остальные файлы вашего проекта в контейнер
COPY . .

# Выполняем миграции Django
RUN python manage.py makemigrations
RUN python manage.py migrate

# Определяем порт, на котором будет работать ваше Django приложение
EXPOSE 8000

# Запускаем Django сервер и Celery в фоновом режиме
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & celery -A celery_file worker --loglevel=info"]
