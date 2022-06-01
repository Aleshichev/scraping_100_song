from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#
# date = input("Введите дату, в формате YYY-MM-DD:")
#
# response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
response = requests.get(f"https://www.billboard.com/charts/hot-100/2010-10-10")
text_html = response.text

soup = BeautifulSoup(text_html, "html.parser")
class_name ="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
data = soup.find_all("h3", id="title-of-a-story", class_=class_name)
# song_names = [song_text.getText() for song_text in song_names_spans]
# song_names = [song.getText() for song in song_names_spans]
songs_list = [(song.getText()).strip() for song in data]
# for song in data:
#     text = song.getText()
#     stripped_text = text.strip()
#     songs_list.append(stripped_text)
print(songs_list)
CLIENT_ID = "1489c98574a04834ae7e694c768778ed" # Сюда вводим полученные данные из панели спотифая
SECRET = "588504e32acf4d4ab6bbfb4134d90598" # Сюда вводим полученные данные из панели спотифая

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/callback",
        client_id=CLIENT_ID,
        client_secret=SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
print(user_id)
# # user_id = "31bsfljvpdnn2gppcnbpavipewky"
#
song_uris = []
# year = date.split("-")[0]
year = 2010
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"2010 Billboard 100", public=False)


#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

