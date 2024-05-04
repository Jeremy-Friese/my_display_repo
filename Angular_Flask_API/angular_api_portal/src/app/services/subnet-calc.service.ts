import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SubnetCalcService {
  // Change endpoint as needed or point to environment files to change.
  apiEndPoint = "http://127.0.0.1:5000";

  constructor(private http: HttpClient,) { }
  subnetAPI(subnet: any) {
    const body = {
      "Subnet": subnet
    }
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post<any>(this.apiEndPoint + `/Subnet`, body, { headers })
  }
}
