FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

COPY migrations .
COPY .env .
COPY alembic.ini .

EXPOSE 8000

CMD ["fastapi", "run", "backend"]