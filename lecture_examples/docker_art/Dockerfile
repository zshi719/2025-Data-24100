FROM python:3.10.15-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY art_date.py .

ENV DATE_FORMAT="%m/%Y"

CMD ["python", "art_date.py"]