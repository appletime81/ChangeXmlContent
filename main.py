import re
import argparse
import html
from tokenize import String
from typing import Dict, List
from lxml import etree

def hdl_argument(argument: String):
    argument = argument.strip()
    argument_split_list = argument.split(' ')
    argument_dict = dict()
    for i, item in enumerate(argument_split_list):
        if i % 2 == 0:
            argument_dict[item] = None
        if i % 2 == 1:
            argument_dict[argument_split_list[i - 1]] = item
    return argument_dict

def replace_garbled(content: List):
    pass


def change_content(fileName, **kwargs: Dict):
    new_lines = []
    with open(f'{fileName}', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for key, value in kwargs.items():
        for i, line in enumerate(lines):
            if re.search(f'<{key}>', lines[i]):
                temp_text = ''.join([item for item in line if item != ' '])
                lines[i] = lines[i].replace(f'{temp_text}', f'<{key}>{value}</{key}>')
            new_lines.append(lines[i])

    str_xml = ''
    for i, line in enumerate(lines):
        str_xml += line
    et = etree.fromstring(str_xml.encode('utf-8'))
    et = et.getroottree()
    et.write('output.xml', pretty_print=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', default=None,
                        help='輸入要更改的標籤及數值，若需更改多個標籤請以空格分開，並以""刮起來 --> 例: "tag_name1 20 tag_name2 30..."')
    parser.add_argument('--file', default=None, help='輸入檔名 --> 例: xxx.xml')
    args = parser.parse_args()
    file_name = args.file
    argument_dict = hdl_argument(args.tag)
    change_content(fileName=file_name, **argument_dict)

    # python main.py --tag "numDlSlot 20" --file output.xml
