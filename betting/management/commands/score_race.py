from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Sum

from betting.models import Bet, CompetitionStanding, Race, RaceResult


class Command(BaseCommand):
    help = "Score bets for a completed race and update standings"

    def add_arguments(self, parser):
        parser.add_argument("race_id", type=int, help="ID of the race to score")

    def handle(self, *args, **options):
        race_id = options["race_id"]

        try:
            race = Race.objects.get(id=race_id)
        except Race.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Race with ID {race_id} not found"))
            return

        # Check if race has results
        results = RaceResult.objects.filter(race=race, verified=True)
        if not results.exists():
            self.stdout.write(self.style.ERROR(f"No verified results found for race: {race.name}"))
            return

        self.stdout.write(f"Scoring race: {race.name}")

        # Get all bets for this race
        bets = Bet.objects.filter(race=race, is_scored=False)

        if not bets.exists():
            self.stdout.write(self.style.WARNING("No unscored bets found for this race"))
            return

        # Create result lookup dictionary
        result_positions = {}
        for result in results:
            result_positions[result.driver_id] = result.position

        # Get competition points configuration
        competition = race.competition
        points_exact = competition.points_for_exact_position
        points_correct = competition.points_for_correct_driver

        scored_count = 0
        total_points_awarded = 0

        # Score each bet
        for bet in bets:
            driver_id = bet.driver_id
            predicted_position = bet.predicted_position

            points_earned = 0

            # Check if driver finished in top 10 (or top 20 if we allow wider predictions)
            if driver_id in result_positions:
                actual_position = result_positions[driver_id]

                # Exact position match
                if actual_position == predicted_position:
                    points_earned = points_exact
                    self.stdout.write(
                        f"  Exact match: {bet.user.email} predicted P{predicted_position} "
                        f"for {bet.driver.last_name} - {points_exact} pts"
                    )

                # Driver in top 10 but wrong position
                elif actual_position <= 10:
                    points_earned = points_correct
                    self.stdout.write(
                        f"  Partial match: {bet.user.email} got {bet.driver.last_name} in top 10 "
                        f"(P{actual_position}) - {points_correct} pts"
                    )

            # Update bet
            bet.points_earned = points_earned
            bet.is_scored = True
            bet.save()

            scored_count += 1
            total_points_awarded += points_earned

        self.stdout.write(self.style.SUCCESS(f"\nScored {scored_count} bets, awarded {total_points_awarded} total points"))

        # Update competition standings
        self.update_standings(race.competition)

        # Update race status
        race.status = "completed"
        race.save()

        self.stdout.write(self.style.SUCCESS("Race scoring complete!"))

    def update_standings(self, competition):
        """Update competition standings based on scored bets"""
        self.stdout.write("\nUpdating competition standings...")

        # Get all users who have placed bets in this competition
        users_with_bets = Bet.objects.filter(race__competition=competition).values_list("user", flat=True).distinct()

        participants = User.objects.filter(id__in=users_with_bets)

        for user in participants:
            # Calculate total points for this user in this competition
            total_points = (
                Bet.objects.filter(user=user, race__competition=competition, is_scored=True).aggregate(
                    total=Sum("points_earned")
                )["total"]
                or 0
            )

            # Count statistics
            races_predicted = Bet.objects.filter(user=user, race__competition=competition).values("race").distinct().count()

            exact_predictions = Bet.objects.filter(
                user=user, race__competition=competition, is_scored=True, points_earned=competition.points_for_exact_position
            ).count()

            partial_predictions = Bet.objects.filter(
                user=user, race__competition=competition, is_scored=True, points_earned=competition.points_for_correct_driver
            ).count()

            # Update or create standing
            standing, created = CompetitionStanding.objects.update_or_create(
                competition=competition,
                user=user,
                defaults={
                    "total_points": total_points,
                    "races_predicted": races_predicted,
                    "exact_predictions": exact_predictions,
                    "partial_predictions": partial_predictions,
                },
            )

            # Update user profile total points
            user.profile.total_points = (
                Bet.objects.filter(user=user, is_scored=True).aggregate(total=Sum("points_earned"))["total"] or 0
            )
            user.profile.save()

        # Assign ranks based on points (highest first)
        standings = CompetitionStanding.objects.filter(competition=competition).order_by("-total_points", "user__email")

        for rank, standing in enumerate(standings, start=1):
            standing.rank = rank
            standing.save()

        self.stdout.write(self.style.SUCCESS(f"Updated standings for {standings.count()} participants"))
