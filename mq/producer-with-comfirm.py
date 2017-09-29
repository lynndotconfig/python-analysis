import pika, sys
from pika import spec

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
    type="direct",
    passive=False,
    durable=True,
    auto_delete=False)  # declare exchange

msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"  # create plain text mssage
msg_ids = []

# confirm handler
def confirm_handler(frame):
    if type(frame.method) == spec.Confirm.SelectOk:
        print "Channel in 'confirm' mode."
    elif type(frame.method) == spec.Basic.Nack:
        if frame.method.delivery_tag in msg_ids:
            print "Message lost!"
    elif type(frame.method) == spec.Basic.Ack:
        if frame.method.delivery_tag in msg_ids:
            print "Confirm received!"
            msg_ids.remove(frame.method.delivery_tag)

channel.confirm_delivery(callback=confirm_handler)

channel.basic_publish(
    body=msg,
    exchange="hello-exchange",
    properties=msg_props,
    routing_key="hola"  # publish msg
)

msg_ids.append(len(msg_ids) + 1)
channel.close()