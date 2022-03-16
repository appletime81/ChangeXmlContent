import re

t1 = 't'
a = '                 @@@t4564564t@@@'

res = ''.join([item for item in a if item != ' '])
print(res)
