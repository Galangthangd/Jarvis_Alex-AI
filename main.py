import speech_recognition as sr
import config
import intents
import model
import utils
import sys

from intents.alarm import Alarm
from intents.translation import Translation
from intents.playsong import Playsong
from intents.chat import Chat
from intents.changeos import Changeos
from intents.time import Time
from intents.definition import Definition
from intents.readnews import Readnews
from intents.weather import Weather
from model.model_training import TrainingModel


def read_voice_cmd(recognizer):
    voice_input = ''
    language = 'en-EN'
    if config.OS_NAME == 'Alex' :
        language = 'vi-VI'
    try:
        with sr.Microphone() as source:
            print('Listening...')
            audio = recognizer.listen(source=source, timeout=5, phrase_time_limit=5)
        voice_input = recognizer.recognize_google(audio,key="GOOGLE_SPEECH_RECOGNITION_API_KEY",language = language)
        print('Input : {}'.format(voice_input))
    except sr.UnknownValueError: pass
    except sr.RequestError: print('Network error.')
    except sr.WaitTimeoutError: pass
    except TimeoutError: pass
    return voice_input.lower()


if __name__ == '__main__':
    training_model = TrainingModel(model.words, model.classes, model.data_x, model.data_y)
    trained_model = training_model.train()
    recognizer = sr.Recognizer()
    #bootup = TrainingModel.get_data_type('Bootup', config.DATA, 'response')
    #utils.speak(bootup .format(username = 'Sir'))
    while True:
        #command = read_voice_cmd(recognizer)
        command = input('cmd : ')
        if command:
            intent = training_model.get_intent(trained_model, command)
            print(intent)
            response = TrainingModel.get_data_type(intent, config.DATA, 'response')
            if intent == 'Greeting' or intent == 'Introduce' or intent == 'Capacities':
                utils.speak(response)
            elif intent:
                try: 
                    makeClass = getattr(sys.modules[__name__], intent)(command, response)
                    launch = getattr(makeClass, 'launch')
                    launch()
                except Exception as exception:
                    utils.speak(TrainingModel.get_data_type('Error', config.DATA, 'response'))
