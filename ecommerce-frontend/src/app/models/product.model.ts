// import { Category } from './category.model';

// export interface Product {
//   id?: string;
//   name: string;
//   description: string;
//   price: number;
//   image?: string;
//   category: string | Category; // Peut être ID ou objet complet
//   stock: number;
//   published: boolean;
//   rating: number;
//   createdAt?: Date;
//   updatedAt?: Date;
// }


import { Category } from './category.model';

export interface Product {
  _id?: string;
  id?: string;
  name: string;
  description: string;
  price: number;
  image?: string;
  category: Category; // Toujours un objet après populate
  stock: number;
  published: boolean;
  rating: number;
  createdAt?: Date;
  updatedAt?: Date;
}