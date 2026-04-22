import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './product-detail.component.html',
  styleUrl: './product-detail.component.css'
})
export class ProductDetailComponent implements OnInit {
  product: Product | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private productService: ProductService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadProduct(id);
    }
  }

  loadProduct(id: string): void {
    this.productService.getById(id).subscribe({
      next: (data) => {
        this.product = data;
      },
      error: (error) => {
        console.error('Erreur lors du chargement du produit', error);
        Swal.fire('Erreur', 'Impossible de charger le produit', 'error');
        this.router.navigate(['/products']);
      }
    });
  }

  getCategoryName(): string {
    return this.product?.category?.name || 'Non définie';
  }

  getStars(rating: number): string[] {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(i <= rating ? 'full' : 'empty');
    }
    return stars;
  }

  getProductId(): string {
    return this.product?._id || this.product?.id || '';
  }

  deleteProduct(): void {
    const id = this.getProductId();
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
            this.router.navigate(['/products']);
          },
          error: (error) => {
            console.error('Erreur lors de la suppression', error);
            Swal.fire('Erreur', 'Impossible de supprimer le produit', 'error');
          }
        });
      }
    });
  }
}