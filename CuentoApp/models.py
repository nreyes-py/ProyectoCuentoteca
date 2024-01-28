from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to="autores_fotos/", blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Cuento(models.Model):
    titulo = models.CharField(max_length=200)
    sinopsis = models.TextField()
    texto_completo = models.TextField()
    fecha_publicacion = models.DateField(default=now)
    autores = models.ManyToManyField(Autor, related_name='autores')
    imagen_portada = models.ImageField(upload_to="cuentos_portadas/", blank=True, null=True)

    def __str__(self):
        return self.titulo

    # def get_absolute_url(self):
    #     return reverse('cuento-detail', kwargs={'pk': self.pk})

class Editorial(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    sitio_web = models.URLField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to="editoriales_logos/", blank=True, null=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('editorial-detail', kwargs={'pk': self.pk})

class Avatar(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    imagen = models.ImageField(upload_to="avatares/")

    def __str__(self):
        return f"Avatar de {self.usuario.username}"
    
