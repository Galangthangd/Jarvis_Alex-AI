import os
import re

import speech_recognition as sr
from googletrans import Translator, constants
from gtts import gTTS
from playsound import playsound

import utils


class Translation:
    MP3_NAME = 'output.mp3'

    def __init__(self, command, response):
        self.command = command 
        self.response = response

    def get_text_and_target(self):
        text = utils.get_search_value(self.input,'Translation','sentence')
        last_char_index = re.search(r'\bin\b|\bto\b', text)
        if last_char_index:
            target = text[last_char_index.regs[0][1] + 1:]
            text = text[:last_char_index.regs[0][0] - 1]
            code = constants.LANGCODES.get(target)
        return text, code

    def launch(self):
        text, target = self.get_text_and_target()

        if target:
            try:
                translator = Translator(service_urls=['translate.googleapis.com'])
                text_to_translate = translator.translate(text, dest=target)
                text = text_to_translate.text

                speak = gTTS(text=text, lang=target, slow=False)
                speak.save(Translation.MP3_NAME)

                try:
                    playsound(Translation.MP3_NAME)
                    os.remove(Translation.MP3_NAME)
                except IOError:
                    pass
            except (sr.RequestError, sr.UnknownValueError) as e:
                print(e)
        else:
            utils.speak('The asked language is not supported by me.')
