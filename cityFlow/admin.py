from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, UserProfile, District, Tag,
    IncidentReport, WaterConsumption, AirQuality, TourismPressure
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Perfil de Usuario"


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ["name", "email", "role", "is_active", "is_staff"]
    list_filter = ["role", "is_active", "is_staff"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Información Personal", {"fields": ["name", "role"]}),
        ("Permisos", {"fields": ["is_active", "is_staff", "is_superuser", "groups", "user_permissions"]}),
    ]
    add_fieldsets = [
        (None, {
            "classes": ["wide"],
            "fields": ["email", "name", "password", "role", "is_staff", "is_superuser"],
        }),
    ]
    search_fields = ["email", "name"]
    ordering = ["email"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "department", "phone_number", "created_at"]
    search_fields = ["user__email", "user__name", "department"]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "area_km2"]
    search_fields = ["code", "name"]
    ordering = ["code"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "district", "status", "created_at"]
    list_filter = ["status", "district", "tags"]
    search_fields = ["title", "description", "user__email"]
    ordering = ["-created_at"]


@admin.register(WaterConsumption)
class WaterConsumptionAdmin(admin.ModelAdmin):
    list_display = ["district", "consumption_m3", "period_date"]
    list_filter = ["district", "period_date"]
    ordering = ["-period_date"]


@admin.register(AirQuality)
class AirQualityAdmin(admin.ModelAdmin):
    list_display = ["district", "no2_level", "pm10_level", "period_date"]
    list_filter = ["district", "period_date"]
    ordering = ["-period_date"]


@admin.register(TourismPressure)
class TourismPressureAdmin(admin.ModelAdmin):
    list_display = ["district", "hut_count", "avg_noise_db", "period_date"]
    list_filter = ["district", "period_date"]
    ordering = ["-period_date"]