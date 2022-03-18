import re
# def replace_text(file_name):
#     new_lines = []
#     with open(f'{file_name}', 'r') as f:
#         lines = f.readlines()
#
#     for i in range(len(lines)):
#         lines[i] = lines[i].replace('&lt;', '<').replace('&gt;', '>').replace('ns0:', '').replace(':ns0', '')
#
#     for i in range(len(lines)):
#         if '</gnbvs></vsData>' in lines[i]:
#             new_lines.append(lines[i].replace('</gnbvs></vsData>', '</gnbvs>'))
#             new_lines.append(lines[i].replace('</gnbvs></vsData>', ']]></vsData>'))
#         elif '</vsData>' in lines[i] and lines[i].count('<') == 1 and lines[i].count('>') == 1:
#             lines[i] = lines[i].replace('</vsData>', ']]></vsData>')
#             new_lines.append(lines[i])
#         elif '<vsData>' in lines[i] and lines[i].count('<') == 1 and lines[i].count('>') == 1:
#             lines[i] = lines[i].replace('<vsData>', '<vsData><![CDATA[')
#             new_lines.append(lines[i])
#         elif '<vsData><gnbvs xmlns="urn:rdns:com:radisys:nr:gnb">' in lines[i]:
#             new_lines.append('           <vsData><![CDATA[\n')
#             new_lines.append('	        <gnbvs xmlns="urn:rdns:com:radisys:nr:gnb">\n')
#         else:
#             new_lines.append(lines[i])
#
#     new_lines = ['<?xml version="1.0" encoding="UTF-8"?>\n'] + new_lines
#
#     with open(f'{file_name}', 'w') as f:
#         f.writelines(new_lines)
#
#
# replace_text('filename.xml')

a = '      <aaa>123</aaa>       \t'
print(re.search(r'<aaa>\d+</aaa>', a).start())
print(re.search(r'<aaa>\d+</aaa>', a).end())
print(a[6:20])
b=  a[6:20]
print(b)

