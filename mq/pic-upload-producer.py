import json
import pika
from optparse import OptionParser

def main():
    AMQP_SERVER = "localhost"
    AMQP_USER = "alert_user"
    AMQP_PASS = "alertme"
    AMQP_VHOST = "/"
    AMQP_EXCHANGE = "upload-pictures"

    opt_parser = OptionParser()
    opt_parser.add_option(
        "-i",
        "--image_id",
        dest="image_id",
        default="123456",
        help="Image id for pictures (e.g 123456)"
    )
    opt_parser.add_option(
        "-u",
        "--user_id",
        dest="user_id",
        default="6543",
        help="User id for pictures(e.g 6543"
    )
    opt_parser.add_option(
        "-p",
        "--image_path",
        dest="image_path",
        default="/path/to/pic.jpg",
        help="Path for pictures(e.g /path/to/pic.jpg"
    )
    args = opt_parser.parse_args()[0]

    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
    conn_params = pika.ConnectionParameters(
        AMQP_SERVER, virtual_host=AMQP_EXCHANGE,
        credentials=creds_broker)
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()
    channel.exchange_declare(
        exchange=AMQP_EXCHANGE,
        type="fanout",
        auto_delete=False,
        durable=True)

    msg = json.dumps(args.message)
    msg_props = pika.BasicProperties()
    msg_props.content_type = "application/json"
    msg_props.durable = False

    channel.basic_publish(
        body=msg,
        exchange=AMQP_EXCHANGE,
        properties=msg_props,
    )


if __name__ == "__main__":
    main()