import requests
import time

queue_name = "notifications.info"
rabbit_user = "guest"
rabbit_pass = "guest"

def purge_queue():
    try:
        res = request.delete("http://localhost:15672/api/queues/%2F" + queue_name + "/contents",
            auth=(rabbit_user, rabbit_pass))
    except Exception as e:
        print e
        return False
    return True


if __name__ == "__main__":
    while True:
        if purge_queue():
            print "Time: %s =====> Purge successfully." % time.ctime()
        else:
            print "Time: %s =====> Failed to Purge." % time.ctime()
        time.sleep(5)
