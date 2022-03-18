import os
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
    tree = etree.parse(f'{fileName}')
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


def print_alert(tag, value, file):
    global TAG
    global VALUE
    global FILENAME
    if not tag:
        # print('請輸需要更改的標籤')
        TAG = input('請輸需要更改的標籤: ')
        args.tag = TAG
        return True
    if not value:
        # print('請輸需要更改的數值')
        VALUE = input('請輸需要更改的數值: ')
        args.value = VALUE
        return True
    if not file:
        # print('請輸需變更的檔案')
        FILENAME = input('請輸需變更的檔案: ')
        args.file = FILENAME
        return True
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', default=None, help='請輸入要更改的tag')
    parser.add_argument('--value', default=None, help='請輸入要更改的數值')
    parser.add_argument('--file', default=None, help='輸入要更改之檔案')
    args = parser.parse_args()

    # 檢查輸入參數是否符合規範
    flag = print_alert(args.tag, args.value, args.file)
    while (flag):
        flag = print_alert(args.tag, args.value, args.file)

    # start processin
    main(fileName=args.file,
         tag=args.tag,
         value=args.value)

    # command example
    # python test_lxml_change_content.py --tag numDlSlot --value 20 --file output.xml
    # python test_lxml_change_content.py --tag "numDlSlot numDlSymbol numUlSlot numUlSymbol" --value "20 30 40 50" --file output.xml