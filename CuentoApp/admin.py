from django.contrib import admin
from .models import Cuento,Autor,Editorial, Avatar
# Register your models here.

admin.site.register(Cuento)
admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Avatar)