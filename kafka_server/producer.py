# coding: utf-8
import time
import json

import os

os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_DRIVER_PYTHON"]="/usr/bin/python3"

from kafka import KafkaProducer
 
# 实例化一个KafkaProducer示例，用于向Kafka投递消息
producer = KafkaProducer(bootstrap_servers='hbase-master:9092')
# 打开数据文件
file = open("/code/wikisearch/wikidata/zhwiki_01","r")
count = 1
for line in file:
    print(count)
    line = line.split('|')
    res = {'id': line[0], 'url': line[1], 'title': line[2], 'text': line[3]}
    res = json.dumps(res)
    producer.send('doc', res.encode('utf8'))
    # result = future.get(timeout=10)
    count = count+1
producer.flush()
