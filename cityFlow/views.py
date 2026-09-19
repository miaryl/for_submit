from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    User, UserProfile, District, Tag,
    IncidentReport, WaterConsumption, AirQuality, TourismPressure
)
from .serializers import (
    UserSerializer, UserProfileSerializer, DistrictSerializer, TagSerializer,
    IncidentReportSerializer, WaterConsumptionSerializer,
    AirQualitySerializer, TourismPressureSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["role", "is_active"]
    search_fields = ["name", "email"]
    ordering_fields = ["id", "name", "created_at"]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by("id")
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["department"]
    search_fields = ["department", "phone_number"]
    ordering_fields = ["id", "created_at"]


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all().order_by("code")
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["code", "name"]
    ordering_fields = ["code", "name", "area_km2"]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "slug"]
    ordering_fields = ["name"]


class IncidentReportViewSet(viewsets.ModelViewSet):
    queryset = IncidentReport.objects.select_related("user", "district").prefetch_related("tags").all()
    serializer_class = IncidentReportSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "district", "tags", "user"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "status"]


class WaterConsumptionViewSet(viewsets.ModelViewSet):
    queryset = WaterConsumption.objects.select_related("district").all()
    serializer_class = WaterConsumptionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["district", "period_date"]
    search_fields = ["district__name", "district__code"]
    ordering_fields = ["consumption_m3", "period_date"]


class AirQualityViewSet(viewsets.ModelViewSet):
    queryset = AirQuality.objects.select_related("district").all()
    serializer_class = AirQualitySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["district", "period_date"]
    search_fields = ["district__name", "district__code"]
    ordering_fields = ["no2_level", "pm10_level", "period_date"]


class TourismPressureViewSet(viewsets.ModelViewSet):
    queryset = TourismPressure.objects.select_related("district").all()
    serializer_class = TourismPressureSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["district", "period_date"]
    search_fields = ["district__name", "district__code"]
    ordering_fields = ["hut_count", "avg_noise_db", "period_date"]