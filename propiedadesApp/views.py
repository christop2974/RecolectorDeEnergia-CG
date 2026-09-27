from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PropiedadForm, SolicitudVisitaForm
from .models import Propiedad, SolicitudVisita


def inicio(request):
    destacadas = Propiedad.objects.filter(destacada=True)[:3]
    if not destacadas.exists():
        destacadas = Propiedad.objects.all()[:3]
    return render(request, 'propiedades/inicio.html', {
        'destacadas': destacadas,
        'total': Propiedad.objects.count(),
    })


def propiedades(request):
    qs = Propiedad.objects.all()
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    comuna = request.GET.get('comuna', '').strip()
    operacion = request.GET.get('operacion', '').strip()

    if q:
        qs = qs.filter(Q(titulo__icontains=q) | Q(comuna__icontains=q) | Q(sector__icontains=q) | Q(descripcion__icontains=q))
    if tipo:
        qs = qs.filter(tipo=tipo)
    if comuna:
        qs = qs.filter(comuna__icontains=comuna)
    if operacion:
        qs = qs.filter(operacion=operacion)

    return render(request, 'propiedades/listado.html', {
        'propiedades': qs,
        'tipos': Propiedad.TIPO_CHOICES,
        'operaciones': Propiedad.OPERACION_CHOICES,
    })


def detalle(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        form = SolicitudVisitaForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.propiedad = propiedad
            solicitud.save()
            messages.success(request, 'Tu solicitud de visita fue registrada correctamente.')
            return redirect('detalle', pk=pk)
    else:
        form = SolicitudVisitaForm()
    return render(request, 'propiedades/detalle.html', {'propiedad': propiedad, 'form': form})


def crear(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Propiedad creada correctamente.')
            return redirect('panel')
    else:
        form = PropiedadForm()
    return render(request, 'propiedades/formulario.html', {'form': form, 'titulo': 'Agregar propiedad'})


def editar(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        form = PropiedadForm(request.POST, instance=propiedad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Propiedad modificada correctamente.')
            return redirect('panel')
    else:
        form = PropiedadForm(instance=propiedad)
    return render(request, 'propiedades/formulario.html', {'form': form, 'titulo': 'Modificar propiedad'})


def eliminar(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, 'Propiedad eliminada correctamente.')
        return redirect('panel')
    return render(request, 'propiedades/eliminar.html', {'propiedad': propiedad})


def panel(request):
    propiedades_qs = Propiedad.objects.all()
    q = request.GET.get('q', '').strip()
    if q:
        propiedades_qs = propiedades_qs.filter(Q(titulo__icontains=q) | Q(comuna__icontains=q))
    return render(request, 'propiedades/panel.html', {'propiedades': propiedades_qs})
