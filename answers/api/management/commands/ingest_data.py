from django.core.management.base import BaseCommand
from api.problem_2_ingestion import IngestWeatherData, IngestYieldData
from api.models import WeatherData, YieldData


class Command(BaseCommand):
    def handle(self, *args, **options):
        if options["d"]:
            print("Deleting All Rows in Tables")
            WeatherData.objects.all().delete()
            YieldData.objects.all().delete()

        weather_data_ingestor = IngestWeatherData("wx_data")
        weather_data_ingestor.run()

        yield_data_ingestor = IngestYieldData("yld_data")
        yield_data_ingestor.run()

    def add_arguments(self, parser):
        parser.add_argument("--d", action="store_true")
