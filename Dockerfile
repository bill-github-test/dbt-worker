FROM python:3.11-bookworm

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", 'dbt-worker.py' ]
