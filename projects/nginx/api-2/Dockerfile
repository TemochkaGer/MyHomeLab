FROM python:3.11-slim

RUN useradd -m apiuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api-2.py .
RUN chown -R apiuser:apiuser /app
USER apiuser

CMD ["python3", "api-2.py"]