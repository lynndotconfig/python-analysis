import dis
import sys


def print_env_cmd(name):
    s = open(name).read()
    co = compile(s, name, 'exec')
    print dis.dis(co)


if __name__ == '__main__':
    print_env_cmd(sys.argv[1])
