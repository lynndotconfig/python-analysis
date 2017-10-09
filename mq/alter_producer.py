import json
import pika
from optparse import OptionParser

def main():
    AMQP_SERVER = "localhost"
    AMQP_USER = "alert_user"
    AMQP_PASS = "alertme"
    AMQP_VHOST = "/"
    AMQP_EXCHANGE = "alerts"

    opt_parser = OptionParser()
    opt_parser.add_option(
        "-r",
        "--routing_key",
        dest="routing_key",
        help="Routing key for message + (e.g myalert.im)"
    )
    opt_parser.add_option(
        "-m",
        "--message",
        dest="message",
        help="Message text for alert."
    )
    args = opt_parser.parse_args()[0]

    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
    conn_params = pika.ConnectionParameters(
        AMQP_SERVER, virtual_host=AMQP_EXCHANGE,
        credentials=creds_broker)
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()

    msg = json.dumps(args.message)
    msg_props = pika.BasicProperties()
    msg_props.content_type = "application/json"
    msg_props.durable = False

    channel.basic_publish(
        body=msg,
        exchange=AMQP_EXCHANGE,
        properties=msg_props,
        routing_key=args.routing_key
    )

    print "Send message %s tagged with routing key '%s' to exchange %s" % (
        json.dumps(args.message), args.routing_key, AMQP_VHOST
    )


if __name__ == "__main__":
    main()