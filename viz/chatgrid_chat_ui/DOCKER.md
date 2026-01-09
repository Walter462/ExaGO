# Docker Deployment Guide

This guide explains how to build and deploy the chat UI application using Docker with support for both Apple ARM64 (M1/M2/M3) and Intel64 (AMD64) architectures.

## Prerequisites

- Docker Desktop 20.10+ with BuildKit enabled
- Docker Buildx (included in Docker Desktop)

## Quick Start

### Option 1: Using Docker Compose (Recommended for local development)

```bash
# Build and run the application
docker-compose up -d

# Access the application at http://localhost:8080
```

To stop the application:
```bash
docker-compose down
```

### Option 2: Using the Build Script

The `docker-build.sh` script simplifies multi-architecture builds:

```bash
# Build for your current platform only (fastest)
./docker-build.sh local

# Build for both ARM64 and AMD64
./docker-build.sh

# Build and push to a registry
IMAGE_NAME=myregistry/chatgrid_chat_ui ./docker-build.sh push
```

### Option 3: Manual Docker Build

#### Build for your current platform:
```bash
docker build -t chatgrid_chat_ui:latest .
```

#### Build for both platforms (requires buildx):
```bash
# Create a new builder instance
docker buildx create --name multiarch-builder --use

# Build for both architectures
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t chatgrid_chat_ui:latest \
  --load \
  .
```

## Running the Container

After building, run the container:

```bash
docker run -d \
  --name chatgrid_chat_ui \
  -p 8080:80 \
  chatgrid_chat_ui:latest
```

Access the application at http://localhost:8080

## Configuration

### Environment Variables

You can pass environment variables to the container:

```bash
docker run -d \
  --name chatgrid_chat_ui \
  -p 8080:80 \
  -e NODE_ENV=production \
  chatgrid_chat_ui:latest
```

### Custom Port

To run on a different port:

```bash
docker run -d \
  --name chatgrid_chat_ui \
  -p 3000:80 \
  chatgrid_chat_ui:latest
```

## Deployment

### Pushing to a Registry

```bash
# Tag the image
docker tag chatgrid_chat_ui:latest your-registry.com/chatgrid_chat_ui:latest

# Push to registry
docker push your-registry.com/chatgrid_chat_ui:latest
```

### Multi-Architecture Push

```bash
# Build and push for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t your-registry.com/chatgrid_chat_ui:latest \
  --push \
  .
```

## Architecture Details

The Dockerfile uses a multi-stage build:

1. **Builder Stage** (Node 20 Alpine)
   - Installs Yarn 3.5.1 via Corepack
   - Installs dependencies
   - Builds the application using Turborepo
   - Supports cross-compilation via BUILDPLATFORM/TARGETPLATFORM

2. **Production Stage** (Nginx Alpine)
   - Serves static files via Nginx
   - Configured for SPA routing
   - Enables gzip compression
   - Sets cache headers for static assets

## Troubleshooting

### BuildKit Error
If you see errors about BuildKit, ensure it's enabled:
```bash
export DOCKER_BUILDKIT=1
```

### Multi-Platform Load Error
Multi-platform images cannot be loaded directly into Docker. Either:
- Build for your current platform only: `./docker-build.sh local`
- Push to a registry: `./docker-build.sh push`

### Port Already in Use
If port 8080 is already in use, choose a different port:
```bash
docker run -d -p 9090:80 chatgrid_chat_ui:latest
```

## Health Check

The container includes a health check that verifies the Nginx server is running:

```bash
# Check container health status
docker inspect --format='{{.State.Health.Status}}' chatgrid_chat_ui
```

## Logs

View container logs:

```bash
# Follow logs
docker logs -f chatgrid_chat_ui

# View last 100 lines
docker logs --tail 100 chatgrid_chat_ui
```

## Cleanup

```bash

# Stop and remove container
docker stop chatgrid_chat_ui && docker rm chatgrid_chat_ui

# Remove image
docker rmi chatgrid_chat_ui:latest

# Remove builder instance
docker buildx rm multiarch-builder
```
