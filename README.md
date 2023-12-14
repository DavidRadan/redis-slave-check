# Redis ICINGA Slave Connectivity Check

### Description
```
This plugin was written to see if all slave redis servers are really connected properly to master server.
Both python 2 and 3 now supported !!!
Tested on Rocky Linux 9.2
```

### Usage
```
python check_redis_slave.py -h
Usage: check_redis_slave.py [options]

Options:
  -h, --help  show this help message and exit
  -H HOST     Slave redis host address
  -P PORT     Redis tcp port, default 6379
  -p yourpassword  password for sentinel cluster

```
 
### Sample Plugin Output
```
[ugur@test]# python check_redis_slave.py -H <slave-redis-host> -P 6383
OK: slave redis is connected properly to master|master_last_io_seconds_ago=4;0;0;0

If slave connectivty was broken due to some reasons that it raised an alert.

[ugur@test]# python check_redis_slave.py -H <slave-redis-host> -P 6383
Critical: slave redis server is failed to connect master.It is down!


[root@redis01 root]# ./check_redis_slave.py -H 127.0.0.1 -P 6379 -p password
OK: slave redis is connected properly to the master|master_last_io_seconds_ago=0;0;0;0

```

### Tested with 
```
Icinga2 + Redis 7.2 - Redis 7.2 Cluster
Rocky Linux 9.2
Python 2
Python 3
```
