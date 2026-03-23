"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

class StreamingPlatform():
    def __init__(self, name):
        self.name = name
        self.catalogue = {}
        self.users = []
        self.artists = []
        self.albums = []
        self.playlists = []
        self.sessions = []
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)
    def add_user(self, user):
        self.users.append(user)
    def add_artist(self, artist):
        self.artists.append(artist)
    def add_album(self, album):
        self.albums.append(album)
    def add_playlist(self, playlist):
        self.playlists.append(playlist)
    def all_users(self):
    	return self.users
    def record_session(self, session):
        pass
    def get_track(self, track_id) -> None | Track:
        pass
    def get_user(self, user_id) -> None | User:
        pass
    def total_listening_time_minutes(self, start, end) -> float:
        pass




