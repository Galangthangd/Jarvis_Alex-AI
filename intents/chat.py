import utils
import config
import json

class Chat:

    def __init__(self, command, response):
        self.os = config.OS_NAME
        self.command = command
        self.response = response
        self.language = 'en-EN'
        self.error = 'sorry, i can not understand'
        if config.OS_NAME == 'Alex' :
            self.language = 'vi-VI'
            self.error = 'xin lỗi, mình không hiểu bạn'
            

    def launch(self):
        f = open('datachat'+self.os+'.json', encoding='utf-8')
        data = json.load(f)
        while True: 
            #questions= utils.read_voice_cmd()
            questions = input('user : ')
            storeAnswers = []
            break_word = ['break','dừng','stop','ngưng']
            if questions in break_word or questions == '': 
                break
            else : 
                for each in data:
                    if questions in each['questions']:
                        storeAnswers.append(each['answers'])
                if(storeAnswers):
                    print(str(storeAnswers))
                    Answers = utils.choose_random(storeAnswers)
                    print(self.os+' : '+Answers)
                    utils.speak(Answers)
                else:
                    print(self.os+' : '+self.error)
                    utils.speak(self.error)
                continue