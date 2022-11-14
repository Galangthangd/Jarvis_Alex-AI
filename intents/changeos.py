import utils
import config
import os

class Changeos:

    def __init__(self, command, response):
        self.os = config.OS_NAME
        self.command = command
        self.response = response

    def launch(self):
        fo = open("assistant_name.txt", "w")
        if self.os == 'Alex':
            fo.write('Jarvis')
        if self.os == 'Jarvis':
            fo.write('Alex')
        fo.close()
        utils.speak(self.response)
        os.system("python main.py")
        exit()