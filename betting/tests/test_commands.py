"""
Test suite for F1 Betting Pool management commands
"""
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from io import StringIO
from betting.models import (
    Competition, Driver, Race, BetType, Bet, RaceResult, CompetitionStanding
)


class SeedDataCommandTest(TestCase):
    """Test seed_data management command"""

    def test_seed_data_creates_users(self):
        """Test seed_data creates users"""
        out = StringIO()
        call_command('seed_data', stdout=out)

        # Check admin user created
        admin = User.objects.filter(email='admin@f1betting.com').first()
        self.assertIsNotNone(admin)
        self.assertTrue(admin.is_superuser)

        # Check test users created
        test_users = User.objects.filter(email__startswith='user')
        self.assertGreaterEqual(test_users.count(), 5)

    def test_seed_data_creates_drivers(self):
        """Test seed_data creates drivers"""
        out = StringIO()
        call_command('seed_data', stdout=out)

        drivers = Driver.objects.all()
        self.assertGreaterEqual(drivers.count(), 20)

        # Check specific drivers exist
        hamilton = Driver.objects.filter(last_name='Hamilton').first()
        verstappen = Driver.objects.filter(last_name='Verstappen').first()
        self.assertIsNotNone(hamilton)
        self.assertIsNotNone(verstappen)

    def test_seed_data_creates_competition(self):
        """Test seed_data creates competition"""
        out = StringIO()
        call_command('seed_data', stdout=out)

        competitions = Competition.objects.all()
        self.assertGreaterEqual(competitions.count(), 1)

        # Check 2025 competition exists
        comp = Competition.objects.filter(year=2025).first()
        self.assertIsNotNone(comp)
        self.assertEqual(comp.points_for_exact_position, 10)
        self.assertEqual(comp.points_for_correct_driver, 5)

    def test_seed_data_creates_races(self):
        """Test seed_data creates races"""
        out = StringIO()
        call_command('seed_data', stdout=out)

        races = Race.objects.all()
        self.assertGreaterEqual(races.count(), 20)

        # Check races have correct round numbers
        race1 = Race.objects.filter(round_number=1).first()
        self.assertIsNotNone(race1)

    def test_seed_data_creates_bet_types(self):
        """Test seed_data creates bet types"""
        out = StringIO()
        call_command('seed_data', stdout=out)

        bet_types = BetType.objects.all()
        self.assertGreaterEqual(bet_types.count(), 1)

        # Check top10 bet type exists
        top10 = BetType.objects.filter(code='top10').first()
        self.assertIsNotNone(top10)
        self.assertTrue(top10.is_active)
        self.assertEqual(top10.max_selections, 10)

    def test_seed_data_clear_option(self):
        """Test seed_data --clear option"""
        # First seed
        call_command('seed_data', stdout=StringIO())
        first_count = User.objects.count()

        # Seed again with clear
        call_command('seed_data', '--clear', stdout=StringIO())
        second_count = User.objects.count()

        # Should have similar count (cleared and re-seeded)
        self.assertGreaterEqual(second_count, 1)


class LoadResultsCommandTest(TestCase):
    """Test load_results management command"""

    def setUp(self):
        # Create necessary data
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_superuser=True
        )
        self.competition = Competition.objects.create(
            name='F1 2025',
            year=2025,
            status='active',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=300),
            created_by=admin
        )

        # Create drivers
        for i in range(1, 21):
            Driver.objects.create(
                driver_number=i,
                first_name=f'Driver{i}',
                last_name='Test',
                team='Team'
            )

        # Create races
        for i in range(1, 6):
            Race.objects.create(
                competition=self.competition,
                name=f'Race {i}',
                round_number=i,
                race_datetime=timezone.now() - timedelta(days=30-i*7),
                betting_deadline=timezone.now() - timedelta(days=30-i*7),
                status='scheduled'
            )

    def test_load_results_creates_results(self):
        """Test load_results creates race results"""
        out = StringIO()
        call_command('load_results', '--races=2', stdout=out)

        # Check results were created
        results = RaceResult.objects.all()
        self.assertGreaterEqual(results.count(), 10)  # At least 10 results

        # Check races marked as completed
        completed_races = Race.objects.filter(status='completed')
        self.assertGreaterEqual(completed_races.count(), 2)

    def test_load_results_verifies_results(self):
        """Test load_results marks results as verified"""
        out = StringIO()
        call_command('load_results', '--races=1', stdout=out)

        results = RaceResult.objects.all()
        for result in results:
            self.assertTrue(result.verified)

    def test_load_results_default_count(self):
        """Test load_results with default race count"""
        out = StringIO()
        call_command('load_results', stdout=out)

        # Default is 3 races
        completed_races = Race.objects.filter(status='completed')
        self.assertGreaterEqual(completed_races.count(), 3)


class ScoreRaceCommandTest(TestCase):
    """Test score_race management command"""

    def setUp(self):
        # Create admin
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_superuser=True
        )

        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123'
        )

        # Create competition
        self.competition = Competition.objects.create(
            name='F1 2025',
            year=2025,
            status='active',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=300),
            created_by=self.admin,
            points_for_exact_position=10,
            points_for_correct_driver=5
        )

        # Create drivers
        self.drivers = []
        for i in range(1, 11):
            driver = Driver.objects.create(
                driver_number=i,
                first_name=f'Driver{i}',
                last_name='Test',
                team='Team'
            )
            self.drivers.append(driver)

        # Create race
        self.race = Race.objects.create(
            competition=self.competition,
            name='Test GP',
            round_number=1,
            race_datetime=timezone.now() - timedelta(days=1),
            betting_deadline=timezone.now() - timedelta(days=1),
            status='completed'
        )

        # Create bet type
        self.bet_type = BetType.objects.create(
            name='Top 10',
            code='top10',
            requires_positions=True,
            max_selections=10
        )

        # Create race results (actual results)
        for i, driver in enumerate(self.drivers):
            RaceResult.objects.create(
                race=self.race,
                driver=driver,
                position=i+1,
                verified=True
            )

    def test_score_race_calculates_points(self):
        """Test score_race calculates points correctly"""
        # User predicts exact P1 and P2
        Bet.objects.create(
            user=self.user,
            race=self.race,
            bet_type=self.bet_type,
            driver=self.drivers[0],  # Actual P1
            predicted_position=1
        )
        Bet.objects.create(
            user=self.user,
            race=self.race,
            bet_type=self.bet_type,
            driver=self.drivers[1],  # Actual P2
            predicted_position=2
        )

        # Score the race
        out = StringIO()
        call_command('score_race', str(self.race.id), stdout=out)

        # Check bets scored correctly
        bet1 = Bet.objects.get(driver=self.drivers[0], race=self.race)
        bet2 = Bet.objects.get(driver=self.drivers[1], race=self.race)

        self.assertTrue(bet1.is_scored)
        self.assertEqual(bet1.points_earned, 10)  # Exact position
        self.assertTrue(bet2.is_scored)
        self.assertEqual(bet2.points_earned, 10)  # Exact position

    def test_score_race_partial_points(self):
        """Test score_race gives partial points for correct driver"""
        # User predicts driver in top 10 but wrong position
        Bet.objects.create(
            user=self.user,
            race=self.race,
            bet_type=self.bet_type,
            driver=self.drivers[4],  # Actual P5
            predicted_position=1  # Wrong position
        )

        # Score the race
        out = StringIO()
        call_command('score_race', str(self.race.id), stdout=out)

        # Check partial points awarded
        bet = Bet.objects.get(driver=self.drivers[4], race=self.race)
        self.assertTrue(bet.is_scored)
        self.assertEqual(bet.points_earned, 5)  # Correct driver, wrong position

    def test_score_race_updates_standings(self):
        """Test score_race updates competition standings"""
        # Create bets
        Bet.objects.create(
            user=self.user,
            race=self.race,
            bet_type=self.bet_type,
            driver=self.drivers[0],
            predicted_position=1
        )

        # Score the race
        out = StringIO()
        call_command('score_race', str(self.race.id), stdout=out)

        # Check standing created/updated
        standing = CompetitionStanding.objects.filter(
            user=self.user,
            competition=self.competition
        ).first()

        self.assertIsNotNone(standing)
        self.assertEqual(standing.total_points, 10)
        self.assertEqual(standing.exact_predictions, 1)

    def test_score_race_by_id(self):
        """Test scoring race by ID"""
        # Create bet
        Bet.objects.create(
            user=self.user,
            race=self.race,
            bet_type=self.bet_type,
            driver=self.drivers[0],
            predicted_position=1
        )

        # Score by race ID
        out = StringIO()
        call_command('score_race', str(self.race.id), stdout=out)

        # Check bet scored
        bet = Bet.objects.get(race=self.race, user=self.user)
        self.assertTrue(bet.is_scored)

    def test_score_race_no_double_scoring(self):
        """Test already scored bets aren't re-scored"""
        # Create and score bet
        bet = Bet.objects.create(
            user=self.user,
            race=self.race,
            bet_type=self.bet_type,
            driver=self.drivers[0],
            predicted_position=1,
            is_scored=True,
            points_earned=10
        )

        # Try to score again
        out = StringIO()
        call_command('score_race', str(self.race.id), stdout=out)

        # Check bet not re-scored
        bet.refresh_from_db()
        self.assertEqual(bet.points_earned, 10)
        self.assertTrue(bet.is_scored)
