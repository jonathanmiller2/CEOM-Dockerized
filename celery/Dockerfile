FROM python:3

WORKDIR /code
COPY . .
WORKDIR /code/app

RUN apt-get update
RUN apt-get install binutils libproj-dev gdal-bin gettext libgettextpo-dev cron netcat -y

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt