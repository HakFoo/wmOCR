import re

name = 'FrostPrime一套'
name = re.findall('$Prime', name)
print(name)