# syntax=docker/dockerfile:1

# Build stage - supports multi-architecture builds
FROM --platform=$BUILDPLATFORM node:20-alpine AS builder

# Set build arguments for cross-compilation
ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG APP_NAME=chatgrid_chat_ui

# Install necessary build tools
RUN apk add --no-cache libc6-compat python3 make g++

WORKDIR /app

# Enable Corepack for Yarn Berry
RUN corepack enable && corepack prepare yarn@3.5.1 --activate

# Copy package files
COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn ./.yarn
COPY apps/web/package.json ./apps/web/
COPY apps/agents/package.json ./apps/agents/

# Install dependencies
RUN yarn install --immutable

# Copy source files
COPY . .

# Build the application
RUN yarn turbo build --filter=web

# Production stage - multi-arch nginx
FROM --platform=$TARGETPLATFORM nginx:alpine AS production
ARG APP_NAME=chatgrid_chat_ui

# Image metadata
LABEL org.opencontainers.image.title="${APP_NAME}"
ENV APP_NAME=${APP_NAME}

# Copy custom nginx config
COPY --from=builder /app/apps/web/dist /usr/share/nginx/html

# Add nginx configuration for SPA routing
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
    # Enable gzip compression \
    gzip on; \
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript; \
    # Cache static assets \
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ { \
        expires 1y; \
        add_header Cache-Control "public, immutable"; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
