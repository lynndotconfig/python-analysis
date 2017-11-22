from jinja2 import Template

path = './config.template'
out_path = './result.txt'

fp = open(path, 'r')
config_content = fp.read()
fp.close()

template = Template(config_content)
print template.render(flavor={'ram': 1024})


