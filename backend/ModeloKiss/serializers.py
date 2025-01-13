from rest_framework import serializers
from .models import EmpresaContratista, EmpresaPrincipal, EmpresaSubcontratista, EmpresasUnidas, Periodo, Solicitud, Trabajadores

# Serializers para los modelos

class EmpresaContratistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaContratista
        fields = ['id_emp_con', 'rut_emp_con', 'nombre_emp_con', 'correo_emp_con', 'status_emp_con']

class EmpresaPrincipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaPrincipal
        fields = ['id_emp_pri', 'rut_emp_pri', 'nombre_emp_pri', 'correo_emp_pri', 'status_emp_pri']

class EmpresaSubcontratistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaSubcontratista
        fields = ['id_emp_subcon', 'rut_emp_subcon', 'nombre_emp_subcon', 'correo_emp_subcon', 'status_emp_subcon']

class EmpresasUnidasSerializer(serializers.ModelSerializer):
    rut_emp_pri = EmpresaPrincipalSerializer()
    rut_emp_con = EmpresaContratistaSerializer()
    rut_emp_subcon = EmpresaSubcontratistaSerializer(allow_null=True)

    class Meta:
        model = EmpresasUnidas
        fields = ['id_emp_uni', 'rut_emp_pri', 'rut_emp_con', 'rut_emp_subcon']

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id_periodo', 'mesanio_periodo', 'minimo_imponible_periodo', 'maximo_imponible_periodo', 'status_periodo']

class SolicitudSerializer(serializers.ModelSerializer):
    id_emp_uni = EmpresasUnidasSerializer()
    id_periodo = PeriodoSerializer()

    class Meta:
        model = Solicitud
        fields = ['id_sol', 'id_emp_uni', 'nombre_contrato_sol', 'cant_trab_acreditar_sol', 'total_trab_sol', 'estado_certificacion_sol', 'id_periodo']

class TrabajadoresSerializer(serializers.ModelSerializer):
    id_sol = SolicitudSerializer()

    class Meta:
        model = Trabajadores
        fields = ['id_trabajador', 'rut_trabajador', 'nombre_trabajador', 'apaterno_trabajador', 'amaterno_trabajador', 'id_sol']



