"""
Test suite for F1 Betting Pool models
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from betting.models import (
    UserProfile, Competition, Driver, Race, BetType,
    Bet, RaceResult, CompetitionStanding
)


class UserProfileModelTest(TestCase):
    """Test UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_profile_creation(self):
        """Test that UserProfile is created automatically with User"""
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertEqual(self.user.userprofile.total_points, 0)

    def test_user_profile_str(self):
        """Test UserProfile string representation"""
        self.assertEqual(
            str(self.user.userprofile),
            'testuser - Profile'
        )

    def test_display_name_defaults_to_username(self):
        """Test display_name defaults to username if not set"""
        self.assertEqual(self.user.userprofile.display_name, 'testuser')

    def test_display_name_custom(self):
        """Test custom display_name"""
        profile = self.user.userprofile
        profile.display_name = 'Test Racer'
        profile.save()
        self.assertEqual(profile.display_name, 'Test Racer')


class CompetitionModelTest(TestCase):
    """Test Competition model"""

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.competition = Competition.objects.create(
            name='F1 2025 Championship',
            description='Test championship',
            year=2025,
            status='active',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=300),
            created_by=self.admin,
            points_for_exact_position=10,
            points_for_correct_driver=5
        )

    def test_competition_creation(self):
        """Test Competition model creation"""
        self.assertEqual(self.competition.name, 'F1 2025 Championship')
        self.assertEqual(self.competition.year, 2025)
        self.assertEqual(self.competition.status, 'active')

    def test_competition_str(self):
        """Test Competition string representation"""
        self.assertEqual(str(self.competition), 'F1 2025 Championship')

    def test_competition_points_configuration(self):
        """Test points configuration"""
        self.assertEqual(self.competition.points_for_exact_position, 10)
        self.assertEqual(self.competition.points_for_correct_driver, 5)

    def test_add_participant(self):
        """Test adding participant to competition"""
        user = User.objects.create_user(
            username='racer1',
            email='racer1@example.com',
            password='pass123'
        )
        self.competition.participants.add(user)
        self.assertIn(user, self.competition.participants.all())


class DriverModelTest(TestCase):
    """Test Driver model"""

    def setUp(self):
        self.driver = Driver.objects.create(
            driver_number=44,
            first_name='Lewis',
            last_name='Hamilton',
            team='Mercedes',
            nationality='British',
            is_active=True
        )

    def test_driver_creation(self):
        """Test Driver model creation"""
        self.assertEqual(self.driver.driver_number, 44)
        self.assertEqual(self.driver.first_name, 'Lewis')
        self.assertEqual(self.driver.last_name, 'Hamilton')
        self.assertEqual(self.driver.team, 'Mercedes')

    def test_driver_str(self):
        """Test Driver string representation"""
        self.assertEqual(str(self.driver), '#44 Lewis Hamilton (Mercedes)')

    def test_driver_full_name_property(self):
        """Test full_name property"""
        self.assertEqual(self.driver.full_name, 'Lewis Hamilton')

    def test_driver_is_active(self):
        """Test driver active status"""
        self.assertTrue(self.driver.is_active)


class RaceModelTest(TestCase):
    """Test Race model"""

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.competition = Competition.objects.create(
            name='F1 2025 Championship',
            year=2025,
            status='active',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=300),
            created_by=self.admin
        )
        self.race = Race.objects.create(
            competition=self.competition,
            name='Bahrain Grand Prix',
            location='Sakhir',
            country='Bahrain',
            round_number=1,
            race_datetime=timezone.now() + timedelta(days=7),
            betting_deadline=timezone.now() + timedelta(days=7),
            status='scheduled'
        )

    def test_race_creation(self):
        """Test Race model creation"""
        self.assertEqual(self.race.name, 'Bahrain Grand Prix')
        self.assertEqual(self.race.round_number, 1)
        self.assertEqual(self.race.status, 'scheduled')

    def test_race_str(self):
        """Test Race string representation"""
        self.assertEqual(str(self.race), 'Bahrain Grand Prix (Round 1)')

    def test_is_betting_open_future_deadline(self):
        """Test betting is open before deadline"""
        self.race.betting_deadline = timezone.now() + timedelta(hours=1)
        self.race.status = 'scheduled'
        self.race.save()
        self.assertTrue(self.race.is_betting_open())

    def test_is_betting_closed_past_deadline(self):
        """Test betting is closed after deadline"""
        self.race.betting_deadline = timezone.now() - timedelta(hours=1)
        self.race.save()
        self.assertFalse(self.race.is_betting_open())

    def test_is_betting_closed_completed_race(self):
        """Test betting is closed for completed races"""
        self.race.status = 'completed'
        self.race.save()
        self.assertFalse(self.race.is_betting_open())


class BetTypeModelTest(TestCase):
    """Test BetType model"""

    def setUp(self):
        self.bet_type = BetType.objects.create(
            name='Top 10 Finish',
            code='top10',
            description='Predict top 10 finishers',
            requires_positions=True,
            max_selections=10,
            is_active=True
        )

    def test_bet_type_creation(self):
        """Test BetType model creation"""
        self.assertEqual(self.bet_type.name, 'Top 10 Finish')
        self.assertEqual(self.bet_type.code, 'top10')
        self.assertTrue(self.bet_type.requires_positions)
        self.assertEqual(self.bet_type.max_selections, 10)

    def test_bet_type_str(self):
        """Test BetType string representation"""
        self.assertEqual(str(self.bet_type), 'Top 10 Finish')


class BetModelTest(TestCase):
    """Test Bet model"""

    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='racer',
            email='racer@example.com',
            password='pass123'
        )

        # Create competition
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.competition = Competition.objects.create(
            name='F1 2025',
            year=2025,
            status='active',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=300),
            created_by=admin
        )

        # Create race
        self.race = Race.objects.create(
            competition=self.competition,
            name='Bahrain GP',
            round_number=1,
            race_datetime=timezone.now() + timedelta(days=7),
            betting_deadline=timezone.now() + timedelta(days=7),
            status='scheduled'
        )

        # Create driver
        self.driver = Driver.objects.create(
            driver_number=44,
            first_name='Lewis',
            last_name='Hamilton',
            team='Mercedes'
        )

        # Create bet type
        self.bet_type = BetType.objects.create(
            name='Top 10',
            code='top10',
            requires_positions=True,
            max_selections=10
        )

        # Create bet
        self.bet = Bet.objects.create(
            user=self.user,
            race=self.race,
            bet_type=self.bet_type,
            driver=self.driver,
            predicted_position=1
        )

    def test_bet_creation(self):
        """Test Bet model creation"""
        self.assertEqual(self.bet.user, self.user)
        self.assertEqual(self.bet.race, self.race)
        self.assertEqual(self.bet.driver, self.driver)
        self.assertEqual(self.bet.predicted_position, 1)
        self.assertFalse(self.bet.is_scored)
        self.assertEqual(self.bet.points_earned, 0)

    def test_bet_str(self):
        """Test Bet string representation"""
        expected = 'racer - Bahrain GP - Lewis Hamilton (P1)'
        self.assertEqual(str(self.bet), expected)

    def test_bet_scoring(self):
        """Test bet scoring"""
        self.bet.points_earned = 10
        self.bet.is_scored = True
        self.bet.save()
        self.assertEqual(self.bet.points_earned, 10)
        self.assertTrue(self.bet.is_scored)


class RaceResultModelTest(TestCase):
    """Test RaceResult model"""

    def setUp(self):
        # Create competition
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        competition = Competition.objects.create(
            name='F1 2025',
            year=2025,
            status='active',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=300),
            created_by=admin
        )

        # Create race
        self.race = Race.objects.create(
            competition=competition,
            name='Bahrain GP',
            round_number=1,
            race_datetime=timezone.now(),
            betting_deadline=timezone.now(),
            status='completed'
        )

        # Create driver
        self.driver = Driver.objects.create(
            driver_number=1,
            first_name='Max',
            last_name='Verstappen',
            team='Red Bull Racing'
        )

        # Create result
        self.result = RaceResult.objects.create(
            race=self.race,
            driver=self.driver,
            position=1,
            grid_position=1,
            fastest_lap=True,
            verified=True
        )

    def test_race_result_creation(self):
        """Test RaceResult model creation"""
        self.assertEqual(self.result.race, self.race)
        self.assertEqual(self.result.driver, self.driver)
        self.assertEqual(self.result.position, 1)
        self.assertTrue(self.result.fastest_lap)
        self.assertTrue(self.result.verified)

    def test_race_result_str(self):
        """Test RaceResult string representation"""
        expected = 'Bahrain GP - P1: Max Verstappen'
        self.assertEqual(str(self.result), expected)

    def test_dnf_result(self):
        """Test DNF race result"""
        dnf_driver = Driver.objects.create(
            driver_number=55,
            first_name='Carlos',
            last_name='Sainz',
            team='Ferrari'
        )
        dnf_result = RaceResult.objects.create(
            race=self.race,
            driver=dnf_driver,
            position=20,
            grid_position=3,
            did_not_finish=True,
            dnf_reason='Engine failure'
        )
        self.assertTrue(dnf_result.did_not_finish)
        self.assertEqual(dnf_result.dnf_reason, 'Engine failure')


class CompetitionStandingModelTest(TestCase):
    """Test CompetitionStanding model"""

    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='racer',
            email='racer@example.com',
            password='pass123'
        )

        # Create competition
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.competition = Competition.objects.create(
            name='F1 2025',
            year=2025,
            status='active',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=300),
            created_by=admin
        )

        # Create standing
        self.standing = CompetitionStanding.objects.create(
            competition=self.competition,
            user=self.user,
            rank=1,
            total_points=50,
            races_predicted=3,
            exact_predictions=5
        )

    def test_standing_creation(self):
        """Test CompetitionStanding model creation"""
        self.assertEqual(self.standing.user, self.user)
        self.assertEqual(self.standing.competition, self.competition)
        self.assertEqual(self.standing.rank, 1)
        self.assertEqual(self.standing.total_points, 50)
        self.assertEqual(self.standing.races_predicted, 3)
        self.assertEqual(self.standing.exact_predictions, 5)

    def test_standing_str(self):
        """Test CompetitionStanding string representation"""
        expected = 'F1 2025 - racer (#1 - 50 pts)'
        self.assertEqual(str(self.standing), expected)

    def test_standing_ordering(self):
        """Test standings are ordered by rank"""
        user2 = User.objects.create_user(
            username='racer2',
            email='racer2@example.com',
            password='pass123'
        )
        standing2 = CompetitionStanding.objects.create(
            competition=self.competition,
            user=user2,
            rank=2,
            total_points=30
        )

        standings = CompetitionStanding.objects.all()
        self.assertEqual(standings[0].rank, 1)
        self.assertEqual(standings[1].rank, 2)
