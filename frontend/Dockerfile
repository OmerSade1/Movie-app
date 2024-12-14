FROM nginx:alpine

RUN apk add --no-cache procps

COPY index.html /usr/share/nginx/html/index.html

ENTRYPOINT ["nginx", "-g", "daemon off;"]