#!/bin/bash

# Script to build and push Docker images to Docker Hub

# Exit immediately if a command exits with a non-zero status.
set -e

# Define your Docker Hub username
DOCKER_HUB_USERNAME="ayon1901"

# Define image names
BACKEND_IMAGE_NAME="human-detection-backend"
FRONTEND_IMAGE_NAME="human-detection-frontend"
TAG="latest"

# Full image names
FULL_BACKEND_IMAGE="${DOCKER_HUB_USERNAME}/${BACKEND_IMAGE_NAME}:${TAG}"
FULL_FRONTEND_IMAGE="${DOCKER_HUB_USERNAME}/${FRONTEND_IMAGE_NAME}:${TAG}"

echo "-------------------------------------"
echo "Building Backend Docker image..."
echo "Image: ${FULL_BACKEND_IMAGE}"
echo "Dockerfile: backend/Dockerfile"
echo "Context: . (project root)"
echo "-------------------------------------"
docker build -t "${FULL_BACKEND_IMAGE}" -f backend/Dockerfile .

echo "-------------------------------------"
echo "Building Frontend Docker image..."
echo "Image: ${FULL_FRONTEND_IMAGE}"
echo "Dockerfile: frontend/Dockerfile"
echo "Context: ./frontend"
echo "-------------------------------------"
docker build -t "${FULL_FRONTEND_IMAGE}" -f frontend/Dockerfile ./frontend

echo "-------------------------------------"
echo "Pushing Backend image to Docker Hub..."
echo "-------------------------------------"
docker push "${FULL_BACKEND_IMAGE}"

echo "-------------------------------------"
echo "Pushing Frontend image to Docker Hub..."
echo "-------------------------------------"
docker push "${FULL_FRONTEND_IMAGE}"

echo "-------------------------------------"
echo "Script finished successfully!"
echo "Backend Image: ${FULL_BACKEND_IMAGE}"
echo "Frontend Image: ${FULL_FRONTEND_IMAGE}"
echo "-------------------------------------" 