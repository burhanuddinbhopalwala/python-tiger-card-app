# importing enum for enumerations
import enum


class Zone(enum.Enum):
    one = 1
    two = 2
    maximum = 999  # * Soft limit

    # * TODO: Add zone here.


class ZipCode(object):
    def __init__(self):
        pass

    def get_journey_zipcode(self, from_z: int, to_z: int):
        if from_z == to_z:
            return from_z

        cross_zone_1 = from_z * (Zone.maximum.value + 1) + to_z  # * 12
        cross_zone_2 = to_z * (Zone.maximum.value + 1) + from_z  # * 21
        cross_zipcode = min(cross_zone_1, cross_zone_2)  # * 12
        return cross_zipcode

        # * Note: As per the above logic maxm zone can be available
