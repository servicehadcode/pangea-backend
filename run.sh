#!/bin/bash
 
# Script to run the Pangea Backend API with Podman
 
# Stop and remove the container and pod if they exist
echo "Cleaning up existing containers and pods..."
podman pod rm -f pangea-pod 2>/dev/null || true
podman rm -f pangea-backend 2>/dev/null || true
podman rm -f pangea-mongo 2>/dev/null || true
 
# Create a pod for networking
echo "Creating pod for networking..."
podman pod create --name pangea-pod -p 5000:5000 -p 27017:27017
 
# Start MongoDB
echo "Starting MongoDB container..."
podman run -d --pod pangea-pod \
    --name pangea-mongo \
    -v pangea-mongo-data:/data/db \
    mongo:4.4
 
# Wait for MongoDB to start
echo "Waiting for MongoDB to start..."
sleep 5
 
# Build the API image
echo "Building API image..."
podman build -t pangea-backend .
 
# Run the API container
echo "Starting API container..."
podman run -d --pod pangea-pod \
    --name pangea-backend \
    -e FLASK_APP=src/app.py \
    -e FLASK_ENV=development \
    -e FLASK_DEBUG=1 \
    -e PORT=5000 \
    -e MONGODB_URI=mongodb://pangea-mongo:27017 \
    -e MONGODB_DB=pangea \
    pangea-backend
 
# Check if the API container is running
if podman ps | grep -q pangea-backend; then
    echo "Pangea Backend API is now running!"
    echo "API is available at: http://localhost:5000"
    echo "MongoDB is available at: localhost:27017"
    echo ""
    echo "To view API logs: podman logs -f pangea-backend"
    echo "To view MongoDB logs: podman logs -f pangea-mongo"
    echo "To stop all containers: ./podman-stop.sh"
else
    echo "Failed to start API container. Checking logs:"
    podman logs pangea-backend
    exit 1
fi
 