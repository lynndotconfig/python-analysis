"""RabbitMQ Cluster Health Check."""
import base64
import httplib
import json
import socket
import sys

EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3

def main():
    """CHECK CONNECTION."""
    server, port = sys.argv[1].split[":"]
    username = sys.argv[2]
    password = sys.argv[3]
    node_list = sys.argv[4]
    mem_critical = int(sys.argv[5])
    mem_warning = int(sys.argv[6])

    conn = httplib.HTTPConnection(server, port)
    path = '/api/nodes'
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

    response = json.loads(response.read())

    for node in response:
        if node["name"] in node_list and node["running"] != False:
            node_list.remove(node["name"])

    missing_len = len(node_list)
    if missing_len:
        print "WARNING: Cluster missing nodes: %s" % str(node_list)
        exit(EXIT_WARNING)

    for node in response:
        if node["mem_used"] > mem_critical:
            print "CRITICAL: Node %s memory usage is %d" % (
                node["name"], node["mem_used"]
            )
            exit(EXIT_CRITICAL)
        if node["mem_used"] > mem_warning:
            print "WARNNING: Node %s memory usage is %d" %(
                node["name"], node["mem_used"]
            )
            exit(EXIT_WARNING)

    print "OK: %d nodes. All memory usage below %d." %(
        len(response), mem_warning)
    sys.exit(EXIT_OK)

if __name__ == '__main__':
    main()
