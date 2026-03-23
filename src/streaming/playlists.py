"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

class Playlist():
    def __init__(self, playlist_id, name, owner, tracks = []):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = tracks

    def add_track(self, track):
        self.tracks.append(track)
    def remove_track(self, track_id):
        pass
    def total_duration_seconds(self) -> int:
        t = 0
        for s in self.tracks:
            t += s.duration_minutes() * 60
        return t

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner, tracks = [], contributors = []):
        super().__init__(playlist_id, name, owner,  tracks = [])
        self.contributors = contributors
    def add_contributor(self, user):
        self.contributors.append(user)
    def remove_contributor(self, user):
        for x in self.contributors:
            if x == user:
                self.contributors.remove(user)

