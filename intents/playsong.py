import pywhatkit
import feedparser
import config
import utils
import keyboard
from random import choice
from time import sleep

class Playsong:

    def __init__(self, command, response):
        self.os = config.OS_NAME
        self.command = command
        self.response = response
        
    def launch(self):
        song = utils.get_search_value(self.command,'Playsong')
        print(song)
        if 'random' in song or 'bừa' in song:
            song = ''
            while song == '' :
                channel_url = feedparser.parse("https://www.youtube.com/feeds/videos.xml?playlist_id=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj")
                song = choice(channel_url.entries).title
                print(song)
        utils.speak(self.response .format(song = song))
        pywhatkit.playonyt(song)
        # close tab when play 240sec
        #sleep(240)
        #keyboard.press_and_release('ctrl+w')
