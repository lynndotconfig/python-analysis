try:
    raise Exception('i am a exception')
except IOError, e:
    print e
finally:
    print 'the finally code'
