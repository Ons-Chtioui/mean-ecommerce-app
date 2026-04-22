import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProductService } from '../../services/product.service';
import { CategoryService } from '../../services/category.service';
import { Product } from '../../models/product.model';
import { Category } from '../../models/category.model';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './product-list.component.html',
  styleUrl: './product-list.component.css'
})
export class ProductListComponent implements OnInit {
  products: Product[] = [];
  filteredProducts: Product[] = [];
  paginatedProducts: Product[] = [];
  categories: Category[] = [];
  
  // Filtres
  searchTerm: string = '';
  selectedCategoryId: string = '';
  sortBy: string = '';
  
  // Pagination
  currentPage: number = 1;
  itemsPerPage: number = 6;
  totalPages: number = 0;
  pages: number[] = [];

  constructor(
    private productService: ProductService,
    private categoryService: CategoryService
  ) { }

  ngOnInit(): void {
    this.loadProducts();
    this.loadCategories();
  }

  loadProducts(): void {
    this.productService.getAll().subscribe({
      next: (data) => {
        this.products = data;
        this.applyFilters();
        console.log('✅ Produits chargés:', data);
      },
      error: (error) => {
        console.error('❌ Erreur chargement produits', error);
        Swal.fire('Erreur', 'Impossible de charger les produits', 'error');
      }
    });
  }

  loadCategories(): void {
    this.categoryService.getAll().subscribe({
      next: (data) => {
        this.categories = data;
        console.log('✅ Catégories chargées:', data);
      },
      error: (error) => {
        console.error('❌ Erreur chargement catégories', error);
      }
    });
  }

  applyFilters(): void {
    console.log('🔍 Application des filtres...');
    
    // 1. Filtrage
    this.filteredProducts = this.products.filter(product => {
      const matchesSearch = product.name.toLowerCase().includes(this.searchTerm.toLowerCase());
      
      let matchesCategory = true;
      if (this.selectedCategoryId && this.selectedCategoryId !== '') {
        const productCategoryId = this.getCategoryId(product.category);
        matchesCategory = productCategoryId === this.selectedCategoryId;
      }
      
      return matchesSearch && matchesCategory;
    });

    // 2. Tri
    this.applySorting();

    // 3. Pagination
    this.updatePagination();
    
    console.log(`✅ ${this.filteredProducts.length} produit(s) trouvé(s)`);
  }

  applySorting(): void {
    if (this.sortBy === 'price_asc') {
      this.filteredProducts.sort((a, b) => a.price - b.price);
    } else if (this.sortBy === 'price_desc') {
      this.filteredProducts.sort((a, b) => b.price - a.price);
    } else if (this.sortBy === 'name_asc') {
      this.filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
    } else if (this.sortBy === 'name_desc') {
      this.filteredProducts.sort((a, b) => b.name.localeCompare(a.name));
    } else if (this.sortBy === 'stock_asc') {
      this.filteredProducts.sort((a, b) => a.stock - b.stock);
    } else if (this.sortBy === 'stock_desc') {
      this.filteredProducts.sort((a, b) => b.stock - a.stock);
    }
  }

  updatePagination(): void {
    this.totalPages = Math.ceil(this.filteredProducts.length / this.itemsPerPage);
    this.pages = Array.from({ length: this.totalPages }, (_, i) => i + 1);
    
    // Réinitialiser à la page 1 si on dépasse
    if (this.currentPage > this.totalPages) {
      this.currentPage = 1;
    }
    
    this.updatePaginatedProducts();
  }

  updatePaginatedProducts(): void {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.paginatedProducts = this.filteredProducts.slice(startIndex, endIndex);
  }

  goToPage(page: number): void {
    this.currentPage = page;
    this.updatePaginatedProducts();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.goToPage(this.currentPage - 1);
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.goToPage(this.currentPage + 1);
    }
  }

  getCategoryId(category: any): string {
    if (typeof category === 'object' && category !== null) {
      return category._id || category.id || '';
    }
    return category || '';
  }

  getCategoryName(category: Category): string {
    return category?.name || 'Non définie';
  }

  deleteProduct(id: string | undefined): void {
    if (!id) return;

    Swal.fire({
      title: 'Êtes-vous sûr ?',
      text: "Cette action est irréversible !",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Oui, supprimer !',
      cancelButtonText: 'Annuler'
    }).then((result) => {
      if (result.isConfirmed) {
        this.productService.delete(id).subscribe({
          next: () => {
            Swal.fire('Supprimé !', 'Le produit a été supprimé.', 'success');
            this.loadProducts();
          },
          error: (error) => {
            console.error('❌ Erreur suppression', error);
            Swal.fire('Erreur', 'Impossible de supprimer le produit', 'error');
          }
        });
      }
    });
  }

  getStars(rating: number): string[] {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(i <= rating ? 'full' : 'empty');
    }
    return stars;
  }

  getProductId(product: Product): string {
    return product._id || product.id || '';
  }

  handleImageError(event: any): void {
    event.target.src = 'https://via.placeholder.com/50?text=No+Image';
  }
}