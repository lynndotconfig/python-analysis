import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

error_queue = channel.queue_declare()  # declare queue
warning_queue = channel.queue_declare()
info_queue = channel.queue_declare()

exchange = "amq.rabbitmq.log"

channel.queue_bind(
    queue=error_queue.method.queue,
    exchange=exchange,
    routing_key="error"
)
channel.queue_bind(
    queue=warning_queue.method.queue,
    exchange=exchange,
    routing_key="warning"
)
channel.queue_bind(
    queue=info_queue.method.queue,
    exchange=exchange,
    routing_key="info"
)

def log(name):
    def log_decorator(fn):
        def wrapper(*args, **kw):
            print "%s: " %(name),
            return fn(*args, **kw)
        return wrapper
    return log_decorator

def callback(channel, method_frame, header_frame, body):
    print body
    import pdb; pdb.set_trace()
    # print "%s" %(msg.body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


channel.basic_consume(  # subscribe consumer
    log('Error')(callback),
    queue=error_queue.method.queue,
)
channel.basic_consume(  # subscribe consumer
    log('Warning')(callback),
    queue=warning_queue.method.queue,
)
channel.basic_consume(  # subscribe consumer
    log('Info')(callback),
    queue=info_queue.method.queue,
)

channel.start_consuming()
