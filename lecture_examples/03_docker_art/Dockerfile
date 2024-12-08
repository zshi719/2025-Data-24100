FROM python:3.10.15-bookworm
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY print_date.py .
CMD ["python", "print_date.py"]