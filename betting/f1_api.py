"""
F1 API Integration
Uses OpenF1 API for race data and driver information
Fallback to manual entry if API is unavailable
"""

import requests
from django.conf import settings
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
    Return sample F1 driver data for 2024 season
    Use this as fallback when API is not available
    """
    return [
        {'number': 1, 'first_name': 'Max', 'last_name': 'Verstappen', 'team': 'Red Bull Racing', 'nationality': 'Dutch'},
        {'number': 11, 'first_name': 'Sergio', 'last_name': 'Perez', 'team': 'Red Bull Racing', 'nationality': 'Mexican'},
        {'number': 44, 'first_name': 'Lewis', 'last_name': 'Hamilton', 'team': 'Mercedes', 'nationality': 'British'},
        {'number': 63, 'first_name': 'George', 'last_name': 'Russell', 'team': 'Mercedes', 'nationality': 'British'},
        {'number': 16, 'first_name': 'Charles', 'last_name': 'Leclerc', 'team': 'Ferrari', 'nationality': 'Monégasque'},
        {'number': 55, 'first_name': 'Carlos', 'last_name': 'Sainz', 'team': 'Ferrari', 'nationality': 'Spanish'},
        {'number': 4, 'first_name': 'Lando', 'last_name': 'Norris', 'team': 'McLaren', 'nationality': 'British'},
        {'number': 81, 'first_name': 'Oscar', 'last_name': 'Piastri', 'team': 'McLaren', 'nationality': 'Australian'},
        {'number': 14, 'first_name': 'Fernando', 'last_name': 'Alonso', 'team': 'Aston Martin', 'nationality': 'Spanish'},
        {'number': 18, 'first_name': 'Lance', 'last_name': 'Stroll', 'team': 'Aston Martin', 'nationality': 'Canadian'},
        {'number': 10, 'first_name': 'Pierre', 'last_name': 'Gasly', 'team': 'Alpine', 'nationality': 'French'},
        {'number': 31, 'first_name': 'Esteban', 'last_name': 'Ocon', 'team': 'Alpine', 'nationality': 'French'},
        {'number': 23, 'first_name': 'Alexander', 'last_name': 'Albon', 'team': 'Williams', 'nationality': 'Thai'},
        {'number': 2, 'first_name': 'Logan', 'last_name': 'Sargeant', 'team': 'Williams', 'nationality': 'American'},
        {'number': 27, 'first_name': 'Nico', 'last_name': 'Hulkenberg', 'team': 'Haas F1 Team', 'nationality': 'German'},
        {'number': 20, 'first_name': 'Kevin', 'last_name': 'Magnussen', 'team': 'Haas F1 Team', 'nationality': 'Danish'},
        {'number': 77, 'first_name': 'Valtteri', 'last_name': 'Bottas', 'team': 'Alfa Romeo', 'nationality': 'Finnish'},
        {'number': 24, 'first_name': 'Zhou', 'last_name': 'Guanyu', 'team': 'Alfa Romeo', 'nationality': 'Chinese'},
        {'number': 3, 'first_name': 'Daniel', 'last_name': 'Ricciardo', 'team': 'AlphaTauri', 'nationality': 'Australian'},
        {'number': 22, 'first_name': 'Yuki', 'last_name': 'Tsunoda', 'team': 'AlphaTauri', 'nationality': 'Japanese'},
    ]


def get_sample_f1_schedule():
    """
    Return sample F1 race schedule for 2025
    Use this as fallback when API is not available
    """
    base_date = datetime(2025, 3, 1)

    races = [
        {'name': 'Bahrain Grand Prix', 'location': 'Bahrain International Circuit', 'country': 'Bahrain'},
        {'name': 'Saudi Arabian Grand Prix', 'location': 'Jeddah Corniche Circuit', 'country': 'Saudi Arabia'},
        {'name': 'Australian Grand Prix', 'location': 'Albert Park Circuit', 'country': 'Australia'},
        {'name': 'Japanese Grand Prix', 'location': 'Suzuka Circuit', 'country': 'Japan'},
        {'name': 'Chinese Grand Prix', 'location': 'Shanghai International Circuit', 'country': 'China'},
        {'name': 'Miami Grand Prix', 'location': 'Miami International Autodrome', 'country': 'USA'},
        {'name': 'Emilia Romagna Grand Prix', 'location': 'Autodromo Enzo e Dino Ferrari', 'country': 'Italy'},
        {'name': 'Monaco Grand Prix', 'location': 'Circuit de Monaco', 'country': 'Monaco'},
        {'name': 'Canadian Grand Prix', 'location': 'Circuit Gilles Villeneuve', 'country': 'Canada'},
        {'name': 'Spanish Grand Prix', 'location': 'Circuit de Barcelona-Catalunya', 'country': 'Spain'},
        {'name': 'Austrian Grand Prix', 'location': 'Red Bull Ring', 'country': 'Austria'},
        {'name': 'British Grand Prix', 'location': 'Silverstone Circuit', 'country': 'United Kingdom'},
        {'name': 'Hungarian Grand Prix', 'location': 'Hungaroring', 'country': 'Hungary'},
        {'name': 'Belgian Grand Prix', 'location': 'Circuit de Spa-Francorchamps', 'country': 'Belgium'},
        {'name': 'Dutch Grand Prix', 'location': 'Circuit Zandvoort', 'country': 'Netherlands'},
        {'name': 'Italian Grand Prix', 'location': 'Autodromo Nazionale di Monza', 'country': 'Italy'},
        {'name': 'Azerbaijan Grand Prix', 'location': 'Baku City Circuit', 'country': 'Azerbaijan'},
        {'name': 'Singapore Grand Prix', 'location': 'Marina Bay Street Circuit', 'country': 'Singapore'},
        {'name': 'United States Grand Prix', 'location': 'Circuit of the Americas', 'country': 'USA'},
        {'name': 'Mexico City Grand Prix', 'location': 'Autódromo Hermanos Rodríguez', 'country': 'Mexico'},
        {'name': 'Brazilian Grand Prix', 'location': 'Autódromo José Carlos Pace', 'country': 'Brazil'},
        {'name': 'Las Vegas Grand Prix', 'location': 'Las Vegas Strip Circuit', 'country': 'USA'},
        {'name': 'Qatar Grand Prix', 'location': 'Losail International Circuit', 'country': 'Qatar'},
        {'name': 'Abu Dhabi Grand Prix', 'location': 'Yas Marina Circuit', 'country': 'UAE'},
    ]

    schedule = []
    for i, race in enumerate(races):
        race_date = base_date + timedelta(weeks=i*2)
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
