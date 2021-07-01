"""A playlist library class."""

from typing import Dict
from .video_playlist import Playlist


class PlaylistLibrary:
    """ A class used to represent a Playlist Library."""
    def __init__(self):
        self._playlists = {}  # A dict of lowercase playlist keys mapping to playlist objects
        # that also contains the true name of the playlist

    @property
    def playlists(self) -> dict:
        """Returns the stored playlists."""
        return self._playlists

    def get_playlist(self, playlist_name) -> Playlist:
        """Returns a named playlist, None if not found."""
        return self._playlists.get(playlist_name.lower(), None)

    def add_playlist(self, playlist_name):
        """Adds a playlist."""
        self._playlists[playlist_name.lower()] = Playlist(playlist_name)

    def remove_playlist(self, playlist_name) -> Playlist:
        """Removes a named playlist. Optionally, you may use the returned popped value."""
        return self._playlists.pop(playlist_name.lower())
