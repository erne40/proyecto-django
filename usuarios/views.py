from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login as django_login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
# from usuarios.models import InformacionExtra

from usuarios.forms import MiFormularioDeCreacion, EdicionDatosUsuario

# Create your views here.

def login(request):
    if request.method == 'POST':
        formulario= AuthenticationForm(request, data= request.POST) #Si llevara imágenes tendría que tener 'request.FILES'
        
        if formulario.is_valid():
            nombre_usuario = formulario.cleaned_data.get('username')
            contrasena = formulario.cleaned_data.get('password')
            usuario = authenticate(username= nombre_usuario, password= contrasena)
            django_login(request, usuario)
            
            # informacion_extra, creado = InformacionExtra.objects.get_or_create(user=request.user)
            return redirect('inicio')
        else:
            return render(request, 'usuarios/login.html', {'formulario': formulario})

    formulario= AuthenticationForm()
    return render(request, 'usuarios/login.html', {'formulario': formulario})

def registro(request):
    
    if request.method == 'POST':
        # formulario= UserCreationForm(request.POST)
        formulario= MiFormularioDeCreacion(request.POST)
        
        if formulario.is_valid():
            formulario.save()
            return redirect('usuarios:login')
        else:
            return render(request, 'usuarios/registro.html', {'formulario': formulario})
    
    # formulario = UserCreationForm()
    formulario = MiFormularioDeCreacion()
    return render(request, 'usuarios/registro.html', {'formulario': formulario})


#POTENCIALES ERRORES
@login_required
def editar_perfil(request):
    
    if request.method == 'POST':
        formulario= EdicionDatosUsuario(request.POST, instance=request.user)
        
        if formulario.is_valid():
            # if formulario.cleaned_data.get('avatar'):
                # request.user.informacionextra.avatar = formulario.cleaned_data.get(avatar)
            # request.user.informacionextra.save()
            formulario.save()
            return redirect('inicio')
        else:
            return render(request, 'usuarios/editar_perfil.html', {'formulario': formulario})
    
    formulario = EdicionDatosUsuario(instance=request.user) # De poner avatares, agregar "initial={'avatar': request.user.informacionextra.avatar}"
    return render(request, 'usuarios/editar_perfil.html', {'formulario': formulario})

class CambioContrasena(PasswordChangeView):
    template_name = 'usuarios/cambiar_contrasena.html'
    success_url= reverse_lazy('usuarios:cambiar_contrasena')