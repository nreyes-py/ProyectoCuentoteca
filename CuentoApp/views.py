from django.shortcuts import render, get_object_or_404, redirect
from .models import Cuento, Autor, Editorial, Avatar
from .forms import CuentoForm, AutorForm, EditorialForm, UsuarioCreacionForm, AvatarForm, User,UsuarioEdicionForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def index(request):
    # Inicializa el contexto con cuentos, autores y editoriales
    context = {
        'cuentos': Cuento.objects.all()[:3],
        'autores': Autor.objects.all()[:3],
        'editoriales': Editorial.objects.all()[:3]
    }

    if request.method == "POST":
        termino_busqueda = request.POST.get("termino_busqueda", "")
        cuentos_buscados = Cuento.objects.filter(titulo__icontains=termino_busqueda)
        context["cuentos"] = cuentos_buscados

        if not cuentos_buscados:
            context['error'] = "No se encontraron cuentos con ese título"

    return render(request, 'CuentoApp/index.html', context)


def acerca_de_mi(request):
    return render(request, "CuentoApp/acerca-de-mi.html")

# Vistas para Cuento
class CuentoListView(ListView):
    model = Cuento
    template_name = 'CuentoApp/cuentos/cuento_list.html'

class CuentoDetailView(DetailView):
    model = Cuento
    template_name = 'CuentoApp/cuentos/cuento_detail.html'

class CuentoCreate(CreateView):
    model = Cuento
    form_class = CuentoForm
    template_name = 'CuentoApp/cuentos/cuento_form.html'
    success_url = reverse_lazy('cuento-list')

    def form_valid(self, form):
        messages.success(self.request, "Cuento creado exitosamente.")
        return super().form_valid(form)

class CuentoUpdate(UpdateView):
    model = Cuento
    form_class = CuentoForm
    template_name = 'CuentoApp/cuentos/cuento_form.html'
    success_url = reverse_lazy('cuento-list')

    def form_valid(self, form):
        messages.success(self.request, "Cuento actualizado con éxito.")
        return super().form_valid(form)

class CuentoDelete(DeleteView):
    model = Cuento
    template_name = 'CuentoApp/cuentos/cuento_confirm_delete.html'
    success_url = reverse_lazy('cuento-list')

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "El cuento ha sido eliminado.")
        return super(CuentoDelete, self).delete(request, *args, **kwargs)

# Vistas para Autor
# Lista de Autores
class AutorListView(ListView):
    model = Autor
    template_name = 'CuentoApp/autores/autor_list.html'

# Detalle de un Autor
class AutorDetailView(DetailView):
    model = Autor
    template_name = 'CuentoApp/autores/autor_detail.html'

# Crear un nuevo Autor
class AutorCreate(CreateView):
    model = Autor
    form_class = AutorForm
    template_name = 'CuentoApp/autores/autor_form.html'
    success_url = reverse_lazy('autor-list')

    def form_valid(self, form):
        messages.success(self.request, "Autor creado exitosamente.")
        return super().form_valid(form)

class AutorUpdate(UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'CuentoApp/autores/autor_form.html'
    success_url = reverse_lazy('autor-list')

    def form_valid(self, form):
        messages.success(self.request, "Autor actualizado exitosamente.")
        return super().form_valid(form)

class AutorDelete(DeleteView):
    model = Autor
    success_url = reverse_lazy('autor-list')
    template_name = 'CuentoApp/autores/autor_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        autor = self.get_object()
        success_url = self.get_success_url()
        autor.delete()
        messages.success(request, "Autor eliminado exitosamente.")
        return HttpResponseRedirect(success_url)

# Vistas para Editorial
class EditorialListView(ListView):
    model = Editorial
    template_name = 'CuentoApp/editorial_list.html'

class EditorialDetailView(DetailView):
    model = Editorial
    template_name = 'CuentoApp/editorial_detail.html'

class EditorialCreate(CreateView):
    model = Editorial
    form_class = EditorialForm
    template_name = 'CuentoApp/editorial_form.html'

class EditorialUpdate(UpdateView):
    model = Editorial
    form_class = EditorialForm
    template_name = 'CuentoApp/editorial_form.html'

class EditorialDelete(DeleteView):
    model = Editorial
    success_url = reverse_lazy('editorial-list')

from django.contrib.auth import logout
def custom_logout(request):
    logout(request)
    return redirect('index')  


def registro(request):
    if request.method == "POST":
        form = UsuarioCreacionForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("username")
            form.save()
            return render(
                request, "CuentoApp/sesion/registro_confirm.html", {"user": user}
            )
    else:
        form = UsuarioCreacionForm()

    return render(request, "CuentoApp/sesion/registro.html", {"form": form})

@login_required
def modificacion_avatar(request):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=request.user)
            avatarViejo = Avatar.objects.filter(usuario=u)
            if len(avatarViejo) > 0:
                avatarViejo[0].delete()

            avatar = Avatar(usuario=u, imagen=form.cleaned_data["imagen"])
            avatar.save()

            imagen = Avatar.objects.get(usuario=request.user.id).imagen.url
            request.session["avatar"] = imagen

            return render(request, "CuentoApp/index.html")
    else:
        form = AvatarForm()
    return render(request, "CuentoApp/sesion/editar-avatar.html", {"form": form})


@login_required
def edicion_perfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UsuarioEdicionForm(request.POST)
        if form.is_valid():
            informacion = form.cleaned_data
            usuario.first_name = informacion["first_name"]
            usuario.last_name = informacion["last_name"]
            usuario.email = informacion["email"]
            usuario.save()
            return render(request, "CuentoApp/index.html")
    else:
        form = UsuarioEdicionForm(
            initial={
                "first_name": usuario.first_name,
                "last_name": usuario.last_name,
                "email": usuario.email,
            }
        )
    return render(request, "CuentoApp/sesion/editar-perfil.html", {"form": form})