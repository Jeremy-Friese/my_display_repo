import { Component, OnInit } from '@angular/core';
import { CalendlyService } from '../services/calendly.service';

@Component({
  selector: 'app-disney-ships',
  templateUrl: './disney-ships.component.html',
  styleUrls: ['./disney-ships.component.scss']
})
export class DisneyShipsComponent implements OnInit{
  constructor(public calendly: CalendlyService) { }
  message = "Hi Gennie, I am interested in a Walt Disney Cruise Package."

  ngOnInit(): void {
    this.calendly.loadCalendlyScript(this.message)
  }

}
