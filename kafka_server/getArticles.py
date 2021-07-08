from kafka import KafkaProducer
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkConf, SparkContext
import json
import sys
import os
os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_DRIVER_PYTHON"]="/usr/bin/python3"


def getarticles(zkQuorum, group, topics, numThreads):
    spark_conf = SparkConf().setAppName("getArticles")
    sc = SparkContext(conf=spark_conf)
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 1)
    # 这里表示把检查点文件写入分布式文件系统HDFS，所以要启动Hadoop
    ssc.checkpoint(".")

    topicAry = topics.split(",")
    print(topicAry)
    print(type(topicAry))
    # 将topic转换为hashmap形式，而python中字典就是一种hashmap
    topicMap = {}
    for topic in topicAry:
        topicMap[topic] = numThreads
    lines = KafkaUtils.createStream(ssc, zkQuorum, group, topicMap).map(lambda x:x[1])
    # lines = KafkaUtils.createDirectStream(ssc=ssc, topics=topicAry, kafkaParams=kafkaParams ).map(lambda x:x[1])
    # lines.foreachRDD(lambda x:print(x.collect()))
    words = lines.map(lambda x: x.split("|"))
    words.foreachRDD(lambda x: x.foreach(lambda x: sendmsg(x)))

    ssc.start()
    ssc.awaitTermination()


# 格式转化，将[id,url,title,text]变为[{'id': }, {'url': }, {'title': }, {'text',}]
def get_json(rdd_list):
    res = {'id': rdd_list[0], 'url': rdd_list[1], 'title': rdd_list[2], 'text': rdd_list[3]}
    print(rdd_list[0])
    return json.dumps(res)


def sendmsg(rdd):
    if rdd.count != 0:
        msg = get_json(rdd)
        # 实例化一个KafkaProducer示例，用于向Kafka投递消息
        producer = KafkaProducer(bootstrap_servers=['hbase-master:9092'])
        producer.send("doc", msg.encode('utf8'))
        # 很重要，不然不会更新
        # producer.flush()


if __name__ == '__main__':
    # 输入的四个参数分别代表着
    # 1.zkQuorum为zookeeper地址
    # 2.group为消费者所在的组
    # 3.topics该消费者所消费的topics
    # 4.numThreads开启消费topic线程的个数
    if (len(sys.argv) < 5):
        print("Usage: getArticles <zkQuorum> <group> <topics> <numThreads>")
        exit(1)
    zkQuorum = sys.argv[1]
    group = sys.argv[2]
    topics = sys.argv[3]
    numThreads = int(sys.argv[4])
    print(group, topics)
    getarticles(zkQuorum, group, topics, numThreads)