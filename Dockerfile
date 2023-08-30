FROM node:20-alpine3.17 AS frontend

WORKDIR /app
COPY bundles-src bundles-src
COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install --save-dev parcel
RUN npm ci

CMD ["./node_modules/.bin/parcel", "build", "bundles-src/index.js", "--dist-dir", "bundle", "--public-url='./'"]



