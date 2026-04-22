import { Routes } from '@angular/router';
import { ProductListComponent } from './pages/product-list/product-list.component';
import { ProductFormComponent } from './pages/product-form/product-form.component';
import { ProductDetailComponent } from './pages/product-detail/product-detail.component';
import { CategoryListComponent } from './pages/category-list/category-list.component';
import { CategoryFormComponent } from './pages/category-form/category-form.component';

export const routes: Routes = [
  { path: '', redirectTo: '/products', pathMatch: 'full' },
  { path: 'products', component: ProductListComponent },
  { path: 'products/new', component: ProductFormComponent },
  { path: 'products/edit/:id', component: ProductFormComponent },
  { path: 'products/:id', component: ProductDetailComponent },
  { path: 'categories', component: CategoryListComponent },
  { path: 'categories/new', component: CategoryFormComponent },
  { path: 'categories/edit/:id', component: CategoryFormComponent },
  { path: '**', redirectTo: '/products' }
];