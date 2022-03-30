import os
import re
import xml.etree.ElementTree as ET

# 全局變數
unique_id = 1
input_file_name = "oam_template_du_wnc.xml"
output_file_name = "oam_template_du_wnc.xml"
root = ET.parse(input_file_name).getroot()

# NUMSLOTPARAMS = os.environ.get("NUMSLOTPARAMS")
NUMSLOTPARAMS = "1"

case_name_dict = {
    "1": "DDDSU",
    "2": "DDDSU(WG8)",
    "3": "DDDDDDDSUU",
    "4": "DDDSUDDSUU",
    "5": "DSUUU",
    "6": "DDSUUUUUUU",
    "7": "DDDSUUDDSU",
    "8": "DDDSUUDDDD",
}

case_params_dict = {
    "1": {
        "numDlSlot": "3",
        "numDlSymbol": "12",
        "numUlSlot": "1",
        "numUlSymbol": "0",
        "p2Pres": "0",
        "numDlSlotP2": "3",
        "numDlSymbolP2": "12",
        "numUlSlotP2": "1",
        "numUlSymbolP2": "0",
        "prachCfgIdx": "145",
    },
    "2": {
        "numDlSlot": "3",
        "numDlSymbol": "10",
        "numUlSlot": "1",
        "numUlSymbol": "2",
        "p2Pres": "0",
        "numDlSlotP2": "3",
        "numDlSymbolP2": "12",
        "numUlSlotP2": "1",
        "numUlSymbolP2": "0",
        "prachCfgIdx": "145",
    },
    "3": {
        "numDlSlot": "7",
        "numDlSymbol": "10",
        "numUlSlot": "2",
        "numUlSymbol": "2",
        "p2Pres": "0",
        "numDlSlotP2": "7",
        "numDlSymbolP2": "10",
        "numUlSlotP2": "2",
        "numUlSymbolP2": "2",
        "prachCfgIdx": "145",
    },
    "4": {
        "numDlSlot": "3",
        "numDlSymbol": "12",
        "numUlSlot": "1",
        "numUlSymbol": "0",
        "p2Pres": "1",
        "numDlSlotP2": "2",
        "numDlSymbolP2": "12",
        "numUlSlotP2": "2",
        "numUlSymbolP2": "0",
        "prachCfgIdx": "145",
    },
    "5": {
        "numDlSlot": "1",
        "numDlSymbol": "12",
        "numUlSlot": "3",
        "numUlSymbol": "0",
        "p2Pres": "0",
        "numDlSlotP2": "1",
        "numDlSymbolP2": "12",
        "numUlSlotP2": "3",
        "numUlSymbolP2": "0",
        "prachCfgIdx": "145",
    },
    "6": {
        "numDlSlot": "2",
        "numDlSymbol": "12",
        "numUlSlot": "7",
        "numUlSymbol": "0",
        "p2Pres": "0",
        "numDlSlotP2": "2",
        "numDlSymbolP2": "12",
        "numUlSlotP2": "7",
        "numUlSymbolP2": "0",
        "prachCfgIdx": "145",
    },
    "7": {
        "numDlSlot": "3",
        "numDlSymbol": "12",
        "numUlSlot": "2",
        "numUlSymbol": "0",
        "p2Pres": "1",
        "numDlSlotP2": "2",
        "numDlSymbolP2": "12",
        "numUlSlotP2": "1",
        "numUlSymbolP2": "0",
        "prachCfgIdx": "145",
    },
    "8": {
        "numDlSlot": "3",
        "numDlSymbol": "12",
        "numUlSlot": "2",
        "numUlSymbol": "0",
        "p2Pres": "1",
        "numDlSlotP2": "4",
        "numDlSymbolP2": "12",
        "numUlSlotP2": "0",
        "numUlSymbolP2": "0",
        "prachCfgIdx": "156",
    },
}


# 遍歷所有的節點
def walkData(root_node, level, result_list):
    global unique_id

    if unique_id == 121 and level == 5 and "vsData" in root_node.tag:
        params_dict = case_params_dict.get(NUMSLOTPARAMS)
        print(f"Your slot case is {case_name_dict.get(NUMSLOTPARAMS)}")
        for param_name, value in params_dict.items():

            tempResultList = re.findall(
                f"<{param_name}>\d+</{param_name}>", root_node.text
            )

            for tempResult in tempResultList:
                root_node.text = root_node.text.replace(
                    tempResult, f"<{param_name}>{value}</{param_name}>"
                )

    temp_list = [unique_id, level, root_node.tag, root_node.attrib, root_node.text]
    result_list.append(temp_list)
    unique_id += 1

    # 遍歷每個子節點
    children_node = root_node
    if len(list(children_node)) == 0:
        return
    for child in list(children_node):
        walkData(child, level + 1, result_list)
    return


def getXmlData(file_name):
    level = 1  # 節點的深度從1開始
    result_list = []
    walkData(root, level, result_list)
    tree = ET.ElementTree(root)
    tree.write(file_name)


def replace_text(file_name):
    new_lines = []
    with open(f"{file_name}", "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = (
            lines[i]
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("ns0:", "")
            .replace(":ns0", "")
        )

    for i in range(len(lines)):
        if "</gnbvs></vsData>" in lines[i]:
            new_lines.append(lines[i].replace("</gnbvs></vsData>", "</gnbvs>"))
            new_lines.append(lines[i].replace("</gnbvs></vsData>", "]]></vsData>"))
        elif (
            "</vsData>" in lines[i]
            and lines[i].count("<") == 1
            and lines[i].count(">") == 1
        ):
            lines[i] = lines[i].replace("</vsData>", "]]></vsData>")
            new_lines.append(lines[i])
        elif (
            "<vsData>" in lines[i]
            and lines[i].count("<") == 1
            and lines[i].count(">") == 1
        ):
            lines[i] = lines[i].replace("<vsData>", "<vsData><![CDATA[")
            new_lines.append(lines[i])
        elif '<vsData><gnbvs xmlns="urn:rdns:com:radisys:nr:gnb">' in lines[i]:
            new_lines.append("           <vsData><![CDATA[\n")
            new_lines.append('	        <gnbvs xmlns="urn:rdns:com:radisys:nr:gnb">\n')
        else:
            new_lines.append(lines[i])

    new_lines = ['<?xml version="1.0" encoding="UTF-8"?>\n'] + new_lines

    with open(f"{file_name}", "w") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    if NUMSLOTPARAMS:
        getXmlData(file_name=input_file_name)
        replace_text(file_name=output_file_name)
