# Another simple XML analyser in just 50 strings of code
# by Denis Khvorostin (denis.khvorostin@gmail.com), 2015

# Returns XML scheme as Python dictionary

import xml.etree.ElementTree as etree
import pprint


# IN: node + data, OUT: data
def walker(node, data):
    nt = node.tag

    # Check if is text in current tag
    if node.text and data[nt].get('_TEXT', False) == False:
        data[nt].update({'_TEXT': True})

    # Check for attributes of current tag
    for attr in node.attrib:

        # If where isn't list of node attributes here, make one
        if data[nt].get('_ATTRIBUTES', False) == False:
            data[nt].update({'_ATTRIBUTES': []})

        if data[nt]['_ATTRIBUTES'].count(attr) == 0:
            data[nt]['_ATTRIBUTES'].append(attr)

    # Check for children tags
    for ch in node:

        ct = ch.tag

        # If where isn't dict of children nodes here, make one
        if data[nt].get(ct, False) == False:
            data[nt].update({ct: {}})

        # recursion...
        data[nt].update(walker(ch, {ct: data[nt][ct]}))

    return data


# Let's analyse some XML
tree = etree.parse('oam_template_du_wnc.xml')
root = tree.getroot()
r = walker(root, {root.tag: {}})

# Make results readable. You can use print() instead
pprint.pprint(r, compact=True)