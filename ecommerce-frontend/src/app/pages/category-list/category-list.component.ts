import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CategoryService } from '../../services/category.service';
import { Category } from '../../models/category.model';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-category-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './category-list.component.html',
  styleUrl: './category-list.component.css'
})
export class CategoryListComponent implements OnInit {
  categories: Category[] = [];

  constructor(private categoryService: CategoryService) { }

  ngOnInit(): void {
    this.loadCategories();
  }

  loadCategories(): void {
    this.categoryService.getAll().subscribe({
      next: (data) => {
        this.categories = data;
      },
      error: (error) => {
        console.error('Erreur lors du chargement des catégories', error);
        Swal.fire('Erreur', 'Impossible de charger les catégories', 'error');
      }
    });
  }

  getCategoryId(category: Category): string {
    return category._id || category.id || '';
  }

  deleteCategory(category: Category): void {
    const id = this.getCategoryId(category);
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
        this.categoryService.delete(id).subscribe({
          next: () => {
            Swal.fire('Supprimé !', 'La catégorie a été supprimée.', 'success');
            this.loadCategories();
          },
          error: (error) => {
            console.error('Erreur lors de la suppression', error);
            Swal.fire('Erreur', 'Impossible de supprimer la catégorie', 'error');
          }
        });
      }
    });
  }
}