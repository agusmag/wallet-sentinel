FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir /etc/nginx/ssl

RUN chown -R root:root /etc/nginx/ssl
RUN chmod -R 600 /etc/nginx/ssl
