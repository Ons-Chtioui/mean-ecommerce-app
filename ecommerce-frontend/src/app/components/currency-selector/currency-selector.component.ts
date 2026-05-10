import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-currency-selector',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './currency-selector.component.html',
  styleUrl: './currency-selector.component.css'
})
export class CurrencySelectorComponent {
  @Input() selectedCurrency: string = 'TND';
  @Output() currencyChange = new EventEmitter<string>();

  currencies = [
    { code: 'TND', label: 'TND — Dinar Tunisien' },
    { code: 'USD', label: 'USD — Dollar américain' },
    { code: 'EUR', label: 'EUR — Euro' },
    { code: 'GBP', label: 'GBP — Livre sterling' },
  ];

  onCurrencyChange(code: string): void {
    this.selectedCurrency = code;
    this.currencyChange.emit(code);
  }
}
