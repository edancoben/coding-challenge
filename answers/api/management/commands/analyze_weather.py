from django.core.management.base import BaseCommand
from django.core.management import call_command
import time
from api.problem_3_analysis import analyze_weather


class Command(BaseCommand):
    def handle(self, *args, **options):

        start = time.time()
        # call_command("ingest_data", d=True)
        # run ingest data first?
        analyze_weather()
        # run sql query
        # maybe include a version where I do the reading in of data from pandas and save it all together
        end = time.time()
        print("elapsed time: ", end - start)
