FROM nginx:alpine
LABEL authors="BiomedicLJZ"

RUN apk add --no-cache procps

COPY index.html /usr/share/nginx/html/index.html

ENTRYPOINT ["nginx", "-g", "daemon off;"]