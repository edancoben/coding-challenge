from django.core.management.base import BaseCommand
from api.problem_2_ingestion import IngestWeatherData, IngestYieldData
from api.models import WeatherData, YieldData
import logging

# adding logging with timestamps
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # want to add the option to delete rows when running again
        if options["d"]:
            logger.info("Deleting All Rows in Weather/Yield Tables")
            WeatherData.objects.all().delete()
            YieldData.objects.all().delete()

        weather_data_ingestor = IngestWeatherData("wx_data")
        weather_data_ingestor.run()

        yield_data_ingestor = IngestYieldData("yld_data")
        yield_data_ingestor.run()

    # --d add arg
    def add_arguments(self, parser):
        parser.add_argument("--d", action="store_true")
