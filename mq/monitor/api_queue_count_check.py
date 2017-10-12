"""RabbitMQ API Queue Count Check."""
import base64
import httplib
import json
import urllib
import socket
import sys

EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

def main():
    """CHECK CONNECTION."""
    server, port = sys.argv[1].split[":"]
    vhost = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    queue_name = sys.argv[5]
    max_unack_critical = int(sys.argv[6])
    max_unack_warn = int(sys.argv[7])
    max_ready_critical = int(sys.argv[8])
    max_ready_warn = int(sys.argv[9])

    conn = httplib.HTTPConnection(server, port)
    path = '/api/queues/%s/%s' %(
        urllib.quote(vhost, safe=''),
        queue_name
    )
    method = 'GET'

    credentials = base64.b64encode("%s:%s" %(username, password))

    try:
        conn.request(
            method,
            path,
            "",
            {
                "Content-Type": "application/json",
                "Authorization": "Basic " + credentials
            }
        )
    except socket.error:
        print "UNKOWN: Could not connect to %s:%s" %(server, port)
        sys.exit(EXIT_UNKNOWN)

    response = conn.getresponse()
    if response.status > 299:
        print "UNKNOWN: Unexpected API Error: %s" % response.read()
        sys.exit(EXIT_UNKNOWN)

    resp_payload = json.loads(response.read())
    msg_cnt_unack = resp_payload["messages_unacknowledged"]
    msg_cnt_ready = resp_payload["messages_ready"]
    msg_cnt_total = resp_payload["messages"]
    
    if msg_cnt_unack >= max_unack_critical:
        print "CRITICAL: %s - %d unack messages." %(
            queue_name, msg_cnt_unack
        )
        exit(EXIT_CRITICAL)
    if msg_cnt_unack >= max_unack_warn:
        print "WARN: %s - %s unack messages." %(
            queue_name, msg_cnt_unack
        )
        exit(EXIT_WARNING)

    if msg_cnt_ready >= max_ready_critical:
        print "CRITICAL: %s - %d unconsumed messages." %(
            queue_name, msg_cnt_ready
        )
        exit(EXIT_CRITICAL)
    if msg_cnt_ready >= max_ready_warn:
        print "WARN: %s - %s unconsumed messages." %(
            queue_name, msg_cnt_ready
        )
        exit(EXIT_WARNING)

    print "OK: %s - %d in-flight messages. %dB used memory." %(
        queue_name, msg_cnt_total, resp_payload["memory"]
    )
    sys.exit(EXIT_OK)

if __name__ == '__main__':
    main()
