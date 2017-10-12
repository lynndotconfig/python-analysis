"""Usage.
$ python nagios_check.py critical
$ echo $?
"""
import sys

status = sys.argv[1]

level = status.lower()

def log_and_exist(code=0):
    print "Status is %s" % (sys.argv[1])
    sys.exit(code)

if level == 'warning':
    log_and_exist(1)

if level == 'critical':
    log_and_exist(2)

if level == 'unknown':
    log_and_exist(3)

if level == 'ok':
    log_and_exist(0)

    