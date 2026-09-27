from django.shortcuts import render
from .models import Consejo


def asesoria(request):
    servicios = [
        'Compra de propiedades',
        'Venta de propiedades',
        'Orientación para arriendo',
        'Evaluación de alternativas',
    ]
    return render(request, 'asesoriaApp/asesoria.html', {'servicios': servicios})


def consejos(request):
    return render(request, 'asesoriaApp/consejos.html', {'consejos': Consejo.objects.filter(activo=True)})
