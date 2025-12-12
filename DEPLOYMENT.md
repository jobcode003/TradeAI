# TradeAI Deployment Guide

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed

### Local Development with Docker Compose

1. **Build and run all services:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop services:**
   ```bash
   docker-compose down
   ```

4. **Access the application:**
   - Application: http://localhost:8000
   - With Nginx: http://localhost

### Building Docker Image

```bash
chmod +x docker-build.sh
./docker-build.sh
```

Or manually:
```bash
docker build -t tradeai:latest .
```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (minikube, GKE, EKS, AKS, etc.)
- kubectl configured
- Docker registry access

### Deployment Steps

1. **Update the image registry in k8s-deployment.yaml:**
   Replace `your-registry/tradeai:latest` with your actual registry URL.

2. **Update secrets:**
   Edit the `tradeai-secrets` section in `k8s-deployment.yaml`:
   - `SECRET_KEY`: Generate a new Django secret key
   - `DATABASE_URL`: Update if using external database
   - `POSTGRES_PASSWORD`: Change to a secure password

3. **Update ConfigMap:**
   Edit `ALLOWED_HOSTS` in the ConfigMap to include your domain.

4. **Build and push Docker image:**
   ```bash
   docker build -t your-registry/tradeai:latest .
   docker push your-registry/tradeai:latest
   ```

5. **Deploy to Kubernetes:**
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

6. **Check deployment status:**
   ```bash
   kubectl get pods -n tradeai
   kubectl get services -n tradeai
   ```

7. **Get the external IP:**
   ```bash
   kubectl get service tradeai-service -n tradeai
   ```

### Scaling

The deployment includes a Horizontal Pod Autoscaler (HPA) that automatically scales between 2-10 replicas based on CPU and memory usage.

Manual scaling:
```bash
kubectl scale deployment tradeai-web --replicas=5 -n tradeai
```

### Monitoring

View logs:
```bash
kubectl logs -f deployment/tradeai-web -n tradeai
```

Execute commands in a pod:
```bash
kubectl exec -it deployment/tradeai-web -n tradeai -- python manage.py shell
```

### Database Migrations

Migrations run automatically via init container. To run manually:
```bash
kubectl exec -it deployment/tradeai-web -n tradeai -- python manage.py migrate
```

### Cleanup

```bash
kubectl delete namespace tradeai
```

## Environment Variables

Required environment variables (set in .env for Docker or k8s secrets):

- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DEBUG`: Set to False in production

## Security Notes

1. **Change default passwords** in production
2. **Use proper secrets management** (e.g., Kubernetes Secrets, AWS Secrets Manager)
3. **Enable HTTPS** with cert-manager or cloud load balancer
4. **Set proper ALLOWED_HOSTS** in production
5. **Use a proper SECRET_KEY** (generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)

## Troubleshooting

### Docker Compose Issues

**Database connection errors:**
```bash
docker-compose down -v
docker-compose up -d
```

**Static files not loading:**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Kubernetes Issues

**Pods not starting:**
```bash
kubectl describe pod <pod-name> -n tradeai
kubectl logs <pod-name> -n tradeai
```

**Database connection issues:**
Check if PostgreSQL is running:
```bash
kubectl get pods -n tradeai | grep postgres
kubectl logs deployment/postgres -n tradeai
```

**Image pull errors:**
Ensure your image is pushed to the registry and credentials are configured:
```bash
kubectl create secret docker-registry regcred \
  --docker-server=<your-registry> \
  --docker-username=<username> \
  --docker-password=<password> \
  -n tradeai
```

Then add to deployment spec:
```yaml
imagePullSecrets:
- name: regcred
```
