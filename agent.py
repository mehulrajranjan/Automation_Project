import pyttsx3
import os
import datetime
import smtplib
import speech_recognition as sr
import webbrowser
import wikipedia

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning, Let me know how can I help you?")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Let me know how can I help you?")
    else:
        speak("Good Evening, Let me know how can I help you?")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing your voice...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('<EMAIL>', '<PASSWORD>')
    server.sendmail('<EMAIL>', to, content)
    server.close()

if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')

            query = query.replace('wikipedia', '').strip()

            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)

            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results. Please be more specific.")
                print(e.options[:5])  # show top 5 options

            except wikipedia.exceptions.PageError:
                speak("Sorry, I could not find anything on Wikipedia.")

            except Exception as e:
                speak("Something went wrong")
                print(e)

        elif 'open notepad' in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)

        elif 'open paint' in query:
            npath = "C:\\Windows\\system32\\mspaint.exe"
            os.startfile(npath)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com/")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com/")

        elif 'open wikipedia' in query:
            webbrowser.open("https://www.wikipedia.org/")

        elif 'open linkedin' in query:
            webbrowser.open("https://www.linkedin.com/")

        elif 'tell me the time' in query:
            time = datetime.datetime.now().strftime("%I:%M:%S")
            speak(time)

        elif 'email' in query:
            try:
                speak("what should I send?")
                content = takecommand()
                to = "<RECIEVER'S EMAIL>"
                sendEmail(to, content)
                speak("Your email has been sent")

            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email")
