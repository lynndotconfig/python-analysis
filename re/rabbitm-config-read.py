import re
from ast import literal_eval
from collections import OrderedDict

from erl_terms import decode

path = './rabbitmq.config.simple'
out_path = './result.txt'
# path = './result.txt'
# out_path = './result3.txt'


BINARY_KEY = (
    'default_vhost',
    'default_user',
    'default_pass',
    'default_permissions',
    'loopback_users',
    'queue_master_locator',
)

STRING_KEY = (
    'cacertfile',
    'certfile',
    'keyfile',
    'http_log_dir',
    'ip',
)

BOOL_KEY = (
    'reverse_dns_lookups',
    'fail_if_no_peer_cert',
    'exit_on_close',
    'nodelay',
    'hipe_compile',
    'ssl',
)

SPACE = '  '  # two space

class ConfDict(OrderedDict):
    def __init__(self):
        super(ConfDict, self).__init__()
        self.last = None

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        if key not in self:
            self.last = key
        super(ConfDict, self).__setitem__(key, value, dict_setitem=dict_setitem)

def is_dict(value):
    return isinstance(value, dict)

def is_tuple(value):
    return isinstance(value, tuple)

def is_list(value):
    return isinstance(value, list)

def is_str(value):
    return isinstance(value, str)

def is_int(value):
    return isinstance(value, int)

def is_float(value):
    return isinstance(value, float)

def is_number(value):
    return isinstance(value, (int, long, float))

def is_binary_key(key):
    if key in BINARY_KEY:
        return True
    return False

def is_string_key(key):
    if key in STRING_KEY:
        return True
    return False

def is_bool_key(key):
    if key in BOOL_KEY:
        return True
    return False

def generate_value(origin, key):
    if is_binary_key(key):
        return '<<"' + origin + '">>'
    if is_string_key(key):
        return '"' + origin + '"'
    if is_bool_key(key):
        return 'true' if origin else 'false'
    return origin

def read(path):
    with open(path, 'r') as fp:
        content = fp.read()
        result = decode(content)
        return result[0]

def update(res):
    # key_addr = 'rabbit.tcp_listen_options.nodelay'
    key_addr = 'rabbit.disk_free_limit'
    value = 12345
    # import pdb; pdb.set_trace()
    # res['rabbit']['tcp_listen_options']['nodelay'] = False
    keys = key_addr.split('.')
    length = len(keys)
    if length <= 1:
        raise Exception('Bad key: %s' % (key_addr))
    target = res
    for key in keys[:-1]:
        try:
            target = target[key]
        except KeyError:
            raise Exception('Bad key: %s' % (key_addr))
    # import pdb; pdb.set_trace()
    try:
        target[keys[-1]] = value
    except KeyError:
        raise Exception('Bad key: %s' % (key_addr))
    return res


def parse(content):
    conf = ConfDict()
    values = []
    ## for value is []
    if len(content) == 0:
        return content
    # for value is ['a', 'b']
    if not is_tuple(content[0]):
        return content
    for item in content:
        if not is_tuple(item):
            raise Exception('config item must be tuple.')
        if not len(item) == 2:
            raise Exception('length for config item should be two.')
        if is_list(item[1]):
            conf[item[0]] = parse(item[1])
        else:
            conf[item[0]] = item[1]
    return conf

def convert_list(lis, key=None):
    start = ['[']
    end = [']']
    copy = []
    length = len(lis)
    for i in range(length):
        copy.append(
            generate_value(lis[i], key))
        if i < length - 1:
            copy.append(',')
    return start + copy + end

def printf(res, level=1):
    # import pdb; pdb.set_trace()
    conf = []
    if len(res) > 0:
        conf.append('[\n')
    for k in res:
        v = res[k]
        conf.append(SPACE * level)
        conf.append('{')
        conf.append(k)
        conf.append(', ')
        if is_str(v) or is_number(v):
            conf.append(
                generate_value(v, k))
            conf.append('}')
            if k == res.last:
                conf.append('\n')
            else:
                conf.append(',\n')
            continue
        if is_dict(v) and len(v) > 0:
            item_str = printf(v, level+1)
            conf.extend(item_str)
        if is_list(v):
            item_str = convert_list(v, k)
            conf.extend(item_str)
        conf.append('}')
        if k == res.last:
            conf.append('\n')
        else:
            conf.append(',\n')
    conf.append(SPACE * level)
    conf.append(']')
    if level == 1:
        conf.append('.')
    return conf

test_path = "./test-str.text"

def test():
    con = read(test_path)
    print "before parse:"
    print con
    print "-" * 20
    print "after parse: "
    res = parse(con)
    print res
    # res = update(res)
    # print "-" * 20
    # print "print format: "
    # string = printf(res)
    # with open(out_path, 'w') as fp:
    #     for s in string:
    #         fp.write(str(s))
    # print string
    # for s in string:
    #   print s
    # print "".join(string)


# test()


input_string = """
[{webmachine, [ 
 {bind_address, "12.34.56.78"}, 
 {port, 12345}, {tcp, 345},
 {document_root, "foo/bar"} 
]}]
"""
input_string2 = """
[{nodes,[{disc,['rabbit@192-168-48-129']},{ram,[rabbit@ubuntu]}]},
 {running_nodes,['rabbit@192-168-48-129',rabbit@ubuntu]},
 {cluster_name,<<"rabbit@192-168-48-129">>},
 {partitions,[]},
 {alarms,[{'rabbit@192-168-48-129',[]},{rabbit@ubuntu,[]}]}]
 """

print 'before: ', input_string2
# make string somewhat more compatible with Python syntax:
compat = re.sub('([a-zA-Z].*?),', r'"\1":', input_string2)

print compat
# # evaluate as literal, see what we get
# res = literal_eval(compat)

# # [{'webmachine': [{'bind_address': '12.34.56.78'}, {'port': 12345},
# # {'document_root': 'foo/bar'}]}]

# print res