// import { Injectable } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
// import { Observable } from 'rxjs';
// import { environment } from '../../environments/environment';
// import { Category } from '../models/category.model';

// @Injectable({
//   providedIn: 'root'
// })
// export class CategoryService {
//   private apiUrl = `${environment.apiUrl}/categories`;

//   constructor(private http: HttpClient) { }

//   getAll(): Observable<Category[]> {
//     return this.http.get<Category[]>(this.apiUrl);
//   }

//   getById(id: string): Observable<Category> {
//     return this.http.get<Category>(`${this.apiUrl}/${id}`);
//   }

//   create(category: Category): Observable<Category> {
//     return this.http.post<Category>(this.apiUrl, category);
//   }

//   update(id: string, category: Category): Observable<Category> {
//     return this.http.put<Category>(`${this.apiUrl}/${id}`, category);
//   }

//   delete(id: string): Observable<any> {
//     return this.http.delete(`${this.apiUrl}/${id}`);
//   }
// }

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { Category } from '../models/category.model';

// Interface pour la réponse du backend
interface ApiResponse<T> {
  success: boolean;
  data: T;
  count?: number;
  message?: string;
}

@Injectable({
  providedIn: 'root'
})
export class CategoryService {
  private apiUrl = `${environment.apiUrl}/categories`;

  constructor(private http: HttpClient) { }

  getAll(): Observable<Category[]> {
    return this.http.get<ApiResponse<Category[]>>(this.apiUrl).pipe(
      map(response => response.data)
    );
  }

  getById(id: string): Observable<Category> {
    return this.http.get<ApiResponse<Category>>(`${this.apiUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }

  create(category: Category): Observable<Category> {
    return this.http.post<ApiResponse<Category>>(this.apiUrl, category).pipe(
      map(response => response.data)
    );
  }

  update(id: string, category: Category): Observable<Category> {
    return this.http.put<ApiResponse<Category>>(`${this.apiUrl}/${id}`, category).pipe(
      map(response => response.data)
    );
  }

  delete(id: string): Observable<any> {
    return this.http.delete<ApiResponse<any>>(`${this.apiUrl}/${id}`);
  }
}