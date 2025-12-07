"""
Tests for F1 API integration module
"""

from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase, override_settings
from django.utils import timezone

from betting.f1_api import F1API, get_sample_f1_drivers, get_sample_f1_schedule


class TestGetSampleF1Drivers(TestCase):
    """Tests for get_sample_f1_drivers helper function"""

    def test_returns_list_of_drivers(self):
        """Should return a list of driver dictionaries"""
        drivers = get_sample_f1_drivers()
        self.assertIsInstance(drivers, list)
        self.assertGreater(len(drivers), 0)

    def test_returns_20_drivers(self):
        """Should return exactly 20 drivers (10 teams x 2)"""
        drivers = get_sample_f1_drivers()
        self.assertEqual(len(drivers), 20)

    def test_driver_has_required_fields(self):
        """Each driver should have number, first_name, last_name, team, nationality"""
        drivers = get_sample_f1_drivers()
        required_fields = ["number", "first_name", "last_name", "team", "nationality"]

        for driver in drivers:
            for field in required_fields:
                self.assertIn(field, driver, f"Driver missing field: {field}")

    def test_driver_numbers_are_unique(self):
        """All driver numbers should be unique"""
        drivers = get_sample_f1_drivers()
        numbers = [d["number"] for d in drivers]
        self.assertEqual(len(numbers), len(set(numbers)))

    def test_known_drivers_present(self):
        """Should include well-known drivers"""
        drivers = get_sample_f1_drivers()
        last_names = [d["last_name"] for d in drivers]

        self.assertIn("Verstappen", last_names)
        self.assertIn("Hamilton", last_names)
        self.assertIn("Leclerc", last_names)
        self.assertIn("Norris", last_names)


class TestGetSampleF1Schedule(TestCase):
    """Tests for get_sample_f1_schedule helper function"""

    def test_returns_list_of_races(self):
        """Should return a list of race dictionaries"""
        schedule = get_sample_f1_schedule()
        self.assertIsInstance(schedule, list)
        self.assertGreater(len(schedule), 0)

    def test_returns_24_races(self):
        """Should return 24 races for 2025 season"""
        schedule = get_sample_f1_schedule()
        self.assertEqual(len(schedule), 24)

    def test_race_has_required_fields(self):
        """Each race should have round, name, location, country, race_datetime, betting_deadline"""
        schedule = get_sample_f1_schedule()
        required_fields = [
            "round",
            "name",
            "location",
            "country",
            "race_datetime",
            "betting_deadline",
        ]

        for race in schedule:
            for field in required_fields:
                self.assertIn(field, race, f"Race missing field: {field}")

    def test_rounds_are_sequential(self):
        """Race rounds should be 1 through 24"""
        schedule = get_sample_f1_schedule()
        rounds = [r["round"] for r in schedule]
        self.assertEqual(rounds, list(range(1, 25)))

    def test_race_datetime_is_timezone_aware(self):
        """Race datetimes should be timezone-aware"""
        schedule = get_sample_f1_schedule()

        for race in schedule:
            self.assertTrue(
                timezone.is_aware(race["race_datetime"]),
                f"Race {race['name']} datetime is not timezone-aware",
            )

    def test_betting_deadline_before_race(self):
        """Betting deadline should be before race datetime"""
        schedule = get_sample_f1_schedule()

        for race in schedule:
            self.assertLess(
                race["betting_deadline"],
                race["race_datetime"],
                f"Race {race['name']} deadline is not before race time",
            )

    def test_betting_deadline_is_two_hours_before(self):
        """Betting deadline should be exactly 2 hours before race"""
        schedule = get_sample_f1_schedule()

        for race in schedule:
            expected_deadline = race["race_datetime"] - timezone.timedelta(hours=2)
            self.assertEqual(
                race["betting_deadline"],
                expected_deadline,
                f"Race {race['name']} deadline is not 2 hours before race",
            )

    def test_known_races_present(self):
        """Should include well-known races"""
        schedule = get_sample_f1_schedule()
        race_names = [r["name"] for r in schedule]

        self.assertIn("Monaco Grand Prix", race_names)
        self.assertIn("British Grand Prix", race_names)
        self.assertIn("Italian Grand Prix", race_names)


@override_settings(F1_API_BASE_URL="https://api.openf1.org/v1")
class TestF1APIInit(TestCase):
    """Tests for F1API initialization"""

    def test_init_sets_base_url(self):
        """Should set base_url from settings"""
        api = F1API()
        self.assertEqual(api.base_url, "https://api.openf1.org/v1")

    def test_init_creates_session(self):
        """Should create a requests session"""
        api = F1API()
        self.assertIsInstance(api.session, requests.Session)

    def test_init_sets_user_agent(self):
        """Should set User-Agent header"""
        api = F1API()
        self.assertEqual(api.session.headers["User-Agent"], "F1BettingPool/1.0")


@override_settings(F1_API_BASE_URL="https://api.openf1.org/v1")
class TestF1APIGetDrivers(TestCase):
    """Tests for F1API.get_drivers method"""

    def setUp(self):
        self.api = F1API()
        self.mock_drivers = [
            {"driver_number": 1, "first_name": "Max", "last_name": "Verstappen"},
            {"driver_number": 44, "first_name": "Lewis", "last_name": "Hamilton"},
        ]

    @patch.object(requests.Session, "get")
    def test_get_drivers_success(self, mock_get):
        """Should return driver data on successful API call"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_drivers
        mock_get.return_value = mock_response

        result = self.api.get_drivers(year=2024)

        self.assertEqual(result, self.mock_drivers)
        mock_get.assert_called_once()

    @patch.object(requests.Session, "get")
    def test_get_drivers_uses_correct_url(self, mock_get):
        """Should call correct API endpoint"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        self.api.get_drivers(year=2024)

        call_args = mock_get.call_args
        self.assertIn("/drivers", call_args[0][0])

    @patch.object(requests.Session, "get")
    def test_get_drivers_404_returns_none(self, mock_get):
        """Should return None on 404 response"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.api.get_drivers(year=2024)

        self.assertIsNone(result)

    @patch.object(requests.Session, "get")
    def test_get_drivers_500_returns_none(self, mock_get):
        """Should return None on 500 response"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.api.get_drivers(year=2024)

        self.assertIsNone(result)

    @patch.object(requests.Session, "get")
    def test_get_drivers_network_error_returns_none(self, mock_get):
        """Should return None on network error"""
        mock_get.side_effect = requests.RequestException("Connection failed")

        result = self.api.get_drivers(year=2024)

        self.assertIsNone(result)

    @patch.object(requests.Session, "get")
    def test_get_drivers_timeout_returns_none(self, mock_get):
        """Should return None on timeout"""
        mock_get.side_effect = requests.Timeout("Request timed out")

        result = self.api.get_drivers(year=2024)

        self.assertIsNone(result)


@override_settings(F1_API_BASE_URL="https://api.openf1.org/v1")
class TestF1APIGetRaceSchedule(TestCase):
    """Tests for F1API.get_race_schedule method"""

    def setUp(self):
        self.api = F1API()
        self.mock_schedule = [
            {"session_key": "2024_1", "session_name": "Bahrain Grand Prix"},
            {"session_key": "2024_2", "session_name": "Saudi Arabian Grand Prix"},
        ]

    @patch.object(requests.Session, "get")
    def test_get_race_schedule_success(self, mock_get):
        """Should return schedule data on successful API call"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_schedule
        mock_get.return_value = mock_response

        result = self.api.get_race_schedule(year=2024)

        self.assertEqual(result, self.mock_schedule)

    @patch.object(requests.Session, "get")
    def test_get_race_schedule_uses_correct_url(self, mock_get):
        """Should call correct API endpoint"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        self.api.get_race_schedule(year=2024)

        call_args = mock_get.call_args
        self.assertIn("/sessions", call_args[0][0])

    @patch.object(requests.Session, "get")
    def test_get_race_schedule_404_returns_none(self, mock_get):
        """Should return None on 404 response"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.api.get_race_schedule(year=2024)

        self.assertIsNone(result)

    @patch.object(requests.Session, "get")
    def test_get_race_schedule_network_error_returns_none(self, mock_get):
        """Should return None on network error"""
        mock_get.side_effect = requests.RequestException("Connection failed")

        result = self.api.get_race_schedule(year=2024)

        self.assertIsNone(result)


@override_settings(F1_API_BASE_URL="https://api.openf1.org/v1")
class TestF1APIGetRaceResults(TestCase):
    """Tests for F1API.get_race_results method"""

    def setUp(self):
        self.api = F1API()
        self.mock_results = [
            {"position": 1, "driver_number": 1},
            {"position": 2, "driver_number": 44},
        ]

    @patch.object(requests.Session, "get")
    def test_get_race_results_success(self, mock_get):
        """Should return results data on successful API call"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_results
        mock_get.return_value = mock_response

        result = self.api.get_race_results(session_key="2024_1")

        self.assertEqual(result, self.mock_results)

    @patch.object(requests.Session, "get")
    def test_get_race_results_uses_correct_url(self, mock_get):
        """Should call correct API endpoint"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        self.api.get_race_results(session_key="2024_1")

        call_args = mock_get.call_args
        self.assertIn("/position", call_args[0][0])

    @patch.object(requests.Session, "get")
    def test_get_race_results_404_returns_none(self, mock_get):
        """Should return None on 404 response"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.api.get_race_results(session_key="2024_1")

        self.assertIsNone(result)

    @patch.object(requests.Session, "get")
    def test_get_race_results_network_error_returns_none(self, mock_get):
        """Should return None on network error"""
        mock_get.side_effect = requests.RequestException("Connection failed")

        result = self.api.get_race_results(session_key="2024_1")

        self.assertIsNone(result)

    @patch.object(requests.Session, "get")
    def test_get_race_results_timeout_returns_none(self, mock_get):
        """Should return None on timeout"""
        mock_get.side_effect = requests.Timeout("Request timed out")

        result = self.api.get_race_results(session_key="2024_1")

        self.assertIsNone(result)
