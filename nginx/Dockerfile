FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

RUN mkdir -p /staticfiles /medias

RUN chown -R nginx:nginx /staticfiles
RUN chown -R nginx:nginx /medias