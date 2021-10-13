from ..zone import Zone


class Fare(object):
    """A Fare Calculator Class for Tiger Card."""

    def __init__(self):
        self.peak_hours = {
            # * Day key: [[slots list in 24 hours format]]
            'monday': [[7, 10.3], [17, 20]],
            'tuesday': [[7, 10.3], [17, 20]],
            'wednesday': [[7, 10.3], [17, 20]],
            'thursday': [[7, 10.3], [17, 20]],
            'friday': [[7, 10.3], [17, 20]],
            'saturday': [[9, 11], [18, 22]],
            'sunday': [[9, 11], [18, 22]]
        }

        self.zone_price = {
            # * Zone.x : [non_peak_price - 0, peak_price - 1, day_capping - 2, weekly_capping - 3]
            Zone.one.value: [25, 30, 100, 500],
            Zone.two.value: [20, 25, 80, 400],
            # * Cross zones prices based on zipcode
            Zone.one.value * 1000 + Zone.two.value: [30, 35, 120, 600]
        }

        self.DEFAULT_CAPPING_FARE = 5
        self.CAPTURE_DAY_CAPPING = 2
        self.CAPTURE_WEEKLY_CAPPING = 3
