import { Injectable, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Socket, io } from 'socket.io-client';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor() { this.setupSocketConnection() }
  private socket!: Socket;

  

  setupSocketConnection() {
    this.socket = io('http://localhost:5000');
    this.socket.on('response', (data) => {
      console.log(data);
    });
  }

  startTask(): Observable<any> {
    this.socket.emit('/test', { data: 'Start the task!' });

    return new Observable(observer => {
      this.socket.on('response', (data) => {
        observer.next(data);
      })
    })
  }



}
