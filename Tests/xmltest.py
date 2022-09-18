
import xml.etree.ElementTree as ET
import os
#tree = ET.parse('xmlfile.txt')
print(os.getcwd())
tree = ET.parse(os.path.join(os.getcwd(),"temp","Content","score.gpif"))
root = tree.getroot()
print(root.tag, root.attrib)

for child in root:
  print(child.tag, ":", child.attrib)