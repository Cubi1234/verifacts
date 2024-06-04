import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HeadlineService {
  private apiUrl = 'http://127.0.0.1:5000/';

  constructor(private http: HttpClient) { }

  getPrediction(headline: string): Observable<any> {
    return this.http.post<any>(this.apiUrl + 'classify', { headline });
  }

  getAllEntries(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + 'all_entries');
  }
}
