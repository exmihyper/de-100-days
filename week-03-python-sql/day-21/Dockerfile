FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY etl_pipeline.py .
COPY sales_data.csv .

CMD ["python", "etl_pipeline.py"]