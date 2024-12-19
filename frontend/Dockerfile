FROM node:22.12 AS build-frontend

WORKDIR /tmp

COPY package-lock.json package.json ./
RUN npm ci

COPY . ./
ENV APP_BACKEND /api/
RUN npm run build

FROM nginx

COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build-frontend /tmp/dist/ /app

CMD ["nginx", "-g", "daemon off;"]
