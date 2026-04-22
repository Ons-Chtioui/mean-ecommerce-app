import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { CategoryService } from '../../services/category.service';
import { Category } from '../../models/category.model';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-product-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './product-form.component.html',
  styleUrl: './product-form.component.css'
})
export class ProductFormComponent implements OnInit {
  productForm: FormGroup;
  categories: Category[] = [];
  isEditMode = false;
  productId: string | null = null;

  constructor(
    private fb: FormBuilder,
    private productService: ProductService,
    private categoryService: CategoryService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.productForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      description: ['', [Validators.required, Validators.minLength(10)]],
      price: [0, [Validators.required, Validators.min(0)]],
      image: [''],
      category: [null, Validators.required],  // 🔥 null au lieu de ''
      stock: [0, [Validators.required, Validators.min(0)]],
      published: [false],
      rating: [0, [Validators.required, Validators.min(0), Validators.max(5)]]
    });
  }

  ngOnInit(): void {
    this.loadCategories();
    
    this.productId = this.route.snapshot.paramMap.get('id');
    if (this.productId) {
      this.isEditMode = true;
      this.loadProduct(this.productId);
    }
  }

  loadCategories(): void {
    this.categoryService.getAll().subscribe({
      next: (data) => {
        this.categories = data;
        console.log('✅ Catégories chargées:', data);
      },
      error: (error) => {
        console.error('❌ Erreur chargement catégories', error);
        Swal.fire('Erreur', 'Impossible de charger les catégories', 'error');
      }
    });
  }

loadProduct(id: string): void {
  this.productService.getById(id).subscribe({
    next: (product) => {
      // 🔥 Extraire l'ID correctement (_id ou id)
      const categoryId = product.category?._id || product.category?.id || product.category;
      
      this.productForm.patchValue({
        name: product.name,
        description: product.description,
        price: product.price,
        image: product.image || '',
        category: categoryId,
        stock: product.stock,
        published: product.published,
        rating: product.rating
      });
      
      console.log('✅ Produit chargé, category ID:', categoryId);
    },
    error: (error) => {
      console.error('❌ Erreur chargement produit', error);
      Swal.fire('Erreur', 'Impossible de charger le produit', 'error');
    }
  });
}

  onSubmit(): void {
    if (this.productForm.invalid) {
      Object.keys(this.productForm.controls).forEach(key => {
        this.productForm.get(key)?.markAsTouched();
      });
      
      Swal.fire({
        icon: 'warning',
        title: 'Formulaire invalide',
        text: 'Veuillez remplir tous les champs obligatoires'
      });
      
      return;
    }

    const formValue = this.productForm.value;

    // Préparer les données
    const productData = {
      name: formValue.name.trim(),
      description: formValue.description.trim(),
      price: Number(formValue.price),
      image: formValue.image?.trim() || '',
      category: formValue.category,
      stock: Number(formValue.stock),
      published: Boolean(formValue.published),
      rating: Number(formValue.rating)
    };

    console.log('📤 Données envoyées:', productData);

    if (this.isEditMode && this.productId) {
      this.productService.update(this.productId, productData).subscribe({
        next: () => {
          Swal.fire('Succès', 'Produit modifié avec succès', 'success');
          this.router.navigate(['/products']);
        },
        error: (error) => {
          console.error('❌ Erreur modification:', error);
          Swal.fire('Erreur', error.error?.message || 'Erreur lors de la modification', 'error');
        }
      });
    } else {
      this.productService.create(productData).subscribe({
        next: () => {
          Swal.fire('Succès', 'Produit créé avec succès', 'success');
          this.router.navigate(['/products']);
        },
        error: (error) => {
          console.error('❌ Erreur création:', error);
          Swal.fire('Erreur', error.error?.message || 'Erreur lors de la création', 'error');
        }
      });
    }
  }

  getStars(rating: number): string[] {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(i <= rating ? 'full' : 'empty');
    }
    return stars;
  }

  setRating(rating: number): void {
    this.productForm.patchValue({ rating });
  }
}