🗣️ Jarvis – AI Voice Assistant in Python

Jarvis is a voice-controlled personal assistant built with Python. It listens to your commands, understands them using speech recognition, and performs real-world tasks like opening websites, fetching news, weather updates, live cricket scores, playing music, telling jokes, and more!

✨ Features

🎙️ Voice Activation → Trigger Jarvis with the keyword “Jarvis”.

🌐 Open Websites → Google, YouTube, Instagram, or any custom site.

🎵 Play Music → From a built-in music library.

📰 Latest News → Get top 5 headlines from NewsAPI.

🏏 Cricket Scores → Live match updates via Cricbuzz API.

☁️ Weather Updates → Current weather of any city using OpenWeatherMap.

⏰ Time & Date → Speak the current time and today’s date.

🤣 Random Jokes → Lighten the mood with a joke.

📖 Wikipedia Search → Quick information summaries.

🛠️ Tech Stack

Python 3.x

SpeechRecognition – Convert speech to text

Pyttsx3 – Text-to-speech (offline)

Requests – API calls (News, Weather, Cricbuzz)

Webbrowser – Open websites

Wikipedia – Fetch summaries

🚀 How It Works

Jarvis keeps listening through the microphone.

When you say “Jarvis”, it activates for 15 seconds.

Speak your command (like “open YouTube”, “tell me the news”, “what’s the weather in Delhi”).

Jarvis processes the request and responds with voice output.

📦 Setup & Installation
git clone https://github.com/your-username/jarvis-voice-assistant.git
cd jarvis-voice-assistant
pip install -r requirements.txt

Requirements (requirements.txt)
speechrecognition
pyttsx3
requests
wikipedia
pyaudio


(Install pyaudio carefully: pip install pipwin && pipwin install pyaudio on Windows)

🔑 API Keys Required

NewsAPI → Get here

OpenWeatherMap API → Get here

Cricbuzz API (RapidAPI) → Get here

Add them in the script as environment variables or directly in the code.

📌 Example Commands

“Jarvis, open Google”

“Jarvis, play Believer”

“Jarvis, tell me the news”

“Jarvis, what’s the cricket score”

“Jarvis, what’s the weather in Mumbai”

“Jarvis, what’s the time”

“Jarvis, tell me a joke”
