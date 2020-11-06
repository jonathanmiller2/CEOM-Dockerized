FROM python:3

ENV PYTHONUNBUFFERED 1

#Create and cd into /code/ on the container, then copy all of the files in the same directory as this Dockerfile from the normal filesystem into /code/ on the container
WORKDIR /code
COPY . .


#GDAL Installation. The libgdal-dev version should match the GDAL version in requirements.txt
#You can see which version of libgdal-dev gets downloaded by uncommenting the "RUN gdal-config --version" line
RUN apt-get update
RUN apt-get install libgdal-dev netcat -y
#RUN gdal-config --version

#Gettext Installation
RUN apt-get install gettext libgettextpo-dev -y

#Unsure what these do, and they are likely not needed, but I am keeping them here in case future GDAL issues arise.
#RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
#RUN export C_INCLUDE_PATH=/usr/include/gdal

#Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]