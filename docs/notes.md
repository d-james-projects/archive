$ sudo mount -r /dev/sdc1 /home/david/mnt

ip route list
netstat -r
route -n
iptables -L

setenforce 0
systemctl disable iptables-services firewalld
systemctl stop iptables-services firewalld

apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
# Install docker if you don't have it already.
apt-get install -y docker-engine
apt-get install -y kubelet kubeadm kubectl kubernetes-cni


netstat -r

terminal 1 (99.99)
----------
nc -l 1234

terminal 2 (98.98)nc
----------
nc 192.168.99.99

export ARCH=amd64
curl -sSL "https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml?raw=true" | sed "s/amd64/${ARCH}/g" | kubectl create -f -

for SERVICES in etcd kube-apiserver kube-controller-manager kube-scheduler flanneld kubelet kubernetes-cni; do
    systemctl restart $SERVICES
    systemctl status $SERVICES
done

    systemctl enable $SERVICES
    systemctl disable $SERVICES

list (ls) hardware
lshw -class network

disable networkmanager
/etc/network/interfaces
ifup/ifdown

cat interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)
auto lo
iface lo inet loopback

auto enp0s3
iface enp0s3 inet dhcp

auto enp0s8
iface enp0s8 inet static
address 192.168.99.99
netmask 255.255.255.0



--pod-network-cidr=10.244.0.0/16
--apiserver-advertise-address=192.168.99.99

kubeadm init --apiserver-advertise-address=192.168.99.99 --pod-network-cidr=10.244.0.0/16 --hostname-override=192.168.99.99


k8-master ~ # kubeadm init --apiserver-advertise-address=192.168.99.99 --pod-network-cidr=10.244.0.0/16
[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
[init] Using Kubernetes version: v1.6.0
[init] Using Authorization mode: RBAC
[preflight] Running pre-flight checks
[certificates] Generated CA certificate and key.
[certificates] Generated API server certificate and key.
[certificates] API Server serving cert is signed for DNS names [k8-master kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.99.99]
[certificates] Generated API server kubelet client certificate and key.
[certificates] Generated service account token signing key and public key.
[certificates] Generated front-proxy CA certificate and key.
[certificates] Generated front-proxy client certificate and key.
[certificates] Valid certificates and keys now exist in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/admin.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/controller-manager.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/scheduler.conf"
[apiclient] Created API client, waiting for the control plane to become ready
[apiclient] All control plane components are healthy after 127.585044 seconds
[apiclient] Waiting for at least one node to register
[apiclient] First node has registered after 6.068691 seconds
[token] Using token: ab3da9.83a88711dc532780
[apiconfig] Created RBAC rules
[addons] Created essential addon: kube-proxy
[addons] Created essential addon: kube-dns

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run (as a regular user):

  sudo cp /etc/kubernetes/admin.conf $HOME/
  sudo chown $(id -u):$(id -g) $HOME/admin.conf
  export KUBECONFIG=$HOME/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  http://kubernetes.io/docs/admin/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join --token ab3da9.83a88711dc532780 192.168.99.99:6443

source <(kubectl completion bash)

kubectl apply -f https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml
kubectl version 
export ARCH=amd64
curl -sSL "https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml?raw=true" | sed "s/amd64/${ARCH}/g" | kubectl create -f -

*****
kubectl create -f https://github.com/kubernetes/dashboard/blob/master/src/deploy/kubernetes-dashboard.yaml
error: error converting YAML to JSON: yaml: line 289: mapping values are not allowed in this context
*****

# Create the clusterrole and clusterrolebinding:
# $ kubectl create -f https://github.com/coreos/flannel/tree/master/Documentation/kube-flannel-rbac.yml
# Create the pod using the same namespace used by the flannel serviceaccount:
# $ kubectl create --namespace kube-system -f https://github.com/coreos/flannel/tree/master/Documentation/kube-flannel.yml

curl -sSL "https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel-rbac.yml?raw=true" > kube-flannel-rbac.yml
kubectl create -f kube-flannel-rbac.yml

curl -sSL "https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml?raw=true" > kube-flannel.yml
kubectl create -f kube-flannel.yml

curl -sSL "https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/kubernetes-dashboard.yaml?raw=true" > kubernetes-dashboard.yaml
ls
cat kubernetes-dashboard.yaml
kubectl create -f kubernetes-dashboard.yaml
kubectl get pods --all-namespaces
docker images


logs in pod flannel (2 containers)
install-cni 
2017-04-26T19:29:59.193541363Z + cp -f /etc/kube-flannel/cni-conf.json /etc/cni/net.d/10-flannel.conf
2017-04-26T19:29:59.220916992Z + true
2017-04-26T19:29:59.220948495Z + sleep 3600
2017-04-26T20:29:59.228642616Z + true
2017-04-26T20:29:59.229746939Z + sleep 3600 

install-cni
Image:
quay.io/coreos/flannel:v0.7.1-amd64 
set -e -x; cp -f /etc/kube-flannel/cni-conf.json /etc/cni/net.d/10-flannel.conf; while true; do sleep 3600; done


flannel logs

Image:
quay.io/coreos/flannel:v0.7.1-amd64
Environment variables:
POD_NAME : 
POD_NAMESPACE : 
Commands:
/opt/bin/flanneld
--ip-masq
--kube-subnet-mgr




http://192.168.99.99:31677/#!/service?namespace=_all

DNS
 2017-04-26T21:00:04.628904211Z I0426 21:00:04.628874       1 dns.go:264] New service: kubernetes-dashboard
2017-04-26T21:03:19.106422881Z I0426 21:03:19.106256       1 dns.go:293] removeService kubernetes-dashboard at path [local cluster svc kube-system kubernetes-dashboard]. Success: true
2017-04-26T21:05:04.628392292Z I0426 21:05:04.628234       1 dns.go:264] New service: kubernetes
2017-04-26T21:05:04.628853029Z I0426 21:05:04.628765       1 dns.go:462] Added SRV record &{Host:kubernetes.default.svc.cluster.local. Port:443 Priority:10 Weight:10 Text: Mail:false Ttl:30 TargetStrip:0 Group: Key:}
2017-04-26T21:05:04.629075303Z I0426 21:05:04.629033       1 dns.go:264] New service: kube-dns
2017-04-26T21:05:04.629342844Z I0426 21:05:04.629222       1 dns.go:462] Added SRV record &{Host:kube-dns.kube-system.svc.cluster.local. Port:53 Priority:10 Weight:10 Text: Mail:false Ttl:30 TargetStrip:0 Group: Key:}
2017-04-26T21:05:04.629561961Z I0426 21:05:04.629457       1 dns.go:462] Added SRV record &{Host:kube-dns.kube-system.svc.cluster.local. Port:53 Priority:10 Weight:10 Text: Mail:false Ttl:30 TargetStrip:0 Group: Key:}
2017-04-26T21:05:57.659283365Z I0426 21:05:57.659126       1 dns.go:264] New service: kubernetes-dashboard 


proxy
 2017-04-26T16:05:35.507415798Z I0426 16:05:35.507190       1 server.go:225] Using iptables Proxier.
2017-04-26T16:05:35.542630445Z W0426 16:05:35.542516       1 server.go:469] Failed to retrieve node info: User "system:serviceaccount:kube-system:kube-proxy" cannot get nodes at the cluster scope. (get nodes k8-master)
2017-04-26T16:05:35.542948093Z W0426 16:05:35.542882       1 proxier.go:304] invalid nodeIP, initializing kube-proxy with 127.0.0.1 as nodeIP
2017-04-26T16:05:35.543027046Z I0426 16:05:35.542998       1 server.go:249] Tearing down userspace rules.
2017-04-26T16:05:35.564744366Z E0426 16:05:35.564646       1 reflector.go:201] k8s.io/kubernetes/pkg/proxy/config/api.go:49: Failed to list *api.Endpoints: User "system:serviceaccount:kube-system:kube-proxy" cannot list endpoints at the cluster scope. (get endpoints)
2017-04-26T16:05:35.565008306Z E0426 16:05:35.564933       1 reflector.go:201] k8s.io/kubernetes/pkg/proxy/config/api.go:46: Failed to list *api.Service: User "system:serviceaccount:kube-system:kube-proxy" cannot list services at the cluster scope. (get services)
2017-04-26T16:05:36.674246404Z I0426 16:05:36.674137       1 conntrack.go:81] Set sysctl 'net/netfilter/nf_conntrack_max' to 131072
2017-04-26T16:05:36.676656281Z I0426 16:05:36.676593       1 conntrack.go:66] Setting conntrack hashsize to 32768
2017-04-26T16:05:36.677217808Z I0426 16:05:36.677064       1 conntrack.go:81] Set sysctl 'net/netfilter/nf_conntrack_tcp_timeout_established' to 86400
2017-04-26T16:05:36.677357506Z I0426 16:05:36.677301       1 conntrack.go:81] Set sysctl 'net/netfilter/nf_conntrack_tcp_timeout_close_wait' to 3600 


linux find all files in sub dir called *.py

find . -type f -name *.py
find . -type f -name *prop*

allow scheduling on master (as well as slaves)
kubectl taint nodes --all node-role.kubernetes.io/master-
kubectl describe nodes

need to modify the kubelet drop in .conf to include --hostname-override=192.168.99.99
/etc/systemd/system/kubelet.service.d
hh
sudo cat 10-kubeadm.conf 
[Service]
Environment="KUBELET_KUBECONFIG_ARGS=--kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true --v=4 --hostname-override=192.168.99.99"
Environment="KUBELET_SYSTEM_PODS_ARGS=--pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true"
Environment="KUBELET_NETWORK_ARGS=--network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin"
Environment="KUBELET_DNS_ARGS=--cluster-dns=10.96.0.10 --cluster-domain=cluster.local"
Environment="KUBELET_AUTHZ_ARGS=--authorization-mode=Webhook --client-ca-file=/etc/kubernetes/pki/ca.crt"
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_SYSTEM_PODS_ARGS $KUBELET_NETWORK_ARGS $KUBELET_DNS_ARGS $KUBELET_AUTHZ_ARGS $KUBELET_EXTRA_ARGS

You can now join any number of machines by running the following on each node
as root:

  kubeadm join --token 5ad7f5.008d98696047fbd4 192.168.99.99:6443

sudo curl -s -L git.io/weave -o /usr/local/bin/weave && sudo chmod +x /usr/local/bin/weave

