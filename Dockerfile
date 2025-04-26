FROM python:3.13-alpine

WORKDIR /app

COPY main.py .

COPY .env .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

