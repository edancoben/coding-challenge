from django.core.management.base import BaseCommand
import time
from api.problem_3_analysis import analyze_weather
from api.models import WeatherAnalysis
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if options["d"]:
            logger.info("Deleting All Rows in Analysis Table")
            WeatherAnalysis.objects.all().delete()

        start = time.time()
        analyze_weather()
        end = time.time()
        logger.info(f"Process Runtime: {end - start} seconds")

    def add_arguments(self, parser):
        parser.add_argument("--d", action="store_true")
