import os
from pprint import pprint
from re import L
try:
    from lxml import etree
except ModuleNotFoundError:
    os.system('pip install lxml')


def load_content(fileName):

    tag_prefix = '{urn:rdns:com:radisys:nr:gnb}'
    tree = etree.parse(f'{fileName}')
    root = tree.getroot()

    # 找出需被修改的節點
    find = etree.XPath("/*/*[13]/*[17]/*[7]/*[6]")
    cdata_text = find(tree)[0].text.strip()
    print(cdata_text)
    cdata_root = etree.fromstring(cdata_text)
    cdata_tree = etree.ElementTree(cdata_root)


    elements = cdata_root.xpath("//*")
    for item in elements:
        if 'numDlSlot' == item.tag.replace(tag_prefix, ''):
            item.text = str(20)
    # print(etree.tostring(cdata_root))
    find(tree)[0].text = etree.tostring(cdata_root)
    et = etree.ElementTree(root)
    et.write('output.xml', pretty_print=True, encoding='unidoe')

    # with open('output.xml', 'r') as f:
    #     lines = f.readlines()
    
    # new_lines = []
    # for i, line in enumerate(lines):
    #     line = line.replace('&lt;', '<').replace('&gt;', '>')
    #     new_lines.append(line)
    
    # with open('output.xml', 'w') as f:
    #     f.writelines(new_lines)



def change_data():
    pass


def save_data():
    pass


if __name__ == '__main__':
    file_name = 'oam_template_du_wnc.xml'
    load_content(file_name)
