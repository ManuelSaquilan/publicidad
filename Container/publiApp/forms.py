from django import forms

from .models import Cliente, Contrato, Pagos
from datetime import timedelta

class ClientesForm(forms.ModelForm):
    """ Formulario de creación de Clientes 
    
    Variables: 

        password1:
        password2:
    
    """

    
    class Meta:
        model = Cliente
        fields = ["username","nombre", "email","video"]

        labels = {"username":"Nombre de Usuario","nombre": "Nombre del Cliente", "email": "Correo Electrónico","video":"video"}

        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control','style':'width:300px'}),
            "nombre": forms.TextInput(attrs={'class': 'form-control','style':'width:300px'}),
            "email": forms.EmailInput(attrs={'class': 'form-control','style':'width:300px','placeholder':'correo electrónico'}),
            "video": forms.FileInput(attrs={'class': 'form-control','style':'width:200'})
        }

    password1 = forms.CharField(label='contraseña', widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'style':'width:300px',
               'placeholder':'Ingrese su contraseña',
               'id':'password1',
               'required':'required'}))
    password2 = forms.CharField(label='confirma contraseña', widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'style':'width:300px',
               'placeholder':'Ingrese nuevamente su contraseña',
               'id':'password2',
               'required':'required'}))

    """def __init__(self, *args, **kwargs):
        super(ClientesForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = self.password1
        self.fields['password2'] = self.password2
    """
    def clean_password2(self):
        """" Validacion de contraseña """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self,commit = True):
        user = super(ClientesForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
"""
class PagosForm(forms.ModelForm):
    class Meta:  # Add the Meta class
        model = Pagos
        fields = ["nombre", "fechaPago", "fechaVencimiento","saldo","pago"]

        labels = {"nombre": "Cliente", "fechaPago": "Fecha de Pago",
                  "fechaVencimiento":"Fecha de Vencimiento","saldo":"A pagar", "pago": "Importe"}

        widgets = {
            "fechaPago": forms.DateInput(attrs={'class': 'form-control','type':'date','style':'width:auto'}),
            "fechaVencimiento": forms.DateInput(attrs={'class': 'form-control','type':'date','style':'width:auto'}),
            "saldo": forms.NumberInput(attrs={'class': 'form-control','style':'width:auto'}),
            "pago": forms.NumberInput(attrs={'class': 'form-control','style':'width:auto'}),
        }

    nombre = forms.ModelChoiceField(queryset=Cliente.objects.filter(usuario_administrador=False), 
                                    widget=forms.Select(attrs={'class': 'form-control','style':'width:auto'}))

    def __init__(self, *args, **kwargs):
        super(PagosForm, self).__init__(*args, **kwargs)
        self.fields['fechaVencimiento'].widget.attrs['value'] = kwargs['initial']['fecha_vencimiento']
        self.fields['saldo'].widget.attrs['value'] = kwargs['initial']['saldo']
        

    def save(self, commit=True):
        pago = super(PagosForm, self).save(commit=False)
        contrato = pago.nombre.contrato  # Obtener la instancia relacionada de Contrato
        contrato.fechaVencimientoActual = pago.fechaVencimiento + timedelta(days=30)
        pago.fechapago = pago.fechaPago
        pago.pago = pago.pago
        contrato.save()  # Guardar la instancia actualizada de Contrato
        pago.save()  # Guardar la instancia de Pago
        return pago
"""    

class ContratoForm(forms.ModelForm):
    class Meta:  # Add the Meta class
        model = Contrato
        fields = ["nombre", "fechaContrato", "fechaVencimientoActual","cuota", "dispositivos"]

        labels = {
            "nombre": "Cliente",
            "fechaContrato": "fecha de Contrato",
            "fechaVencimientoActual": "fecha de Vencimiento",
            "cuota": "Valor de Cuota",
            "dispositivos": "Cantidad de Dispositivos",
        }

        widgets = {
            "fechaContrato": forms.DateInput(attrs={'class': 'form-control','type':'date','style':'width:auto'}),
            "fechaVencimientoActual": forms.DateInput(attrs={'class': 'form-control','type':'date','style':'width:auto'}),
            "cuota": forms.NumberInput(attrs={'class': 'form-control','style':'width:auto'}),
            "dispositivos": forms.NumberInput(attrs={'class': 'form-control','style':'width:auto'}),
        }

    nombre = forms.ModelChoiceField(queryset=Cliente.objects.filter(usuario_administrador=False), 
                                    widget=forms.Select(attrs={'class': 'form-control','style':'width:auto'}))