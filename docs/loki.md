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
``` bash
helm upgrade loki grafana/loki-stack  --set grafana.enabled=true,prometheus.enabled=true,prometheus.alertmanager.persistentVolume.enabled=false,prometheus.server.persistentVolume.enabled=false,loki.persistence.enabled=true,loki.persistence.storageClassName=local-path,loki.persistence.size=10Gi -f values.yaml
```

``` yaml
loki:
  enabled: true
  config:
    storage_config:
      aws:
        # Note: use a fully qualified domain name, like localhost.
        # full example: http://loki:supersecret@localhost.:9000
        #s3: http://user:password@192.168.2.222:9000
        s3: s3://user:password@192.168.2.222:9000/test
        s3forcepathstyle: true
      boltdb_shipper:
        active_index_directory: /loki/boltdb-shipper-active
        cache_location: /loki/boltdb-shipper-cache
        cache_ttl: 24h         # Can be increased for faster performance over longer query periods, uses more disk space
        shared_store: s3

    schema_config:
      configs:
        - from: 2020-07-01
          store: boltdb-shipper
          object_store: aws
          schema: v11
          index:
            prefix: index_
            period: 24h
```

