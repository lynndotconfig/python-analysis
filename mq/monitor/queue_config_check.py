"""RabbitMQ Queue config check."""
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
    auto_delete = json.loads(sys.argv[6].lower())
    durable = json.loads(sys.argv[7].lower())

    conn = httplib.HTTPConnection(server, port)
    path = '/api/queues/%s/%s' % (
        urllib.quote(vhost, safe=""),
        urllib.quote(queue_name))
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
    if response.status == 404:
        print "CRITICAL: Queue %s does not exist." % queue_name
        exit(EXIT_CRITICAL)
    elif response.status > 299:
        print "UNKNOWN: Unexpected API Error: %s" % response.read()
        sys.exit(EXIT_UNKNOWN)

    response = json.loads(response.read())

    if response["auto_delete"] != auto_delete:
        print "WARN: Queue '%s' - auto_delete flag is NOT %s." %(
            queue_name, auto_delete
        )
        exit(EXIT_WARNING)
    if response["durable"] != durable:
        print "WARN: Queue '%s' - durable flag is NOT %s." %(
            queue_name, durable
        )
        exit(EXIT_WARNING)

    print "OK: Queue %s configured correctly."  %(queue_name)
    sys.exit(EXIT_OK)

if __name__ == '__main__':
    main()
