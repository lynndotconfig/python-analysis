# -*- coding: UTF-8 -*-
import pika

# 身份验证信息
credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

# 连接到RabbitMQ Server
conn_broker = pika.BlockingConnection(conn_params)  # connect to server
# 获取channel
channel = conn_broker.channel()  # get channel

# declare exchange, if not exist, then create it, else go on;
# 声明交换器“hello-exchange”, 如果服务器上已存在，则忽略；否则，创建交换器。
channel.exchange_declare(
    exchange="hello-exchange",
    exchange_type="direct",
    passive=False,
    durable=True,
    auto_delete=False
)

# 声明队列
channel.queue_declare(queue="hello-queue")  # declare queue
# 绑定队列"hello-queue"到交换器“hello-exchange”， 路由键为“hola”
channel.queue_bind(
    queue="hello-queue",
    exchange="hello-exchange",
    routing_key="hola"
)

# 定义消息处理函数
def msg_consumer(channel, method, header, body):  # function for consumer
    # 从队列收到消息后立即发送，消息确认ACK
    channel.basic_ack(delivery_tag=method.delivery_tag)
    # 当消息内容为“quit”时，退出消费者进程
    if body == 'quit':
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        # 打印收到的消息
        print body
    return

# 订阅消息队列"hello-queue"
channel.basic_consume(  # subscribe consumer
    msg_consumer,
    queue="hello-queue",
    consumer_tag="hello-consumer"
)

# 启动消费者
channel.start_consuming()  # start to comsume
