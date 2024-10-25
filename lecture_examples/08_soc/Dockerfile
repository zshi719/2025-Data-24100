FROM python:3.10.15-bookworm

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
WORKDIR /app/src
CMD ["python", "app.py"]
