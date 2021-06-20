from abc import ABC, abstractmethod

import numpy as np
import typing


class MultipleTargetFilter(ABC):
    @abstractmethod
    def predict(self, delta_t):
        pass

    @abstractmethod
    def update(self, measurements):
        pass

    @abstractmethod
    def get_filtered_objects(self) -> typing.Tuple[np.ndarray, np.ndarray]:
        """
        Return list of filtered targets. One estimate is defined by its state vector and its covariance matrix.
        """
        pass

    @abstractmethod
    def get_measurement_matrix(self):
        """
        Return the current measurement matrix.
        """
        pass

    @abstractmethod
    def get_process_noise_matrix(self):
        """
        Return the current process noise matrix.
        """
        pass
