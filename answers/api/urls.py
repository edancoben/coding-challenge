from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WeatherDataViewSet, YieldDataViewSet, WeatherAnalysisViewSet


router = DefaultRouter()
router.register(r"weather", WeatherDataViewSet, basename="weather")
router.register(r"yield", YieldDataViewSet, basename="yield")
router.register(r"weather/stats", WeatherAnalysisViewSet, basename="weather/stats")
urlpatterns = [
    path("", include(router.urls)),
]
