FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir /etc/nginx/ssl

RUN mkdir /etc/nginx/dhparams

RUN chmod -R 600 /etc/nginx/ssl
