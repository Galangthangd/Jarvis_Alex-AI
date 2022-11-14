import datetime
import utils
import config
import requests
import json
from translate import Translator
from random import randint

class Readnews:

    def __init__(self, command, response):
        self.os = config.OS_NAME
        self.command = command
        self.response = response
        self.language = 'en-EN'
        if config.OS_NAME == 'Alex' :
            self.language = 'vi-VI'
            

    def launch(self):
        queue = utils.get_search_value(self.command,'Readnews')
        params = {
            'apiKey': '30d02d187f7140faacf9ccd27a1441ad',
            "from_param": datetime.date.today(),
            "language":'en',
            "q":queue,
        }
        api_result = requests.get('http://newsapi.org/v2/top-headlines?', params)
        news = json.loads(api_result.text)
        translator= Translator(to_lang=self.language)
        totalResults = news['totalResults']
        count_total = 20 if totalResults > 20 else totalResults
        random_news_int = randint(0,count_total)
        if totalResults > 0:
            for number,new in enumerate(news['articles'],start=1):
                if number == random_news_int:
                    title = translator.translate(new['title'])
                    description = translator.translate(new['description'])
                    print('speak now')
                    utils.speak(self.response .format(title = title,description = description))
                    break