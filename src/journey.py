class InvalidJourney(Exception):
    pass


class DailyJourney(object):
    """A journey class - Use case 1."""

    # * TODO: getter and setter approach should be taken.
    def __init__(self, journey: list):
        try:
            self.day = str(journey[0]).lower()
            self.time = float(journey[1])
            self.from_z = int(journey[2])
            self.to_z = int(journey[3])
        except Exception as error:
            raise InvalidJourney(error)

    def get_journey_parts(self) -> list:
        """Reuturns journey parts."""
        return [self.day, self.time, self.from_z, self.to_z]


class WeeklyJourney(object):
    """A journey class with all daily consolidated s- use case 2."""

    # * TODO: getter and setter approach should be taken.
    def __init__(self, journey: list):
        try:
            self.day = str(journey[0]).lower()
            self.day_fare = float(journey[1])
            self.from_z = int(journey[2])
            self.to_z = int(journey[3])
        except Exception as error:
            raise InvalidJourney(error)

    def get_journey_parts(self) -> list:
        """Reuturns journey parts."""
        return [self.day, self.day_fare, self.from_z, self.to_z]
