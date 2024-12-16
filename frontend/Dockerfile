FROM node:22.12 as build-frontend

WORKDIR /tmp

COPY package.json ./
RUN npm install

COPY . ./
ENV APP_BACKEND /api/
RUN npm run build


FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build-frontend /tmp/dist/ /app

CMD ["nginx", "-g", "daemon off;"]
