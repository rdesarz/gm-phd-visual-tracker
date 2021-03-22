import unittest
from scipy.optimize import linear_sum_assignment
import numpy as np

from python.src.track import compute_cost_matrix, Track, Measurement, ImageFrame, MeasurementState, TrackState, \
    compute_spatio_temporal_cost


def make_empty_frame(width: int, height: int) -> ImageFrame:
    return ImageFrame(image=np.array([]), width=width, height=height)


def make_no_speed_track_state(x: float, y: float, width: int, height: int) -> TrackState:
    return TrackState(x=x, y=y, width=width, height=height, x_dot=0., y_dot=0.)


class TracksTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_measurement = Measurement(state=MeasurementState(x=4., y=6., width=10, height=10),
                                            frame=make_empty_frame(100, 100))

        self.mock_track = Track(state=make_no_speed_track_state(x=4., y=6., width=10, height=10),
                                frame=make_empty_frame(100, 100))

    def test_compute_spatio_temporal_cost_same_measurement_and_track(self):
        self.assertAlmostEqual(compute_spatio_temporal_cost(self.mock_track, self.mock_measurement), 0.)

    def test_linear_sum_assignment(self):
        cost_matrix = np.array([[1., 2., 3.],
                                [2., 2., 3.],
                                [1., 4., 6.]])

        row_ind, col_ind = linear_sum_assignment(cost_matrix, maximize=True)

        if __name__ == '__main__':
            unittest.main()
