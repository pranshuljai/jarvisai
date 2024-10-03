from flask import Flask, render_template, request
import wikipediaapi
import yt_dlp
import webbrowser
import os
import platform

# Initialize Flask app
app = Flask(__name__)

# Initialize Wikipedia API with a valid user agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='JarvisAI/1.0 (https://github.com/pranshuljai/jarvisai)'  # Update this with your details
)

# Register Chrome as the browser
chrome_path = r'C:/Users/pc/AppData/Local/Google/Chrome/Application/chrome.exe'  # Adjust the path if needed
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# Helper function to process the command
def process_command(command):
    if "hi" in command or "hello" in command or "hey" in command:
        return "Hi sir, nice to meet you."
    elif "who is your creator" in command:
        return "My creator is Pranshul Jain."
    elif "shutdown" in command:
        return shutdown_computer()
    elif "restart" in command:
        return restart_computer()
    elif "open" in command:
        return open_website(command)
    elif "open images of" in command:
        return open_image(command)
    elif "play" in command:
        return play_song(command)
    elif "what is" in command or "tell me about" in command:
        return wikipedia_search(command)
    else:
        return "Sorry, I didn't understand that command."

# Function to search Wikipedia
def wikipedia_search(command):
    search_term = command.replace("what is", "").replace("tell me about", "").strip()
    
    if search_term:
        page = wiki_wiki.page(search_term)
        if page.exists():
            return page.summary[:500]  # Get the first 500 characters
        else:
            return f"Sorry, I couldn't find any information on {search_term}."
    return "Please specify what you'd like to know."

# Function to play a song using YouTube
def play_song(command):
    song_name = command.replace("play", "").strip()
    if song_name:
        search_query = '+'.join(song_name.split())
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
            'extract_flat': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            if info_dict and 'entries' in info_dict and len(info_dict['entries']) > 0:
                video_url = info_dict['entries'][0]['url']
                webbrowser.get('chrome').open(video_url)
                return f"Playing song: {song_name}"
            else:
                return "Sorry, I couldn't find that song."
    return "Please specify a valid song name."

# Function to open websites dynamically
def open_website(command):
    if "open" in command:
        website_name = command.replace("open", "").strip()
        if website_name:
            url = f"https://www.{website_name}.com"
            webbrowser.get('chrome').open(url)
            return f"Opening {website_name}."
        else:
            return "Please specify the website you want to open."

# Function to open Google Images for a specific search
def open_image(command):
    if "open images of" in command:
        search_term = command.replace("open images of", "").strip()
        if search_term:
            webbrowser.get('chrome').open(f"https://www.google.com/search?hl=en&tbm=isch&q={search_term.replace(' ', '+')}")
            return f"Opening images for {search_term}."
        else:
            return "Please specify what images you want to open."

# Function to shutdown the computer
def shutdown_computer():
    if platform.system() == "Windows":
        os.system("shutdown /s /t 1")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("sudo shutdown now")
    return "Shutting down the computer."

# Function to restart the computer
def restart_computer():
    if platform.system() == "Windows":
        os.system("shutdown /r /t 1")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("sudo reboot")
    return "Restarting the computer."

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        command = request.form['command'].lower()
        response = process_command(command)
        return render_template('index.html', response=response)
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
