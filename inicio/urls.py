from django.urls import path
#from proyecto_django.views import mi_vista, mostrar_fecha, saludar, mi_primer_template, prueba_template
from inicio import views

urlpatterns = [
    path('', views.mi_vista),
    path('mostrar-fecha/', views.mostrar_fecha),
    path('saludar/<str:nombre>/<str:apellido>/', views.saludar),
    path('mi-primer-template/', views.mi_primer_template),
    path('prueba-template/', views.prueba_template),
    path('crear-animal/', views.crear_animal),
    path('prueba-render/', views.prueba_render)
]
