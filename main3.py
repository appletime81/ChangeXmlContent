import os
import xml.etree.ElementTree as ET
import argparse
from pprint import pprint

TAG = ''
VALUE = ''
FILENAME = ''

try:
    from lxml import etree
except ModuleNotFoundError:
    os.system('pip install lxml')
tag_prefix = '{urn:rdns:com:radisys:nr:gnb}'


def main(fileName, tag, value):
    tree = ET.parse(f'{fileName}')
    root = tree.getroot()

    # 找出需被修改的節點
    find = etree.XPath("/*/*[13]/*[17]/*[7]/*[6]")
    cdata_text = find(tree)[0].text.strip()
    cdata_root = etree.fromstring(cdata_text)

    # 修改節點內容
    root = change_data(original_root=root,
                       original_tree=tree,
                       target_root=cdata_root,
                       find=find,
                       tag=tag,
                       value=value)

    # 儲存檔案
    save_data(original_root=root, file_name=fileName)


def change_data(original_root, original_tree, target_root, find, tag, value):
    elements = target_root.xpath("//*")
    values = value.split(' ')
    tags = tag.split(' ')
    for tag, value in zip(tags, values):
        for item in elements:
            if f'{tag}' == item.tag.replace(tag_prefix, ''):
                item.text = value
    find(original_tree)[0].text = etree.tostring(target_root)
    return original_root


def save_data(original_root, file_name):
    new_lines = list()
    et = etree.ElementTree(original_root)
    et.write(f'{file_name}', pretty_print=True, encoding='utf-8')

    with open(f'{file_name}', 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].replace('&lt;', '<').replace('&gt;', '>')

    for i in range(len(lines)):
        if '</gnbvs></vsData>' in lines[i]:
            new_lines.append(lines[i].replace('</gnbvs></vsData>', '</gnbvs>'))
            new_lines.append(lines[i].replace('</gnbvs></vsData>', ']]></vsData>'))
        elif '</vsData>' in lines[i] and lines[i].count('<') == 1 and lines[i].count('>') == 1:
            lines[i] = lines[i].replace('</vsData>', ']]></vsData>')
            new_lines.append(lines[i])
        elif '<vsData>' in lines[i] and lines[i].count('<') == 1 and lines[i].count('>') == 1:
            lines[i] = lines[i].replace('<vsData>', '<vsData><![CDATA[')
            new_lines.append(lines[i])
        elif '<vsData><gnbvs xmlns="urn:rdns:com:radisys:nr:gnb">' in lines[i]:
            new_lines.append('           <vsData><![CDATA[\n')
            new_lines.append('	        <gnbvs xmlns="urn:rdns:com:radisys:nr:gnb">\n')
        else:
            new_lines.append(lines[i])

    new_lines = ['<?xml version="1.0" encoding="UTF-8"?>\n'] + new_lines

    with open(f'{file_name}', 'w') as f:
        f.writelines(new_lines)


if __name__ == '__main__':
    # start processin
    main(fileName=args.file,
         tag=args.tag,
         value=args.value)