import { Routes } from '@angular/router';
import { TrabajadoresPage } from './pages/trabajadores/trabajadores.page'; // Ajusta el path según tu estructura

export const routes: Routes = [
  { path: '', redirectTo: 'trabajadores', pathMatch: 'full' },
  { path: 'trabajadores', component: TrabajadoresPage },


];

