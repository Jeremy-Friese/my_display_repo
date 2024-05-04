import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';
import { AnimateOnScrollModule } from 'primeng/animateonscroll';
import { CarouselModule } from 'primeng/carousel'; 

import { MaterialModule } from './material-module';
import { DisneyComponent } from './disney/disney.component';
import { FooterComponent } from './shared/footer/footer.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { PrivacyComponent } from './privacy/privacy.component';
import { HomeComponent } from './home/home.component';
import { DisneyShipsComponent } from './disney-ships/disney-ships.component';

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    PrivacyComponent,
    DisneyComponent,
    HomeComponent,
    DisneyShipsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    NgbModule,
    CommonModule,
    AnimateOnScrollModule,
    CarouselModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
