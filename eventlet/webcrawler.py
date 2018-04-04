import eventlet

from eventlet.green import urllib2

urls = [
	"http://www.google.com/intl/en_ALL/images/logo.gif",
	"https://www.python.org/static/img/python-logo.png",
	"http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif"
]

def fetch(url):
	print "opening ", url
	body =  urllib2.urlopen(url).read(),
	print "done with ", url
	return url, body


pool = eventlet.GreenPool()
for url, body in pool.imap(fetch, urls):
	print "got body from ", url, "of length ", len(body)
