BROKERS="hbase-master hbase-slave1 hbase-slave2 hbase-slave3"

# Kafka的安装目录
KAFKA_HOME="/root/kafka"

for broker in $BROKERS

do

        echo "INFO:starting kafka server on ${broker}"

        ssh $broker  "nohup /root/kafka/bin/kafka-server-start.sh -daemon /root/kafka/config/server.properties >/dev/null
 2>&1 &  "

        if [ $? != 0 ];

        then

                echo "Can not starting kafka server on host ${broker}";

                exit 1;
				
        fi
done
