FROM python:3.11-bookworm

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", 'dbt-worker.py' ]
