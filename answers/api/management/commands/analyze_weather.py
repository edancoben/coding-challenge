from django.core.management.base import BaseCommand
from django.core.management import call_command
import time
from api.problem_3_analysis import analyze_weather
from api.models import WeatherAnalysis
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if options["d"]:
            WeatherAnalysis.objects.all().delete()

        # run ingest data first?
        # call_command("ingest_data", d=True)

        start = time.time()
        analyze_weather()
        end = time.time()
        logger.info("elapsed time: ", end - start)

    def add_arguments(self, parser):
        parser.add_argument("--d", action="store_true")
