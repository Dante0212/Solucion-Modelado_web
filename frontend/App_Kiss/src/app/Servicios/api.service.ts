import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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

  consultaTrabajadores(filtros: any, tabla: string, campos: string[]): Observable<any[]> {
    const params = {
      tabla: tabla,
      campos: campos.join(','),
      filtros: this.convertirFiltrosAString(filtros),  // Convierte los filtros a string
    };

    console.log('Consultando con los siguientes parámetros:', params); // Verifica los parámetros

    return this.http.get<any[]>(`${this.baseUrl}api/consulta_trabajadores/`, { params });
  }
  convertirFiltrosAString(filtros: any): string {
    const filtrosString = Object.entries(filtros)
      .map(([key, value]) => `${key}=${value}`)
      .join('&');
    return filtrosString;
  }
}

