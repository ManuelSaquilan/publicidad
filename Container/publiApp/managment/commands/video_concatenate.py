from django.core.management.base import BaseCommand
from views import video_list

class Command(BaseCommand):
    help = 'Concatena los videos de los clientes'

    def handle(self, *args, **options):
        video_list(None)
        self.stdout.write(self.style.SUCCESS('Concatenación de videos completada'))