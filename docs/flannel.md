# setup 
``` bash
sudo docker run --restart always --net=host -p 9000:9000 -p 9001:9001 -v /disks/1:/data --name minio -d quay.io/minio/minio server /data --console-address ":9001"
```

!> **check** it is runnning ```nc -w 5 -v <ipaddr> 9001```

https://docs.projectcalico.org/getting-started/kubernetes/flannel/flannel
https://docs.projectcalico.org/networking/determine-best-networking#about-calico-networking

wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

flannel changing backend to vxlan
kubectl edit configmap -n kube-system kube-flannel-cfg <- change udp for vxlan
kubectl delete pod -n kube-system -l app=flannel

flannel directrouting=true

IPAM host-local
change to calico

curl https://docs.projectcalico.org/manifests/canal.yaml -O

``` bash
net-conf.json: |
                {
                    "Network": "10.244.0.0/16",
                    "Backend": {
                        "Type": "vxlan",
                        "Directrouting": true  #There is no section by default. If you want to modify it, you must reinstall the flannel plugin! ! !
                }
```

for dhcp on internal net
VBoxManage dhcpserver add –netname intnet –ip 10.13.13.100 –netmask 255.255.255.0 –lowerip 10.13.13.101 –upperip 10.13.13.254 –enable

using /etc/network/interfaces for static ip 192.168.1.1 and 1.2
enp0s8:

intnet <- internal network type vbox

starting with
``` json
  net-conf.json: |
    {
      "Network": "10.244.0.0/16",
      "Backend": {
        "Type": "host-gw"
      }
    }
```
``` yaml
      containers:
      - name: kube-flannel
        image: quay.io/coreos/flannel:v0.15.1
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        - --iface=enp0s8
```

edit configmap
restart pods

``` bash
kubectl edit cm -n kube-system kube-flannel-cfg
kubectl delete pods -n kube-system -l app=flannel
```
canal.yaml
will need to set CALICO_IPV4POOL_CIDR

``` bash
kubectl apply -f canal.yaml
```

The geeky details of what you get:

Policy
Calico
IPAM
Host-local
CNI
Calico
Overlay
VXLAN
Routing
Static
Datastore
Kubernetes

IPAM -> calico?
