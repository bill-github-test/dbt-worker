FROM python:3.11-bookworm

WORKDIR /app

COPY . /app

RUN pip install -r requirement.txt

CMD ["python", "worker.py"]