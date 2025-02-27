# -*- coding: utf-8 -*-
# @Time    : 2023/6/22 16:58
# @Author  : SPC
# @File    : aio_kafka.py
# @Project : kafka_data
# @Software: PyCharm
import json
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError
import random


# class RandomPartitioner:
#     def __init__(self, partitions):
#         self.partitions = partitions

#     def __call__(self, topic, key, value, all_partitions, available_partitions):
#         # 生成一个随机的分区索引
#         random_partition = random.choice(available_partitions)
#         return random_partition


def result_to_kafka(c: str, m: str, wafer_id: str, ai_result: str, result_name: str, eqp_blk: str, topic: str):
    s = ''
    # name = m[:-4]  # -4
    # if c == "EL_OK_22.6":
    #     s = "EL_OK_DX"  # EL_OK_DX bin
    # else:
    if ai_result == 0:
        s = "OK"  # 当为正常片时，则传送信号OK
    elif ai_result == 1:
        s = "NG"  # 当为NG片时，则传送信号NG
    if ai_result == 1:   # 只推送NG
        # 配置Kafka连接信息
        bootstrap_servers = 'f4kafka01.aikosolar.net:9092,f4kafka02.aikosolar.net:9092,f4kafka03.aikosolar.net:9092'  # Kafka broker的地址和端口
        # topic = 'data-collection-ai-ct-agrade'  # 要写入的Kafka主题
        # 创建KafkaProducer实例
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                acks='all',  # 确认写入的所有副本都已接收到消息
                                retries=2,  # 发送失败时的重试次数
                                # partitioner=RandomPartitioner,
                                )

        ticks = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 当前时间戳
        # 指定要发送的分区，随机指定的分区
        # partition = 2
        partitions = producer.partitions_for(topic)
        partition = random.choice(list(partitions))
        # 准备要发送的消息
        # message = b'Hello, Kafka!'  # 将消息转换为字节串
        data = {
            'eqp_blk': eqp_blk,
            'wafer_id': wafer_id,
            'photo_id': m,
            'work_time': ticks,
            'grade': s,
            'result': result_name
        }
        # 将JSON对象转换为字符串
        message = json.dumps(data).encode('utf-8')
        # 发送消息到Kafka主题
        # 发送消息到Kafka主题
        try:
            producer.send(topic, key=eqp_blk.encode('utf-8'), value=message, partition=partition)
            # producer.send(topic, key=eqp_blk.encode('utf-8'), value=message)
            # producer.flush()  # 刷新缓冲区，确保消息被发送
            print('消息已成功发送到Kafka主题')
        except KafkaError as e:
            print('发送消息到Kafka主题时发生错误:', e)
        # 关闭KafkaProducer实例
        producer.close()


if __name__ == "__main__":
    result_to_kafka(c='NG', m='EL_18.3_13.10.2023-12-52-13_111111111_8_3.png', wafer_id='1111111111', ai_result=1, result_name='EL划伤', eqp_blk='DCT02A', topic='halm-ai-a')
    # key = 'CT1601A'.encode('utf-8')
    # print(key)
