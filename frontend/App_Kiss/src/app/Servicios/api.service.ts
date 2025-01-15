import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'http://127.0.0.1:8000/modelo/';

  constructor(private http: HttpClient) {}

  obtenerTablasYCampos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}api/tablas/`);
  }

  consultaTrabajadores(filtros: any, tabla: string, campos: string[], usarRelaciones: boolean = true): Observable<any[]> {
    if (!tabla || campos.length === 0) {
      console.error('Error: La tabla o los campos no están definidos.');
      return new Observable(); // Retorna un observable vacío en caso de error
    }

    let params = new HttpParams().set('tabla', tabla);

    // Formatear campos según si se quieren relaciones o no
    const camposFormateados = usarRelaciones ? this.formatearCampos(campos) : campos.join(',');
    params = params.set('campos', camposFormateados);

    // Agregar filtros si existen
    if (filtros) {
      const filtrosString = this.convertirFiltrosAString(filtros);
      if (filtrosString) {
        params = params.set('filtros', filtrosString);
      }
    }

    console.log('Parámetros enviados al backend:', params.toString());

    return this.http.get<any[]>(`${this.baseUrl}api/consulta_trabajadores/`, { params });
  }

  // Método para convertir los filtros en un string adecuado para la consulta
  convertirFiltrosAString(filtros: any): string | null {
    if (!filtros || Object.keys(filtros).length === 0) {
      return null; // Retorna null si no hay filtros
    }
    return Object.entries(filtros)
      .map(([key, value]) => `${key}=${value}`)
      .join('&'); // Usar '&' como separador
  }

  // Método para formatear los campos correctamente, manejando relaciones
  private formatearCampos(campos: string[]): string {
    return campos.map(campo => campo.startsWith('rel:') ? campo.replace('rel:', '') : campo).join(',');
}

}



