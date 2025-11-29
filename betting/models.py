from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with betting statistics"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.total_points} points"

    class Meta:
        ordering = ['-total_points']


class Competition(models.Model):
    """F1 Season/Championship"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=200, help_text="e.g., F1 2024 Championship")
    description = models.TextField(blank=True)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_competitions')
    participants = models.ManyToManyField(User, related_name='competitions', blank=True)

    # Points configuration
    points_for_exact_position = models.IntegerField(default=10, help_text="Points for predicting exact position")
    points_for_correct_driver = models.IntegerField(default=5, help_text="Points for correct driver in top 10")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.year})"

    class Meta:
        ordering = ['-year', '-start_date']


class Driver(models.Model):
    """F1 Driver"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    driver_number = models.IntegerField(unique=True)
    team = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    photo = models.URLField(blank=True, null=True)

    # API integration fields
    api_driver_id = models.CharField(max_length=50, blank=True, null=True, unique=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.driver_number} {self.first_name} {self.last_name} ({self.team})"

    class Meta:
        ordering = ['driver_number']


class Race(models.Model):
    """Individual F1 Race"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('betting_open', 'Betting Open'),
        ('betting_closed', 'Betting Closed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='races')
    name = models.CharField(max_length=200, help_text="e.g., Monaco Grand Prix")
    location = models.CharField(max_length=200, help_text="e.g., Circuit de Monaco")
    country = models.CharField(max_length=100)
    round_number = models.IntegerField(validators=[MinValueValidator(1)])

    race_datetime = models.DateTimeField()
    betting_deadline = models.DateTimeField(help_text="When betting closes for this race")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    # API integration fields
    api_race_id = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.competition.year} - Round {self.round_number}: {self.name}"

    def is_betting_open(self):
        """Check if betting is still open for this race"""
        return timezone.now() < self.betting_deadline and self.status in ['scheduled', 'betting_open']

    class Meta:
        ordering = ['competition', 'round_number']
        unique_together = ['competition', 'round_number']


class BetType(models.Model):
    """Extensible bet types for future expansion"""
    TYPE_CHOICES = [
        ('top10', 'Top 10 Finishers'),
        ('podium', 'Podium (Top 3)'),
        ('winner', 'Race Winner'),
        ('pole', 'Pole Position'),
        ('fastest_lap', 'Fastest Lap'),
        ('dnf', 'Did Not Finish'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True, choices=TYPE_CHOICES)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    requires_positions = models.BooleanField(default=True, help_text="Whether this bet type requires position ordering")
    max_selections = models.IntegerField(default=10, help_text="Maximum number of drivers to select")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']


class Bet(models.Model):
    """User's prediction for a race"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='bets')
    bet_type = models.ForeignKey(BetType, on_delete=models.CASCADE, related_name='bets')

    # For Top 10 bet: stored as JSON or related model
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='bets')
    predicted_position = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    # Scoring
    points_earned = models.IntegerField(default=0)
    is_scored = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.race.name} - P{self.predicted_position}: {self.driver}"

    class Meta:
        ordering = ['race', 'user', 'predicted_position']
        unique_together = ['user', 'race', 'bet_type', 'predicted_position']


class RaceResult(models.Model):
    """Actual race results"""
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='race_results')
    position = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(22)])

    # Additional data
    grid_position = models.IntegerField(blank=True, null=True)
    fastest_lap = models.BooleanField(default=False)
    did_not_finish = models.BooleanField(default=False)
    dnf_reason = models.CharField(max_length=200, blank=True)

    # API integration
    api_result_id = models.CharField(max_length=50, blank=True, null=True)

    verified = models.BooleanField(default=False, help_text="Admin verified result")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.race.name} - P{self.position}: {self.driver}"

    class Meta:
        ordering = ['race', 'position']
        unique_together = ['race', 'driver']


class CompetitionStanding(models.Model):
    """Overall competition standings/leaderboard"""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='standings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='standings')

    total_points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    # Statistics
    races_predicted = models.IntegerField(default=0)
    exact_predictions = models.IntegerField(default=0)
    partial_predictions = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.competition.name} - #{self.rank} {self.user.email} ({self.total_points} pts)"

    class Meta:
        ordering = ['competition', '-total_points', 'user']
        unique_together = ['competition', 'user']
