import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { PrivacyComponent } from './privacy/privacy.component';
import { DisneyComponent } from './disney/disney.component';
import { DisneyShipsComponent } from './disney-ships/disney-ships.component';


const routes: Routes = [
  { path: 'home', component: HomeComponent, pathMatch: 'full' },
  { path: 'disney', component: DisneyComponent, pathMatch: 'full'},
  { path: 'disney-cruise', component: DisneyShipsComponent },
  { path: 'privacy', component: PrivacyComponent, pathMatch: 'full'},
  { path: '', component:HomeComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
