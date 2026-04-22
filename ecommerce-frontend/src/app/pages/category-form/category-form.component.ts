import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { CategoryService } from '../../services/category.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-category-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './category-form.component.html',
  styleUrl: './category-form.component.css'
})
export class CategoryFormComponent implements OnInit {
  categoryForm: FormGroup;
  isEditMode = false;
  categoryId: string | null = null;

  constructor(
    private fb: FormBuilder,
    private categoryService: CategoryService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.categoryForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      description: ['']
    });
  }

  ngOnInit(): void {
    this.categoryId = this.route.snapshot.paramMap.get('id');
    if (this.categoryId) {
      this.isEditMode = true;
      this.loadCategory(this.categoryId);
    }
  }

  loadCategory(id: string): void {
    this.categoryService.getById(id).subscribe({
      next: (category) => {
        this.categoryForm.patchValue(category);
      },
      error: (error) => {
        console.error('Erreur lors du chargement de la catégorie', error);
        Swal.fire('Erreur', 'Impossible de charger la catégorie', 'error');
      }
    });
  }

  onSubmit(): void {
    if (this.categoryForm.invalid) {
      Object.keys(this.categoryForm.controls).forEach(key => {
        this.categoryForm.get(key)?.markAsTouched();
      });
      return;
    }

    const categoryData = this.categoryForm.value;

    if (this.isEditMode && this.categoryId) {
      this.categoryService.update(this.categoryId, categoryData).subscribe({
        next: () => {
          Swal.fire('Succès', 'Catégorie modifiée avec succès', 'success');
          this.router.navigate(['/categories']);
        },
        error: (error) => {
          console.error('Erreur lors de la modification', error);
          Swal.fire('Erreur', 'Impossible de modifier la catégorie', 'error');
        }
      });
    } else {
      this.categoryService.create(categoryData).subscribe({
        next: () => {
          Swal.fire('Succès', 'Catégorie créée avec succès', 'success');
          this.router.navigate(['/categories']);
        },
        error: (error) => {
          console.error('Erreur lors de la création', error);
          Swal.fire('Erreur', 'Impossible de créer la catégorie', 'error');
        }
      });
    }
  }
}