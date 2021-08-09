FROM python:3

WORKDIR /code
COPY . .
WORKDIR /code/app


#GDAL Installation. The libgdal-dev version should match the GDAL version in requirements.txt
#You can see which version of libgdal-dev gets downloaded by uncommenting the "RUN gdal-config --version" line
RUN apt-get update
RUN apt-get install libgdal-dev netcat -y

#Gettext Installation
RUN apt-get install gettext libgettextpo-dev -y

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt