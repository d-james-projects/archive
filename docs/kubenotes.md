dont lose connection
ping -i 5 localhost

basic checks/debug

docker running
systemctl status docker
docker ps -a

pull test image
docker run -it --rm busybox
docker pull busybox
docker images

kubelet running
systemctl -l --no-pager status kubelet
/usr/bin/kubelet --kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true --pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true --network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin --cluster-dns=10.96.0.10 --cluster-domain=cluster.local --authorization-mode=Webhook --client-ca-file=/etc/kubernetes/pki/ca.crt

add logging
edit kubelet systemctl config (/etc/systemd/system or usr/lib/systemd/system)
--v=4
systemctl daemon-reload
systemctl restart kubelet
systemctl -l --no-pager status kubelet

journalctl --unit=kubelet -xr --no-pager > /tmp/kublet.log
journalctl -f

run as a cmd (sudo su -)
cmd >>file.txt 2>&1
/usr/bin/kubelet --kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true --pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true --network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin --cluster-dns=10.96.0.10 --cluster-domain=cluster.local --authorization-mode=Webhook --client-ca-file=/etc/kubernetes/pki/ca.crt --v=4 >>/tmp/kubelog 2>&1

pod logging and controls
export KUBECONFIG=$HOME/admin.conf
kubectl get pods -o wide --all-namespaces
kubectl describe nodes --all-namespaces
kubectl describe services --all-namespaces
kubectl run -i --tty busybox --image=busybox -- sh
kubectl exec -ti busybox-4153010557-gltkd -- sh

kubectl logs etcd-k8-master --namespace=kube-system >/tmp/etcdlog
sudo less /var/log/containers/etcd-k8-master_kube-system_etcd-*
change logging level
etcd
curl http://127.0.0.1:2379/config/local/log -XPUT -d '{"Level":"DEBUG"}'
curl http://127.0.0.1:2379/config/local/log -XPUT -d '{"Level":"INFO"}'
not shared approach across all containers
apiserver
edit /etc/kubernetes/manifest file and restart kubelet

testing etcd
kubectl exec etcd-k8-master --namespace=kube-system -- etcdctl -v
kubectl exec etcd-k8-master --namespace=kube-system -- etcdctl set /mykey helloworld
kubectl exec etcd-k8-master --namespace=kube-system -- etcdctl get /mykey

testing kube proxy
kubectl proxy
sudo iptables -L
sudo iptables-save

testing api server
kubectl proxy
curl <address>/version
kubectl cluster-info dump >/tmp/cluster.dump

dns
create busybox
kubectl exec -ti busybox -- nslookup kubernetes

/usr/bin/kubelet --kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true --pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true --network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin --cluster-dns=10.96.0.10 --cluster-domain=cluster.local --authorization-mode=Webhook --client-ca-file=/etc/kubernetes/pki/ca.crt --v=4 --hostname-override=192.168.99.99 >>/tmp/kubelog 2>&1

removal and clean down

kubectl get node
kubectl drain 192.168.99.99 --delete-local-data --force --ignore-daemonsets
kubectl delete node 192.168.99.99

sudo kubeadm reset
[preflight] Running pre-flight checks
[reset] Stopping the kubelet service
[reset] Unmounting mounted directories in "/var/lib/kubelet"
[reset] Removing kubernetes-managed containers
[reset] Deleting contents of stateful directories: [/var/lib/kubelet /etc/cni/net.d /var/lib/etcd]
[reset] Deleting contents of config directories: [/etc/kubernetes/manifests /etc/kubernetes/pki]
[reset] Deleting files: [/etc/kubernetes/admin.conf /etc/kubernetes/kubelet.conf /etc/kubernetes/controller-manager.conf /etc/kubernetes/scheduler.conf]


apt-get remove kubelet kubeadm kubernetes-cni
ls /opt/cni/bin
rm -r /opt/cni/*
rmdir /opt/cni
rm -r /var/lib/kubelet
/var/run/kubernetes
/var/lib/etcd

drain node
remove node
docker?

weave launch
--log-level=debug





