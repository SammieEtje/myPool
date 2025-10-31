from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from betting.models import Driver, BetType, Competition, Race
from betting.f1_api import get_sample_f1_drivers, get_sample_f1_schedule
from datetime import datetime, date


class Command(BaseCommand):
    help = 'Seed database with initial F1 data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Driver.objects.all().delete()
            BetType.objects.all().delete()
            Race.objects.all().delete()
            Competition.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared'))

        self.stdout.write('Seeding database...')

        # Create admin user if doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@f1betting.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))

        # Create sample test users
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f'testuser{i}',
                defaults={
                    'email': f'user{i}@test.com',
                    'first_name': f'Test',
                    'last_name': f'User {i}'
                }
            )
            if created:
                user.set_password('test123')
                user.save()
                self.stdout.write(f'Created test user: testuser{i}')

        # Create bet types
        bet_types = [
            {
                'name': 'Top 10 Finishers',
                'code': 'top10',
                'description': 'Predict the top 10 finishing positions',
                'is_active': True,
                'requires_positions': True,
                'max_selections': 10
            },
            {
                'name': 'Podium (Top 3)',
                'code': 'podium',
                'description': 'Predict the top 3 finishers',
                'is_active': False,
                'requires_positions': True,
                'max_selections': 3
            },
            {
                'name': 'Race Winner',
                'code': 'winner',
                'description': 'Predict the race winner',
                'is_active': False,
                'requires_positions': False,
                'max_selections': 1
            }
        ]

        for bet_type_data in bet_types:
            bet_type, created = BetType.objects.get_or_create(
                code=bet_type_data['code'],
                defaults=bet_type_data
            )
            if created:
                self.stdout.write(f'Created bet type: {bet_type.name}')

        # Create drivers
        drivers_data = get_sample_f1_drivers()
        for driver_data in drivers_data:
            driver, created = Driver.objects.get_or_create(
                driver_number=driver_data['number'],
                defaults={
                    'first_name': driver_data['first_name'],
                    'last_name': driver_data['last_name'],
                    'team': driver_data['team'],
                    'nationality': driver_data['nationality'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created driver: #{driver.driver_number} {driver.first_name} {driver.last_name}')

        # Create competition
        competition, created = Competition.objects.get_or_create(
            year=2025,
            name='F1 2025 World Championship',
            defaults={
                'description': 'The 2025 Formula 1 World Championship season',
                'status': 'published',
                'start_date': date(2025, 3, 1),
                'end_date': date(2025, 12, 1),
                'created_by': admin_user,
                'points_for_exact_position': 10,
                'points_for_correct_driver': 5
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created competition: {competition.name}'))

        # Add all test users as participants
        test_users = User.objects.filter(username__startswith='testuser')
        competition.participants.set(test_users)

        # Create races
        schedule_data = get_sample_f1_schedule()
        for race_data in schedule_data:
            race, created = Race.objects.get_or_create(
                competition=competition,
                round_number=race_data['round'],
                defaults={
                    'name': race_data['name'],
                    'location': race_data['location'],
                    'country': race_data['country'],
                    'race_datetime': race_data['race_datetime'],
                    'betting_deadline': race_data['betting_deadline'],
                    'status': 'betting_open'
                }
            )
            if created:
                self.stdout.write(f'Created race: Round {race.round_number} - {race.name}')

        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin:    admin / admin123')
        self.stdout.write('  Test users: testuser1-5 / test123')
        self.stdout.write('\nYou can now run: python manage.py runserver')
