import json
import os
import platform

fo = open("assistant_name.txt", "r+")
OS_NAME = fo.read(6)
fo.close()
APP_DETAILS_FILE = 'config/applications.json'

with open('config/config'+OS_NAME+'.json', encoding="utf8") as file:
    DATA = json.load(file)

if os.path.exists(APP_DETAILS_FILE) is False:
    with open(APP_DETAILS_FILE, 'w') as file:
        file.write('{}')
