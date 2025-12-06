from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r"competitions", views.CompetitionViewSet, basename="competition")
router.register(r"races", views.RaceViewSet, basename="race")
router.register(r"drivers", views.DriverViewSet, basename="driver")
router.register(r"bet-types", views.BetTypeViewSet, basename="bettype")
router.register(r"bets", views.BetViewSet, basename="bet")
router.register(r"profiles", views.UserProfileViewSet, basename="userprofile")
router.register(r"standings", views.CompetitionStandingViewSet, basename="standing")
router.register(r"race-results", views.RaceResultViewSet, basename="raceresult")

urlpatterns = [
    path("api/", include(router.urls)),
]
