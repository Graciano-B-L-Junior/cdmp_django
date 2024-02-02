FROM python:3.10.13-bookworm

WORKDIR /web
COPY ./app .


RUN apt-get upgrade

RUN apt-get update && \
    apt-get install -y python3-pip

RUN pip install -r requirements.txt && pip install psycopg

RUN chmod a+x app_build.sh && chmod a+x app_build_dev.sh
RUN adduser --disabled-password cdmp
RUN chown -R cdmp:cdmp /web
USER cdmp



