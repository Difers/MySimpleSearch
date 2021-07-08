#stop
#!/bin/bash
BROKERS="hbase-master hbase-slave1 hbase-slave2 hbase-slave3"

for host in $BROKERS

do
        ssh $host "source /etc/profile;jps |grep Kafka |cut -c 1-6 |xargs kill -s 9"
        echo "$host kafka is stopping"
done
