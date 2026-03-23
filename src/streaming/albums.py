"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
class Album():
    def __init__(self, album_id, title, artist, release_year, tracks = None):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = tracks if tracks is not None else []


    def add_track(self, track):
        track.album = self
        self.tracks.append(track)
        self.tracks.sort(key=lambda t: t.track_number)

    def duration_seconds(self):
        if not self.tracks:
            return 0 
        t = 0
        for s in self.tracks:
            t += s.duration_seconds 
        return t

    def track_ids(self):
        return {t.track_id for t in self.tracks}

