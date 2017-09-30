import pika, sys

# use default guest username and password
credentials = pika.PlainCredentials("guest", "guest")

# use defautl vhost(/) and default port(5672)
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to the server
channel = conn_broker.channel()  # get channel

# passive(False): if exist, normally return, else, created and return ;
# passive(True): if exist, normally return; else, return err
channel.exchange_declare(
    exchange="hello-exchange",
    exchange_type="direct",
    passive=False,
    durable=True,
    auto_delete=False)  # declare exchange

msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"  # create plain text mssage

channel.basic_publish(
    body=msg,
    exchange="hello-exchange",
    properties=msg_props,
    routing_key="hola"  # publish msg
)