"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

class Artist():
    def __init__(self, artist_id, name, tracks = None, genre = ""):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = tracks
        self.tracks = list(tracks) if tracks is not None else []

    def add_track(self, track):
        self.tracks.append(track)
    def track_count(self):
        return len(self.tracks)
