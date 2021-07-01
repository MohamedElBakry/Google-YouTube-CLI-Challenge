"""A video player class."""

from random import randint
from .video_library import VideoLibrary
from .playlist_library import PlaylistLibrary


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlist_library = PlaylistLibrary()
        self._current_video = None
        self._current_state = None

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        # Sort videos by 'lexicographical' (dictionary) order of the video titles
        videos = self._video_library.get_all_videos()
        for video in sorted(videos, key=lambda v: v.title):
            print(video)    # Uses overloaded __str__ to nicely print the video's information

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot play video: Video does not exist")
            return

        if self._current_state != "STOPPED" and self._current_state is not None:
            self.stop_video()

        if video.is_flagged:
            print(f"Cannot play video: Video is currently flagged (reason: {video.flag_reason})")
            return

        print(f"Playing video: {video.title}")
        self._current_video = video
        self._current_state = "PLAYING"

    def stop_video(self):
        """Stops the current video."""
        if self._current_state == "STOPPED" or self._current_video is None:
            print("Cannot stop video: No video is currently playing")
            return

        print(f"Stopping video: {self._current_video.title}")
        self._current_state = "STOPPED"

    def play_random_video(self):
        """Plays a random video from the video library."""
        allowed_videos = [video for video in self._video_library.get_all_videos() if not video.is_flagged]
        num_videos = len(allowed_videos)
        if num_videos == 0:
            print("No videos available")
            return

        # num_videos - 1 because randint is inclusive, so we can avoid an IndexError
        random_index = randint(0, num_videos - 1)
        video_id = allowed_videos[random_index].video_id
        self.play_video(video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self._current_state == "STOPPED" or self._current_video is None:
            print("Cannot pause video: No video is currently playing")

        elif self._current_state == "PAUSED":
            print(f"Video already paused: {self._current_video.title}")

        else:
            print(f"Pausing video: {self._current_video.title}")
            self._current_state = "PAUSED"

    def continue_video(self):
        """Resumes playing the current video."""
        if self._current_state == "STOPPED" or self._current_video is None:
            print("Cannot continue video: No video is currently playing")

        elif self._current_state != "PAUSED":
            print("Cannot continue video: Video is not paused")

        else:
            print(f"Continuing video: {self._current_video.title}")
            self._current_state = "PLAYING"

    def show_playing(self):
        """Displays video currently playing."""
        if self._current_state == "STOPPED" or self._current_video is None:
            print("No video is currently playing")
            return

        video = self._current_video
        playing_status = f"Currently playing: {video}"

        if self._current_state == "PAUSED":
            playing_status += " - PAUSED"

        print(playing_status)

    def create_playlist(self, playlist_name: str):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self._playlist_library.get_playlist(playlist_name) is not None:
            print("Cannot create playlist: A playlist with the same name already exists")
            return

        self._playlist_library.add_playlist(playlist_name)
        print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        # TODO: maybe make separate starting warning template of "Cannot add video to playlist"
        # Playlist exists?
        warning_message_template = f"Cannot add video to {playlist_name}: %s does not exist"
        playlist = self._playlist_library.get_playlist(playlist_name)
        if playlist is None:
            print(warning_message_template % "Playlist")
            return

        # Video exists?
        video = self._video_library.get_video(video_id)
        if video is None:
            print(warning_message_template % "Video")

        # No duplicate videos
        elif video_id in playlist.video_ids:
            print(f"Cannot add video to {playlist_name}: Video already added")
        elif video.is_flagged:
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flag_reason})")
        else:
            playlist.video_ids.append(video_id)
            print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""
        num_playlists = len(self._playlist_library.playlists)
        if num_playlists == 0:
            print("No playlists exist yet")
            return

        print("Showing all playlists:")
        # Sort the playlist by the key/item[0] (which is the playlist's name)
        sorted_playlists = dict(sorted(self._playlist_library.playlists.items(), key=lambda item: item[0]))
        for playlist in sorted_playlists.values():
            print(playlist.name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlist = self._playlist_library.get_playlist(playlist_name)
        if playlist is None:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return

        print(f"Showing playlist: {playlist_name}")
        if len(playlist.video_ids) == 0:
            print(f"No videos here yet")
            return

        for video_id in playlist.video_ids:
            video = self._video_library.get_video(video_id)
            print(video)

    def remove_from_playlist(self, playlist_name: str, video_id: str):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        # Playlist exists?
        playlist = self._playlist_library.get_playlist(playlist_name)
        if playlist is None:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return

        # Video exists?
        video = self._video_library.get_video(video_id)
        if video is None:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")

        # Video in playlist?
        elif video_id not in playlist.video_ids:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

        # Success
        else:
            playlist.video_ids.remove(video_id)
            print(f"Removed video from {playlist_name}: {video.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlist_library.get_playlist(playlist_name)
        if playlist is None:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return

        playlist.video_ids.clear()
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self._playlist_library.get_playlist(playlist_name) is None:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return

        self._playlist_library.remove_playlist(playlist_name)
        print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        self._search("title", search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        self._search("tags", video_tag)

    def _search(self, video_attribute, search_term):
        """Dynamically searches for and displays all the videos whose attribute contains the search_term.

        Args:
            search_term: The query to be used in search.
        """
        search_results_num = 0
        videos = sorted(self._video_library.get_all_videos(), key=lambda v: v.title)
        search_results_video_ids = []
        results_str = ""
        for video in videos:
            searched_attribute = getattr(video, video_attribute)
            if type(searched_attribute) is str:     # If true, the attribute is a search term, and not a video tag
                searched_attribute = searched_attribute.lower()
            elif type(searched_attribute) is dict and searched_attribute:
                searched_attribute = list(map(str.lower, searched_attribute))

            if not video.is_flagged and search_term.lower() in searched_attribute:      # Display allowed, search-matched videos
                search_results_num += 1
                search_results_video_ids.append(video.video_id)
                results_str += f"{search_results_num}) {video}\n"

        if search_results_num == 0 or (search_term[0] != "#" and video_attribute == "tags"):
            print(f"No search results for {search_term}")
            return

        print(f"Here are the results for {search_term}:\n{results_str}", end="")
        try:
            # The assertion fails when the strings below are printed through input
            # So, they are individually printed, then the input is captured
            print("Would you like to play any of the above? If yes, specify the number of the video."
                  "\nIf your answer is not a valid number, we will assume it's a no.")
            inputted_video_number = int(input())
        except ValueError:
            return

        if inputted_video_number <= search_results_num:
            video_id = search_results_video_ids[inputted_video_number - 1]
            self.play_video(video_id)


    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        # Video exists?
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot flag video: Video does not exist")

        # Video already flagged?
        elif video.is_flagged:
            print("Cannot flag video: Video is already flagged")

        # Flag the video
        else:
            video.flag_reason = flag_reason
            video.is_flagged = True
            # Stop the video if it's playing or paused
            if (self._current_state == "PLAYING" or self._current_state == "PAUSED") and self._current_video.video_id == video.video_id:
                self.stop_video()

            print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        # Video exists?
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot remove flag from video: Video does not exist")

        # Video is not flagged?
        elif not video.is_flagged:
            print("Cannot remove flag from video: Video is not flagged")

        else:
            video.is_flagged = False
            print(f"Successfully removed flag from video: {video.title}")
