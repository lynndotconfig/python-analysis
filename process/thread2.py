import thread 

import time

input = None

lock = thread.allocate_lock()


def threadProc():
    print "sub thread id: ", thread.get_ident()
    print "sub thread %d wait lock..." % thread.get_ident()
    lock.acquire()
    print "sub thread %d get lock." % thread.get_ident()
    print "sub thread %d receive input: %s" % (thread.get_ident(), input)
    print "sub thread %d release lock" % thread.get_ident()
    lock.release()
    time.sleep(1)


thread.start_new_thread(threadProc, ())
print "Main thread id: ", thread.get_ident()
while True:
    print "Main thread %d wait lock..." % thread.get_ident()
    lock.acquire()
    print "Main thread %d get lock." % thread.get_ident()
    input = raw_input()
    print "Main thread %d release lock" % thread.get_ident()
    lock.release()
    time.sleep(1)
