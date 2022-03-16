import os

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
    cdata_root = etree.fromstring(cdata_text)

    # 更改節點內容
    cdata_root = change_data(root=cdata_root, prefix=tag_prefix)

    # 儲存檔案
    save_data(tree, root, cdata_root, find)


def change_data(root, prefix):
    elements = root.xpath("//*")
    for item in elements:
        if 'numDlSlot' == item.tag.replace(prefix, ''):
            item.text = str(20)
    return root


def save_data(tree, root, target_root, find):
    find(tree)[0].text = etree.tostring(target_root)
    et = etree.ElementTree(root)
    et.write('output.xml', pretty_print=True)

    with open('output.xml', 'r') as f:
        lines = f.readlines()

    new_lines = []
    for i, line in enumerate(lines):
        line = line.replace('&lt;', '<').replace('&gt;', '>')
        new_lines.append(line)

    with open('output.xml', 'w') as f:
        f.writelines(new_lines)


if __name__ == '__main__':
    file_name = 'oam_template_du_wnc.xml'
    load_content(file_name)
