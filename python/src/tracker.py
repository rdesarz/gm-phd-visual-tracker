import datetime
import typing

import numpy as np

from python.src.multiple_target_filter import MultipleTargetFilter
from python.src.track import Track
from python.src.track_association import TrackAssociator


class BoundingBox(typing.NamedTuple):
    x: float
    y: float
    width: int
    height: int


class Detection(typing.NamedTuple):
    timestamp: datetime.datetime
    bounding_box: BoundingBox
    image: np.ndarray
    confidence_score: float


class Tracker:
    def __init__(self, filter: MultipleTargetFilter, track_associator):
        self.filter: MultipleTargetFilter = filter
        self.track_associator: TrackAssociator = track_associator
        self.tracks: typing.List[Track] = []
        # self.birth_model

    def processDetections(self, timestamp: datetime.datetime, detections: typing.List[Detection]):
        # Compute time delta between last update and current update
        # self.birth_model.update(detections)

        # Predict and update filter
        # self.filter.predict(delta_t)
        # self.filter.update(detections)

        # Compute estimates
        # estimates = [compute_estimate(target_state, target_covariance, detections[0].image) for
        #              target_state, target_covariance in filter.get_filtered_targets()]

        # Associate track with new estimates
        # associated_tracks, unassigned_tracks, unassigned_estimates = self.track_associator.associate(tracks, filtered_target)

        # Update tracks according to association. Keep measurement, covariance and process noise matrix if track is lost
        # at next update (To perform additional prediction step)
        # for association in associated_tracks:
        #     association.track.frames.append(
        #         TrackFrame(timestamp, association.estimate.state, association.estimate.frame))
        #     association.track.measurement = filter.get_measurement_matrix()
        #     association.track.process_noise = filter.get_process_noise_matrix()
        #     association.track.covariance = estimate.covariance

        # Perform additional prediction step for unassigned tracks
        # for track in unassigned_tracks:
        #     if track.unassigned_nb_steps < threshold:
        #         track.append(add_additional_track)
        #     else:
        #         self.tracks.remove(track)

        # Perform re-identification for unassigned estimates

        pass
