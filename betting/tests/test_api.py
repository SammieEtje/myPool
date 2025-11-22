"""
Test suite for F1 Betting Pool API endpoints
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from betting.models import (
    Competition, Driver, Race, BetType, Bet, RaceResult, CompetitionStanding
)


class CompetitionAPITest(TestCase):
    """Test Competition API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True
        )
        self.competition = Competition.objects.create(
            name='F1 2025',
            year=2025,
            status='active',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=300),
            created_by=self.admin
        )

    def test_list_competitions(self):
        """Test listing competitions"""
        response = self.client.get('/api/competitions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_competition_detail(self):
        """Test getting competition detail"""
        response = self.client.get(f'/api/competitions/{self.competition.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'F1 2025')

    def test_join_competition_authenticated(self):
        """Test joining competition while authenticated"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/competitions/{self.competition.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, self.competition.participants.all())

    def test_join_competition_unauthenticated(self):
        """Test joining competition while unauthenticated fails"""
        response = self.client.post(f'/api/competitions/{self.competition.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DriverAPITest(TestCase):
    """Test Driver API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.driver = Driver.objects.create(
            driver_number=44,
            first_name='Lewis',
            last_name='Hamilton',
            team='Mercedes',
            is_active=True
        )

    def test_list_drivers(self):
        """Test listing drivers"""
        response = self.client.get('/api/drivers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_driver_detail(self):
        """Test getting driver detail"""
        response = self.client.get(f'/api/drivers/{self.driver.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['driver_number'], 44)
        self.assertEqual(response.data['first_name'], 'Lewis')


class RaceAPITest(TestCase):
    """Test Race API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
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
        self.race = Race.objects.create(
            competition=self.competition,
            name='Bahrain GP',
            round_number=1,
            race_datetime=timezone.now() + timedelta(days=7),
            betting_deadline=timezone.now() + timedelta(days=7),
            status='scheduled'
        )

    def test_list_races(self):
        """Test listing races"""
        response = self.client.get('/api/races/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_race_detail(self):
        """Test getting race detail"""
        response = self.client.get(f'/api/races/{self.race.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Bahrain GP')

    def test_filter_races_by_competition(self):
        """Test filtering races by competition"""
        response = self.client.get(f'/api/races/?competition={self.competition.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_upcoming_races(self):
        """Test filtering upcoming races"""
        response = self.client.get('/api/races/?upcoming=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class BetTypeAPITest(TestCase):
    """Test BetType API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.bet_type = BetType.objects.create(
            name='Top 10',
            code='top10',
            requires_positions=True,
            max_selections=10,
            is_active=True
        )

    def test_list_bet_types(self):
        """Test listing bet types"""
        response = self.client.get('/api/bet-types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_only_active_bet_types_shown(self):
        """Test only active bet types are shown"""
        inactive_bet_type = BetType.objects.create(
            name='Inactive',
            code='inactive',
            is_active=False
        )
        response = self.client.get('/api/bet-types/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['code'], 'top10')


class BetAPITest(TestCase):
    """Test Bet API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
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
        self.race = Race.objects.create(
            competition=self.competition,
            name='Bahrain GP',
            round_number=1,
            race_datetime=timezone.now() + timedelta(days=7),
            betting_deadline=timezone.now() + timedelta(days=7),
            status='scheduled'
        )
        self.driver = Driver.objects.create(
            driver_number=44,
            first_name='Lewis',
            last_name='Hamilton',
            team='Mercedes'
        )
        self.bet_type = BetType.objects.create(
            name='Top 10',
            code='top10',
            requires_positions=True,
            max_selections=10
        )

    def test_create_bet_authenticated(self):
        """Test creating a bet while authenticated"""
        self.client.force_authenticate(user=self.user)
        data = {
            'race': self.race.id,
            'bet_type': self.bet_type.id,
            'driver': self.driver.id,
            'predicted_position': 1
        }
        response = self.client.post('/api/bets/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bet.objects.count(), 1)

    def test_create_bet_unauthenticated(self):
        """Test creating a bet while unauthenticated fails"""
        data = {
            'race': self.race.id,
            'bet_type': self.bet_type.id,
            'driver': self.driver.id,
            'predicted_position': 1
        }
        response = self.client.post('/api/bets/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_bet_after_deadline(self):
        """Test cannot place bet after deadline"""
        self.race.betting_deadline = timezone.now() - timedelta(hours=1)
        self.race.save()

        self.client.force_authenticate(user=self.user)
        data = {
            'race': self.race.id,
            'bet_type': self.bet_type.id,
            'driver': self.driver.id,
            'predicted_position': 1
        }
        response = self.client.post('/api/bets/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_my_bets(self):
        """Test listing user's bets"""
        self.client.force_authenticate(user=self.user)

        # Create a bet
        Bet.objects.create(
            user=self.user,
            race=self.race,
            bet_type=self.bet_type,
            driver=self.driver,
            predicted_position=1
        )

        response = self.client.get('/api/bets/my_bets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_bulk_create_bets(self):
        """Test bulk creating bets for top 10"""
        self.client.force_authenticate(user=self.user)

        # Create 10 drivers
        drivers = []
        for i in range(1, 11):
            driver = Driver.objects.create(
                driver_number=i,
                first_name=f'Driver{i}',
                last_name='Test',
                team='Team'
            )
            drivers.append(driver)

        # Bulk create bets
        predictions = [
            {'driver': d.id, 'predicted_position': i+1}
            for i, d in enumerate(drivers)
        ]

        data = {
            'race': self.race.id,
            'bet_type': self.bet_type.id,
            'predictions': predictions
        }

        response = self.client.post('/api/bets/bulk_create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bet.objects.filter(user=self.user).count(), 10)


class RaceResultAPITest(TestCase):
    """Test RaceResult API endpoints"""

    def setUp(self):
        self.client = APIClient()
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
        self.race = Race.objects.create(
            competition=competition,
            name='Bahrain GP',
            round_number=1,
            race_datetime=timezone.now(),
            betting_deadline=timezone.now(),
            status='completed'
        )
        self.driver = Driver.objects.create(
            driver_number=1,
            first_name='Max',
            last_name='Verstappen',
            team='Red Bull Racing'
        )
        self.result = RaceResult.objects.create(
            race=self.race,
            driver=self.driver,
            position=1,
            verified=True
        )

    def test_list_race_results(self):
        """Test listing race results"""
        response = self.client.get('/api/race-results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_results_for_race(self):
        """Test getting results for specific race"""
        response = self.client.get(f'/api/races/{self.race.id}/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CompetitionStandingAPITest(TestCase):
    """Test CompetitionStanding API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
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
        self.standing = CompetitionStanding.objects.create(
            competition=self.competition,
            user=self.user,
            rank=1,
            total_points=50
        )

    def test_list_standings(self):
        """Test listing competition standings"""
        response = self.client.get('/api/standings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_standings_by_competition(self):
        """Test filtering standings by competition"""
        response = self.client.get(f'/api/standings/?competition={self.competition.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_standings_ordered_by_rank(self):
        """Test standings are ordered by rank"""
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        CompetitionStanding.objects.create(
            competition=self.competition,
            user=user2,
            rank=2,
            total_points=30
        )

        response = self.client.get('/api/standings/')
        self.assertEqual(response.data[0]['rank'], 1)
        self.assertEqual(response.data[1]['rank'], 2)
