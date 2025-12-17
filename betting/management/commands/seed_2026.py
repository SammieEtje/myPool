from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from betting.models import Competition, Driver, Race


def get_2026_drivers():
    """
    Return F1 2026 driver lineup
    Based on expected 2026 regulations and team lineups
    Note: This is speculative for teams without confirmed lineups
    """
    return [
        # Red Bull Racing
        {"number": 1, "first_name": "Max", "last_name": "Verstappen", "team": "Red Bull Racing", "nationality": "Dutch"},
        {"number": 11, "first_name": "Sergio", "last_name": "Perez", "team": "Red Bull Racing", "nationality": "Mexican"},
        # Ferrari
        {"number": 16, "first_name": "Charles", "last_name": "Leclerc", "team": "Ferrari", "nationality": "Monégasque"},
        {"number": 44, "first_name": "Lewis", "last_name": "Hamilton", "team": "Ferrari", "nationality": "British"},
        # Mercedes
        {"number": 63, "first_name": "George", "last_name": "Russell", "team": "Mercedes", "nationality": "British"},
        {"number": 12, "first_name": "Andrea", "last_name": "Kimi Antonelli", "team": "Mercedes", "nationality": "Italian"},
        # McLaren
        {"number": 4, "first_name": "Lando", "last_name": "Norris", "team": "McLaren", "nationality": "British"},
        {"number": 81, "first_name": "Oscar", "last_name": "Piastri", "team": "McLaren", "nationality": "Australian"},
        # Aston Martin
        {"number": 14, "first_name": "Fernando", "last_name": "Alonso", "team": "Aston Martin", "nationality": "Spanish"},
        {"number": 18, "first_name": "Lance", "last_name": "Stroll", "team": "Aston Martin", "nationality": "Canadian"},
        # Alpine
        {"number": 10, "first_name": "Pierre", "last_name": "Gasly", "team": "Alpine", "nationality": "French"},
        {"number": 61, "first_name": "Jack", "last_name": "Doohan", "team": "Alpine", "nationality": "Australian"},
        # Williams
        {"number": 23, "first_name": "Alexander", "last_name": "Albon", "team": "Williams", "nationality": "Thai"},
        {"number": 55, "first_name": "Carlos", "last_name": "Sainz", "team": "Williams", "nationality": "Spanish"},
        # Haas
        {"number": 27, "first_name": "Nico", "last_name": "Hulkenberg", "team": "Haas F1 Team", "nationality": "German"},
        {"number": 31, "first_name": "Esteban", "last_name": "Ocon", "team": "Haas F1 Team", "nationality": "French"},
        # Audi F1 Team (rebranded from Sauber)
        {"number": 77, "first_name": "Valtteri", "last_name": "Bottas", "team": "Audi F1 Team", "nationality": "Finnish"},
        {"number": 24, "first_name": "Zhou", "last_name": "Guanyu", "team": "Audi F1 Team", "nationality": "Chinese"},
        # RB F1 Team
        {"number": 22, "first_name": "Yuki", "last_name": "Tsunoda", "team": "RB F1 Team", "nationality": "Japanese"},
        {"number": 40, "first_name": "Liam", "last_name": "Lawson", "team": "RB F1 Team", "nationality": "New Zealander"},
    ]


def get_2026_schedule():
    """
    Return F1 2026 race schedule
    Based on expected 2026 calendar (speculative dates)
    All datetimes are timezone-aware (UTC)
    """
    races = [
        {
            "name": "Bahrain Grand Prix",
            "location": "Bahrain International Circuit",
            "country": "Bahrain",
            "date": datetime(2026, 3, 15, 15, 0),
        },
        {
            "name": "Saudi Arabian Grand Prix",
            "location": "Jeddah Corniche Circuit",
            "country": "Saudi Arabia",
            "date": datetime(2026, 3, 22, 17, 0),
        },
        {
            "name": "Australian Grand Prix",
            "location": "Albert Park Circuit",
            "country": "Australia",
            "date": datetime(2026, 4, 5, 15, 0),
        },
        {
            "name": "Japanese Grand Prix",
            "location": "Suzuka Circuit",
            "country": "Japan",
            "date": datetime(2026, 4, 12, 14, 0),
        },
        {
            "name": "Chinese Grand Prix",
            "location": "Shanghai International Circuit",
            "country": "China",
            "date": datetime(2026, 4, 19, 15, 0),
        },
        {
            "name": "Miami Grand Prix",
            "location": "Miami International Autodrome",
            "country": "USA",
            "date": datetime(2026, 5, 3, 15, 30),
        },
        {
            "name": "Emilia Romagna Grand Prix",
            "location": "Autodromo Enzo e Dino Ferrari",
            "country": "Italy",
            "date": datetime(2026, 5, 17, 15, 0),
        },
        {
            "name": "Monaco Grand Prix",
            "location": "Circuit de Monaco",
            "country": "Monaco",
            "date": datetime(2026, 5, 24, 15, 0),
        },
        {
            "name": "Spanish Grand Prix",
            "location": "Circuit de Barcelona-Catalunya",
            "country": "Spain",
            "date": datetime(2026, 5, 31, 15, 0),
        },
        {
            "name": "Canadian Grand Prix",
            "location": "Circuit Gilles Villeneuve",
            "country": "Canada",
            "date": datetime(2026, 6, 14, 14, 0),
        },
        {
            "name": "Austrian Grand Prix",
            "location": "Red Bull Ring",
            "country": "Austria",
            "date": datetime(2026, 6, 28, 15, 0),
        },
        {
            "name": "British Grand Prix",
            "location": "Silverstone Circuit",
            "country": "United Kingdom",
            "date": datetime(2026, 7, 5, 15, 0),
        },
        {
            "name": "Belgian Grand Prix",
            "location": "Circuit de Spa-Francorchamps",
            "country": "Belgium",
            "date": datetime(2026, 7, 26, 15, 0),
        },
        {
            "name": "Hungarian Grand Prix",
            "location": "Hungaroring",
            "country": "Hungary",
            "date": datetime(2026, 8, 2, 15, 0),
        },
        {
            "name": "Dutch Grand Prix",
            "location": "Circuit Zandvoort",
            "country": "Netherlands",
            "date": datetime(2026, 8, 30, 15, 0),
        },
        {
            "name": "Italian Grand Prix",
            "location": "Autodromo Nazionale di Monza",
            "country": "Italy",
            "date": datetime(2026, 9, 6, 15, 0),
        },
        {
            "name": "Azerbaijan Grand Prix",
            "location": "Baku City Circuit",
            "country": "Azerbaijan",
            "date": datetime(2026, 9, 20, 13, 0),
        },
        {
            "name": "Singapore Grand Prix",
            "location": "Marina Bay Street Circuit",
            "country": "Singapore",
            "date": datetime(2026, 10, 4, 14, 0),
        },
        {
            "name": "United States Grand Prix",
            "location": "Circuit of the Americas",
            "country": "USA",
            "date": datetime(2026, 10, 18, 14, 0),
        },
        {
            "name": "Mexico City Grand Prix",
            "location": "Autódromo Hermanos Rodríguez",
            "country": "Mexico",
            "date": datetime(2026, 10, 25, 14, 0),
        },
        {
            "name": "Brazilian Grand Prix",
            "location": "Autódromo José Carlos Pace",
            "country": "Brazil",
            "date": datetime(2026, 11, 8, 14, 0),
        },
        {
            "name": "Las Vegas Grand Prix",
            "location": "Las Vegas Strip Circuit",
            "country": "USA",
            "date": datetime(2026, 11, 21, 22, 0),
        },
        {
            "name": "Qatar Grand Prix",
            "location": "Losail International Circuit",
            "country": "Qatar",
            "date": datetime(2026, 11, 29, 15, 0),
        },
        {
            "name": "Abu Dhabi Grand Prix",
            "location": "Yas Marina Circuit",
            "country": "UAE",
            "date": datetime(2026, 12, 6, 14, 0),
        },
    ]

    schedule = []
    for i, race in enumerate(races):
        # Convert naive datetime to timezone-aware datetime (UTC)
        race_date = timezone.make_aware(race["date"])
        deadline = race_date - timedelta(hours=2)

        schedule.append(
            {
                "round": i + 1,
                "name": race["name"],
                "location": race["location"],
                "country": race["country"],
                "race_datetime": race_date,
                "betting_deadline": deadline,
            }
        )

    return schedule


def create_drivers(drivers_data, clear_existing=False, stdout=None):
    """Create or update 2026 drivers."""
    if clear_existing:
        Driver.objects.all().delete()
        if stdout:
            stdout.write("Clearing existing drivers...")
            stdout.write("Drivers cleared")
    for driver_data in drivers_data:
        driver, created = Driver.objects.get_or_create(
            driver_number=driver_data["number"],
            defaults={
                "first_name": driver_data["first_name"],
                "last_name": driver_data["last_name"],
                "team": driver_data["team"],
                "nationality": driver_data["nationality"],
                "is_active": True,
            },
        )
        if created:
            if stdout:
                stdout.write(f"Created driver: #{driver.driver_number} {driver.first_name} {driver.last_name}")
        else:
            if driver.team != driver_data["team"]:
                driver.team = driver_data["team"]
                driver.save()
                if stdout:
                    stdout.write(
                        f"Updated driver team: #{driver.driver_number} {driver.first_name} {driver.last_name} -> {driver.team}"
                    )


def create_competition(admin_user, stdout=None):
    """Create or get 2026 competition."""
    competition, created = Competition.objects.get_or_create(
        year=2026,
        name="F1 2026 World Championship",
        defaults={
            "description": "The 2026 Formula 1 World Championship season - New Era with revolutionary power unit regulations",
            "status": "published",
            "start_date": date(2026, 3, 1),
            "end_date": date(2026, 12, 15),
            "created_by": admin_user,
            "points_for_exact_position": 10,
            "points_for_correct_driver": 5,
        },
    )
    if created:
        if stdout:
            stdout.write(f"Created competition: {competition.name}")
    else:
        if stdout:
            stdout.write(f"Competition already exists: {competition.name}")
    return competition


def create_races(competition, schedule_data, stdout=None):
    """Create 2026 races."""
    for race_data in schedule_data:
        race, created = Race.objects.get_or_create(
            competition=competition,
            round_number=race_data["round"],
            defaults={
                "name": race_data["name"],
                "location": race_data["location"],
                "country": race_data["country"],
                "race_datetime": race_data["race_datetime"],
                "betting_deadline": race_data["betting_deadline"],
                "status": "betting_open",
            },
        )
        if created:
            if stdout:
                stdout.write(f"Created race: Round {race.round_number} - {race.name}")


def print_summary(competition, stdout=None):
    """Print seeding summary."""
    if stdout:
        stdout.write("\n" + "=" * 50)
        stdout.write("F1 2026 season data seeded successfully!")
        stdout.write("=" * 50)
        stdout.write("\n2026 Season Details:")
        stdout.write(f"  Competition: {competition.name}")
        stdout.write(f"  Drivers: {Driver.objects.filter(is_active=True).count()}")
        stdout.write(f"  Races: {Race.objects.filter(competition=competition).count()}")
        stdout.write(f"  Participants: {competition.participants.count()}")
        stdout.write("\nNote: Audi F1 Team debuts in 2026 (formerly Kick Sauber)")
        stdout.write("New power unit regulations take effect this season!")


class Command(BaseCommand):
    help = "Seed database with F1 2026 season data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear-drivers",
            action="store_true",
            help="Clear existing drivers before seeding",
        )

    def handle(self, *args, **options):
        self.stdout.write("Seeding 2026 F1 season data...")

        # Get admin user
        try:
            admin_user = User.objects.get(username="admin")
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("Admin user not found. Please run seed_data first."))
            return

        # Create drivers
        drivers_data = get_2026_drivers()
        create_drivers(drivers_data, options["clear_drivers"], self.stdout)

        # Create competition
        competition = create_competition(admin_user, self.stdout)

        # Add test users as participants
        test_users = User.objects.filter(username__startswith="testuser")
        if test_users.exists():
            competition.participants.set(test_users)
            self.stdout.write(f"Added {test_users.count()} test users as participants")

        # Create races
        schedule_data = get_2026_schedule()
        create_races(competition, schedule_data, self.stdout)

        # Print summary
        print_summary(competition, self.stdout)
