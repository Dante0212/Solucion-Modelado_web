from django.urls import path
from . import views
from . import models

urlpatterns = [
    path('empresa-contratista/', views.EmpresaContratistaList.as_view(), name='empresa-contratista-list'),
    path('empresa-principal/', views.EmpresaPrincipalList.as_view(), name='empresa-principal-list'),
    path('empresa-subcontratista/', views.EmpresaSubcontratistaList.as_view(), name='empresa-subcontratista-list'),
    path('empresas-unidas/', views.EmpresasUnidasList.as_view(), name='empresas-unidas-list'),
    path('periodo/', views.PeriodoList.as_view(), name='periodo-list'),
    path('solicitud/', views.SolicitudList.as_view(), name='solicitud-list'),
    path('trabajadores/', views.TrabajadoresList.as_view(), name='trabajadores-list'),
    path('api/tablas/', views.obtener_tablas_campos, name='obtener_tablas_campos'),
    path('api/consulta_trabajadores/', views.consulta_trabajadores, name='consulta_trabajadores'),

    
]

