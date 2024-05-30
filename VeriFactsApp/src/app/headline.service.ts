import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MysqlService } from './bd.service'

@Injectable({
  providedIn: 'root'
})
export class HeadlineService {
  private apiUrl = 'http://127.0.0.1:5000/predict';

  constructor(private http: HttpClient, private mysqlService: MysqlService) { }

  getPrediction(headline: string): Observable<any> {
    return this.http.post<any>(this.apiUrl, { headline });
  }
}
