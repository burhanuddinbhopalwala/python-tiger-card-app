from __future__ import absolute_import

from .fare import Fare
from ..zone import ZipCode
from utils.logger import logger
from ..journey import DailyJourney

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
                total_fare += self.zone_price[from_z][peak_price_applicable]
                logger.debug(
                    f'## Current total_fare  {total_fare} before travelling #{from_z}-#{to_z}')
                logger.debug(
                    f'Capping for zone #{from_z}-#{to_z} is #{self.zone_price[from_z][self.CAPTURE_DAY_CAPPING]}')
                if total_fare > self.zone_price[from_z][self.CAPTURE_DAY_CAPPING]:
                    total_fare -= self.zone_price[from_z][peak_price_applicable]
                    total_fare += self.DEFAULT_CAPPING_FARE
                logger.debug(f'Final total fare after travelling zone #{from_z}-#{to_z} {total_fare}')
                return total_fare
            else:
                zipcode = ZipCode().get_journey_zipcode(from_z, to_z)

                # * Check for daily capping
                logger.debug(
                    f'## Current total_fare  {total_fare} before travelling #{from_z}-#{to_z}')
                logger.debug(
                    f'Capping for zone #{from_z}-#{to_z} is #{self.zone_price[zipcode][self.CAPTURE_DAY_CAPPING]}')
                total_fare += self.zone_price[zipcode][peak_price_applicable]
                if total_fare > self.zone_price[zipcode][self.CAPTURE_DAY_CAPPING]:
                    total_fare -= self.zone_price[zipcode][peak_price_applicable]
                    total_fare += self.DEFAULT_CAPPING_FARE
                logger.debug(f'Final total fare after travelling zone #{from_z}-#{to_z} {total_fare}')
                return total_fare

        except Exception as error:
            raise error

    def get_day_fare(self, journies: list) -> int:
        try:
            logger.info('## journies: %s', journies)
            total_fare = 0
            for journey in journies:
                total_fare = self.__calculate_day_fare(journey, total_fare)
            logger.info(
                '## Total consolidated fare for the above journies: %s', total_fare)
            return total_fare
        except Exception as error:
            logger.exception(error.message)
            raise error


# if __name__ == '__main__':
#     fc = FareCalculator()
#     fc.get_day_fare([['Monday', 10.45, 1, 1], ['Saturday',
#                                                16.15, 1, 2], ['Sunday', 18.15, 2, 1]])
