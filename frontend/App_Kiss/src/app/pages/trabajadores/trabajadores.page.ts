import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../Servicios/api.service';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { CdkDragDrop } from '@angular/cdk/drag-drop'; // Importar para drag and drop
import { ReactiveFormsModule } from '@angular/forms';
import { DragDropModule } from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-trabajadores',
  templateUrl: './trabajadores.page.html',
  styleUrls: ['./trabajadores.page.scss'],
  standalone: true,
  imports: [CommonModule, IonicModule, FormsModule, ReactiveFormsModule, DragDropModule],
})
export class TrabajadoresPage implements OnInit {

  tablas: any[] = [];
  datos: any[] = [];
  tablaSeleccionada: string = '';
  camposSeleccionados: string[] = [];
  filtrosForm!: any;

  constructor(
    private apiService: ApiService,
    private fb: FormBuilder
  ) {}

  ngOnInit() {
    this.cargarTablasYCampos();
    this.filtrosForm = this.fb.group({
      nombre_trabajador: [''],
      rut_trabajador: [''],
      apaterno_trabajador: [''],
      amaterno_trabajador: [''],
      id_sol: [''],
      id_sol_id: [''],
      id_trabajador: [''],
      nombre_emp_con: [''],
    });
  }

  cargarTablasYCampos() {
    this.apiService.obtenerTablasYCampos().subscribe(
      (data) => {
        this.tablas = data;
      },
      (error) => {
        console.error('Error al obtener las tablas y campos:', error);
      }
    );
  }

  seleccionarTabla(tabla: any) {
    this.tablaSeleccionada = tabla.table;
    console.log('Tabla seleccionada:', this.tablaSeleccionada);
  }

  seleccionarCampo(campo: string) {
    if (!this.camposSeleccionados.includes(campo)) {
      this.camposSeleccionados = [...new Set([...this.camposSeleccionados, campo])];
      this.agregarCampoAlFormulario(campo);
    }
    console.log('Campos seleccionados:', this.camposSeleccionados);
  }

  toggleCampo(campo: string) {
    const index = this.camposSeleccionados.indexOf(campo);
    if (index > -1) {
      this.camposSeleccionados.splice(index, 1);
      this.eliminarCampoDelFormulario(campo);
    } else {
      this.camposSeleccionados.push(campo);
      this.agregarCampoAlFormulario(campo);
    }
  }

  agregarCampoAlFormulario(campo: string) {
    const camposConRelaciones = [
      ('')
    ];

    let campoFinal = campo;

    // Añadimos '__' si el campo es una relación
    if (camposConRelaciones.includes(campo)) {
      campoFinal = `${campo}__`;
      console.log(`Campo con relación detectado: ${campoFinal}`);
    } else {
      console.log(`Campo sin relación: ${campoFinal}`);
    }

    // Verificamos si el campo ya existe en el formulario antes de añadirlo
    if (!this.filtrosForm.get(campoFinal)) {
      this.filtrosForm.addControl(campoFinal, this.fb.control(''));
      console.log(`Campo añadido al formulario: ${campoFinal}`);
    } else {
      console.log(`El campo ${campoFinal} ya existe en el formulario.`);
    }

    // Aseguramos que el campo no se agregue a camposSeleccionados más de una vez
    if (!this.camposSeleccionados.includes(campoFinal)) {
      this.camposSeleccionados.push(campoFinal);
    }
  }




  eliminarCampoDelFormulario(campo: string) {
    this.filtrosForm.removeControl(campo);
  }

  obtenerFiltros() {
    const filtros: any = {};

    // Iteramos sobre todos los campos seleccionados
    this.camposSeleccionados.forEach(campo => {
      const valorFiltro = this.filtrosForm.get(campo)?.value;
      console.log('Valor del filtro para', campo, ':', valorFiltro); // Asegúrate de que el valor no sea null o undefined
      if (valorFiltro) { // Asegúrate de que el filtro tenga un valor
        filtros[campo] = valorFiltro;
      }
    });

    console.log('Filtros generados:', filtros); // Verifica el contenido de los filtros
    return filtros;
  }

  cargarDatos() {
    if (!this.tablaSeleccionada || this.camposSeleccionados.length === 0) {
      console.error('Debe seleccionar una tabla y al menos un campo.');
      return;
    }

    // Asegúrate de eliminar cualquier campo innecesario
    const camposSinDuplicados = Array.from(new Set(this.camposSeleccionados));
    console.log('Campos sin duplicados antes de enviar:', camposSinDuplicados);

    // Llamada al servicio para obtener los datos
    this.apiService.consultaTrabajadores(this.obtenerFiltros(), this.tablaSeleccionada, camposSinDuplicados).subscribe(
      (data) => {
        // Asignar los datos obtenidos a la variable `datos`
        this.datos = data;

        // Verificar la estructura de los datos y prepararlos para la vista
        this.datos.forEach(item => {
          // Aquí podrías agregar lógica adicional si necesitas procesar algún campo especial
          // Por ejemplo, si tienes campos relacionados, podrías transformarlos de forma automática
        });

        console.log('Datos obtenidos:', this.datos);
      },
      (error) => {
        console.error('Error al obtener los datos:', error);
      }
    );
}


  eliminarFiltro(campo: string): void {
    this.filtrosForm.removeControl(campo);
    this.camposSeleccionados = this.camposSeleccionados.filter(c => c !== campo);
    this.datos = []; // Limpia los datos cargados
    console.log('Datos eliminados debido a la eliminación del filtro');
  }

  eliminarColumna(campo: string) {
    const index = this.camposSeleccionados.indexOf(campo);
    if (index > -1) {
      this.camposSeleccionados.splice(index, 1);
      this.eliminarCampoDelFormulario(campo);
    }
    console.log('Columna eliminada:', campo);
  }

  // Manejo del drag and drop
  onDragStart(field: string) {
    console.log('Iniciando drag para el campo:', field);
  }

  onDragEnd(field: string) {
    console.log('Finalizando drag para el campo:', field);
  }

  onDrop(event: CdkDragDrop<any[]>) {
    const campo = event.item.data;
    if (!this.camposSeleccionados.includes(campo)) {
      this.camposSeleccionados.push(campo);
    }
    console.log('Campo arrastrado:', campo);
  }

  generarFiltro(): string {
    let filtros = '';
    if (this.filtrosForm.value.status_emp_con) {
      filtros += `status_emp_con=${this.filtrosForm.value.status_emp_con}&`;
    }
    if (this.filtrosForm.value.estado_certificacion_sol) {
      filtros += `estado_certificacion_sol=${this.filtrosForm.value.estado_certificacion_sol}&`;
    }
    // Agrega más filtros según sea necesario

    return filtros.slice(0, -1); // Elimina el último '&' si lo hay
  }

  aplicarFiltros() {
    const filtros: any = {};

    // Recorre los campos seleccionados para generar los filtros
    this.camposSeleccionados.forEach((campo) => {
      const valorFiltro = this.filtrosForm.get(campo)?.value;
      if (valorFiltro) {
        filtros[campo] = valorFiltro;  // Agrega el filtro solo si tiene valor
      }
    });

    console.log('Filtros antes de convertir:', filtros);  // Verifica el objeto filtros

    if (Object.keys(filtros).length > 0) {
      // No generar el string de filtros manualmente, usa la función que ya tienes en el servicio
      const filtrosString = this.apiService.convertirFiltrosAString(filtros);
      console.log('Filtros convertidos a string:', filtrosString);  // Verifica el string generado

      this.apiService.consultaTrabajadores(filtros, 'trabajadores', this.camposSeleccionados)
        .subscribe(
          (data) => {
            console.log('Datos obtenidos:', data);
            this.datos = data;  // Asigna los datos obtenidos a una variable
          },
          (error) => {
            console.error('Error al obtener datos:', error);
          }
        );
    } else {
      console.log('No se han proporcionado filtros válidos');
    }
  }
  obtenerRelaciones(item: any): string[] {
    const relaciones = [];
    // Itera sobre las propiedades del objeto `item` y selecciona las que contienen relaciones
    for (let key in item) {
      if (item.hasOwnProperty(key) && key.includes('__')) { // Si el campo tiene un '__', es una relación
        relaciones.push(key);
      }
    }
    return relaciones;
  }


}












