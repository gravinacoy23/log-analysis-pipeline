FROM python:3.11-slim

WORKDIR /log-analysis-pipeline

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python3 scripts/log_generator.py -c 100

CMD ["python","main.py"]
