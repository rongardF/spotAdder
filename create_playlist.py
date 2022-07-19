import json
import requests
from secrets import import spotify_user_id, spotify_token

class CreatePlaylist(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.user_id= spotify_user_id
        self.spotify_token=spotify_token
    
    def get_youtube_client(self):
        pass
    
    def get_liked_videos(self):
        pass
    
    def create_playlist(self):
        request_body= json.dumps({"name": "Youtube Liked Videoss", \
                                 "description": "All liked Youtube videos", \
                                 "public": True})
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        
        response= requests.post(query, data=request_body, headers={"Content-Type":"application/json", \
                                                                   "Authorization":"Bearer {}"}).format(spotify_token)
        
        response_json=response.json()
        
        return response_json["id"]
    
    def get_spotify_uri(self, song_name, artist):
        query="https://api.spotify.com/v1/search?q=Muse&type=track%2C{}artist&limit=10".format(song_name, artist) # this URI is no correct probably!!
        
        response=requests.get(query, headers={"Content-Type":"application/json", \
                                                                   "Authorization":"Bearer {}"}).format(spotify_token)
        
        response_json=response.json()
        songs= response_json["tracks"]["items"]
        
        # only use first song
        uri=songs[0]["uri"]
        
        return
        
    def add_song_to_playlist(self):
        pass