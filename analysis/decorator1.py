def should_say(fn):

    def say(*args):
        print "say somethong..."
        fn(*args)
    return say


def func():
	print "in func"

func=should_say(func)
func()