from django.core.management.base import BaseCommand, CommandError
from sensors.datalogger import start_logging,stop_logging

class Command(BaseCommand):
    help = "Subscribe to the relevant MQTT sensor topics and store in database tables"

    def add_arguments(self, parser):
        # could be start or stop
        parser.add_argument("action", choices=["start","stop"],type=str)

    def handle(self, *args, **options):
        if options["action"] == "start":
            start_logging()
        elif options["action"] == "stop":
            stop_logging()


