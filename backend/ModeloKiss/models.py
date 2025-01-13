# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class EmpresaContratista(models.Model):
    id_emp_con = models.AutoField(primary_key=True, db_comment='\r\nID EMPRESA CONTRATISTA')
    rut_emp_con = models.CharField(unique=True, max_length=25, db_comment='RUT EMPRESA CONTRATISTA')
    nombre_emp_con = models.CharField(max_length=255, db_comment='NOMBRE EMEPRESA CONTRATISTA')
    correo_emp_con = models.CharField(max_length=255, db_comment='CORREO EMPRESA CONTRATISTA')
    status_emp_con = models.IntegerField(db_comment='0 DESACTIVADO\r\n1 ACTIVADO')

    class Meta:
        managed = False
        db_table = 'empresa_contratista'


class EmpresaPrincipal(models.Model):
    id_emp_pri = models.AutoField(primary_key=True, db_comment='ID Empresa Principal')
    rut_emp_pri = models.CharField(unique=True, max_length=25, db_comment='RUT EMPRESA Principal')
    nombre_emp_pri = models.CharField(max_length=255, db_comment='NOMBRE EMPRESA PRINCIPAL')
    correo_emp_pri = models.CharField(max_length=255, db_comment='CORREO EMPRESA PRINCIPAL')
    status_emp_pri = models.IntegerField(db_comment='0 DESACTIVADA\r\n1 ACTIVADA')

    class Meta:
        managed = False
        db_table = 'empresa_principal'


class EmpresaSubcontratista(models.Model):
    id_emp_subcon = models.AutoField(primary_key=True, db_comment='ID EMPRESA SUBCONTRATISTA')
    rut_emp_subcon = models.CharField(unique=True, max_length=25, db_comment='RUT EMPRESA SUBCONTRATISTA')
    nombre_emp_subcon = models.CharField(max_length=255, db_comment='NOMBRE EMPRESA SUBCONTRATISTA')
    correo_emp_subcon = models.CharField(max_length=255, db_comment='CORREO EMPRESA SUBCONTRATISTA')
    status_emp_subcon = models.IntegerField(db_comment='0 DESACTIVADO\r\n1 ACTIVADO')

    class Meta:
        managed = False
        db_table = 'empresa_subcontratista'


class EmpresasUnidas(models.Model):
    id_emp_uni = models.AutoField(primary_key=True, db_comment='ID EMPRESAS UNIDAS')
    rut_emp_pri = models.ForeignKey(EmpresaPrincipal, models.DO_NOTHING, db_column='rut_emp_pri', to_field='rut_emp_pri', db_comment='RUT EMPRESA PRINCIPAL')
    rut_emp_con = models.ForeignKey(EmpresaContratista, models.DO_NOTHING, db_column='rut_emp_con', to_field='rut_emp_con', db_comment='RUT EMPRESA CONTRATISTA')
    rut_emp_subcon = models.ForeignKey(EmpresaSubcontratista, models.DO_NOTHING, db_column='rut_emp_subcon', to_field='rut_emp_subcon', blank=True, null=True, db_comment='RUT EMPRESA SUBCONTRATISTA')

    class Meta:
        managed = False
        db_table = 'empresas_unidas'


class Periodo(models.Model):
    id_periodo = models.AutoField(primary_key=True, db_comment='ID PERIODO')
    mesanio_periodo = models.IntegerField(db_comment='ANIO Y MES EJEM 202404')
    minimo_imponible_periodo = models.IntegerField(db_comment='MINIMO IMPONIBLE POR PERIODOS')
    maximo_imponible_periodo = models.IntegerField(db_comment='MAXIMO IMPONIBLE POR PERIODOS')
    status_periodo = models.IntegerField(db_comment='0 DESACTIVADO\r\n1 ACTIVADO')

    class Meta:
        managed = False
        db_table = 'periodo'


class Solicitud(models.Model):
    id_sol = models.AutoField(primary_key=True, db_comment='ID SOLICITUD')
    id_emp_uni = models.ForeignKey(EmpresasUnidas, models.DO_NOTHING, db_column='id_emp_uni', db_comment='ID EMPRESAS UNIDAS')
    nombre_contrato_sol = models.CharField(max_length=255, db_comment='NOMBRE CONTRATO PROYECTO SOLICITUD')
    cant_trab_acreditar_sol = models.IntegerField(db_comment='CANTIDAD TRABAJADORES CERTIFICAR SOLICITUD')
    total_trab_sol = models.IntegerField(db_comment='CANTIDAD TOTALES DE LA EMPRESA ')
    estado_certificacion_sol = models.CharField(max_length=14, db_comment='ESTADO CERTIFICACION')
    id_periodo = models.ForeignKey(Periodo, models.DO_NOTHING, db_column='id_periodo', db_comment='ID PERIODO')

    class Meta:
        managed = False
        db_table = 'solicitud'


class Trabajadores(models.Model):
    id_trabajador = models.AutoField(primary_key=True, db_comment='ID TRABAJADOR')
    rut_trabajador = models.CharField(max_length=25, db_comment='RUT TRABAJADOR')
    nombre_trabajador = models.CharField(max_length=25, db_comment='NOMBRE TRABAJADOR')
    apaterno_trabajador = models.CharField(max_length=25, db_comment='APELLIDO PATERNO TRABAJADOR')
    amaterno_trabajador = models.CharField(max_length=25, db_comment='APELLIDO MATERNO TRABAJADOR')
    id_sol = models.ForeignKey(Solicitud, models.DO_NOTHING, db_column='id_sol', db_comment='ID SOLICITUD')

    class Meta:
        managed = False
        db_table = 'trabajadores'
