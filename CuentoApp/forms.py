from django import forms
from .models import Cuento, Autor, Editorial
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validar_longitud_minima(value):
    if len(value) < 10:
        raise ValidationError(
            _('El texto es muy corto.'),
            params={'value': value},
        )
    


class AvatarForm(forms.Form):
    imagen = forms.ImageField(label="Avatar", required=True)


class CuentoForm(forms.ModelForm):
    resumen = forms.CharField(widget=forms.Textarea, help_text="Escribe un breve resumen del cuento.")

    class Meta:
        model = Cuento
        fields = ['titulo', 'sinopsis', 'texto_completo', 'fecha_publicacion', 'autores', 'imagen_portada']
        widgets = {
            'fecha_publicacion': forms.SelectDateWidget,
            'sinopsis': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        }

    def clean_texto_completo(self):
        data = self.cleaned_data['texto_completo']
        validar_longitud_minima(data)
        return data

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellido', 'biografia', 'fecha_nacimiento', 'foto']
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'fecha_nacimiento': forms.SelectDateWidget,
        }
        help_texts = {
            'fecha_nacimiento': "Selecciona tu fecha de nacimiento.",
        }

class EditorialForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea, help_text="Descripción de la editorial.")

    class Meta:
        model = Editorial
        fields = ['nombre', 'direccion', 'telefono', 'sitio_web', 'email', 'logo', 'descripcion']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
        }

class UsuarioCreacionForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=50, required=True)
    password1 = forms.CharField(
        label="Contraseña", max_length=50, required=True, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        max_length=50,
        required=True,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {k: "" for k in fields}




class UsuarioEdicionForm(UserChangeForm):
    email = forms.EmailField(label="Email", max_length=50, required=True)
    first_name = forms.CharField(label="Nombre", max_length=50, required=False)
    last_name = forms.CharField(label="Apellido", max_length=50, required=False)
    password = None

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
        help_texts = {k: "" for k in fields}