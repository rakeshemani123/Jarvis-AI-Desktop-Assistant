import datetime
import operator
import os
import re
import smtplib
import sys
import time
import webbrowser
from PyQt5.QtGui import QMovie
import PyPDF4
import cv2
import geocoder
import instaloader
import psutil
import pyttsx3
import pywhatkit as wk
import requests
import speech_recognition as sr
import wikipedia
import winsound
from bs4 import BeautifulSoup
from PIL import ImageGrab
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import urllib.request
import pyautogui as p


from jarvisui import Ui_MainWindow

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you today?")


def news():
    main_url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=9b9ce35ef59c43798fc8ca2cab29ae21'
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")

def pdf_reader():
    book = open("my-pdf", "rb")
    pdfReader = PyPDF4.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages in this book: {pages}")
    speak("Sir, please enter the page number I have to read")
    pg = int(input("please enter the page no:"))
    if 1 <= pg <= pages:
        page = pdfReader.getPage(pg - 1)
        text = page.extractText()
        speak(text)
    else:
        speak("Sorry, the page number is out of range.")

def add(a, b):
    """same as a + b"""
    return a + b

def sub(a, b):
    """same as a - b"""
    return a - b

def mul(a, b):
    """same as a * b"""
    return a * b

def div(a, b):
    """same as a / b"""
    return a / b

def alarm(time_to_set):
    current_time = time.strftime("%I:%M %p")
    while current_time != time_to_set:
        current_time = time.strftime("%I:%M %p")
        time.sleep(1)
    print("Time to wake up!")
    winsound.Beep(1000, 10000)

def get_directions(place):
    try:
        g = geocoder.ip('me')
        if g.latlng:
            current_location = f"{g.latlng[0]},{g.latlng[1]}"
            webbrowser.open(f"https://www.google.com/maps/dir/{current_location}/{place}")
            speak(f"Opening directions to {place} in your web browser.")
        else:
            speak("Sorry, I couldn't determine your current location.")
    except Exception as e:
        print(e)
        speak("Sorry, I am unable to fetch directions at the moment.")

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
        r = sr.Recognizer()
        print("Listening... on mic")
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = r.listen(source,timeout=5, phrase_time_limit=5)
            except Exception as e:
                print(f"Error capturing audio: {e}")
                return "None"
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            print("Say that again please...")
            return "None"
        return query


    def TaskExecution(self):
        wishMe()
        while True:
            query = self.takeCommand().lower()
            print(query)
            if 'open notepad' in query:
                npath = "C:\\Windows\\System32\\notepad.exe"
                os.startfile(npath)
            elif 'close notepad' in query:
                os.system("taskkill /f /im notepad.exe")
            elif 'open command prompt' in query:
                os.system("start cmd")
            elif 'close command prompt' in query:
                os.system("taskkill /f /im cmd.exe")
            elif 'search on youtube' in query:
                speak("What would you like to watch?")
                video_query = self.takeCommand().lower()
                wk.playonyt(video_query)
            elif 'close browser' in query:
                os.system("taskkill /f /im msedge.exe")
            elif 'search on google' in query:
                speak("what should i search?")
                query = self.takeCommand().lower()
                webbrowser.open(f"{query}")
            elif 'open word' in query:
                path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\Wordpad.lnk"
                os.startfile(path)
            elif 'close word' in query:
                os.system("taskkill /f /im WINWORD.EXE")
            elif 'open instagram' in query:
                webbrowser.open("https://www.instagram.com/")
            elif 'open facebook' in query:
                webbrowser.open("https://www.facebook.com/")
            elif 'switch the window' in query:
                p.hotkey("alt", "tab")
            elif 'tell me latest news' in query:
                speak("please wait sir, fetching for latest news")
                news()
            elif "where am i" in query or "where are we" in query:
                speak("Wait a moment sir, let me check.")
                try:
                    g = geocoder.ip('me')
                    if g.city and g.country:
                        speak(f"Sir, we are in {g.city} of {g.country}")
                    else:
                        speak("I'm sorry, I couldn't determine the location accurately.")
                except Exception as e:
                    print(e)
                    speak("Sorry, I am unable to find your location due to a network issue.")
            elif "instagram profile" in query or "profile on instagram" in query:
                speak("sir enter the username properly.")
                name = input("Enter username here:")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"Sir here is the profile of the user")
                speak("Sir would you like to download the profile picture of this account")
                condition = self.takeCommand().lower()
                if 'yes' in condition:
                    mod = instaloader.Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak("I am done sir, profile picture is saved")
                else:
                    pass
            elif 'take screenshot' in query:
                speak("Sir, please tell me the name for this screenshot file")
                name = self.takeCommand().lower()
                speak("Please hold the screen for a few seconds. I am taking a screenshot.")
                screenshot = ImageGrab.grab()
                screenshot.save(f"{name}.png")
                speak("I am done, sir. The screenshot is saved.")
            elif 'read pdf' in query:
                pdf_reader()
            elif "make the files private" in query or "make the files public" in query:
                speak("Sir please tell me you want to make the files private or public")
                condition = self.takeCommand().lower()
                if "private" in condition:
                    os.system("attrib +h /s /d")
                    speak("Sir, all the files are now hidden")
                elif "public" in condition:
                    os.system("attrib -h /s /d")
                    speak("Sir, all the files are now visible to everyone")
            elif 'can you calculate' in query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("say what you want to calculate, Example 2 plus 2")
                    print("listening.....")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)

                def get_operator_fn(op):
                    return {
                        '+': operator._add_,
                        '-': operator._sub_,
                        '*': operator._mul_,
                        'x': operator._mul_,
                        'X': operator._mul_,
                        '/': operator._truediv_
                    }[op]

                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)

                parts = my_string.split()
                result = eval_binary_expr(*parts)
                print(result)
                speak("your result is" + str(result))
            elif 'play movie' in query:
                music_dir = "F:\www.5MovieRulz.es - Miss Shetty Mr Polishetty (2023) 720p Telugu HQ HDRip - x264 - (DD+5.1 - 192Kbps & AAC) - 1.4GB - ESub.mkv"
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"Sir, the time is {strTime}")
                speak(f"Sir, the time is {strTime}")
            elif 'open code' in query:
                codePath = "jarvis.py"
                os.startfile(codePath)
            elif "temperature" in query:
                search = "temperature in Hyderabad"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temperature_text = data.find(string=re.compile(r'(\d+°C)'))
                if temperature_text:
                    temperature = re.search(r'(\d+°C)', temperature_text).group()
                    speak(f"Current {search} is {temperature}")
                else:
                    speak("Sorry, I couldn't retrieve the temperature at the moment.")
            elif 'battery' in query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"Your system has {percentage} percent battery remaining.")
                if percentage >= 75:
                    speak("we have enough power to continue our work")
                elif 40 <= percentage < 75:
                    speak("we can work for a while but look out for charging")
                elif 20 <= percentage < 40:
                    speak("consider plugging your device on charging")
                elif percentage < 20:
                    speak("please charge the device")
            elif "get directions to" in query:
                query = query.replace("get directions to ", "")
                get_directions(query)
            elif 'open camera' in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    if not ret:
                        print("Error: Could not capture frame")
                        break
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
            elif 'volume up' in query:
                p.press("volumeup")
            elif 'volume down' in query:
                p.press("volumedown")
            elif 'mute' in query:
                p.press("volumemute")
            elif 'alarm' in query:
                speak("Sir, please tell me the time to set the alarm. For example, set alarm to 10:30 pm.")
                tt = self.takeCommand().lower()
                tt = tt.replace("set alarm to ", "").replace(".", "").upper()
                alarm(tt)
            else:
                speak("Sorry, I couldn't understand that. Please say that again.")



startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton.clicked.connect(self.login)
        

    def startTaskExecution(self):
        self.ui.movie = QMovie("Voice-assistant-motion-effect.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        if not self.logged_in:
            QMessageBox.warning(self, "Access Denied", "Please login to access this functionality.")

    def login(self):
        while True:
            username = self.ui.lineEdit.text()
            password = self.ui.lineEdit_2.text()
            if username == "test" and password == "test":
                QMessageBox.information(self, "Login Successful", "Welcome, User!")
                startExecution.start()
                break
            else:
                self.ui.lineEdit.setText("")
                self.ui.lineEdit_2.setText("")
                self.ui.lineEdit.setFocus()
                response = QMessageBox.warning(self, "Login Failed", "Invalid username or password. Try again?", QMessageBox.Retry)
                if response == QMessageBox.Retry:
                    break

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString(Qt.ImhTime)
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis = Main()
    jarvis.show()
    exit(app.exec_())
