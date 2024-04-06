from colorama import Fore, Back, Style
import requests
import os
import glob
import threading
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import pygame
from gtts import gTTS
import random


API_KEY = '2PY0c8RpBJBELddc6y1NFsVUwBqyRxfr'

location = "37.83805150,27.83839305"

url = f"https://api.tomorrow.io/v4/weather/realtime?location=aydin=&apikey=2PY0c8RpBJBELddc6y1NFsVUwBqyRxfr"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

#print(response.text) #Hava Durumuna ait tüm bilgiler

weather = response.text[287:291]

def sil_benzer_dosyalari(dizin, kisim):

    dosya_listesi = glob.glob(os.path.join(dizin, f"*{kisim}*"))

    for dosya in dosya_listesi:
        try:
            os.remove(dosya)
        except Exception as e:
            print(f"{dosya} silinemedi. Hata: {e}")

dizin = "C:\\Users\\akbab\\OneDrive\\Masaüstü\\Hermes\\Hermes"
kisim = "ses"
sil_benzer_dosyalari(dizin, kisim)

openai.api_key = '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'
      
load_dotenv()
model = 'gpt-3.5-turbo'

r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

if len(voices) == 0:
    print("Ses motorları bulunamadı. Lütfen ses motorlarınızı kontrol edin.")
    exit()

engine.setProperty('rate', 150)

name = "Yutek"
greetings = [f"Hello !"]

def listen_for_wake_word(source):
    print("Please say 'Hi' for start chat!")
    print("")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="en-US")
            if "hi" in text.lower():
                print("Hello!") # Hello yu algıladı
                print("")
                greetingSounds1 = gTTS(text=random.choice(greetings), lang="en")
                greetingSounds1.save("greetingSound1.mp3")
                pygame.init()
                pygame.mixer.music.load("greetingSound1.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                pygame.quit()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass

def listen_and_respond(source):
    while True:
        print(Fore.GREEN +"Im listening to you!!!")
        print(Style.RESET_ALL)
        audio = r.listen(source)
        try:
            dizin = "C:\\Users\\akbab\\OneDrive\\Masaüstü\\Hermes\\Hermes"
            kisim = "ses"

            def generate_random_number(start, end):
                return random.randint(start, end - 1)
            random_number = generate_random_number(1, 100)
            soundLocation = f"C:\\Users\\akbab\\OneDrive\\Masaüstü\\Hermes\\Hermes\\ses{random_number}.mp3"

            def play():
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(soundLocation)
                pygame.mixer.music.play()

            def cooldown():
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)

            sound_thread = threading.Thread(target=play)
            wait_thread = threading.Thread(target=cooldown)

            def zartzurt():
                sound_thread.start()
                wait_thread.start()
                sound_thread.join()
                wait_thread.join()
                        
            text = r.recognize_google(audio)

            metin = text +" (Just explain in one short sentence.)"
            print(Fore.YELLOW+f"You said: {text}")
            print(Style.RESET_ALL)
            print("")

            def weathersec():
                cevap = f"temperature: {weather}"
                ses = gTTS(text=cevap,lang="en-us")
                print(cevap)
                print("")
                ses.save(soundLocation)
                zartzurt()
                listen_and_respond(source)
            

            def enough():
                cevap= "Okey, see you later!"
                ses = gTTS(text=cevap,lang="en-us")
                print(cevap)
                print("")
                ses.save(soundLocation)
                zartzurt()
                listen_for_wake_word(source)

            def bye():
                cevap= "Bye Bye!"
                ses = gTTS(text=cevap,lang="en-us")
                print(cevap)
                print("")
                ses.save(soundLocation)
                zartzurt()
                exit()

            def zaman():
              t = time.localtime()
              current_time = time.strftime("%H:%M:%S", t)
              random_number = generate_random_number(1, 100)
              answer = "It's " + current_time
              konusma = gTTS(text=answer, lang="en")
              konusma.save(soundLocation)
              print(answer)
              print("")
              #print("Oluşturulan rastgele sayı:", random_number)
              zartzurt()
              listen_and_respond(source)
            
            def konus(cevap,location):
                ses = gTTS(text=cevap,lang="en-us")
                location = soundLocation
                ses.save(location)
                print(sozluk[text.lower()])
                zartzurt()
                listen_and_respond(source)

            sozluk = {
                "what's your name":"My name is Hermes!",
                "what is your name":"My name is Hermes!",
                "what can you do":"I can answer  questions and provide information.",
                "what's your daily routine like":"Answer all your quesitons.",
                "whats your daily routine like":"Answer all your quesitons.",
                "do you have any hobbies":"my main focus is assisting and interacting with users like you",
                "how are you doing today":"Im doing well",
                "how old are you": "I am an artificial intelligence designed to be helpful and informative. I don't have a age",
                "where are you from":"Im from Aydın",
                "who was created you":"Hermes was develpoed by a student",
                "who did you":"Hermes was develpoed by a student",
                "what have you been up to lately":"just keeping busy with tasks",
                "tell me a joke":"Here is one for you:\nWhy don’t scientists trust atoms?\nBecause they make of things!",
            }

            if "goodbye" in text.lower():
                bye()

            if "enough" in text.lower():
                enough()

            if "what is the temperature" in text.lower():
                weathersec()

            if "what is the time"  in text.lower():
                zaman()

            if "what time is it" in text.lower():
                zaman()

            keys = list(sozluk.keys())
            if text.lower() in sozluk:
                konus(sozluk[text.lower()],soundLocation)
                print("Hazır ifade konuşuluyor")

            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{metin}"}])
            response_text = response.choices[0].message.content
            print(response_text)
            print("")

            #print("Oluşturulan rastgele sayı:", random_number)
            tts = gTTS(text=response_text, lang='en')
            tts.save(soundLocation)
            zartzurt()

            #seconds = pygame.mixer.Sound(soundLocation).get_length()
            #print(f"Cevap Süresi: {seconds}")
    
        except sr.UnknownValueError:
            #print("Ops! Sorry I couldn't understand you.")
            #print("I listening again. Please speak clearly.")
            #listen_and_respond(source)
            pass

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

with sr.Microphone() as source:
    listen_for_wake_word(source)

if __name__ == "__main__":
    listen_for_wake_word(source)