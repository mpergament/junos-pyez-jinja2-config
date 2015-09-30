from pprint import pprint
from jnpr.junos import Device
from bracket_expansion import *
import yaml
import sys
import os
import jinja2
import ipaddress
from glob import glob
from jinja2 import Template

yamlfile = open("junos.yml", "wb")


# Create all interface names
yamlfile.write("---\n")

intconfig = ""
maxports = 72
maxifl = 4
startifl = 100
startipnet = u'198.0.0.0/14'

#Create interface range
#host_ports:
#   et-0/0/[0-71]
yamlfile.write("host_ports:\n")
intconfig += "   et-0/0/[0-" + str(maxports - 1) + "]\n"

# Create all ifls
intconfig += "ports_ifl_start: " + str(startifl) + "\n"
intconfig += "ports_ifl_end: " + str(startifl + maxifl) + "\n"

# Create ifl to IP map
#port_ip_map:
#   et-0/0/0.100: 198.0.0.1/24
#   et-0/0/0.101: 198.0.1.1/24
#   et-0/0/0.102: 198.0.2.1/24
z = 0
ipstart = ipaddress.ip_network(startipnet)

#List of all /24 within /14
subnet24list = list(ipstart.subnets(new_prefix=24))

intconfig += "port_ip_map:\n"
for x in range(0, maxports):
    for y in range(startifl, startifl + maxifl):
        intconfig += "   et-0/0/" + str(x) + "." + str(y) + ": " + \
                   str(list(subnet24list[z].hosts())[0]) + \
                   "/" + str(subnet24list[z].prefixlen) + "\n"
        z += 1

yamlfile.write(intconfig)
yamlfile.close()

# YAML file.
datavars = yaml.load(open("junos.yml").read())

# Jinja2 template file.
#template = Template(open("template.j2").read())
loader = jinja2.FileSystemLoader(os.getcwd())
jenv = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
jenv.filters['bracket_expansion'] = bracket_expansion
template = jenv.get_template("template.j2")

print template.render(datavars)

#dev = Device(host='s3bu-tme-qfx5200-1.englab.juniper.net', user='mpergament' )
#dev.open()

#pprint( dev.facts )

#dev.close()
