import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pytube as pt 
from dotenv import load_dotenv
import os
load_dotenv()


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                               client_secret=os.getenv("CLIENT_SECRET"),
                                               redirect_uri=os.getenv("REDIRECT_URI"),
                                               scope="playlist-modify-public, playlist-modify-private"))


ytpl_link = input("Type The YT Playlist Url->> ")
sfpl_link = input("Type the Spotify Playlist->> ")
sfpl_id = None

if("playlist?" in ytpl_link and "www.youtube.com" in ytpl_link):
    ytpl = pt.Playlist(ytpl_link)
    if(sfpl_link == ""):
        sfpl = sp.user_playlist_create(user=sp.me()["id"], name=ytpl.title, public=False)
        sfpl_id = sfpl["id"]
    else:
        sfpl_id = sfpl_link.split('/')[-1]

    found = 0
    not_found = 0
    for vid in ytpl.videos:
        query = f"artist:{vid.author} track:{vid.title}"
        result = sp.search(q=query, limit=1, type="track")
        if result["tracks"]["items"]:
            track = result["tracks"]["items"][0]
            sp.playlist_add_items(sfpl_id, [track["uri"]])
            print(f"{n}. Track '{track['name']}' by {', '.join([artist['name'] for artist in track['artists']])} added to the playlist.")
            found += 1
        else:
            print(query, "- Not Found!")
            not_found += 1
else:
    print("Not a youtube playlist Url!")





