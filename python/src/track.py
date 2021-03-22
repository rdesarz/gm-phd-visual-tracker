import typing
import numpy as np


class ImageFrame(typing.NamedTuple):
    image: np.ndarray
    width: int
    height: int


class TrackState(typing.NamedTuple):
    x: float
    y: float
    x_dot: float
    y_dot: float
    width: int
    height: int

    def position(self):
        return np.array([self.x, self.y])


class Track(typing.NamedTuple):
    state: TrackState
    frame: ImageFrame


class MeasurementState(typing.NamedTuple):
    x: float
    y: float
    width: int
    height: int

    def position(self):
        return np.array([self.x, self.y])


class Measurement(typing.NamedTuple):
    state: MeasurementState
    frame: ImageFrame


def compute_spatio_temporal_cost(track: Track, measurement: Measurement) -> float:
    """
    Compute spatio-temporal cost between a track and a new measurement as a normalized Euclidian distance (normalized
    by width and height of the image frame)
    :param track:
    :param measurement:
    :return: cost
    """
    return np.linalg.norm((track.state.position() - measurement.state.position()) * np.array(
        [1. / track.frame.width, 1. / track.frame.height]))


def compute_total_cost(track: Track, measurement: Measurement) -> float:
    """
    Compute total association cost between a track and a new measurement (spatio-temporal + visual cost)
    :param track:
    :param measurement:
    :return:
    """
    return compute_spatio_temporal_cost(track, measurement)


def compute_cost_matrix(tracks: typing.List[Track], measurements: typing.List[Measurement]) -> np.ndarray:
    """
    For each pair of track and measurement, compute the associated cost and return the associated matrix
    :param tracks: tracks
    :param measurements: measurement
    """
    cost_matrix = np.empty((len(tracks), len(measurements)))
    for track_index, track in enumerate(tracks):
        for measurement_index, measurement in enumerate(measurements):
            cost_matrix[track_index][measurement_index] = compute_total_cost(track, measurement)

    return cost_matrix
