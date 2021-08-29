FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . .
WORKDIR /code/app

RUN apt-get update
RUN apt-get install binutils libproj-dev libgdal-dev gdal-bin gettext libgettextpo-dev netcat -y

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir GDAL==2.4