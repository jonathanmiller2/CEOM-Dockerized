FROM python:3

ENV PYTHONUNBUFFERED 1

#Create and cd into /code/ on the container, then copy all of the files in the same directory as this Dockerfile from the normal filesystem into /code/ on the container
WORKDIR /code
COPY . .
WORKDIR /code/app

#maybe this will work?
#COPY ../supervisord.conf /etc/supervisord.conf

RUN apt-get update
# RUN apt list -a gdal-bin
RUN apt-get install binutils libproj-dev libgdal-dev=3.2.2+dfsg-2+deb11u2 gdal-bin=3.2.2+dfsg-2+deb11u2 gettext libgettextpo-dev netcat supervisor -y

#Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir GDAL==3.2.2

#Run entrypoint.sh
ENTRYPOINT ["/code/app/entrypoint.sh"]