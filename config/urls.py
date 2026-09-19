from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cityFlow.views import (
    UserViewSet, UserProfileViewSet, DistrictViewSet, TagViewSet,
    IncidentReportViewSet, WaterConsumptionViewSet,
    AirQualityViewSet, TourismPressureViewSet
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", UserProfileViewSet, basename="profile")
router.register(r"districts", DistrictViewSet, basename="district")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"incidents", IncidentReportViewSet, basename="incident")
router.register(r"water-consumption", WaterConsumptionViewSet, basename="water-consumption")
router.register(r"air-quality", AirQualityViewSet, basename="air-quality")
router.register(r"tourism-pressure", TourismPressureViewSet, basename="tourism-pressure")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]