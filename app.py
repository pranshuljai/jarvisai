from flask import Flask, render_template, request
import os
import platform
import webbrowser
import pyttsx3
import wikipediaapi
import yt_dlp  # Ensure you have yt-dlp installed (pip install yt-dlp)

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate

# Initialize Wikipedia API with a user agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='JarvisAI/1.0 (https://github.com/pranshuljai/jarvis-ai)'  # Specify your user agent here
)

# Register Chrome as the browser
chrome_path = r'C:/Users/pc/AppData/Local/Google/Chrome/Application/chrome.exe'  # Update this path if necessary
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def get_command(command):
    """Process the command."""
    command = command.lower()  # Convert to lowercase for easier matching

    if "shutdown" in command:
        shutdown_computer()
        return "Shutting down the computer..."
    elif "restart" in command:
        restart_computer()
        return "Restarting the computer..."
    elif "open" in command:
        return open_website(command)
    elif "open images of" in command:
        return open_image(command)
    elif "play" in command:
        return play_song(command)
    elif "what is" in command or "tell me about" in command:
        return wikipedia_search(command)
    elif "who is your creator" in command:
        return "My creator is Pranshul Jain."
    else:
        return "Sorry, I didn't understand that command."

def shutdown_computer():
    """Shutdown the computer."""
    if platform.system() == "Windows":
        os.system("shutdown /s /t 1")  # Shutdown immediately on Windows
    elif platform.system() in ["Linux", "Darwin"]:
        os.system("sudo shutdown now")  # Shutdown on Linux or macOS

def restart_computer():
    """Restart the computer."""
    if platform.system() == "Windows":
        os.system("shutdown /r /t 1")  # Restart immediately on Windows
    elif platform.system() in ["Linux", "Darwin"]:
        os.system("sudo reboot")  # Restart on Linux or macOS

def open_website(command):
    """Open websites dynamically based on the command."""
    website_name = command.replace("open", "").strip()
    if website_name:
        url = f"https://www.{website_name}.com"
        webbrowser.get('chrome').open(url)
        return f"Opening {website_name}."
    return "Please specify the website you want to open."

def open_image(command):
    """Open an image search based on the command."""
    search_term = command.replace("open images of", "").strip()
    if search_term:
        webbrowser.get('chrome').open(f"https://www.google.com/search?hl=en&tbm=isch&q={search_term.replace(' ', '+')}")
        return f"Opening images for {search_term}."
    return "Please specify what images you want to open."

def play_song(command):
    """Play a song based on the command using YouTube."""
    song_name = command.replace("play", "").strip()
    if song_name:
        search_query = '+'.join(song_name.split())
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
            'extract_flat': True,  # Only search, don't download
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            if info_dict and 'entries' in info_dict and len(info_dict['entries']) > 0:
                video_url = info_dict['entries'][0]['url']
                webbrowser.get('chrome').open(video_url)
                return f"Playing {song_name}."
            else:
                return "Sorry, I couldn't find that song."
    return "Please specify which song you want to play."

def wikipedia_search(command):
    """Fetch summary from Wikipedia based on the command."""
    if "what is" in command:
        search_term = command.replace("what is", "").strip()
    elif "tell me about" in command:
        search_term = command.replace("tell me about", "").strip()
    else:
        search_term = command.strip()  # Just take the command as is

    if search_term:
        page = wiki_wiki.page(search_term)
        if page.exists():
            summary = page.summary[:500]  # Get the first 500 characters of the summary
            return summary  # Return the summary instead of speaking it
        else:
            return f"Sorry, I couldn't find any information on {search_term}."
    return "Please specify what you'd like to know."

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    if request.method == 'POST':
        command = request.form['command']
        response = get_command(command)
    return render_template('index.html', response=response)

if __name__ == "__main__":
    app.run(debug=True)
