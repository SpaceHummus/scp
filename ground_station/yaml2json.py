import sys
import yaml
import json


if len (sys.argv)<2:
    file_name=input("please enter source YAML file name:")
else:
    file_name=sys.argv[1]

## Create a variable to hold the data to import
os_list = {}
## Read the YAML file
with open(file_name) as infile:
# Marshall the YAML into the variable defined above
    os_list = yaml.load(infile, Loader=yaml.FullLoader)
#Open a file to write the JSON output. The 'w' makes the file writable
with open("test.json", 'w') as outfile:
     # Marshall the JSON, setting "indent" makes the file more readabl
    json.dump(os_list, outfile, indent=4)
    print("JSON file written.")