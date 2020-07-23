FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

#GDAL Installation. The libgdal-dev version should match the GDAL version in requirements.txt
#You can see which version of libgdal-dev gets downloaded by uncommenting the "RUN gdal-config --version" line
RUN apt-get update
RUN apt-get install libgdal-dev -y
#RUN gdal-config --version

#These are likely not needed, but I am keeping them here in case future GDAL issues arise.
#RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
#RUN export C_INCLUDE_PATH=/usr/include/gdal

RUN pip install -r requirements.txt
COPY . /code/