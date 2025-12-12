#!/bin/bash

# Build and push Docker image
echo "Building Docker image..."
docker build -t tradeai:latest .

# Tag for your registry (update with your registry URL)
# docker tag tradeai:latest your-registry/tradeai:latest
# docker push your-registry/tradeai:latest

echo "Docker image built successfully!"
echo ""
echo "To run locally with Docker Compose:"
echo "  docker-compose up -d"
echo ""
echo "To deploy to Kubernetes:"
echo "  1. Update k8s-deployment.yaml with your registry URL"
echo "  2. Update secrets in k8s-deployment.yaml"
echo "  3. Run: kubectl apply -f k8s-deployment.yaml"
echo ""
echo "To check deployment status:"
echo "  kubectl get pods -n tradeai"
echo "  kubectl get services -n tradeai"
