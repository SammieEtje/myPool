from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Bet, BetType, Competition, CompetitionStanding, Driver, Race, RaceResult, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "email", "display_name", "avatar", "total_points", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile"]


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ["id", "first_name", "last_name", "driver_number", "team", "nationality", "photo", "is_active"]


class CompetitionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    participants_count = serializers.SerializerMethodField()
    races_count = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = [
            "id",
            "name",
            "description",
            "year",
            "status",
            "start_date",
            "end_date",
            "created_by",
            "participants_count",
            "races_count",
            "points_for_exact_position",
            "points_for_correct_driver",
            "created_at",
        ]

    def get_participants_count(self, obj):
        return obj.participants.count()

    def get_races_count(self, obj):
        return obj.races.count()


class RaceSerializer(serializers.ModelSerializer):
    competition_name = serializers.CharField(source="competition.name", read_only=True)
    is_betting_open = serializers.BooleanField(read_only=True)

    class Meta:
        model = Race
        fields = [
            "id",
            "competition",
            "competition_name",
            "name",
            "location",
            "country",
            "round_number",
            "race_datetime",
            "betting_deadline",
            "status",
            "is_betting_open",
            "created_at",
        ]


class BetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetType
        fields = ["id", "name", "code", "description", "is_active", "requires_positions", "max_selections"]


class BetSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    race_name = serializers.CharField(source="race.name", read_only=True)
    driver_name = serializers.SerializerMethodField()
    bet_type_name = serializers.CharField(source="bet_type.name", read_only=True)

    class Meta:
        model = Bet
        fields = [
            "id",
            "user",
            "user_email",
            "race",
            "race_name",
            "bet_type",
            "bet_type_name",
            "driver",
            "driver_name",
            "predicted_position",
            "points_earned",
            "is_scored",
            "created_at",
        ]
        read_only_fields = ["user", "user_email", "points_earned", "is_scored", "created_at"]

    def get_driver_name(self, obj):
        return f"{obj.driver.first_name} {obj.driver.last_name}"

    def validate(self, data):
        """Validate that betting is still open for this race"""
        race = data.get("race")
        if race and not race.is_betting_open():
            raise serializers.ValidationError("Betting is closed for this race")
        return data


class BetCreateSerializer(serializers.Serializer):
    """Serializer for creating multiple bets at once (Top 10)"""

    race = serializers.PrimaryKeyRelatedField(queryset=Race.objects.all())
    bet_type = serializers.PrimaryKeyRelatedField(queryset=BetType.objects.all())
    predictions = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField()), min_length=1, max_length=10
    )

    def validate(self, data):
        race = data["race"]
        if not race.is_betting_open():
            raise serializers.ValidationError("Betting is closed for this race")

        # Validate predictions format: [{"driver": 1, "position": 1}, ...]
        predictions = data["predictions"]
        positions = set()
        drivers = set()

        for pred in predictions:
            if "driver" not in pred or "position" not in pred:
                raise serializers.ValidationError("Each prediction must have 'driver' and 'position' fields")

            position = pred["position"]
            driver = pred["driver"]

            if position in positions:
                raise serializers.ValidationError(f"Position {position} is duplicated")
            if driver in drivers:
                raise serializers.ValidationError(f"Driver {driver} is duplicated")

            positions.add(position)
            drivers.add(driver)

        return data


class RaceResultSerializer(serializers.ModelSerializer):
    driver_name = serializers.SerializerMethodField()
    race_name = serializers.CharField(source="race.name", read_only=True)

    class Meta:
        model = RaceResult
        fields = [
            "id",
            "race",
            "race_name",
            "driver",
            "driver_name",
            "position",
            "grid_position",
            "fastest_lap",
            "did_not_finish",
            "dnf_reason",
            "verified",
            "created_at",
        ]

    def get_driver_name(self, obj):
        return f"{obj.driver.first_name} {obj.driver.last_name}"


class CompetitionStandingSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_display_name = serializers.CharField(source="user.profile.display_name", read_only=True)
    competition_name = serializers.CharField(source="competition.name", read_only=True)

    class Meta:
        model = CompetitionStanding
        fields = [
            "id",
            "competition",
            "competition_name",
            "user",
            "user_email",
            "user_display_name",
            "total_points",
            "rank",
            "races_predicted",
            "exact_predictions",
            "partial_predictions",
            "updated_at",
        ]


class RaceDetailSerializer(serializers.ModelSerializer):
    """Detailed race view with results and bets"""

    competition = CompetitionSerializer(read_only=True)
    results = RaceResultSerializer(many=True, read_only=True)
    user_bets = serializers.SerializerMethodField()

    class Meta:
        model = Race
        fields = [
            "id",
            "competition",
            "name",
            "location",
            "country",
            "round_number",
            "race_datetime",
            "betting_deadline",
            "status",
            "is_betting_open",
            "results",
            "user_bets",
        ]

    def get_user_bets(self, obj):
        """Get current user's bets for this race"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            bets = obj.bets.filter(user=request.user)
            return BetSerializer(bets, many=True).data
        return []
