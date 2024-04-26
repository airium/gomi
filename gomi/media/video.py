from __future__ import annotations

__all__ = ["gvfc", "get_video_framecount"]

from .mediainfo import getMediaInfo


def get_video_framecount(path) -> int:
    for track in getMediaInfo(path).video_tracks:
        return int(getattr(track, "frame_count", 0))
    return 0


getVID_FC = get_video_framecount
