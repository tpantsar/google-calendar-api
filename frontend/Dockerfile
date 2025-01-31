FROM node:22 AS build-stage
WORKDIR /app
COPY . .
RUN npm ci
RUN npm run build

ENV VITE_BACKEND_URL=http://localhost:8080/api

# Build the final image from nginx
FROM nginx:alpine

# COPY the directory dist from the build-stage to /usr/share/nginx/html
COPY --from=build-stage /app/dist /usr/share/nginx/html