// import { Injectable } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
// import { Observable } from 'rxjs';
// import { environment } from '../../environments/environment';
// import { Product } from '../models/product.model';

// @Injectable({
//   providedIn: 'root'
// })
// export class ProductService {
//   private apiUrl = `${environment.apiUrl}/products`;

//   constructor(private http: HttpClient) { }

//   getAll(): Observable<Product[]> {
//     return this.http.get<Product[]>(this.apiUrl);
//   }

//   getById(id: string): Observable<Product> {
//     return this.http.get<Product>(`${this.apiUrl}/${id}`);
//   }

//   getByCategory(categoryId: string): Observable<Product[]> {
//     return this.http.get<Product[]>(`${this.apiUrl}/category/${categoryId}`);
//   }

//   create(product: Product): Observable<Product> {
//     return this.http.post<Product>(this.apiUrl, product);
//   }

//   update(id: string, product: Product): Observable<Product> {
//     return this.http.put<Product>(`${this.apiUrl}/${id}`, product);
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
import { Product } from '../models/product.model';

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
export class ProductService {
  private apiUrl = `${environment.apiUrl}/products`;

  constructor(private http: HttpClient) { }

  getAll(): Observable<Product[]> {
    return this.http.get<ApiResponse<Product[]>>(this.apiUrl).pipe(
      map(response => response.data)
    );
  }

  getById(id: string): Observable<Product> {
    return this.http.get<ApiResponse<Product>>(`${this.apiUrl}/${id}`).pipe(
      map(response => response.data)
    );
  }

  getByCategory(categoryId: string): Observable<Product[]> {
    return this.http.get<ApiResponse<Product[]>>(`${this.apiUrl}/category/${categoryId}`).pipe(
      map(response => response.data)
    );
  }

  create(product: Product): Observable<Product> {
    return this.http.post<ApiResponse<Product>>(this.apiUrl, product).pipe(
      map(response => response.data)
    );
  }

  update(id: string, product: Product): Observable<Product> {
    return this.http.put<ApiResponse<Product>>(`${this.apiUrl}/${id}`, product).pipe(
      map(response => response.data)
    );
  }

  delete(id: string): Observable<any> {
    return this.http.delete<ApiResponse<any>>(`${this.apiUrl}/${id}`);
  }
}