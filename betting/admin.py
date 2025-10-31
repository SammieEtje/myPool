from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    UserProfile, Competition, Driver, Race, BetType,
    Bet, RaceResult, CompetitionStanding
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('display_name', 'avatar', 'total_points')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Competition)
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


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('driver_number', 'first_name', 'last_name', 'team', 'nationality', 'is_active')
    list_filter = ('team', 'nationality', 'is_active')
    search_fields = ('first_name', 'last_name', 'team', 'driver_number')
    ordering = ('driver_number',)


@admin.register(Race)
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


@admin.register(BetType)
class BetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'requires_positions', 'max_selections')
    list_filter = ('is_active', 'requires_positions')
    search_fields = ('name', 'code', 'description')


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'race', 'bet_type', 'driver', 'predicted_position', 'points_earned', 'is_scored')
    list_filter = ('race__competition', 'race', 'bet_type', 'is_scored')
    search_fields = ('user__email', 'driver__last_name', 'race__name')
    ordering = ('race', 'user', 'predicted_position')
    readonly_fields = ('points_earned', 'is_scored', 'created_at')


@admin.register(RaceResult)
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


@admin.register(CompetitionStanding)
class CompetitionStandingAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user', 'competition', 'total_points', 'races_predicted', 'exact_predictions')
    list_filter = ('competition',)
    search_fields = ('user__email', 'competition__name')
    ordering = ('competition', '-total_points')
    readonly_fields = ('updated_at',)


# Customize admin site headers
admin.site.site_header = "F1 Betting Pool Admin"
admin.site.site_title = "F1 Betting Admin"
admin.site.index_title = "Welcome to F1 Betting Pool Administration"
