import typing


class Measurement(typing.NamedTuple):
    

class Tracker:
    def __init__(self, filter, track_associator):
        self.filter = filter
        self.track_associator = track_associator

    def update(self, measurements: typing.List[Measurement]):

