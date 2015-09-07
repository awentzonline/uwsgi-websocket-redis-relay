FROM nginx

RUN sed -i '/sendfile/s/^/#/g' /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
