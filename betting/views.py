from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bet, BetType, Competition, CompetitionStanding, Driver, Race, RaceResult, UserProfile
from .serializers import (
    BetCreateSerializer,
    BetSerializer,
    BetTypeSerializer,
    CompetitionSerializer,
    CompetitionStandingSerializer,
    DriverSerializer,
    RaceDetailSerializer,
    RaceResultSerializer,
    RaceSerializer,
    UserProfileSerializer,
)


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Allow read access to all, write access only to authenticated users"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for competitions"""
    queryset = Competition.objects.filter(
        status__in=['published', 'active', 'completed']
    ).select_related(
        'created_by',
        'created_by__profile'
    ).prefetch_related(
        'participants',
        'races'
    )
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def standings(self, request, pk=None):
        """Get standings/leaderboard for a competition"""
        competition = self.get_object()
        standings = CompetitionStanding.objects.filter(
            competition=competition
        ).select_related(
            'user',
            'user__profile'
        ).order_by('rank')
        serializer = CompetitionStandingSerializer(standings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def races(self, request, pk=None):
        """Get all races for a competition"""
        competition = self.get_object()
        races = competition.races.select_related('competition').all()
        serializer = RaceSerializer(races, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a competition"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        competition = self.get_object()

        if competition.status != 'published':
            return Response(
                {'error': 'Competition is not open for joining'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user in competition.participants.all():
            return Response(
                {'message': 'Already joined this competition'},
                status=status.HTTP_200_OK
            )

        competition.participants.add(request.user)

        # Create standing entry
        CompetitionStanding.objects.get_or_create(
            competition=competition,
            user=request.user
        )

        return Response(
            {'message': 'Successfully joined competition'},
            status=status.HTTP_200_OK
        )


class RaceViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for races"""
    queryset = Race.objects.select_related('competition').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RaceDetailSerializer
        return RaceSerializer

    def get_queryset(self):
        queryset = Race.objects.select_related(
            'competition',
            'competition__created_by',
            'competition__created_by__profile'
        ).prefetch_related(
            'results__driver',
            'bets__driver',
            'bets__bet_type'
        )

        # Filter by competition
        competition_id = self.request.query_params.get('competition', None)
        if competition_id:
            queryset = queryset.filter(competition_id=competition_id)

        # Filter by status
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)

        # Filter upcoming races
        upcoming = self.request.query_params.get('upcoming', None)
        if upcoming:
            queryset = queryset.filter(race_datetime__gte=timezone.now())

        return queryset

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get results for a race"""
        race = self.get_object()
        results = race.results.select_related(
            'driver',
            'race'
        ).filter(verified=True).order_by('position')
        serializer = RaceResultSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def my_bet(self, request, pk=None):
        """Get current user's bet for this race"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        race = self.get_object()
        bets = Bet.objects.select_related(
            'driver',
            'bet_type',
            'race'
        ).filter(user=request.user, race=race)
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data)


class DriverViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for drivers"""
    queryset = Driver.objects.filter(is_active=True)
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BetTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for bet types"""
    queryset = BetType.objects.filter(is_active=True)
    serializer_class = BetTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BetViewSet(viewsets.ModelViewSet):
    """API endpoint for bets"""
    serializer_class = BetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own bets"""
        return Bet.objects.select_related(
            'race',
            'race__competition',
            'driver',
            'bet_type'
        ).filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the user when creating a bet"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple bets at once (for Top 10 predictions)"""
        serializer = BetCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        race = serializer.validated_data['race']
        bet_type = serializer.validated_data['bet_type']
        predictions = serializer.validated_data['predictions']

        # Delete existing bets for this race/bet_type
        Bet.objects.filter(
            user=request.user,
            race=race,
            bet_type=bet_type
        ).delete()

        # Create new bets
        bets = []
        for pred in predictions:
            driver_id = pred['driver']
            position = pred['position']

            try:
                driver = Driver.objects.get(id=driver_id)
            except Driver.DoesNotExist:
                return Response(
                    {'error': f'Driver with id {driver_id} does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            bet = Bet(
                user=request.user,
                race=race,
                bet_type=bet_type,
                driver=driver,
                predicted_position=position
            )
            bets.append(bet)

        Bet.objects.bulk_create(bets)

        return Response(
            {'message': f'Successfully created {len(bets)} bets'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def my_bets(self, request):
        """Get all bets for the current user"""
        bets = self.get_queryset()

        # Filter by race
        race_id = request.query_params.get('race', None)
        if race_id:
            bets = bets.filter(race_id=race_id)

        # Filter by competition
        competition_id = request.query_params.get('competition', None)
        if competition_id:
            bets = bets.filter(race__competition_id=competition_id)

        serializer = self.get_serializer(bets, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for user profiles"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.select_related('user').all()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class CompetitionStandingViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for competition standings"""
    queryset = CompetitionStanding.objects.select_related(
        'competition',
        'user',
        'user__profile'
    ).all()
    serializer_class = CompetitionStandingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = CompetitionStanding.objects.select_related(
            'competition',
            'user',
            'user__profile'
        )

        # Filter by competition
        competition_id = self.request.query_params.get('competition', None)
        if competition_id:
            queryset = queryset.filter(competition_id=competition_id)

        return queryset.order_by('rank')


class RaceResultViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for race results"""
    queryset = RaceResult.objects.select_related(
        'race',
        'race__competition',
        'driver'
    ).filter(verified=True)
    serializer_class = RaceResultSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = RaceResult.objects.select_related(
            'race',
            'race__competition',
            'driver'
        ).filter(verified=True)

        # Filter by race
        race_id = self.request.query_params.get('race', None)
        if race_id:
            queryset = queryset.filter(race_id=race_id)

        return queryset.order_by('race__race_datetime', 'position')
