import fnmatch
import json
import os
import random
import re
import webbrowser
import playsound

from gtts import gTTS

import pyttsx3
import speech_recognition as sr

import config
from model.voice_analyzer import VoiceAnalyzer


def choose_random(response):
    return random.choice(response)

def speak(response):
    os_name = config.OS_NAME
    if os_name == 'Alex':
        tts = gTTS(text=response, lang='vi', slow=False)
        #if not os.path.exists(code+".mp3"):
        tts.save(os_name+".mp3")
        playsound.playsound(os_name+".mp3", False)
        os.remove(os_name+".mp3")
    if os_name == 'Jarvis':
        engine = pyttsx3.init()
        engine.say(response)
        engine.setProperty("rate", 130)
        engine.runAndWait()

def find_file(pattern, path):
    paths = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                paths.append(os.path.join(root, name))
        if paths:
            return paths

def get_search_value(command, intent_name, match_flag='word'):
    intents = config.DATA['intents']
    utterances = [intent['utterances'] for intent in intents if intent['tag'] == intent_name][0]
    if match_flag == 'word':
        words = ['\\b' + word + '\\b' for utterance in utterances for word in utterance.split(' ')]
        words = '|'.join(words)
    elif match_flag == 'sentence':
        words = '|'.join(utterances)
    return re.sub(words, '', command, flags=re.IGNORECASE).strip()

def get_path_from_file(app):
    with open(config.APP_DETAILS_FILE) as file:
        app_details = json.load(file)
    app = app_details.get(app)
    if app:
        return app.get('path')

def get_path(app, ext, directories):
    patterns = [f'{app}{ext}', f'{app}*.{ext}', f'*{app}.{ext}', f'*{app}*.{ext}']
    for directory in directories:
        for pattern in patterns:
            result = find_file(pattern, directory)
            if result:
                if len(result):
                    return get_multiple_paths(result, ext)
                else:
                    return result

def tranform_data_json():
    # f = open('datachat'+self.os+'.json', encoding='utf-8')
    f = open('datachatcc.json', encoding='utf-8')
    data = json.load(f)
    for element in data:
        if 'id' in element :
            del element['id']
        if 'time' in element :
            del element['time']

    with open("datachatcc.json", "w", encoding='utf8') as outfile:
        outfile.write(json.dumps(data, ensure_ascii=False))

def get_multiple_paths(paths, ext):
    speak('I got multiple applications. Which one would you like to open?')
    for path in paths:
        exe_name = os.path.basename(path).replace(ext, '')
        speak(exe_name)
        sentiments = VoiceAnalyzer().get_polarity_scores()
        if sentiments:
            max_key = max(sentiments, key=sentiments.get)
            if max_key == 'neu' or max_key == 'pos':
                return path

def add_to_json(app_details):
    with open(config.APP_DETAILS_FILE, 'r+') as file:
        data = json.load(file)
        data.update(app_details)
        file.seek(0)
        json.dump(data, file)

def read_voice_cmd(language):
    recognizer = sr.Recognizer()
    voice_input = ''
    try:
        with sr.Microphone() as source:
            print('Listening...')
            audio = recognizer.listen(source=source, timeout=5, phrase_time_limit=5)
        voice_input = recognizer.recognize_google(audio,key="GOOGLE_SPEECH_RECOGNITION_API_KEY",language = language)
        print('Input : {}'.format(voice_input))
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        print('Network error.')
    except sr.WaitTimeoutError:
        pass
    except TimeoutError:
        pass

    return voice_input.lower()
