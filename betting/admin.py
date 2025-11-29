from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.db.models import Count, Q
from django.utils import timezone

from .models import Bet, BetType, Competition, CompetitionStanding, Driver, Race, RaceResult, UserProfile


class F1BettingAdminSite(AdminSite):
    site_header = "F1 Betting Pool Admin"
    site_title = "F1 Betting Admin"
    index_title = "Welcome to F1 Betting Pool Administration"

    def index(self, request, extra_context=None):
        """
        Override the index view to add baseline statistics
        """
        extra_context = extra_context or {}

        # User statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        superusers = User.objects.filter(is_superuser=True).count()
        total_groups = Group.objects.count()

        # Competition statistics
        total_competitions = Competition.objects.count()
        active_competitions = Competition.objects.filter(status='active').count()

        # Race statistics
        total_races = Race.objects.count()
        completed_races = Race.objects.filter(status='completed').count()
        upcoming_races = Race.objects.filter(
            status='scheduled',
            race_datetime__gte=timezone.now()
        ).count()

        # Driver statistics
        total_drivers = Driver.objects.count()
        active_drivers = Driver.objects.filter(is_active=True).count()

        # Betting statistics
        total_bets = Bet.objects.count()
        scored_bets = Bet.objects.filter(is_scored=True).count()
        unscored_bets = total_bets - scored_bets
        users_with_bets = Bet.objects.values('user').distinct().count()

        # Race results statistics
        total_results = RaceResult.objects.count()
        verified_results = RaceResult.objects.filter(verified=True).count()

        # Bet types statistics
        total_bet_types = BetType.objects.count()
        active_bet_types = BetType.objects.filter(is_active=True).count()

        # Competition standings
        total_standings = CompetitionStanding.objects.count()

        # Build statistics context
        extra_context['statistics'] = {
            'users': {
                'total': total_users,
                'active': active_users,
                'superusers': superusers,
                'groups': total_groups,
                'with_bets': users_with_bets,
            },
            'competitions': {
                'total': total_competitions,
                'active': active_competitions,
            },
            'races': {
                'total': total_races,
                'completed': completed_races,
                'upcoming': upcoming_races,
                'pending': total_races - completed_races,
            },
            'drivers': {
                'total': total_drivers,
                'active': active_drivers,
                'inactive': total_drivers - active_drivers,
            },
            'bets': {
                'total': total_bets,
                'scored': scored_bets,
                'unscored': unscored_bets,
            },
            'results': {
                'total': total_results,
                'verified': verified_results,
                'unverified': total_results - verified_results,
            },
            'bet_types': {
                'total': total_bet_types,
                'active': active_bet_types,
            },
            'standings': {
                'total': total_standings,
            },
        }

        return super().index(request, extra_context)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('display_name', 'avatar', 'total_points')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Create custom admin site instance
admin_site = F1BettingAdminSite(name='f1admin')

# Register User with custom admin
admin_site.register(User, UserAdmin)
admin_site.register(Group)


@admin.register(Competition, site=admin_site)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'status', 'start_date', 'end_date', 'created_by')
    list_filter = ('status', 'year')
    search_fields = ('name', 'description')
    filter_horizontal = ('participants',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'year', 'status')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Points Configuration', {
            'fields': ('points_for_exact_position', 'points_for_correct_driver')
        }),
        ('Management', {
            'fields': ('created_by', 'participants')
        }),
    )


@admin.register(Driver, site=admin_site)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('driver_number', 'first_name', 'last_name', 'team', 'nationality', 'is_active')
    list_filter = ('team', 'nationality', 'is_active')
    search_fields = ('first_name', 'last_name', 'team', 'driver_number')
    ordering = ('driver_number',)


@admin.register(Race, site=admin_site)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'name', 'competition', 'country', 'race_datetime', 'betting_deadline', 'status')
    list_filter = ('status', 'competition', 'country')
    search_fields = ('name', 'location', 'country')
    ordering = ('competition', 'round_number')
    fieldsets = (
        ('Race Information', {
            'fields': ('competition', 'name', 'location', 'country', 'round_number')
        }),
        ('Schedule', {
            'fields': ('race_datetime', 'betting_deadline')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('API Integration', {
            'fields': ('api_race_id',),
            'classes': ('collapse',)
        }),
    )


@admin.register(BetType, site=admin_site)
class BetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'requires_positions', 'max_selections')
    list_filter = ('is_active', 'requires_positions')
    search_fields = ('name', 'code', 'description')


@admin.register(Bet, site=admin_site)
class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'race', 'bet_type', 'driver', 'predicted_position', 'points_earned', 'is_scored')
    list_filter = ('race__competition', 'race', 'bet_type', 'is_scored')
    search_fields = ('user__email', 'driver__last_name', 'race__name')
    ordering = ('race', 'user', 'predicted_position')
    readonly_fields = ('points_earned', 'is_scored', 'created_at')


@admin.register(RaceResult, site=admin_site)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('race', 'position', 'driver', 'grid_position', 'fastest_lap', 'did_not_finish', 'verified')
    list_filter = ('race__competition', 'race', 'verified', 'fastest_lap', 'did_not_finish')
    search_fields = ('driver__last_name', 'race__name')
    ordering = ('race', 'position')
    fieldsets = (
        ('Result Information', {
            'fields': ('race', 'driver', 'position')
        }),
        ('Additional Data', {
            'fields': ('grid_position', 'fastest_lap', 'did_not_finish', 'dnf_reason')
        }),
        ('Verification', {
            'fields': ('verified',)
        }),
        ('API Integration', {
            'fields': ('api_result_id',),
            'classes': ('collapse',)
        }),
    )


@admin.register(CompetitionStanding, site=admin_site)
class CompetitionStandingAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user', 'competition', 'total_points', 'races_predicted', 'exact_predictions')
    list_filter = ('competition',)
    search_fields = ('user__email', 'competition__name')
    ordering = ('competition', '-total_points')
    readonly_fields = ('updated_at',)
