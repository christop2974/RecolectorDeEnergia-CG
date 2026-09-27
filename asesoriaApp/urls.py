from django.urls import path
from . import views
urlpatterns = [
    path('', views.asesoria, name='asesoria'),
    path('consejos/', views.consejos, name='consejos'),
]
