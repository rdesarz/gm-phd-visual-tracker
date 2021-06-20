import typing
import numpy as np
from scipy.optimize import linear_sum_assignment

from python.src.track import ImageFrame, Track


class EstimateState(typing.NamedTuple):
    x: float
    y: float
    width: int
    height: int

    def position(self):
        return np.array([self.x, self.y])


class Estimate(typing.NamedTuple):
    state: EstimateState
    covariance: np.ndarray
    frame: ImageFrame


class AssociatedTrackEstimate(typing.NamedTuple):
    track: Track
    estimate: Estimate
    association_cost: float


def compute_spatio_temporal_cost(track: Track, estimate: Estimate) -> float:
    """
    Compute spatio-temporal cost between a track and a new measurement as a normalized Euclidian distance (normalized
    by width and height of the image frame)
    :param track:
    :param estimate:
    :return: cost
    """
    return np.linalg.norm((track.state.position() - estimate.state.position()) * np.array(
        [1. / track.frame.width, 1. / track.frame.height]))


# TODO: compute visual cost
def compute_visual_cost(track: Track, estimate: Estimate) -> float:
    return 0.


def compute_visual_spatio_temporal_cost(track: Track, estimate: Estimate) -> float:
    """
    Compute total association cost between a track and a new measurement (spatio-temporal + visual cost)
    :param track:
    :param estimate:
    :return:
    """
    return compute_spatio_temporal_cost(track, estimate) + compute_visual_cost(track, estimate)


def compute_visual_spatio_temporal_cost_matrix(tracks: typing.List[Track],
                                               estimates: typing.List[Estimate]) -> np.ndarray:
    """
    For each pair of track and measurement, compute the associated cost and return the associated matrix
    :param tracks: tracks
    :param estimates: measurement
    """
    cost_matrix = np.empty((len(tracks), len(estimates)))
    for track_index, track in enumerate(tracks):
        for measurement_index, measurement in enumerate(estimates):
            cost_matrix[track_index][measurement_index] = compute_visual_spatio_temporal_cost(track, measurement)

    return cost_matrix


def hungarian_assignment(cost_matrix: np.ndarray):
    """

    :param cost_matrix: cost_matrix used for assignment
    :return:
    """
    return linear_sum_assignment(cost_matrix)


class TrackAssociator:
    def __init__(self, association_cost_threshold: float,
                 cost_matrix_computation_strategy: typing.Callable = compute_visual_spatio_temporal_cost_matrix,
                 assignment_strategy: typing.Callable = hungarian_assignment):
        """
        :param association_cost_threshold: threshold used to determine if an association is valid. The association is
            valid only if above this threshold.
        :param cost_matrix_computation_strategy: strategy to compute the cost matrix used for assignment. Default one is
        visual-spatiotemporal cost.
        :param assignment_strategy: strategy for assignment between tracks and estimates. Default is Hungarian algorithm.
        """
        self.cost_matrix_computation_strategy = cost_matrix_computation_strategy
        self.assignment_algorithm = assignment_strategy
        self.association_cost_threshold = association_cost_threshold

    def associate(self, tracks: typing.List[Track], estimates: typing.List[Estimate]) -> typing.Tuple[
        typing.List[AssociatedTrackEstimate], typing.List[Track], typing.List[Estimate]]:
        """
        Associates tracks and estimates based on the defined strategies
        :param tracks: list of tracks at time k-1
        :param estimates: list of estimates extracted from filter at time k
        :return: associated track and estimate, non-associated tracks and non-associated estimates
        """
        # Step 1: create set containing all tracks and estimates
        tracks_set = set(tracks)
        estimates_set = set(estimates)

        # Step 2: compute cost matrix used for assignment
        cost_matrix = self.cost_matrix_computation_strategy(tracks, estimates)

        # Step 3: get optimal assignment
        track_indices, estimate_indices = self.assignment_algorithm(cost_matrix)

        # Step 4: create track with existing assignment
        associated_tracks = []
        for track_index, estimate_index in zip(track_indices, estimate_indices):
            if cost_matrix[track_index][estimate_index] >= self.association_cost_threshold:
                associated_tracks.append(
                    AssociatedTrackEstimate(track=tracks[track_index], estimate=estimates[estimate_index],
                                            association_cost=cost_matrix[track_index][estimate_index]))

            tracks_set.remove(tracks[track_index])
            estimates_set.remove(estimates[estimate_index])

        unassigned_tracks = list(tracks_set)
        unassigned_estimates = list(estimates_set)

        return associated_tracks, unassigned_tracks, unassigned_estimates
