FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d

COPY ./app/eomf/static/ /nginx_static_files

#TODO: This will likely change when fixing the django media runtime thing. (Django's media has to be accessed at runtime and thus you can't just copy on startup and call it good)
COPY ./app/eomf/media/ /nginx_media_files