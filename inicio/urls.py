from django.urls import path
#from proyecto_django.views import mi_vista, mostrar_fecha, saludar, mi_primer_template, prueba_template
from inicio import views

#app_name = 'inicio'

urlpatterns = [
    path('', views.mi_vista, name= 'inicio'),
    path('mostrar-fecha/', views.mostrar_fecha, name= 'mostrar_fecha'),
    path('saludar/<str:nombre>/<str:apellido>/', views.saludar, name= 'saludar'),
    path('mi-primer-template/', views.mi_primer_template, name= 'mi_primer_template'),
    path('prueba-template/', views.prueba_template, name= 'prueba_template'),
    path('prueba-render/', views.prueba_render, name= 'prueba_render'),
    
    # Animales con vistas
    # path('crear-animal/', views.crear_animal, name= 'crear_animal'),
    # path('animales/', views.lista_animales, name= 'lista_animales'),
    # path('modificar-animal/<int:id_animal>', views.modificar_animal, name= 'modificar_animal'),
    # path('eliminar-animal/<int:id_animal>', views.eliminar_animal, name= 'eliminar_animal'),
    # path('mostrar-animal/<int:id_animal>', views.mostrar_animal, name= 'mostrar_animal'),

    # Animales con CBV (Clases Basadas en Vistas)
    path('animales/', views.ListaAnimales.as_view(), name= 'lista_animales'),
    path('crear-animal/', views.CrearAnimal.as_view(), name= 'crear_animal'),
    path('modificar-animal/<int:pk>', views.ModificarAnimal.as_view(), name= 'modificar_animal'),
    path('eliminar-animal/<int:pk>', views.EliminarAnimal.as_view(), name= 'eliminar_animal'),
    path('mostrar-animal/<int:pk>', views.MostrarAnimal.as_view(), name= 'mostrar_animal'),
]
