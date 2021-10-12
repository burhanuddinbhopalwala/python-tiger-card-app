from __future__ import absolute_import

from .fare import Fare
from ..zone import ZipCode
from utils.logger import logger
from ..journey import WeeklyJourney

logger = logger('INFO', __name__)


class WeeklyFareCalculator(Fare):
    """A Fare Calculator Class for Tiger Card."""

    def __init__(self):
        super().__init__()

    def __calculate_weekly_fare(self, journey: list, total_fare: int) -> int:
        """A __calculate_fare private method weekly - Use case 2.

        Args:
            journey (list): [day, day_fare, from zone, to zone]
            total_fare (int): fare calculated till previous journies
        """

        try:
            day_final_fare = 0
            # * Extracting day journey part
            day, day_fare, from_z, to_z = WeeklyJourney(
                journey).get_journey_parts()

            # * Weekly capping pass...
            if total_fare >= self.zone_price[from_z][self.CAPTURE_WEEKLY_CAPPING]:
                return total_fare

            # * Check for day capping
            if from_z == to_z:
                # * Check for daily capping
                if day_fare > self.zone_price[from_z][self.CAPTURE_DAY_CAPPING]:
                    day_final_fare = self.zone_price[from_z][self.CAPTURE_DAY_CAPPING]
                day_final_fare = day_fare

                if total_fare + day_final_fare > self.zone_price[from_z][self.CAPTURE_WEEKLY_CAPPING]:
                    return self.zone_price[from_z][self.CAPTURE_WEEKLY_CAPPING]
                else:
                    return total_fare + day_final_fare
            else:
                zipcode = ZipCode().get_journey_zipcode(from_z, to_z)

                # * Check for daily capping
                if day_fare > self.zone_price[zipcode][self.CAPTURE_DAY_CAPPING]:
                    day_final_fare = self.zone_price[zipcode][self.CAPTURE_DAY_CAPPING]
                day_final_fare = day_fare

                if total_fare + day_final_fare > self.zone_price[zipcode][self.CAPTURE_WEEKLY_CAPPING]:
                    return self.zone_price[zipcode][self.CAPTURE_WEEKLY_CAPPING]
                else:
                    return total_fare + day_final_fare
        except Exception as error:
            raise error

    def get_weekly_fare(self, journies: list) -> int:
        try:
            logger.info('## daily journies: %s', journies)
            total_fare = 0
            for journey in journies:
                total_fare = self.__calculate_weekly_fare(journey, total_fare)
            logger.info(
                '## Total weekly consolidated fare for the above journies: %s', total_fare)
            return total_fare
        except Exception as error:
            logger.exception(error)
            raise error
