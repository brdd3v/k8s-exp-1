## NOTES


Build:
```
minikube image build -t fastapi-app .
```
or
```
docker build -t fastapi-app .
minikube image load fastapi-app:latest
```

Confirm:
```
minikube image ls | grep fastapi
```
