from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import io
import os
import glob

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options)

mp3_fp = io.BytesIO()
r = sr.Recognizer()


def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either, pattern)))


while True:
    with sr.Microphone() as source:
        print("I'm here 1")
        audio = r.listen(source)
        try:
            if 'samantha' in r.recognize_sphinx(audio):
                print("I'm here 2")
                audio = r.listen(source)
                command = r.recognize_sphinx(audio)
                print(command)
                if 'never mind' in command and 'play' not in command:
                    tts = gTTS('Okay', lang='en')
                    tts.save('out.mp3')
                    play(AudioSegment.from_mp3('out.mp3'))
                    os.system('rm out.mp3')
                    break
                elif 'play ' in command:
                    if 'by' in command:
                        artist = command.split(' by ')[1]
                        song = command.split(' by ')[0][5:]
                        print(song)
                        print(artist)
                        for i in insensitive_glob('/home/will/Music/%s - %s.mp3' % (artist, song)):
                            play(AudioSegment.from_mp3(i))
        except sr.UnknownValueError:
            continue
