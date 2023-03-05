# Setup
# Setup Storage Components
# OpenEBS

?> **Tip** refer to this guide https://openebs.io/docs/user-guides/installation#installation-through-kubectl

?> **check** versions used for this openebs-3.4 running VERSION="22.04 LTS (Jammy Jellyfish)" kube GitVersion:"v1.23.8+k3s1"


**Clone the latest chart repo and checkout the gh-pages for the yaml files**
# Clone latest charts
``` bash
git clone https://github.com/openebs/charts.git
cd charts/
git checkout gh-pages
```
# Pre-reqs
***install pre-reqs (this is basically iscsid running on each worker node with storage)***
``` bash
kubectl create -f openebs-ubuntu-setup.yaml
kubectl get pods -n openebs
```
# Install the operators
``` bash
kubectl get sc
kubectl create -f openebs-operator.yaml
kubectl create -f jiva-operator.yaml
kubectl get sc
kubectl get all -n openebs
```
?> **Help** samples of user created yaml can be found in this [repo](https://github.com/d-james-projects/archive/tree/master/storage)
# create some policy and storage class for jiva
``` bash
vim policy.yaml
vim sc.yaml
kubectl create -f policy.yaml 
kubectl create -f sc.yaml
kubectl get sc
```
# now use the classes and create some storage and workloads
``` bash
kubectl apply -f examples/local-hostpath/example-jiva.yaml
kubectl get pods -A
kubectl get pvc -A
```

# Minio
?> **check** versions used for this minio operator 4.5.8 running VERSION="22.04 LTS (Jammy Jellyfish)" kube GitVersion:"v1.23.8+k3s1"
``` bash
helm repo add minio https://operator.min.io/
helm show values minio/operator | less
```
# use ingress for the operator console 
``` bash
helm show values minio/operator > operator-values-ingress.yaml
vim operator-values-ingress.yaml
kubectl get ingressclass -n traefik traefik -o yaml
helm upgrade --namespace minio-operator --create-namespace minio-operator minio/operator -f operator-values-ingress.yaml
kubectl get ingress -A
```
# get token and log into the console
``` bash
kubectl -n minio-operator  get secret console-sa-secret -o jsonpath="{.data.token}" | base64 --decode
```
# use helm chart for tenant install - seems fairly straightforward vs. console
``` bash
helm show values minio/tenant > minio-tenant.yaml
vim minio-tenant.yaml
helm install --namespace minio-tenant --create-namespace tenant minio/tenant -f minio-tenant.yaml
kubectl get pvc -A
kubectl get all -n minio-tenant
```
# login and view tenant console
``` bash
kubectl get svc -A
kubectl --namespace minio-tenant port-forward svc/minio 9443:443 --address 192.168.56.201
```
# use mc in docker container to access s3 buckets
# start docker container
``` bash
docker run -it --name mc --entrypoint=/bin/sh --net=host minio/mc
```
# use mc
``` bash
mc --insecure alias set minio https://192.168.56.201:9443
mc --insecure ls minio
```

