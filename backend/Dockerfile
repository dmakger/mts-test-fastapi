# Базовый образ с Python 3.11
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /backend

# Копируем файлы проекта
COPY . .

# Устанавливаем переменную окружения для поиска модулей
# ENV PYTHONPATH=/app

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Открываем порт
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
