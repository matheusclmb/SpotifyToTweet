import requests
import tweepy
import time
from pprint import pprint

CONSUMER_KEY = "YOUR CONSUMER KEY"
CONSUMER_SECRET = "YOUR CONSUMER SECRET KEY"
ACCESS_TOKEN_TWITTER = "TWITTER ACCESS TOKEN"
ACCESS_TOKEN_SECRET = "SECRET ACCESS TOKEN"

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = 'SPOTIFY OAUTH'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_TWITTER, ACCESS_TOKEN_SECRET)

# Create API object

api = tweepy.API(auth)


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link
    }

    return current_track_info
    new_tweet = api.update_status(f"Now playing {track_name} By {artist_names}\nListen on Spotify: {link}")
    return new_tweet


def main():
    current_track_id = None
    while True:
        current_track_info = get_current_track(ACCESS_TOKEN)

        if current_track_info['id'] != current_track_id:
            pprint(
                current_track_info,
                indent=4,
            )
            current_track_id = current_track_info['id']
            current_track_name = current_track_info["track_name"]
            current_artists = current_track_info["artists"]
            current_link = current_track_info["link"]
            new_tweet = api.update_status(f"Now playing {current_track_name} By {current_artists}\nListen on Spotify: {current_link}")

        time.sleep(1)


if __name__ == '__main__':
    main()
