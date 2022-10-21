# Setup
# Setup Openebs

?> **Tip** refer to this guide https://openebs.io/docs/user-guides/jiva/jiva-prerequisites

?> **check** versions used for this openebs-3.3.1 running VERSION="22.04 LTS (Jammy Jellyfish)" kube GitVersion:"v1.23.8+k3s1"


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
kubectl create -f hostpath-operator.yaml
kubectl create -f jiva-operator.yaml
kubectl create -f openebs-lite-sc.yaml
kubectl get sc
kubectl get all -n openebs
```
?> **Help** samples of user created yaml can be found in this [repo](https://github.com/d-james-projects/archive/tree/master/openebs)
# create some policy and storage class for jiva
``` bash
vim jiva-policy.yaml
vim jiva-sc.yaml
kubectl create -f jiva-policy.yaml 
kubectl create -f jiva-sc.yaml
kubectl get sc
```
# now use the classes and create some storage and workloads
``` bash
vim pvc.yaml
vim deploy.yaml
kubectl create -f pvc.yaml
kubectl get pvc -A
kubectl get pv
kubectl describe pv
```