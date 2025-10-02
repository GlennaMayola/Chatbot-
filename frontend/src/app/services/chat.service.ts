import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class PdfChatService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  uploadPDF(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/upload-pdf/`, formData);
  }

  askQuestion(query: string): Observable<any> {
    const formData = new FormData();
    formData.append('query', query);
    return this.http.post(`${this.apiUrl}/ask/`, formData);
  }
}
