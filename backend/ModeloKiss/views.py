from rest_framework import generics
from .models import EmpresaContratista, EmpresaPrincipal, EmpresaSubcontratista, EmpresasUnidas, Periodo, Solicitud, Trabajadores
from .serializers import EmpresaContratistaSerializer, EmpresaPrincipalSerializer, EmpresaSubcontratistaSerializer, EmpresasUnidasSerializer, PeriodoSerializer, SolicitudSerializer, TrabajadoresSerializer
from django.http import JsonResponse
from .models import Trabajadores, EmpresaContratista, EmpresaPrincipal, Solicitud
from django.db.models import Q
from django.apps import apps
from django.core.exceptions import FieldError
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Vistas para cada modelo

class EmpresaContratistaList(generics.ListCreateAPIView):
    queryset = EmpresaContratista.objects.all()
    serializer_class = EmpresaContratistaSerializer

class EmpresaPrincipalList(generics.ListCreateAPIView):
    queryset = EmpresaPrincipal.objects.all()
    serializer_class = EmpresaPrincipalSerializer

class EmpresaSubcontratistaList(generics.ListCreateAPIView):
    queryset = EmpresaSubcontratista.objects.all()
    serializer_class = EmpresaSubcontratistaSerializer

class EmpresasUnidasList(generics.ListCreateAPIView):
    queryset = EmpresasUnidas.objects.all()
    serializer_class = EmpresasUnidasSerializer

class PeriodoList(generics.ListCreateAPIView):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer

class SolicitudList(generics.ListCreateAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

class TrabajadoresList(generics.ListCreateAPIView):
    queryset = Trabajadores.objects.all()
    serializer_class = TrabajadoresSerializer


def obtener_tablas_campos(request):
    model_names = apps.get_models()
    tables_info = []

    for model in model_names:
        table_name = model._meta.db_table
        fields = [field.name for field in model._meta.get_fields()]
        tables_info.append({'table': table_name, 'fields': fields})

    return JsonResponse(tables_info, safe=False)

from django.http import JsonResponse
from django.db.models import Q
from .models import Trabajadores

from django.http import JsonResponse
from django.db.models import Q
from .models import Trabajadores


from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import FieldError

from django.db.models import Q
from django.core.exceptions import FieldError
from django.http import JsonResponse

from django.core.exceptions import FieldError

def consulta_trabajadores(request):
    filtros = request.GET.get('filtros', None)
    tabla = request.GET.get('tabla', None)
    campos = request.GET.get('campos', '')

    # Validar si se especificó la tabla
    if not tabla:
        return JsonResponse({'error': 'El parámetro "tabla" es obligatorio.'}, status=400)

    # Listado de tablas válidas
    tablas_validas = {
        'trabajadores': Trabajadores,
        'empresa_principal': EmpresaPrincipal,
        'empresa_contratista': EmpresaContratista,
        'solicitud': Solicitud,
        'periodo': Periodo,
        'empresa_subcontratista': EmpresaSubcontratista,
        'empresas_unidas': EmpresasUnidas,
    }

    if tabla not in tablas_validas:
        return JsonResponse({'error': 'Tabla no válida.'}, status=400)

    modelo = tablas_validas[tabla]

    # Procesar campos relacionados
    campos_mapeados = procesar_campos(request)

    # Construir filtro dinámico
    filtro_q = Q()
    if filtros:
        try:
            filtros_dict = dict(f.split('=') for f in filtros.split('&') if '=' in f)
            for campo, valor in filtros_dict.items():
                valores = [v.strip() for v in valor.split(',')]
                filtro_q &= Q(**{f"{campo}__in": valores})
        except ValueError:
            return JsonResponse({'error': 'Formato inválido en filtros.'}, status=400)

    # Filtrar datos y excluir relaciones nulas
    try:
        queryset = (
            modelo.objects.filter(filtro_q)
            .exclude(**{f"{campo}__isnull": True for campo in CAMPOS_RELACIONADOS.values()})
            .select_related(*[campo.split('__')[0] for campo in CAMPOS_RELACIONADOS.values() if '__' in campo])
            .values(*campos_mapeados)
        )
    except FieldError as e:
        return JsonResponse({'error': f"Campo inválido: {str(e)}"}, status=400)

    data = list(queryset)
    return JsonResponse(data, safe=False)


CAMPOS_RELACIONADOS = {
    'id_sol': 'id_sol',  # ID de la solicitud asociada
    'nombre_contrato_sol': 'id_sol__nombre_contrato_sol',  # Nombre del contrato en la solicitud
    'nombre_emp_con': 'id_sol__id_emp_uni__rut_emp_con__nombre_emp_con',  # Nombre de la empresa contratista
    'nombre_emp_pri': 'id_sol__id_emp_uni__rut_emp_pri__nombre_emp_pri',  # Nombre de la empresa principal
    'nombre_emp_subcon': 'id_sol__id_emp_uni__rut_emp_subcon__nombre_emp_subcon',  # Nombre de la empresa subcontratista (opcional)
}

def procesar_campos(request):
    campos = request.GET.get('campos', '').split(',')
    campos_mapeados = []

    for campo in campos:
        if campo in CAMPOS_RELACIONADOS:
            campos_mapeados.append(CAMPOS_RELACIONADOS[campo])
        else:
            campos_mapeados.append(campo)  # Campo directo

    return campos_mapeados


