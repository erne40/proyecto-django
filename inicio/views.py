from django.shortcuts import render

# Create your views here.
from datetime import datetime
from django.http import HttpResponse
from django.template import Template, Context, loader
from inicio.models import Animal
from django.shortcuts import render, redirect
from inicio.forms import CreacionAnimalFormulario , BuscarAnimal

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
    
    if nombre_a_buscar:
        animales = Animal.objects.filter()
    else:
        animales = Animal.objects.all(nombre__icontains=nombre_a_buscar)
    
    animales = Animal.objects.all()
    # print(animales)
    formulario_busqueda = BuscarAnimal()
    return render(request, 'inicio/lista_animales.html', {'animales': animales, 'formulario': formulario_busqueda})

def prueba_render(request):
    datos = {'nombre': 'Pepe'}
    # template = loader.get_template(r'prueba_render.html')
    # template_renderizado = template.render(datos)
    # return HttpResponse(template_renderizado)

    return render(request, r'inicio/prueba_render.html', datos)