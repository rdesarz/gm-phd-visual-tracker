import dataclasses
import datetime
import typing

import numpy as np


class ImageFrame(typing.NamedTuple):
    """Stores an image with metadata (width and height)"""
    image: np.ndarray
    width: int
    height: int


class TrackState(typing.NamedTuple):
    """Stores the state of a track"""
    x: float
    y: float
    x_dot: float
    y_dot: float
    width: int
    height: int

    def position(self) -> np.ndarray:
        """
        Return the position of the track in image frame as an array.
        """
        return np.array([self.x, self.y])


class TrackFrame(typing.NamedTuple):
    timestamp: datetime.datetime
    image: ImageFrame
    state: TrackState


@dataclasses
class Track:
    """Track of an object in video stream"""
    id: int
    frames: typing.List[TrackFrame]
    unassigned_nb_steps: float
    measurement: np.ndarray
    process_noise: np.ndarray
    covariance: np.ndarray
