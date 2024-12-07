FROM python:3.10.15-bookworm

WORKDIR /app
RUN apt-get update 
RUN apt-get install -y sqlite3


COPY requirements.txt .
RUN pip install -r requirements.txt


ENV PYTHONUNBUFFERED=1
WORKDIR /app/src
CMD ["python", "flask_app.py"]
