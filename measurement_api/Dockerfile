FROM python:3.8-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSED 5000

CMD ["python", "api.py"]
