import pika, sys
from pika import spec

# use default guest username and password
credentials = pika.PlainCredentials("guest", "guest")

# use defautl vhost(/) and default port(5672)
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to the server
channel = conn_broker.channel()  # get channel

channel.confirm_delivery()

msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"  # create plain text mssage

if channel.basic_publish(
    body=msg,
    exchange="hello-exchange",
    properties=msg_props,
    routing_key="hola"):  # publish msg
    print "Confirm received!"
else:
    print "Message lost!"

channel.close()
