from __future__ import absolute_import

from .fare import Fare
from ..zone import ZipCode
from utils.logger import logger
from ..journey import WeeklyJourney
from utils.util import chunk_generator

logger = logger('INFO', __name__)


class WeeklyFareCalculator(Fare):
    """A Fare Calculator Class for Tiger Card."""

    def __init__(self):
        super().__init__()

    def __calculate_weekly_fare(self, journey: list, total_fare: int, week_capped: bool, longest_route: int) -> list:
        """A __calculate_fare private method weekly - Use case 2.

        Args:
            journey (list): [day, day_fare, from zone, to zone]
            total_fare (int): fare calculated till previous journies
        """

        try:
            if week_capped:
                return [total_fare, week_capped]

            day_final_fare = 0
            # * Extracting day journey part
            day, day_fare, from_z, to_z = WeeklyJourney(
                journey).get_journey_parts()

            # * Check for day capping
            if from_z == to_z:
                # * Check for the longest route for daily capping
                if longest_route == 0:
                    longest_route = from_z

                # * Check for daily capping
                if day_fare > self.zone_price[from_z][self.CAPTURE_DAY_CAPPING]:
                    day_final_fare = self.zone_price[from_z][self.CAPTURE_DAY_CAPPING]
                day_final_fare = day_fare

                if total_fare + day_final_fare > self.zone_price[longest_route][self.CAPTURE_WEEKLY_CAPPING]:
                    return [self.zone_price[longest_route][self.CAPTURE_WEEKLY_CAPPING], True, longest_route]
                else:
                    logger.debug(
                        f'{day} total_fare {total_fare} day_final_fare {day_final_fare} add {total_fare + day_final_fare}')
                    return [total_fare + day_final_fare, False, longest_route]
            else:
                zipcode = ZipCode().get_journey_zipcode(from_z, to_z)

                # * Check for the longest route for daily capping
                if any([longest_route == 0, zipcode > longest_route]):
                    longest_route = zipcode

                # * Check for daily capping
                if day_fare > self.zone_price[zipcode][self.CAPTURE_DAY_CAPPING]:
                    day_final_fare = self.zone_price[zipcode][self.CAPTURE_DAY_CAPPING]
                day_final_fare = day_fare

                if total_fare + day_final_fare > self.zone_price[longest_route][self.CAPTURE_WEEKLY_CAPPING]:
                    return [self.zone_price[longest_route][self.CAPTURE_WEEKLY_CAPPING], True, longest_route]
                else:
                    logger.debug(
                        f'{day} before total_fare {total_fare} after {total_fare + day_final_fare}')
                    return [total_fare + day_final_fare, False, longest_route]
        except Exception as error:
            raise error

    def get_weekly_fare(self, journies: list) -> int:
        try:
            logger.info('## daily journies: %s', journies)
            total_fare = 0  # * Across all the weeks
            weekly_journies = list(chunk_generator(journies, 7))
            # pdb.set_trace()
            logger.debug(f'## Weekly journies split {weekly_journies}')

            for week_chunk in weekly_journies:
                weekly_fare = 0
                longest_route = 0
                week_capped = False  # * Tracking if the week capping for any zipcode is reached or not.
                for journey in week_chunk:
                    weekly_fare, week_capped, longest_route = self.__calculate_weekly_fare(journey, weekly_fare, week_capped, longest_route)
                logger.info(
                    '## Total weekly consolidated fare for the above journies: %s', weekly_fare)
                total_fare += weekly_fare
            return total_fare
        except Exception as error:
            logger.exception(error)
            raise error
