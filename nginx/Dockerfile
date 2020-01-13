FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir -p /etc/certs

COPY /etc/letsencrypt/live/ /etc/certs/
COPY /usr/share/nginx/html /usr/share/nginx/html
