from django.urls import path
from .views import EstudianteListCreateView, EstudianteDetailView, EstudianteSearchView

urlpatterns = [
    path('estudiantes/', EstudianteListCreateView.as_view(), name='estudiante-list-create'),
    path('estudiantes/<int:pk>/', EstudianteDetailView.as_view(), name='estudiante-detail'),
    path('estudiantes/search/', EstudianteSearchView.as_view(), name='estudiante-search'),
]
