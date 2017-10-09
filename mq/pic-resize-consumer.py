import json, smtplib
import pika

def main():
    AMQP_SERVER = "localhost"
    AMQP_USER = "alert_user"
    AMQP_PASS = "alertme"
    AMQP_VHOST = "/"
    AMQP_EXCHANGE = "upload-pictures"

    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
    conn_params = pika.ConnectionParameters(
        AMQP_SERVER, virtual_host=AMQP_EXCHANGE,
        credentials=creds_broker)
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()

    channel.exchange_declare(
        exchange=AMQP_EXCHANGE,
        type="topic",
        auto_delete=False,
        durable=True)

    channel.queue_declare(queue="resize-pictures", auto_delete=False)

    channel.queue_bind(
        queue="resize-pictures",
        exchange=AMQP_EXCHANGE)

    channel.basic_consume(
        add_points_to_user,
        queue="resize-pictures",
        no_ack=False,
        consumer_tag="resize-pictures"
    )


def add_points_to_user(channel, method, header, body):
    """Add points to user."""
    if body == 'quit':
        channel.basic_cancel(consumer_tag="resize-pictures")
        channel.stop_consuming()
    else:
        msg = json.loads(body)
        print "Resize pictures to user: %s\n" % msg.user_id
        channel.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__":
    main()
