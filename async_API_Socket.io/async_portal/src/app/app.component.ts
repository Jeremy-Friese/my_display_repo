import { Component, OnInit } from '@angular/core';
import { ApiService } from './service/api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'async_portal';
  data: any;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchData();
    console.log(this.data)
  }

  fetchData() {
    this.apiService.startTask().subscribe((data) => {
      console.log(data)
      this.data = data
    })
  }
}
