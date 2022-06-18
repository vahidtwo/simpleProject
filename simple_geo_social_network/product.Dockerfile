FROM python:3.8-slim-buster

WORKDIR /srv

ENV debian_frontend noninteractive

RUN apt-get update -y ;\
    apt install -y \
    build-essential \
    libmemcached-dev \
    zlib1g-dev \
    gcc g++ \
    inetutils-ping \
    netcat

COPY infrastructure/requirements.txt .

RUN pip install -r ./requirements.txt

COPY . .
ENV DJANGO_SETTINGS_MODULE "settings"
CMD [ "uwsgi", "--strict", "--master", "--vacuum", "--die-on-term", "--enable-threads", "--max-requests", "1000", "--reload-on-rss", "2048", "--worker-reload-mercy", "30", "--cheaper-algo", "busyness", "--processes", "64", "--cheaper", "8", "--cheaper-initial", "256", "--cheaper-overload", "1", "--cheaper-step", "128", "--cheaper-busyness-multiplier", "30", "--cheaper-busyness-min" , "20", "--cheaper-busyness-max" , "70", "--cheaper-busyness-backlog-alert", "16", "--cheaper-busyness-backlog-step", "2", "--http", ":6001", "--wsgi-file", "/srv/infrastructure/wsgi.py" ]
