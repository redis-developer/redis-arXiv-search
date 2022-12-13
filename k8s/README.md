# Running with Kubernetes

This demo leverages the pre-built docker containers deployed in a sandbox k8s environment on your localhost.

## Prerequisites
If you already have a K8s cluster, bypass the setup steps and utilize the K8s manifests and configs however you need.

Install [kubectl](https://kubernetes.io/docs/reference/kubectl/), [kind](https://kind.sigs.k8s.io/), and [kompose](https://kompose.io/).

## Create Cluster with Kind
```bash
kind create cluster --config=cluster.yaml
kubectl cluster-info --context kind-arxiv-search
```

Then apply the ingress:
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Apply the resources:
```bash
kubectl apply -f redis-vector-db.yaml
```
>Pause for like 30 seconds here to make sure Redis is up

```bash
kubectl apply -f backend.yaml
```

## Validate Cluster
```bash
kubectl get nodes
```
```bash
kubectl get pods
```
Inspect logs etc...
## Expose Ports and Test App
Port forward the backend service to connect to the app on `localhost:8888`:
```
kubectl port-forward service/backend 8888:8888
```

Then navigate to `http://localhost:8888/`

## Cleaning Up

```bash
kind delete cluster --name arxiv-search
```

