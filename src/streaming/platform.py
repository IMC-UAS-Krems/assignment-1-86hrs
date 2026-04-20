"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from datetime import datetime, timedelta
from .users import User, PremiumUser, FamilyMember
from .tracks import Track, Song
from .artists import Artist
from .albums import Album
from .playlists import Playlist, CollaborativePlaylist
from .sessions import ListeningSession


class StreamingPlatform:
    """
    Main class of the application
    Attributes: name, catalogue, users, artists, albums, playlists, sessions
    """
    def __init__(self, name: str):
        self.name = name
        self._catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []

    def add_track(self, track: Track):
        self._catalogue[track.track_id] = track

    def add_user(self, user: User):
        self._users[user.user_id] = user

    def add_artist(self, artist: Artist):
        self._artists[artist.artist_id] = artist

    def add_album(self, album: Album):
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session: ListeningSession):
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id: str):
        return self._catalogue.get(track_id)

    def get_user(self, user_id: str):
        return self._users.get(user_id)

    def get_artist(self, artist_id: str):
        return self._artists.get(artist_id)

    def get_album(self, album_id: str):
        return self._albums.get(album_id)

    def all_users(self):
        return list(self._users.values())

    def all_tracks(self):
        return list(self._catalogue.values())

    """
    Loops throughs all sessions and adds up the listening minutes of each session
    """
    def total_listening_time_minutes(self, start: datetime, end: datetime):
        total_seconds = 0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60

    """
    Look at only premium users, count how many distinct tracks each of them streamed in the last N days, then return the average number of unique tracks per premium user or 0 if there are none.
    """
    def avg_unique_tracks_per_premium_user(self, days: int = 30):
        from_date = datetime.now() - timedelta(days=days)
        premium_users = [
            user for user in self.all_users() if isinstance(user, PremiumUser)
        ]

        if not premium_users:
            return 0.0

        total_unique = 0
        for user in premium_users:
            seen = set()
            for s in self._sessions:
                if s.timestamp >= from_date and s.user == user:
                    seen.add(s.track.track_id)
            total_unique += len(seen)

        return total_unique / len(premium_users)

    """
    Creates a dictionary mapping each track to user ids that listened to it, returning the tracks whose set is the larget and none is there is no session
    """
    def track_with_most_distinct_listeners(self):
        if not self._sessions:
            return None

        listeners = {}

        for session in self._sessions:
            track_id = session.track.track_id
            user_id = session.user.user_id

            if track_id not in listeners:
                listeners[track_id] = set()

            listeners[track_id].add(user_id)

        best_track_id = None
        max_count = 0

        for track_id, users in listeners.items():
            if len(users) > max_count:
                max_count = len(users)
                best_track_id = track_id

        return self._catalogue.get(best_track_id)

    """
    Group listening sessions by user type calculates the average session length for each group and return them ranked from longest to shortest.
    """
    def avg_session_duration_by_user_type(self):
        if not self._sessions:
            return []

        groups = {}

        for session in self._sessions:
            type_name = type(session.user).__name__

            if type_name not in groups:
                groups[type_name] = []

            groups[type_name].append(session.duration_listened_seconds)

        averages = []

        for type_name, durations in groups.items():
            avg = sum(durations) / len(durations)
            averages.append((type_name, avg))

        averages.sort(key=lambda x: x[1], reverse=True)
        return averages

    """
    Iterates through the users keeping only FamilyMember instances that also fit the age_threshold and then sums up their session duration converted to minutes, it returns 0.0 if no macthing users or sessions exist
    """
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18):
        total_seconds = 0

        for session in self._sessions:
            user = session.user
            if isinstance(user, FamilyMember) and user.age < age_threshold:
                total_seconds += session.duration_listened_seconds

        return total_seconds / 60

    """
    Iterates through sessions, counting only where the tracks is a Song/AlbumTrack (containing an Artist attribute) and counts the total listening minutes per artists then its sorts them in descending order and returns a tuple containing (Artist, Minutes)
    """
    def top_artists_by_listening_time(self, n: int = 5):
        artist_listening_time = {}

        for session in self._sessions:
            if not isinstance(session.track, Song):
                continue

            artist = session.track.artist
            minutes = session.duration_listened_minutes()

            if artist not in artist_listening_time:
                artist_listening_time[artist] = 0.0
            artist_listening_time[artist] += minutes

        results = list(artist_listening_time.items())
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:n]

    """
    Searches the user by the user id, if none is found or the user doesn't have sessions the function returns None, if eyes then it find the genre with highest total listening time and returns a tuple of (genre, percentage_of_time_listened)
    """
    def user_top_genre(self, user_id: str):
        user = self._users.get(user_id)

        if not user or not user.sessions:
            return None

        genre_times = {}

        for session in user.sessions:
            genre = session.track.genre

            if genre not in genre_times:
                genre_times[genre] = 0

            genre_times[genre] += session.duration_listened_seconds

        top_genre = None
        max_time = 0

        for genre, seconds in genre_times.items():
            if seconds > max_time:
                max_time = seconds
                top_genre = genre

        total_seconds = sum(genre_times.values())
        percentage = (max_time / total_seconds) * 100

        return (top_genre, percentage)

    """
    Iterates through playlists, keeping track only of CollaborativePlaylist instacnes and for each one counts the distinc artists. It returns playlists where the artist count exceeds the threshold
    """
    def collaborative_playlists_with_many_artists(self, threshold: int = 3):
        result = []

        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artist_ids = set()

                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artist_ids.add(track.artist.artist_id)

                if len(artist_ids) > threshold:
                    result.append(playlist)

        return result

    """
    Calculate the average number of tracks separately for regular playlists and collaborative playlists returning both averages in a dictionary.
    """
    def avg_tracks_per_playlist_type(self):
        standard = []
        collaborative = []

        for playlist in self._playlists.values():
            if type(playlist) is Playlist:
                standard.append(playlist)
            elif isinstance(playlist, CollaborativePlaylist):
                collaborative.append(playlist)

        def average(playlists):
            if not playlists:
                return 0.0
            total = sum(len(p.tracks) for p in playlists)
            return total / len(playlists)

        return {
            "Playlist": average(standard),
            "CollaborativePlaylist": average(collaborative),
        }

    """
    Iterate through the users and collect every track they have listened to, then check which albums they have listened to. Returns a list of users paired with the album titles they completed (User, [albums])
    """
    def users_who_completed_albums(self):
        result = []

        for user in self._users.values():
            listened_track_ids = set()

            for session in user.sessions:
                listened_track_ids.add(session.track.track_id)

            completed_albums = []

            for album in self._albums.values():
                if not album.tracks:
                    continue

                if album.track_ids().issubset(listened_track_ids):
                    completed_albums.append(album.title)

            if completed_albums:
                result.append((user, completed_albums))

        return result
