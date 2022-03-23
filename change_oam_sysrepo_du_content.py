import os
import re
import xml.etree.ElementTree as ET

# 全局變數
unique_id = 1
input_file_name = 'oam_template_du_wnc.xml'
output_file_name = 'oam_template_du_wnc.xml'
root = ET.parse(input_file_name).getroot()

# get environment variables
NUMDLSLOT = os.environ.get('NUMDLSLOT')
NUMDLSYMBOL = os.environ.get('NUMDLSYMBOL')
NUMULSLOT = os.environ.get('NUMULSLOT')
NUMULSYMBOL = os.environ.get('NUMULSYMBOL')



# 遍歷所有的節點
def walkData(root_node, level, result_list):
    global unique_id

    if unique_id == 121 and level == 5 and 'vsData' in root_node.tag:
        numDlSlotPart = root_node.text[re.search(f'<numDlSlot>\d+</numDlSlot>', root_node.text).start(): \
                                       re.search(f'<numDlSlot>\d+</numDlSlot>', root_node.text).end()]
        numDlSymbolPart = root_node.text[re.search(f'<numDlSymbol>\d+</numDlSymbol>', root_node.text).start(): \
                                         re.search(f'<numDlSymbol>\d+</numDlSymbol>', root_node.text).end()]
        numUlSlotPart = root_node.text[re.search(f'<numUlSlot>\d+</numUlSlot>', root_node.text).start(): \
                                       re.search(f'<numUlSlot>\d+</numUlSlot>', root_node.text).end()]
        numUlSymbolPart = root_node.text[re.search(f'<numUlSymbol>\d+</numUlSymbol>', root_node.text).start(): \
                                         re.search(f'<numUlSymbol>\d+</numUlSymbol>', root_node.text).end()]

        root_node.text = root_node.text.replace(numDlSlotPart, f'<numDlSlot>{NUMDLSLOT}</numDlSlot>')
        root_node.text = root_node.text.replace(numDlSymbolPart, f'<numDlSymbol>{NUMDLSYMBOL}</numDlSymbol>')
        root_node.text = root_node.text.replace(numUlSlotPart, f'<numUlSlot>{NUMULSLOT}</numUlSlot>')
        root_node.text = root_node.text.replace(numUlSymbolPart, f'<numUlSymbol>{NUMULSYMBOL}</numUlSymbol>')

    temp_list = [unique_id, level, root_node.tag, root_node.attrib, root_node.text]
    print(unique_id, level, root_node.tag, root_node.attrib, root_node.text)
    result_list.append(temp_list)
    unique_id += 1

    # 遍歷每個子節點
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        walkData(child, level + 1, result_list)
    return


def getXmlData(file_name):
    level = 1  # 節點的深度從1開始
    result_list = []
    walkData(root, level, result_list)
    tree = ET.ElementTree(root)
    tree.write(file_name)
    return result_list


def replace_text(file_name):
    new_lines = []
    with open(f'{file_name}', 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].replace('&lt;', '<').replace('&gt;', '>').replace('ns0:', '').replace(':ns0', '')

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
    R = getXmlData(file_name=input_file_name)
    replace_text(file_name=output_file_name)
