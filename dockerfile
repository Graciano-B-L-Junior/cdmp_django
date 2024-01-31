FROM python:3.10.13-bookworm

WORKDIR /app
COPY ./app /app



RUN apt-get upgrade

RUN apt-get update && \
    apt-get install -y python3-pip

RUN pip install -r requirements.txt
RUN pip install psycopg

RUN python manage.py makemigrations

RUN python manage.py collectstatic --noinput

RUN groupadd -r cdmp && useradd -r -g cdmp cdmp
USER cdmp




