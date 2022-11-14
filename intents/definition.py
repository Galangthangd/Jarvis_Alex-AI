import utils
import config
import wikipedia

class Definition:

    def __init__(self, command, response):
        self.os = config.OS_NAME
        self.command = command
        self.response = response

    def launch(self):
        things = utils.get_search_value(self.command,'Definition')
        info = wikipedia.summary(things,1)
        utils.speak(info .format(things = things))