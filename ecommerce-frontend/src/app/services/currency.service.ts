import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { environment } from '../../environments/environment';

interface CurrencyRatesApiResponse {
  success: boolean;
  data: {
    rates: Record<string, number>;
    base: string;
    time_last_update_unix?: number;
  };
}

interface ConvertApiResponse {
  success: boolean;
  data: {
    amount: number;
    from: string;
    to: string;
    converted_amount: number;
  };
}

export interface CurrencyRates {
  rates: Record<string, number>;
  base: string;
}

export interface ConvertResult {
  amount: number;
  from: string;
  to: string;
  converted_amount: number;
}

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {
  private apiUrl = `${environment.apiUrl}/currency`;

  constructor(private http: HttpClient) {}

  getRates(base: string = 'USD'): Observable<CurrencyRates> {
    return this.http
      .get<CurrencyRatesApiResponse>(`${this.apiUrl}/rates?base=${base}`)
      .pipe(
        map(response => response.data),
        catchError(err => throwError(() => err))
      );
  }

  convert(amount: number, from: string, to: string): Observable<ConvertResult> {
    return this.http
      .get<ConvertApiResponse>(
        `${this.apiUrl}/convert?amount=${amount}&from=${from}&to=${to}`
      )
      .pipe(
        map(response => response.data),
        catchError(err => throwError(() => err))
      );
  }
}
