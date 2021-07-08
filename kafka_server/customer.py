from kafka import KafkaConsumer
import logging
# logging.basicConfig(level=logging.DEBUG)

consumer = KafkaConsumer('doc', bootstrap_servers='hbase-master:9092')
print('start receive')
for msg in consumer:
    print((msg.value).decode('utf8'))