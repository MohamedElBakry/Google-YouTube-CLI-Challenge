"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)

        # Keeps track of if this video is flagged, and the reasoning for it
        self._is_flagged = False
        self._flag_reason = None

    def __str__(self):
        """Returns the a string of the Video object formatted in a friendly and readable way."""
        tags = " ".join(self._tags)
        video_info = f"{self._title} ({self._video_id}) [{tags}]"
        if self._is_flagged:
            video_info += f" - FLAGGED (reason: {self._flag_reason})"
        return video_info

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    @property
    def is_flagged(self) -> bool:
        """Returns whether the video is flagged."""
        return self._is_flagged

    @is_flagged.setter
    def is_flagged(self, value: bool):
        """Sets the value of is_flagged."""
        self._is_flagged = value

    @property
    def flag_reason(self) -> str or None:
        """Returns the flag reason of a video."""
        return self._flag_reason

    @flag_reason.setter
    def flag_reason(self, value: str or None):
        """Sets the value of the video's flag reason."""
        self._flag_reason = value
