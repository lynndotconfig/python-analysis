"""RabbitMQ Connection Check."""
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

    creds_broker = pika.PlainCredentials(username, password)
    conn_param = pika.ConnectionParameters(
        server,
        virtual_host=vhost,
        credentials=creds_broker
    )

    try:
        conn_broker = pika.BlockingConnection(conn_param)
        conn_broker.channel()
    except Exception:
        print "CRITICAL: Could not connect to %s:%s" %(server, port)
        sys.exit(EXIT_CRITICAL)

    print "OK: Connect to %s:%s sucessfully" %(server, port)
    sys.exit(EXIT_OK)

if __name__ == '__main__':
    main()
