Para ejecutar la función video_list una vez por semana, puedes crear un comando de gestión personalizado y programarlo utilizando un programador de tareas como cron en Linux o Task Scheduler en Windows.

Crea un comando de gestión personalizado:
Crea un archivo video_concatenate.py dentro de la carpeta management/commands de tu aplicación PubliApp:

PubliApp/management/commands/video_concatenate.py


from django.core.management.base import BaseCommand
from PubliApp.views import video_list

class Command(BaseCommand):
    help = 'Concatena los videos de los clientes'

    def handle(self, *args, **options):
        video_list(None)
        self.stdout.write(self.style.SUCCESS('Concatenación de videos completada'))

//////////////////////////////

Yo en mi proyecto estoy utilizando un pluging llamado django-cron.

Basicamente este pluging se basa en que crear una tarea y puedes decirle que se ejecute cada X minutos o a una hora en concreto.

También puedes forzar la ejecución de los crons desde el manage para que comprobar si se está ejecutando correctamente.

Ejemplo
from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        pass    # do your thing here

        //////

superusaurio: manuel
nombre: Manuel Saquilan
mail: manuel.saquilan@gmail.com
pass: Cali2021++


linea borrada en base_template

<script>
        
        setInterval(function() {
            $.ajax({
                type: 'GET',
                url: '{% url "publicidad:ping_view" %}',
                success: function(data) {
                    console.log('Ping sent!');
                }
            });
        }, 60000); // 1 minuto
        
    </script>