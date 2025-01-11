from django.core.management import BaseCommand

from src.property_finder.tasks.threads import ProcessUpdateEvents


class Command(BaseCommand):
    def handle(self, *args, **options):
        process = ProcessUpdateEvents()
        process.start()
