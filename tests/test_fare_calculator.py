from __future__ import absolute_import

import pytest
import unittest

from utils.logger import logger
from src.fare_calculators.daily_fare_calculator import DailyFareCalculator
from src.fare_calculators.weekly_fare_calculator import WeeklyFareCalculator

logger = logger('INFO', __name__)


@pytest.mark.integrationtest
class TestJourneyFare(unittest.TestCase):
    """A class to test journey list fare of a Tiger Card customer."""

    def setUp(self):
        # * Daily journies - Use Case 1
        self.test_day_journies = [['Monday', 10.20, 2, 1], ['Monday', 10.45, 1, 1],
                                  ['Monday', 16.15, 1, 1], ['Monday', 18.15, 1, 1], ['Monday', 19.00, 1, 2]]
        self.exact_day_fare = 120  # * Please refer  the feeback README.md

        # * Weekly journies - Use Case 2
        self.test_weekly_journies = [['Monday', 120, 1, 2], ['Tuesday', 120, 1, 2],
                                     ['Wednesday', 120, 1, 2], ['Thursday', 120, 1, 2], ['Friday', 80, 1, 1],
                                     ['Saturday', 40, 1, 2], ['Sunday', 40, 1, 2], ['Monday', 100, 1, 2]]
        self.exact_weekly_fare = 700  # * Please refer  the feeback README.md

        # * Use Case 3 (Each Journey test)
        self.test_day_journies = [['Monday', 10.20, 2, 1], ['Monday', 10.45, 1, 1],
                                  ['Monday', 16.15, 1, 1], ['Monday', 18.15, 1, 1], ['Monday', 19.00, 1, 2]]
        self.exact_day_fare = 120  # * Please refer  the feeback README.md

        self.exact_day_EACH_fare = [35, 25, 25, 30, 5, 120]
        # {'journey_#1': 35, 'journey_#2': 25, 'journey_#3': 25, 'journey_#4': 30, 'journey_#5': 5, 'total_fare': 120}

    @pytest.mark.dailyfaretest
    def test_day_journies_fare(self):
        test_fare = DailyFareCalculator().get_day_fare(self.test_day_journies)
        assert self.exact_day_fare == test_fare

    @pytest.mark.weeklyfaretest
    def test_weekly_journies_fare(self):
        test_fare = WeeklyFareCalculator().get_weekly_fare(self.test_weekly_journies)
        assert self.exact_weekly_fare == test_fare

    @pytest.mark.dailyfareEACHtest
    def test_day_journies_each_fare(self):
        test_fare = DailyFareCalculator().get_day_with_each_fare(self.test_day_journies)
        assert self.exact_day_EACH_fare == test_fare

    def tearDown(self):
        self.test_day_journies = None
        self.test_weekly_journies = None
