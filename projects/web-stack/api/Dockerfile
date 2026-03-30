# Базовый образ (slim для экономии места)
# python:3.11-slim = 150 Мб
FROM python:3.11-slim

# Методанные образа (не влияют на работу, для документации)
LABEL maintainer="temochkager@yandex.ru"
LABEL version="1.0"
LABEL description="HomeLab API Service"

# Рабочая директория внутри контейнера
# Все последующие команды выполняются в этой папке
WORKDIR /app

# Копируем только файл зависимостей сначала
# Это позволяет кэшировать слой установки пакетов
COPY requirements.txt .

# Устанавливаем зависимости
# --no-cache-dir не сохраняет кэш pip (эткономит место)
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
# Копируем после установки зависимостей (для кэширования)
COPY app.py .

# Переменная окружения (доступна в приложении через os.getenv())
ENV FlASK_ENV=production
ENV CoNTAINER_NAME=api-container

# Документируем порт (не открываем)
EXPOSE 5000

# Команда запуска контейнера
# Используем exec-form (массив) для правильной обработки сигналов
CMD ["python", "app.py"]

# Альтернатива : ENTRYPOINT + CMD
# ENTRYPOINT ["python"]
# CMD ["app.py"]