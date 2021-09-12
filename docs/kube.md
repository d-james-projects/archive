ip route list
netstat -r
route -n
iptables -L

setenforce 0
systemctl disable iptables-services firewalld
systemctl stop iptables-services firewalld

netstat -r
terminal 1 (99.99)
----------
nc -l 1234
terminal 2 (98.98)nc
----------
nc 192.168.99.99


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

linux find all files in sub dir called *.py

find . -type f -name *.py
find . -type f -name *prop*
