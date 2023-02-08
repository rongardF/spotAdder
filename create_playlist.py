# tutorial video - https://www.youtube.com/watch?v=7J_qcttfnJA 

import json
import requests
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

from secrets import CLIENT_ID, CLIENT_TOKEN

base_uri=r"https://api.spotify.com/v1"

class CreatePlaylist(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.user_id= CLIENT_ID
        self.spotify_token=CLIENT_TOKEN
        self.youtube_client=self.get_youtube_client()
        self.all_songs_info={}
    
    def get_youtube_client(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "credentials.json"
    
        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
        
        return youtube
    
    def get_liked_videos(self):
        request = self.youtube_client.videos().list(part="snippet,contentDetails,statistics", \
                                                    myRating="like" \
                                                    )
        response = request.execute()
        
        # collect each video and get important information
        for item in response["items"]:
            video_title=item["snippet"]["title"]
            youtube_url="https://www.youtube.com/watch?v={}".format(item["id"])
            
            # use youtube.dl library to collect song name & artist
            video=youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False) 
            song_name=video["track"] # there is no such key in the response from YoutubeDL, will fail here
            artist=video["artist"]
            self.all_songs_info[video_title]={"youtube_url":youtube_url, \
                                              "song_name": song_name, \
                                              "artist": artist, \
                                              "spotify_uri": self.get_spotify_uri(song_name, artist)}
    
    def create_playlist(self):
        request_body= json.dumps({"name": "Youtube Liked Videos", \
                                 "description": "All liked Youtube videos", \
                                 "public": True})
        
        query = base_uri+"/users/{}/playlists".format(self.user_id)
        
        response= requests.post(query, data=request_body, headers={"Content-Type":"application/json", \
                                                                   "Authorization":"Bearer {}"}).format(self.spotify_token)
        
        response_json=response.json()
        
        return response_json["id"]
    
    def get_spotify_uri(self, song_name, artist):
        query=base_uri+"/search?q={}&type=track%2Cartist&market=US&limit=10&offset=5".format(song_name + artist) # get the track based on song and artist name
        
        response=requests.get(query, headers={"Content-Type":"application/json", \
                                               "Authorization":"Bearer {}"}).format(self.spotify_token)
        
        response_json=response.json()
        songs= response_json["tracks"]["items"]
        
        # only use first song
        uri=songs[0]["uri"]
        
        return uri
        
    def add_song_to_playlist(self):
        # populate songs dictionary
        self.get_liked_videos()
        
        # collect uri for all songs
        uris=[]
        for song, info in self.all_songs_info.items():
            uris.append(info["spotify_uri"])
            
        # create new playlist in spotify
        playlist_id=self.create_playlist()
        
        # add all songs into new playlist
        request_data=json.dump(uris)
        
        query=base_uri+"/playlists/{}/tracks".format(playlist_id)
        
        response= requests.post(query, \
                              data=request_data, \
                              headers={"Content-Type" : "application/json", \
                                       "Authorization":"Bearer {}".format(self.spotify_token)})
        
        response_json=response.json()
        
        return response_json

if __name__=="__main__":
    obj=CreatePlaylist()
    obj.add_song_to_playlist()
