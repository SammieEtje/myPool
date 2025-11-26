"""
F1 API Integration
Uses OpenF1 API for race data and driver information
Fallback to manual entry if API is unavailable
"""

import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta


class F1API:
    """Wrapper for F1 API integration"""

    def __init__(self):
        self.base_url = settings.F1_API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'F1BettingPool/1.0'
        })

    def get_drivers(self, year=2024):
        """
        Get list of drivers for a specific year
        Note: OpenF1 API structure may vary - this is a template
        """
        try:
            # OpenF1 example endpoint
            response = self.session.get(
                f"{self.base_url}/drivers",
                params={'session_key': f'{year}_latest'},
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch drivers: {response.status_code}")
                return None

        except requests.RequestException as e:
            print(f"Error fetching drivers: {e}")
            return None

    def get_race_schedule(self, year=2024):
        """Get race schedule for a specific year"""
        try:
            # This is a template - adjust based on actual API structure
            response = self.session.get(
                f"{self.base_url}/sessions",
                params={'year': year, 'session_type': 'Race'},
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch schedule: {response.status_code}")
                return None

        except requests.RequestException as e:
            print(f"Error fetching schedule: {e}")
            return None

    def get_race_results(self, session_key):
        """Get race results for a specific session"""
        try:
            response = self.session.get(
                f"{self.base_url}/position",
                params={'session_key': session_key},
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch results: {response.status_code}")
                return None

        except requests.RequestException as e:
            print(f"Error fetching results: {e}")
            return None


def get_sample_f1_drivers():
    """
    Return F1 2025 driver lineup
    Based on confirmed 2025 driver changes and team lineups
    """
    return [
        # Red Bull Racing
        {'number': 1, 'first_name': 'Max', 'last_name': 'Verstappen', 'team': 'Red Bull Racing', 'nationality': 'Dutch'},
        {'number': 11, 'first_name': 'Sergio', 'last_name': 'Perez', 'team': 'Red Bull Racing', 'nationality': 'Mexican'},

        # Ferrari (Lewis Hamilton joins!)
        {'number': 16, 'first_name': 'Charles', 'last_name': 'Leclerc', 'team': 'Ferrari', 'nationality': 'Monégasque'},
        {'number': 44, 'first_name': 'Lewis', 'last_name': 'Hamilton', 'team': 'Ferrari', 'nationality': 'British'},

        # Mercedes (Antonelli replaces Hamilton)
        {'number': 63, 'first_name': 'George', 'last_name': 'Russell', 'team': 'Mercedes', 'nationality': 'British'},
        {'number': 12, 'first_name': 'Andrea', 'last_name': 'Kimi Antonelli', 'team': 'Mercedes', 'nationality': 'Italian'},

        # McLaren
        {'number': 4, 'first_name': 'Lando', 'last_name': 'Norris', 'team': 'McLaren', 'nationality': 'British'},
        {'number': 81, 'first_name': 'Oscar', 'last_name': 'Piastri', 'team': 'McLaren', 'nationality': 'Australian'},

        # Aston Martin
        {'number': 14, 'first_name': 'Fernando', 'last_name': 'Alonso', 'team': 'Aston Martin', 'nationality': 'Spanish'},
        {'number': 18, 'first_name': 'Lance', 'last_name': 'Stroll', 'team': 'Aston Martin', 'nationality': 'Canadian'},

        # Alpine (Doohan joins)
        {'number': 10, 'first_name': 'Pierre', 'last_name': 'Gasly', 'team': 'Alpine', 'nationality': 'French'},
        {'number': 61, 'first_name': 'Jack', 'last_name': 'Doohan', 'team': 'Alpine', 'nationality': 'Australian'},

        # Williams (Sainz joins)
        {'number': 23, 'first_name': 'Alexander', 'last_name': 'Albon', 'team': 'Williams', 'nationality': 'Thai'},
        {'number': 55, 'first_name': 'Carlos', 'last_name': 'Sainz', 'team': 'Williams', 'nationality': 'Spanish'},

        # Haas (Ocon joins)
        {'number': 27, 'first_name': 'Nico', 'last_name': 'Hulkenberg', 'team': 'Haas F1 Team', 'nationality': 'German'},
        {'number': 31, 'first_name': 'Esteban', 'last_name': 'Ocon', 'team': 'Haas F1 Team', 'nationality': 'French'},

        # Kick Sauber (future Audi)
        {'number': 77, 'first_name': 'Valtteri', 'last_name': 'Bottas', 'team': 'Kick Sauber', 'nationality': 'Finnish'},
        {'number': 24, 'first_name': 'Zhou', 'last_name': 'Guanyu', 'team': 'Kick Sauber', 'nationality': 'Chinese'},

        # RB (Lawson joins)
        {'number': 22, 'first_name': 'Yuki', 'last_name': 'Tsunoda', 'team': 'RB F1 Team', 'nationality': 'Japanese'},
        {'number': 40, 'first_name': 'Liam', 'last_name': 'Lawson', 'team': 'RB F1 Team', 'nationality': 'New Zealander'},
    ]


def get_sample_f1_schedule():
    """
    Return F1 2025 race schedule
    Based on provisional 2025 calendar
    All datetimes are timezone-aware (UTC)
    """
    races = [
        {'name': 'Bahrain Grand Prix', 'location': 'Bahrain International Circuit', 'country': 'Bahrain', 'date': datetime(2025, 3, 16, 15, 0)},
        {'name': 'Saudi Arabian Grand Prix', 'location': 'Jeddah Corniche Circuit', 'country': 'Saudi Arabia', 'date': datetime(2025, 3, 23, 17, 0)},
        {'name': 'Australian Grand Prix', 'location': 'Albert Park Circuit', 'country': 'Australia', 'date': datetime(2025, 4, 6, 15, 0)},
        {'name': 'Japanese Grand Prix', 'location': 'Suzuka Circuit', 'country': 'Japan', 'date': datetime(2025, 4, 13, 14, 0)},
        {'name': 'Chinese Grand Prix', 'location': 'Shanghai International Circuit', 'country': 'China', 'date': datetime(2025, 4, 20, 15, 0)},
        {'name': 'Miami Grand Prix', 'location': 'Miami International Autodrome', 'country': 'USA', 'date': datetime(2025, 5, 4, 15, 30)},
        {'name': 'Emilia Romagna Grand Prix', 'location': 'Autodromo Enzo e Dino Ferrari', 'country': 'Italy', 'date': datetime(2025, 5, 18, 15, 0)},
        {'name': 'Monaco Grand Prix', 'location': 'Circuit de Monaco', 'country': 'Monaco', 'date': datetime(2025, 5, 25, 15, 0)},
        {'name': 'Spanish Grand Prix', 'location': 'Circuit de Barcelona-Catalunya', 'country': 'Spain', 'date': datetime(2025, 6, 1, 15, 0)},
        {'name': 'Canadian Grand Prix', 'location': 'Circuit Gilles Villeneuve', 'country': 'Canada', 'date': datetime(2025, 6, 15, 14, 0)},
        {'name': 'Austrian Grand Prix', 'location': 'Red Bull Ring', 'country': 'Austria', 'date': datetime(2025, 6, 29, 15, 0)},
        {'name': 'British Grand Prix', 'location': 'Silverstone Circuit', 'country': 'United Kingdom', 'date': datetime(2025, 7, 6, 15, 0)},
        {'name': 'Belgian Grand Prix', 'location': 'Circuit de Spa-Francorchamps', 'country': 'Belgium', 'date': datetime(2025, 7, 27, 15, 0)},
        {'name': 'Hungarian Grand Prix', 'location': 'Hungaroring', 'country': 'Hungary', 'date': datetime(2025, 8, 3, 15, 0)},
        {'name': 'Dutch Grand Prix', 'location': 'Circuit Zandvoort', 'country': 'Netherlands', 'date': datetime(2025, 8, 31, 15, 0)},
        {'name': 'Italian Grand Prix', 'location': 'Autodromo Nazionale di Monza', 'country': 'Italy', 'date': datetime(2025, 9, 7, 15, 0)},
        {'name': 'Azerbaijan Grand Prix', 'location': 'Baku City Circuit', 'country': 'Azerbaijan', 'date': datetime(2025, 9, 21, 13, 0)},
        {'name': 'Singapore Grand Prix', 'location': 'Marina Bay Street Circuit', 'country': 'Singapore', 'date': datetime(2025, 10, 5, 14, 0)},
        {'name': 'United States Grand Prix', 'location': 'Circuit of the Americas', 'country': 'USA', 'date': datetime(2025, 10, 19, 14, 0)},
        {'name': 'Mexico City Grand Prix', 'location': 'Autódromo Hermanos Rodríguez', 'country': 'Mexico', 'date': datetime(2025, 10, 26, 14, 0)},
        {'name': 'Brazilian Grand Prix', 'location': 'Autódromo José Carlos Pace', 'country': 'Brazil', 'date': datetime(2025, 11, 9, 14, 0)},
        {'name': 'Las Vegas Grand Prix', 'location': 'Las Vegas Strip Circuit', 'country': 'USA', 'date': datetime(2025, 11, 22, 22, 0)},
        {'name': 'Qatar Grand Prix', 'location': 'Losail International Circuit', 'country': 'Qatar', 'date': datetime(2025, 11, 30, 15, 0)},
        {'name': 'Abu Dhabi Grand Prix', 'location': 'Yas Marina Circuit', 'country': 'UAE', 'date': datetime(2025, 12, 7, 14, 0)},
    ]

    schedule = []
    for i, race in enumerate(races):
        # Convert naive datetime to timezone-aware datetime (UTC)
        race_date = timezone.make_aware(race['date'])
        deadline = race_date - timedelta(hours=2)

        schedule.append({
            'round': i + 1,
            'name': race['name'],
            'location': race['location'],
            'country': race['country'],
            'race_datetime': race_date,
            'betting_deadline': deadline
        })

    return schedule
