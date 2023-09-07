FROM node:alpine as builder

WORKDIR /app
COPY package.json package-lock.json ./
ENV CI=1
RUN npm ci

COPY . .
RUN npm run build -- --prod --output-path=/dist

# 2. Развертываем приложение Angular на NGINX
FROM nginx:alpine

# Заменяем дефолтную страницу nginx соответствующей веб-приложению
#RUN rm -rf /usr/share/nginx/html/*
#COPY --from=builder /dist /usr/share/nginx/html
#
#COPY ./.nginx/nginx.conf /etc/nginx/nginx.conf
#
#ENTRYPOINT ["nginx", "-g", "daemon off;"]
