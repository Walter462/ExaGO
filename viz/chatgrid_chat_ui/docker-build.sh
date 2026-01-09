#!/bin/bash

# Script to build multi-architecture Docker images
# Supports Apple ARM64 (M1/M2/M3) and Intel64 (AMD64)

set -e

IMAGE_NAME="${IMAGE_NAME:-chatgrid_chat_ui}"
IMAGE_TAG="${IMAGE_TAG:-latest-multi-platform}"

echo "Building multi-architecture Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "Platforms: linux/amd64, linux/arm64"

# Create buildx builder if it doesn't exist
if ! docker buildx inspect multiarch-builder > /dev/null 2>&1; then
    echo "Creating new buildx builder instance..."
    docker buildx create --name multiarch-builder --use
else
    echo "Using existing buildx builder..."
    docker buildx use multiarch-builder
fi

# Bootstrap the builder
docker buildx inspect --bootstrap

# Build and push (or load for single platform)
if [ "$1" == "push" ]; then
    echo "Building and pushing to registry..."
    docker buildx build \
        --platform linux/amd64,linux/arm64 \
        -t ${IMAGE_NAME}:${IMAGE_TAG} \
        --push \
        .
elif [ "$1" == "local" ]; then
    echo "Building for local platform only..."
    docker buildx build \
        --platform linux/$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/') \
        -t ${IMAGE_NAME}:${IMAGE_TAG} \
        --load \
        .
else
    echo "Building for both platforms (saving to Docker)..."
    docker buildx build \
        --platform linux/amd64,linux/arm64 \
        -t ${IMAGE_NAME}:${IMAGE_TAG} \
        --load \
        .
    echo ""
    echo "Note: Multi-platform images cannot be loaded directly to Docker."
    echo "Use './docker-build.sh local' to build for your current platform only,"
    echo "or './docker-build.sh push' to push to a registry."
fi

echo ""
echo "Build complete! 🎉"
echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
