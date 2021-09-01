dev1@k8-master ~/weave-util $ cat /tmp/weave.log 
INFO: 2017/05/17 21:04:24.070832 Command line options: map[nickname:k8-master no-dns:true port:6783 status-addr:0.0.0.0:6782 ipalloc-range:10.32.0.0/12 log-level:debug docker-api: conn-limit:30 http-addr:127.0.0.1:6784 iface:vethwe-pcap ipalloc-init:consensus=2]
INFO: 2017/05/17 21:04:24.071256 Communication between peers is unencrypted.
INFO: 2017/05/17 21:04:24.088249 Our name is 4e:2e:60:5d:49:47(k8-master)
INFO: 2017/05/17 21:04:24.088616 Launch detected - using supplied peer list: [192.168.99.98 192.168.99.99]
INFO: 2017/05/17 21:04:24.088914 Checking for pre-existing addresses on weave bridge
INFO: 2017/05/17 21:04:24.099164 [allocator 4e:2e:60:5d:49:47] Initialising with persisted data
INFO: 2017/05/17 21:04:24.099502 Sniffing traffic on vethwe-pcap (via pcap)
INFO: 2017/05/17 21:04:24.127724 ->[192.168.99.99:6783] attempting connection
INFO: 2017/05/17 21:04:24.128679 ->[192.168.99.98:6783] attempting connection
INFO: 2017/05/17 21:04:24.140395 ->[192.168.99.99:57864] connection accepted
INFO: 2017/05/17 21:04:24.144539 ->[192.168.99.99:57864|4e:2e:60:5d:49:47(k8-master)]: connection shutting down due to error: cannot connect to ourself
INFO: 2017/05/17 21:04:24.145396 ->[192.168.99.99:6783|4e:2e:60:5d:49:47(k8-master)]: connection shutting down due to error: cannot connect to ourself
INFO: 2017/05/17 21:04:24.147456 ->[192.168.99.98:6783|4a:a7:26:e0:34:74(k8-worker)]: connection ready; using protocol version 2
INFO: 2017/05/17 21:04:24.154173 overlay_switch ->[4a:a7:26:e0:34:74(k8-worker)] using sleeve
INFO: 2017/05/17 21:04:24.170885 ->[192.168.99.98:6783|4a:a7:26:e0:34:74(k8-worker)]: connection added (new peer)
DEBU: 2017/05/17 21:04:24.171380 sleeve ->[192.168.99.98:6783|4a:a7:26:e0:34:74(k8-worker)]: Confirm
INFO: 2017/05/17 21:04:24.148699 Listening for HTTP control messages on 127.0.0.1:6784
INFO: 2017/05/17 21:04:24.172716 Listening for metrics requests on 0.0.0.0:6782
DEBU: 2017/05/17 21:04:24.173233 sleeve ->[192.168.99.98:6783|4a:a7:26:e0:34:74(k8-worker)]: confirmed
DEBU: 2017/05/17 21:04:24.173387 sleeve ->[192.168.99.98:6783|4a:a7:26:e0:34:74(k8-worker)]: sendHeartbeat
DEBU: 2017/05/17 21:04:24.198215 [allocator 4e:2e:60:5d:49:47]: Allocator.OnGossip: 754 bytes
DEBU: 2017/05/17 21:04:24.209725 sleeve ->[192.168.99.98:6783|4a:a7:26:e0:34:74(k8-worker)]: handleHeartbeat
DEBU: 2017/05/17 21:04:24.209952 sleeve ->[192.168.99.98:6783|4a:a7:26:e0:34:74(k8-worker)]: handleHeartbeatAck
DEBU: 2017/05/17 21:04:24.209974 sleeve ->[192.168.99.98:6783|4a:a7:26:e0:34:74(k8-worker)]: sendFragTest
INFO: 2017/05/17 21:04:24.216981 ->[192.168.99.98:6783|4a:a7:26:e0:34:74(k8-worker)]: connection fully established

