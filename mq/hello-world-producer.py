# -*- coding: UTF-8 -*-
import pika, sys

# use default guest username and password
# 身份验证信息
credentials = pika.PlainCredentials("guest", "guest")

# use default vhost(/) and default port(5672)
# 使用默认的vhost “/” , 默认端口 5672
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

# 连接RabbitMQ Server
conn_broker = pika.BlockingConnection(conn_params)  # connect to the server
# 获取 channel
channel = conn_broker.channel()  # get channel

# passive(False): if exist, normally return, else, created and return ;
# passive(True): if exist, normally return; else, return err
# 声明名称为“hello-exchange”，类型为“direct”的交换器exchange
channel.exchange_declare(
    exchange="hello-exchange",
    exchange_type="direct",
    passive=False,
    durable=True,
    auto_delete=False)  # declare exchange

# 提取命令行中的消息参数
msg = sys.argv[1]
msg_props = pika.BasicProperties()
# 消息的内容格式为“text/plain”
msg_props.content_type = "text/plain"  # create plain text mssage

# 发布消息到“hello-exchange”的交换器，消息路由键为“hola”
channel.basic_publish(
    body=msg,
    exchange="hello-exchange",
    properties=msg_props,
    routing_key="hola"  # publish msg
)