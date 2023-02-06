FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH /app

# tutaj chyba subscriber.py ;D
COPY publisher.py .

CMD ["python", "subscriber.py"]