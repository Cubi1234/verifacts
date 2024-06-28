import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FactCheckService {
  private apiUrl = 'http://localhost:5000/fact_check';

  constructor(private http: HttpClient) {}

  getFactCheck(query: string, languageCode: string): Observable<any> {
    const params = new HttpParams()
      .set('query', query)
      .set('languageCode', languageCode);

    return this.http.get<any>(this.apiUrl, { params });
  }
}
