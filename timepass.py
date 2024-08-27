import os
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import sys
import requests
import eel

# Initialize eel
eel.init("www")

# Initialize speech engine and recognizer
engine = pyttsx3.init()
r = sr.Recognizer()
voices = engine.getProperty('voices')

def speak(text):
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 135)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def takecommand():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = r.listen(source, timeout=2, phrase_time_limit=5)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"User Said: {command}\n")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return "none"
    except sr.RequestError as e:
        speak("Sorry, my speech service is down")
        return f"Could not request results; {e}"
    except Exception as e:
        return f"An error occurred: {e}"
    return command.lower()



@eel.expose
def process_command():
   
    command = takecommand()
    if command == "none":
        return "none"

    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}"
        speak(response)

    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        response = "Opening Google"

    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube"

    elif 'play music' in command:
        music_dir = 'C:\\Users\\Music'
        songs = os.listdir(music_dir)
        if songs:
            speak("Playing music")
            os.startfile(os.path.join(music_dir, songs[0]))
            response = "Playing music"
        else:
            speak("No music files found in the directory")
            response = "No music files found in the directory"

    elif 'search' in command:
        search_query = command.replace('search', '').strip()
        if search_query:
            speak(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            response = f"Searching for {search_query}"
        else:
            speak("What do you want to search for?")
            response = "What do you want to search for?"

    elif 'joke' in command:
        response = requests.get('https://official-joke-api.appspot.com/random_joke').json()
        joke = f"Here's a joke: {response['setup']} - {response['punchline']}"
        speak(joke)
        response = joke

    elif 'exit' in command or 'quit' in command or 'stop' in command:
        speak("Goodbye! Have a nice day.")
        sys.exit()
    
    else:
        response = "I am sorry, I can't help with that yet. Please try something else."

    return response

def main():
    eel.start('index.html', mode='edge', host='localhost', block=True)

if __name__ == "__main__":
    main()
