import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Configurare Spotify API
client_id = "c16b96de76ee4322b055d42dbe35b597"  # Înlocuiește cu propriul Client ID
client_secret = "603f5fb689c44c92bc75fc01328651c1"  # Înlocuiește cu propriul Client Secret

# Autentificare cu Spotify API
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Citește fișierul Excel
file_path = "C:/Users/Hodis Florin/Desktop/Spoty/LinkSpotify.xlsx"  # Înlocuiește cu calea reală către fișierul tău
df = pd.read_excel(file_path)

# Creează o funcție pentru a căuta albumele pe Spotify
def get_album_link(artist, album):
    try:
        query = f"artist:{artist} album:{album}"
        results = sp.search(q=query, type="album", limit=1)
        if results['albums']['items']:
            return results['albums']['items'][0]['external_urls']['spotify']  # Link-ul albumului
        else:
            return "Nu s-a găsit"  # Dacă nu găsește albumul
    except Exception as e:
        return f"Eroare: {e}"

# Adaugă linkurile în coloana C
df['Spotify Link'] = df.apply(lambda row: get_album_link(row['Artist'], row['Album']), axis=1)

# Salvează rezultatele într-un fișier Excel nou
output_file = "albume_cu_linkuri.xlsx"
df.to_excel(output_file, index=False)

print(f"Linkurile au fost generate și salvate în {output_file}!")
