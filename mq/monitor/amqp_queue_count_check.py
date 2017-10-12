"""RabbitMQ Queue Count Check."""
import sys

import pika

EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKOWN = 3

def main():
    """CHECK CONNECTION."""
    server, port = sys.argv[1].split[":"]
    vhost = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    queue_name = sys.argv[5]
    max_critical = int(sys.argv[6])
    max_warn = int(sys.argv[7])

    creds_broker = pika.PlainCredentials(username, password)
    conn_param = pika.ConnectionParameters(
        server,
        virtual_host=vhost,
        credentials=creds_broker
    )

    try:
        conn_broker = pika.BlockingConnection(conn_param)
        channel = conn_broker.channel()
    except Exception:
        print "CRITICAL: Could not connect to %s:%s" %(server, port)
        sys.exit(EXIT_CRITICAL)

    try:
        response = channel.queue_declare(
            queue=queue_name,
            passive=True
        )
    except pika.exceptions.AMQPChannelError:
        print "CRITICAL: Queue %s does not exist." % queue_name
        exit(EXIT_CRITICAL)

    if response.method.message_count >= max_critical:
        print "CRITICAL: Queue %s message count: %d" % (
            queue_name, response.method.message_count
        )
        exit(EXIT_CRITICAL)
    if response.method.message_count >= max_warn:
        print "WARN: Queue %s message count: %d" % (
            queue_name, response.method.message_count
        )
        exit(EXIT_WARNING)

    print "OK: Queue %s message count %d" %(
        queue_name, response.method.message_count
    )
    sys.exit(EXIT_OK)

if __name__ == '__main__':
    main()
