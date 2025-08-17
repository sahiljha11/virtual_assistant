import speech_recognition as sr
import webbrowser
import time
import os
import requests
import pyttsx3

recognizer = sr.Recognizer()
    


def speak(text):
    safe_text = text.replace("'", "''")
    command = f'powershell -Command "Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{safe_text}\');"'
    print(command)  # Debug
    os.system(command)

def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=90dad0e6457a4d91be9d04eaccf8b4f0"
        response = requests.get(url)
        data = response.json()
        print(data)
        if data.get("status") == "ok":
            articles = data.get("articles", [])[:5]
            if not articles:
                return "Sorry, no news headlines found."
            # Number the headlines for clarity
            news_list = [f"Headline {i+1}: {article.get('title', '')}" for i, article in enumerate(articles) if article.get("title")]
            news_text = "Here are the top news headlines. " + " ".join(news_list)
            return news_text
        else:
            return "Sorry, I could not fetch the news."
    except Exception as e:
        return "Sorry, there was an error fetching the news."

def get_cricket_score():
    try:
        url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
            "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        for match in data.get("matches", []):
            if "score" in match:
                score = match["score"]["display"]
                return f"Latest cricket score: {score}"
        return "Sorry, I could not fetch the cricket score."
    except Exception as e:
        return "Sorry, there was an error fetching the cricket score."

# --- Music library as a dictionary ---
music_library = {
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
    "see you again": "https://www.youtube.com/watch?v=RgKAFK5djSk",
    "cheap thrills": "https://www.youtube.com/watch?v=nYh-n7EOtMA",
    "saiyaara": "https://www.youtube.com/watch?v=BSJa1UytM8w",
    "chikni chameli": "https://www.youtube.com/watch?v=QcQpqWhTBCE"
}

if __name__ == "__main__":
    speak("initializing jarvis...")
    active_until = 0  # Timestamp until which Jarvis is active

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            query = query.lower()

            current_time = time.time()

            if "jarvis" in query:
                print("Trigger word detected.")
                speak("Yes sir")
                active_until = current_time + 15  # Activate for 15 seconds

            elif current_time < active_until:
                if "open google" in query:
                    speak("opening google.")
                    webbrowser.open("https://www.google.com")
                elif "open youtube" in query:
                    speak("opening youtube.")
                    webbrowser.open("https://www.youtube.com")
                elif "open instagram" in query:
                    speak("opening instagram.")
                    webbrowser.open("https://www.instagram.com")
                elif "music" in query:
                    speak("sure, playing music.")
                    # Play a default song from the music library
                    first_song = next(iter(music_library))
                    webbrowser.open(music_library[first_song])
                elif "news" in query:
                    news = get_news()
                    speak(news)
                elif "cricket score" in query or "cricket" in query:
                    score = get_cricket_score()
                    speak(score)
                elif "play" in query:
                    song_name = query.split("play", 1)[1].strip().lower()
                    if song_name in music_library:
                        speak(f"Playing {song_name}.")
                        webbrowser.open(music_library[song_name])
                    else:
                        speak("Sorry, I don't have that song.")
                elif "tell news" in query or "news headlines" in query:
                    news = get_news()
                    speak(news)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
