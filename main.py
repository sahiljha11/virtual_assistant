import speech_recognition as sr
import webbrowser
import time
import requests
import pyttsx3
import random
import os
import wikipedia
import pyjokes

recognizer = sr.Recognizer()

def speak(text):
    """Safe TTS function that always works"""
    try:
        print(f"Jarvis: {text}")
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS error: {e}")

# ----------------- NEWS -----------------
def get_news():
    try:
        NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_NEWS_API_KEY")
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data.get("status") == "ok":
            articles = data.get("articles", [])[:5]
            if not articles:
                return "Sorry, no news headlines found."
            news_list = [f"Headline {i+1}: {a.get('title', '')}" for i, a in enumerate(articles) if a.get("title")]
            return "Here are the top news headlines. " + " ".join(news_list)
        return "Sorry, I could not fetch the news."
    except Exception as e:
        return f"Error fetching the news: {e}"

# ----------------- CRICKET -----------------
def get_cricket_score():
    try:
        url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        for match_type in data.get("typeMatches", []):
            for series in match_type.get("seriesMatches", []):
                series_data = series.get("seriesAdWrapper", {})
                for match in series_data.get("matches", []):
                    if "matchScore" in match:
                        team1 = match["matchInfo"]["team1"]["teamName"]
                        team2 = match["matchInfo"]["team2"]["teamName"]
                        score1 = match["matchScore"]["team1Score"]["inngs1"]
                        score_text = f"{team1}: {score1['runs']}/{score1['wickets']} in {score1['overs']} overs"
                        return f"Latest cricket score: {score_text} against {team2}."
        return "Sorry, I could not fetch the cricket score."
    except Exception as e:
        return f"Error fetching the cricket score: {e}"

# ----------------- WEATHER -----------------
def get_weather(city="Mumbai"):
    try:
        API_KEY = os.getenv("WEATHER_API_KEY", "35f9a8f54261454489b172941251608")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("cod") == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            return f"The weather in {city} is {desc} with a temperature of {temp}°C."
        else:
            return f"Sorry, I could not fetch the weather. Error: {response.get('message', '')}"
    except Exception as e:
        return f"Error fetching weather: {e}"


# ----------------- MUSIC -----------------
music_library = {
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
    "see you again": "https://www.youtube.com/watch?v=RgKAFK5djSk",
    "cheap thrills": "https://www.youtube.com/watch?v=nYh-n7EOtMA",
    "saiyaara": "https://www.youtube.com/watch?v=BSJa1UytM8w",
    "chikni chameli": "https://www.youtube.com/watch?v=QcQpqWhTBCE"
}

# ----------------- MAIN -----------------
if __name__ == "__main__":
    speak("Testing speech synthesis before starting Jarvis.")
    speak("Initializing Jarvis...")

    active_until = 0  # Jarvis stays active after trigger

    while True:
        print("Listening...")
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                query = recognizer.recognize_google(audio).lower()
                print(f"You said: {query}")
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                continue
            except sr.RequestError:
                print("Google Speech Recognition service error.")
                continue
            except Exception as e:
                print(f"Mic error: {e}")
                continue

        current_time = time.time()

        # --- TRIGGER WORD ---
        if "jarvis" in query:
            print("Trigger word detected.")
            speak("Yes sir")
            active_until = current_time + 30  # Active for 30 seconds

        # --- COMMANDS ---
        elif current_time < active_until:
            # Websites
            if "open google" in query:
                speak("Opening Google.")
                webbrowser.open("https://www.google.com")
            elif "open youtube" in query:
                speak("Opening YouTube.")
                webbrowser.open("https://www.youtube.com")
            elif "open instagram" in query:
                speak("Opening Instagram.")
                webbrowser.open("https://www.instagram.com")

            # Music
            elif "music" in query:
                song = random.choice(list(music_library.keys()))
                speak(f"Playing {song}.")
                webbrowser.open(music_library[song])
            elif "play" in query:
                song_name = query.split("play", 1)[1].strip().lower()
                if song_name in music_library:
                    speak(f"Playing {song_name}.")
                    webbrowser.open(music_library[song_name])
                else:
                    speak("Sorry, I don't have that song.")

            # News & Cricket
            elif "news" in query:
                news = get_news()
                speak(news)
            elif "cricket" in query:
                score = get_cricket_score()
                speak(score)

            # Time & Date
            elif "time" in query:
                current_time_str = time.strftime("%I:%M %p")
                speak(f"The current time is {current_time_str}.")
            elif "date" in query:
                current_date = time.strftime("%A, %d %B %Y")
                speak(f"Today is {current_date}.")

            # Weather
            elif "weather" in query:
                city = "Mumbai"  # default
                if "in" in query:
                    city = query.split("in")[-1].strip()
                speak(get_weather(city))


            # Wikipedia
            elif "who is" in query or "what is" in query:
                try:
                    topic = query.replace("who is", "").replace("what is", "").strip()
                    summary = wikipedia.summary(topic, sentences=2)
                    speak(summary)
                except Exception:
                    speak("Sorry, I could not find that on Wikipedia.")

            # Jokes
            elif "joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            # Google Search
            elif "search for" in query:
                search_query = query.replace("search for", "").strip()
                speak(f"Searching Google for {search_query}.")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")

            # Open Apps (Windows only)
            elif "open notepad" in query:
                speak("Opening Notepad.")
                os.system("notepad.exe")
            elif "open calculator" in query:
                speak("Opening Calculator.")
                os.system("calc.exe")
            elif "open command prompt" in query:
                speak("Opening Command Prompt.")
                os.system("start cmd")
            elif "open powershell" in query:
                speak("Opening PowerShell.")
                os.system("start powershell")
            elif "open file explorer" in query:
                speak("Opening File Explorer.")
                os.system("explorer.exe")
            elif "open whatsapp" in query:
                speak("Opening WhatsApp.")
                os.system("start WhatsApp.exe")

            # System Control (Windows only)
            elif "shutdown system" in query:
                speak("Shutting down your computer.")
                os.system("shutdown /s /t 1")
            elif "restart system" in query:
                speak("Restarting your computer.")
                os.system("shutdown /r /t 1")
            elif "lock system" in query:
                speak("Locking your computer.")
                os.system("rundll32.exe user32.dll,LockWorkStation")
            elif "game" in query:
                speak("Launching a game.")
                webbrowser.open("https://chromedino.com/")

            # Exit
            elif "shutdown" in query or "exit" in query or "quit" in query:
                speak("Goodbye, sir. Shutting down.")
                break

            
