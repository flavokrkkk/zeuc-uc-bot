# Stage 1: Сборка фронтенда
FROM node:alpine as build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . ./
RUN npm run build

# Stage 2: Контейнер для копирования артефактов
FROM alpine:latest
WORKDIR /frontend
COPY --from=build /app/dist .

# Оставляем только собранные файлы
