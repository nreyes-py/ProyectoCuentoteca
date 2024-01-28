from django.urls import path
from .views import *
from CuentoApp import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', index, name='index'),
    path("acerca-de-mi/", acerca_de_mi, name="acerca_de_mi"),
    path('login/', LoginView.as_view(template_name='CuentoApp/sesion/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('registro/', views.registro, name='registro'),
    path("agregar-avatar", views.modificacion_avatar, name="agregar_avatar"),
    path("editar-perfil/", views.edicion_perfil, name="editar_perfil"),
    path('cuentos/', CuentoListView.as_view(), name='cuento-list'),
    path('cuento/<int:pk>/', CuentoDetailView.as_view(), name='cuento-detail'),
    path('cuento/crear/', CuentoCreate.as_view(), name='cuento-create'),
    path('cuento/<int:pk>/editar/', CuentoUpdate.as_view(), name='cuento-update'),
    path('cuento/<int:pk>/eliminar/', CuentoDelete.as_view(), name='cuento-delete'),
    path('autores/', AutorListView.as_view(), name='autor-list'),
    path('autor/<int:pk>/', AutorDetailView.as_view(), name='autor-detail'),
    path('autor/crear/', AutorCreate.as_view(), name='autor-create'),
    path('autor/<int:pk>/editar/', AutorUpdate.as_view(), name='autor-update'),
    path('autor/<int:pk>/eliminar/', AutorDelete.as_view(), name='autor-delete'),
    path('editoriales/', EditorialListView.as_view(), name='editorial-list'),
    path('editorial/<int:pk>/', EditorialDetailView.as_view(), name='editorial-detail'),
    path('editorial/crear/', EditorialCreate.as_view(), name='editorial-create'),
    path('editorial/<int:pk>/editar/', EditorialUpdate.as_view(), name='editorial-update'),
    path('editorial/<int:pk>/eliminar/', EditorialDelete.as_view(), name='editorial-delete'),
    # Añadir aquí otras rutas si son necesarias
]

