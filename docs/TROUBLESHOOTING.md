# Week 13 Troubleshooting

## ImagePullBackOff
The image may not be loaded into Minikube. Re-run:

```bash
minikube image load week13-helpdesk:v1.0.0
```

Then restart the Deployment:

```bash
kubectl rollout restart deployment/helpdesk -n week13
```

## PVC Pending
Check the default StorageClass:

```bash
kubectl get storageclass
kubectl describe pvc postgres-data -n week13
```

## Help Desk pods are not Ready
Check whether PostgreSQL is Ready and inspect the application logs:

```bash
kubectl get pods -n week13
kubectl logs deployment/helpdesk -n week13
```

## Browser cannot reach the application
Use port-forward:

```bash
kubectl port-forward svc/helpdesk 8080:80 -n week13
```

Then browse to http://localhost:8080.

## Secret missing
Create it locally (do not commit it):

```bash
kubectl create secret generic helpdesk-secret \
  --namespace week13 \
  --from-literal=DB_PASSWORD=week13-demo-password
```
