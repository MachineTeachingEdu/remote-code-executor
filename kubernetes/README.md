kubectl create secret docker-registry gcr-json-key \
 --docker-server=gcr.io \
 --docker-username=\_json_key \
 --docker-password="$(cat ./machine-teaching-service-account-credentials.json)" \
 --docker-email=kubernetes-service-account@tcc-mt.iam.gserviceaccount.com

`kubectl apply -f worker-configmap.yaml
kubectl apply -f svc-worker.yaml
kubectl apply -f worker-deployment.yaml`
