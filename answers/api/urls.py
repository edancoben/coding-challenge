from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WeatherDataViewSet, YieldDataViewSet, WeatherAnalysisViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r"weather", WeatherDataViewSet, basename="weather")
router.register(r"yield", YieldDataViewSet, basename="yield")

# stats_router = DefaultRouter(trailing_slash=False)
# stats_router.register(r"stats", WeatherAnalysisViewSet, basename="stats")
urlpatterns = [
    path("", include(router.urls)),
    # path("weather/stats/", WeatherAnalysisViewSet.as_view(actions={"get": "list"})),
]
