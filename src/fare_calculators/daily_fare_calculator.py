from __future__ import absolute_import

from .fare import Fare
from utils.logger import logger
from ..journey import DailyJourney

from utils.logger import logger

logger = logger('INFO', __name__)


class DailyFareCalculator(Fare):
    """A Fare Calculator Class for Tiger Card."""

    def __init__(self):
        super().__init__()

    def __calculate_day_fare(self, journey: list, total_fare: int) -> int:
        """A __calculate_fare private method day - Use case 1.

        Args:
            journey (list): [day, time, from zone, to zone]
            total_fare (int): fare calculated till previous journies
        """

        try:
            # * Extracting journey part
            day, time, from_z, to_z = DailyJourney(
                journey).get_journey_parts()

            # * Finding the peak price applicablity
            peak_price_applicable = False
            peak_slots = self.peak_hours[day]
            for slot in peak_slots:
                if time > slot[0] and time < slot[1]:
                    peak_price_applicable = True

            # * finding the peak/non_peak hour price
            if from_z == to_z:
                # * Check for daily capping
                if total_fare > self.zone_price[from_z][self.CAPTURE_DAY_CAPPING]:
                    return self.DEFAULT_CAPPING_FARE
                return self.zone_price[from_z][peak_price_applicable]
            else:
                cross_zone_1 = from_z * 10 + to_z  # * 12
                cross_zone_2 = to_z * 10 + from_z  # * 21
                cross_zone = min(cross_zone_1, cross_zone_2)  # * 12

                # * Check for daily capping
                if total_fare > self.zone_price[cross_zone][self.CAPTURE_DAY_CAPPING]:
                    return self.DEFAULT_CAPPING_FARE
                return self.zone_price[cross_zone][peak_price_applicable]

        except Exception as error:
            raise error

    def get_day_fare(self, journies: list) -> int:
        try:
            logger.info('## journies: %s', journies)
            total_fare = 0
            for journey in journies:
                total_fare += self.__calculate_day_fare(journey, total_fare)
            logger.info(
                '## Total consolidated fare for the above journies: %s', total_fare)
            return total_fare
        except Exception as error:
            logger.exception(error)
            raise error


if __name__ == '__main__':
    fc = FareCalculator()
    fc.get_day_fare([['Monday', 10.45, 1, 1], ['Saturday',
                                               16.15, 1, 2], ['Sunday', 18.15, 2, 1]])
