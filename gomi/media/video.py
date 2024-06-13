from __future__ import annotations

__all__ = ["getVID_FC", "get_video_framecount", "get_video_frame_rate", "get_video_time_length"]

from .mediainfo import getMediaInfo


def get_video_framecount(path) -> int:
    for track in getMediaInfo(path).video_tracks:
        return int(getattr(track, "frame_count", 0))
    return 0


def get_video_frame_rate(path) -> float:
    for track in getMediaInfo(path).video_tracks:
        return float(getattr(track, "frame_rate", 0))
    return 0.0


def get_video_time_length(path) -> float:
    for track in getMediaInfo(path).video_tracks:
        return float(getattr(track, "duration", 0))
    return 0.0


getVID_FC = get_video_framecount
