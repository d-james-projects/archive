# setup minio
``` bash
sudo docker run --restart always --net=host -p 9000:9000 -p 9001:9001 -v /disks/1:/data --name minio -d quay.io/minio/minio server /data --console-address ":9001"
```

!>check it is runnning ```nc -w 5 -v <ipaddr> 9001```

# loki install k3d
``` bash
k3d cluster create mycluster -v /tmp/data:/tmp/data@server[0] -v /var/log/journal:/tmp/journal@server[0]
```

``` bash
helm upgrade --install loki grafana/loki-stack  --set grafana.enabled=true,prometheus.enabled=true,prometheus.alertmanager.persistentVolume.enabled=false,prometheus.server.persistentVolume.enabled=false,loki.persistence.enabled=true,loki.persistence.storageClassName=local-path,loki.persistence.size=10Gi
```