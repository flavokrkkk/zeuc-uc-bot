# Stage 1: Сборка фронтенда
FROM node:alpine as build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . ./
RUN npm run build

FROM alpine:latest
WORKDIR /frontend
COPY --from=build /app/dist .