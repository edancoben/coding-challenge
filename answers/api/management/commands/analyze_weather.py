from django.core.management.base import BaseCommand
import time


class Command(BaseCommand):
    def handle(self, *args, **options):

        start = time.time()
        # run ingest data first?
        # run sql query
        # maybe include a version where I do the reading in of data from pandas and save it all together
        end = time.time()
        print("elapsed time: ", end - start)
