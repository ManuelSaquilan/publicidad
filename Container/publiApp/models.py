import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete

from django.conf import settings
import uuid

class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, nombre, password):
        if not email:
            raise ValueError('El usuario debe tener un email')

        usuario = self.model(
            username = username,
            email=email,
            nombre=nombre,
            password=password,
        )

        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, username, email, nombre, password):
        usuario = self.create_user(
            username=username,
            email=email,
            nombre=nombre,
            password=password,
            )
        usuario.usuario_administrador = True
        usuario.save(using=self._db)
        return usuario
    
    def get_by_natural_key(self, username):
        return self.get(username=username)

class Cliente(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField('Nombre de usuario',unique=True, max_length=100)
    nombre = models.CharField(max_length=100,verbose_name='Nombre',null=False,unique=True) # VERBOSE nombre de las filas en superususario #
    email = models.EmailField(max_length=254,verbose_name='Correo electrónico',null=False,unique=True)
    password = models.CharField(max_length=100,verbose_name="Contraseña",null=False)
    video = models.FileField(upload_to='videos/',null=True,blank=True)
    activo = models.BooleanField(verbose_name='Activo',null=True,default=True)
    usuario_administrador = models.BooleanField(default= False)
    connection_count = models.IntegerField(default=0)
    last_activity = models.DateTimeField(default=timezone.now)
    last_ping = models.DateTimeField(default=timezone.now)
    objects = UsuarioManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['nombre','email','password']

    def __str__(self):
        #fila = "Nombre: "+" - "+ str(self.nombre)+" Mail: "+ str(self.mail)+" - "+" Password "+ str(self.password)+" - "+" Activo: "+ str(self.activo)+" - "+" Deuda: "+ str(self.deuda)
        fila = self.username
        return fila
    
    def get_fields(self):
        return [
            (field.verbose_name, field.value_from_object(self))
            for field in self.__class__._meta.fields[1:]
        ]
    
    def has_perm(self,perm,ob = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador
    

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'clientes'
        ordering = ['nombre']

    

class Pagos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.ForeignKey(Cliente,on_delete=models.CASCADE,null=False, blank=False)
    fechaPago = models.DateField(null=False)
    fechaVencimiento = models.DateField(null=False)
    saldo = models.PositiveIntegerField(null=False)
    pago = models.PositiveIntegerField(null=False)

    
    def __str__(self):
        fila = "Nombre"+str(self.nombre)+" - "+"Fecha"+str(self.fechaPago)+"Fecha Vencimiento"+str(self.fechaVencimiento)+"Fecha Proximo Vencimiento"+str(self.fechaProxVencimiento)+" - "+"Pago"+str(self.pago)
        return fila
    
    def get_fields(self):
        return [
            (field.verbose_name, field.value_from_object(self))
            for field in self.__class__._meta.fields[1:]
        ]
    
    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        db_table = 'pagos'
        ordering = ['id']
    
class Contrato(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.OneToOneField(Cliente,on_delete=models.CASCADE,null=False, blank=False)
    fechaContrato = models.DateField(null=False)
    fechaVencimientoActual = models.DateField(null=False,default=datetime.date.today)
    debe = models.BooleanField(null=True,default=True)
    cuota = models.PositiveIntegerField(null=False)
    dispositivos = models.PositiveSmallIntegerField(null=False, default=3)

    def __str__(self):
        fila = "Nombre"+str(self.nombre)+" - "+"Fecha"+str(self.fechaContrato)+" - "+"Cuota"+str(self.cuota)+" - "+"Dispositivos"+str(self.dispositivos)
        return fila
    
    def get_fields(self):
        return [
            (field.verbose_name, field.value_from_object(self))
            for field in self.__class__._meta.fields[1:]
        ]

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        db_table = 'contrato'
        ordering = ['id']



        
@receiver(post_delete, sender=Session)
def session_deleted(sender, instance, **kwargs):
    # Aquí puedes agregar la lógica que necesitas
    print("La sesión ha sido eliminada")


class CustomSession(models.Model):
    session_key = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    data = models.JSONField(default=dict)  # o un campo de texto si prefieres almacenar datos serializados
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    last_activity = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        return timezone.now() > self.expires_at