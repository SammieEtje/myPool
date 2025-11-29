import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from betting.models import (
    Bet,
    BetType,
    Competition,
    CompetitionStanding,
    Driver,
    Race,
    RaceResult,
)


class Command(BaseCommand):
    help = 'Load sample race results and standings for demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--races',
            type=int,
            default=3,
            help='Number of races to add results for (default: 3)',
        )

    def handle(self, *args, **options):
        num_races = options['races']

        # Get the 2025 competition
        try:
            competition = Competition.objects.get(year=2025, name__icontains='2025')
        except Competition.DoesNotExist:
            self.stdout.write(self.style.ERROR('2025 competition not found. Run seed_data first.'))
            return

        # Get races
        races = list(Race.objects.filter(competition=competition).order_by('round_number')[:num_races])

        if not races:
            self.stdout.write(self.style.ERROR('No races found. Run seed_data first.'))
            return

        # Get all drivers
        drivers = list(Driver.objects.filter(is_active=True))
        if len(drivers) < 10:
            self.stdout.write(self.style.ERROR('Not enough drivers. Run seed_data first.'))
            return

        self.stdout.write(f'\nLoading results for {len(races)} race(s)...\n')

        # Sample realistic results based on 2024 form
        sample_results = [
            # Bahrain GP - Verstappen dominance
            [
                ('Verstappen', 1), ('Leclerc', 16), ('Norris', 4), ('Piastri', 81),
                ('Hamilton', 44), ('Russell', 63), ('Alonso', 14), ('Sainz', 55),
                ('Perez', 11), ('Gasly', 10)
            ],
            # Saudi Arabia - Ferrari strong
            [
                ('Leclerc', 16), ('Verstappen', 1), ('Hamilton', 44), ('Norris', 4),
                ('Piastri', 81), ('Russell', 63), ('Sainz', 55), ('Alonso', 14),
                ('Perez', 11), ('Ocon', 31)
            ],
            # Australia - McLaren double
            [
                ('Norris', 4), ('Piastri', 81), ('Verstappen', 1), ('Hamilton', 44),
                ('Leclerc', 16), ('Russell', 63), ('Alonso', 14), ('Sainz', 55),
                ('Gasly', 10), ('Perez', 11)
            ],
        ]

        for idx, race in enumerate(races):
            self.stdout.write(f'\n=== {race.name} (Round {race.round_number}) ===')

            # Clear existing results
            RaceResult.objects.filter(race=race).delete()

            # Use sample result if available, otherwise generate random
            if idx < len(sample_results):
                result_data = sample_results[idx]
            else:
                # Generate random result
                random_drivers = random.sample(drivers, 10)
                result_data = [(d.last_name, d.driver_number) for d in random_drivers]

            # Create results
            for position, (last_name, driver_number) in enumerate(result_data, 1):
                try:
                    driver = Driver.objects.get(driver_number=driver_number)
                    result = RaceResult.objects.create(
                        race=race,
                        driver=driver,
                        position=position,
                        verified=True
                    )
                    self.stdout.write(f'  P{position}: {driver.first_name} {driver.last_name} ({driver.team})')
                except Driver.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  Driver #{driver_number} not found, skipping'))

            # Update race status
            race.status = 'completed'
            race.save()

        # Score all completed races
        self.stdout.write(self.style.SUCCESS('\n\nScoring races and updating standings...'))

        from django.core.management import call_command
        for race in races:
            self.stdout.write(f'Scoring {race.name}...')
            call_command('score_race', race.id)

        # Display standings
        self.stdout.write(self.style.SUCCESS('\n\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('CURRENT STANDINGS'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        standings = CompetitionStanding.objects.filter(
            competition=competition
        ).order_by('-total_points')[:10]

        if standings:
            self.stdout.write(f'{"Rank":<6} {"User":<25} {"Points":<10} {"Races":<8} {"Exact":<8}')
            self.stdout.write('-' * 60)
            for standing in standings:
                self.stdout.write(
                    f'{standing.rank:<6} '
                    f'{standing.user.email[:24]:<25} '
                    f'{standing.total_points:<10} '
                    f'{standing.races_predicted:<8} '
                    f'{standing.exact_predictions:<8}'
                )
        else:
            self.stdout.write('No standings yet. Users need to place bets first.')

        self.stdout.write(self.style.SUCCESS('\n\nRace results loaded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'✓ {len(races)} race(s) completed'))
        self.stdout.write(self.style.SUCCESS(f'✓ Standings updated'))
        self.stdout.write('\nVisit the app to see the results and leaderboard!')
