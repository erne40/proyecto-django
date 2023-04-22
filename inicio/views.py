from django.shortcuts import render

# Create your views here.
from datetime import datetime
from django.http import HttpResponse
from django.template import Template, Context, loader
from inicio.models import Animal
from django.shortcuts import render, redirect
from inicio.forms import CreacionAnimalFormulario , BuscarAnimal, ModificarAnimalFormulario

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def mi_vista(request):
    # print('Pase por aca')
    # return HttpResponse('<h1>Mi primera vista</h1>')
    return render(request, r'inicio/index.html')

# Versión con HttpResponse:
""" def mostrar_fecha(request):
    dt = datetime.now()
    dt_formateado = dt.strftime("%A %d %B %Y %I:%M")
    return HttpResponse (f'<p>{dt_formateado}</p>') """

def saludar(request, nombre, apellido):
    return HttpResponse(f'<h1>Hola {nombre} {apellido}</h1>')

def mi_primer_template(request):   
    archivo = open(r'C:\Users\ernes\OneDrive\Escritorio\Proyectos\proyecto-django\templates\mi_primer_template.html', 'r')
    template = Template(archivo.read())
    archivo.close()
    contexto = Context()
    template_renderizado = template.render(contexto)
    return HttpResponse(template_renderizado)

# Versión con Template:
def mostrar_fecha(request):
    dt = datetime.now()
    dt_formateado = dt.strftime("%A %d %B %Y %I:%M")
    
    """ archivo = open(r'mostrar_fecha.html', 'r')
    template = Template(archivo.read())
    archivo.close() """
    template = loader.get_template(r'inicio/mostrar_fecha.html')
    
    datos = {'fecha': dt_formateado}
    
    """ contexto = Context({'fecha': dt_formateado})
    template_renderizado = template.render(contexto) """
    
    template_renderizado = template.render({'fecha': dt_formateado})
     
    return HttpResponse(template_renderizado)

def prueba_template(request):
    
    datos = {
        'nombre': 'Pepito',
        'apellido': 'Grillo',
        'edad': 25,
        'años': [
            1995, 2004, 2014, 2017, 2021, 2022
        ]
        }
    
    template = loader.get_template(r'inicio/prueba_template.html')
    template_renderizado = template.render(datos)
    return HttpResponse(template_renderizado)

@login_required
def prueba_render(request):
    datos = {'nombre': 'Pepe'}
    # template = loader.get_template(r'prueba_render.html')
    # template_renderizado = template.render(datos)
    # return HttpResponse(template_renderizado)

    return render(request, r'inicio/prueba_render.html', datos)

# ----------------------
# Vistas comunes para animales
# ----------------------

#v1
""" def crear_animal(request):
    animal = Animal(nombre='Ricardito', edad=3)
    print(animal.nombre)
    print(animal.edad)
    animal.save()
    datos = {'animal':animal}
    template = loader.get_template(r'inicio/crear_animal.html')
    template_renderizado = template.render(datos)
    return HttpResponse(template_renderizado) """

#v2
""" def crear_animal(request):
    # print(type(request))
    # rint(type(request.POST))
    # print(request.POST)
    if request.method == "POST":
        animal = Animal(nombre= request.POST['nombre'], edad=request.POST['edad'])
        animal.save()
    return render(request, 'inicio/crear_animal_v2.html') """

#v3
def crear_animal(request):
    if request.method == "POST":
        formulario = CreacionAnimalFormulario(request.POST)
        
        if formulario.is_valid():
            datos_correctos = formulario.cleaned_data
            
            animal = Animal(nombre= datos_correctos['nombre'], edad= datos_correctos['edad'])
            animal.save()
            
            return redirect('lista_animales')
            
    formulario = CreacionAnimalFormulario()
    return render(request, 'inicio/crear_animal_v3.html', {'formulario': formulario})

def lista_animales(request):
    nombre_a_buscar = request.GET.get('nombre', None)
    
    #Deprecado
    """ if nombre_a_buscar:
        animales = Animal.objects.filter()
    else:
        animales = Animal.objects.all(nombre__icontains=nombre_a_buscar) """
    
    #Versión buena
    if nombre_a_buscar:
        animales = Animal.objects.filter(nombre__icontains=nombre_a_buscar)
    else:
        animales = Animal.objects.all()
    
    #animales = Animal.objects.all()
    formulario_busqueda = BuscarAnimal()
    return render(request, 'inicio/lista_animales.html', {'animales': animales, 'formulario': formulario_busqueda})

def eliminar_animal(request, id_animal):
    id_animal
    animal_a_eliminar = Animal.objects.get(id=id_animal)
    animal_a_eliminar.delete()
    return redirect('lista_animales')

def mostrar_animal(request, id_animal):
    id_animal
    animal_a_mostrar = Animal.objects.get(id=id_animal)
    return render(request, 'inicio/mostrar_animal.html', {'animal_a_mostrar': animal_a_mostrar})

def modificar_animal(request, id_animal):
    id_animal
    animal_a_modificar = Animal.objects.get(id=id_animal)
    if request.method == "POST":
        formulario = ModificarAnimalFormulario(request.POST)
        if formulario.is_valid():
            data_limpia = formulario.cleaned_data
            animal_a_modificar.nombre = data_limpia['nombre']
            animal_a_modificar.edad = data_limpia['edad']
            animal_a_modificar.save()
            
            return redirect('lista_animales')
        else:
            return render(request, 'inicio/modificar_animal.html', {"formulario": formulario, "id_animal": id_animal})
    
    formulario = ModificarAnimalFormulario(initial={'nombre': animal_a_modificar.nombre, 'edad': animal_a_modificar.edad})
    return render(request, 'inicio/modificar_animal.html', {"formulario": formulario, "id_animal": id_animal})

# ----------------------
# CBV (Clases Basadas en Vistas) para animales
# ----------------------

class ListaAnimales(ListView):
    model = Animal
    template_name = 'inicio/CBV/lista_animales.html'

class CrearAnimal(CreateView):
    model = Animal
    template_name = 'inicio/CBV/crear_animal_v3.html'
    success_url = '/inicio/animales/'
    fields = ['nombre', 'edad']

class ModificarAnimal(LoginRequiredMixin, UpdateView):
    model = Animal
    template_name = 'inicio/CBV/modificar_animal.html'
    success_url = '/inicio/animales/'
    fields = ['nombre', 'edad', 'cant_dientes']
    # Se puede usar:
    # form = ...

class EliminarAnimal(LoginRequiredMixin, DeleteView): # Primero debe heredar el Mixin
    model = Animal
    template_name = 'inicio/CBV/eliminar_animal.html'
    success_url = '/inicio/animales/'

class MostrarAnimal(DetailView):
    model = Animal
    template_name = 'inicio/CBV/mostrar_animal.html'
    