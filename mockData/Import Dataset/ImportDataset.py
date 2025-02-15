import json
import sys
from xml.etree.ElementTree import iterparse

attributes=[elem.attrib 
            for _, elem in iterparse(sys.argv[1]) 
            if elem.tag == "Record"]

with open("Output.json","w") as file:
    json.dump(attributes, file, indent=4)