def should_say(fn):

    def say(*args):
        print "say somethong..."
        fn(*args)
    return say


@should_say
def func():
    print 'in func'


func()