FROM python:3

ENV PYTHONUNBUFFERED 1

#Create and cd into /code/ on the container, then copy all of the files in the same directory as this Dockerfile from the normal filesystem into /code/ on the container
WORKDIR /code
COPY . .

RUN apt-get update
RUN apt-get install binutils libproj-dev gdal-bin gettext libgettextpo-dev cron netcat -y

#Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Cron
COPY crontab /etc/cron.d/cron-python
RUN chmod 0644 /etc/cron.d/cron-python
RUN crontab /etc/cron.d/cron-python

#Run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]