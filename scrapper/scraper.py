import lyricsgenius
import os
from dotenv import load_dotenv

# Load environment variables from the root folder
env_path = os.path.join(os.path.dirname(__file__), '..', 'genius_api.env')
load_dotenv(dotenv_path=env_path)

api_token = os.getenv("GENIUS_ACCESS_TOKEN")
if not api_token:
    print("Error: GENIUS_ACCESS_TOKEN not found in genius_api.env.")
    exit(1)

genius = lyricsgenius.Genius(api_token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], timeout=15, retries=3)

# 1. Open and read your text file
file_name = 'songs.txt'
try:
    with open(file_name, 'r', encoding='utf-8') as file:
        song_list = [line.strip() for line in file.readlines() if line.strip()]
except FileNotFoundError:
    print(f"Couldn't find '{file_name}'")
    exit()

# 2. Output folder
output_folder = "../data"

# Create the data folder if it doesn't already exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 3. Loop through the list and fetch lyrics
for title in song_list:
    print(f"Searching for '{title}' by ABBA...")
    
    try:
        song = genius.search_song(title, "ABBA")
        
        if song is not None and "abba" in song.artist.lower():
            print(f"✅ Found it! Saving lyrics for {song.title}...\n")
            
            safe_title = title.replace("/", "-") 
            # This will save to: ../data/Dancing Queen.txt
            save_path = os.path.join(output_folder, f"{safe_title}.txt")
            
            with open(save_path, "w", encoding="utf-8") as text_file:
                text_file.write(song.lyrics)
        else:
            print(f"❌ Skipped '{title}': Not found or not recognized as an ABBA song.\n")
            
    except Exception as e:
        print(f"⚠️ Oops! We hit a snag with '{title}'. Moving on to the next one...\n")

print(f"All done! Your lyrics are safely tucked away in the '{output_folder}' folder.")