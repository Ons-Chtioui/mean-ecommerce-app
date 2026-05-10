# DevNet E-Commerce Platform

Projet DevNet — Application e-commerce full-stack conforme à la cahier des charges.

## Stack technique

| Couche | Technologie |
|--------|-------------|
| Backend | Python 3.11 + FastAPI + Motor (MongoDB async) |
| Frontend | Angular 17 |
| Base de données | MongoDB 7 |
| Conteneurisation | Docker + Docker Compose |
| CI/CD | Jenkins (Jenkinsfile) |
| Tests | pytest + httpx + mongomock-motor + Hypothesis |

## Architecture

```
E-commerce/
├── backend-python/          # FastAPI backend (Python)
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── routers/             # categories, products, currency
│   ├── schemas/             # Pydantic v2 schemas
│   ├── services/            # currency_service (TTLCache)
│   ├── tests/               # pytest test suite
│   ├── Dockerfile
│   └── requirements.txt
├── ecommerce-frontend/      # Angular 17 frontend
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml       # Orchestration complète
├── deploy.sh                # Script de déploiement automatisé
└── Jenkinsfile              # Pipeline CI/CD
```

## Démarrage rapide

### Avec Docker Compose (recommandé)

```bash
# Déploiement complet en une commande
./deploy.sh
```

Ou manuellement :

```bash
docker compose build
docker compose up -d
```

- Frontend : http://localhost:80
- API : http://localhost:8000
- Documentation API : http://localhost:8000/docs

### Développement local

**Backend Python :**
```bash
cd backend-python
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend Angular :**
```bash
cd ecommerce-frontend
npm install
ng serve
```

## API REST

### Catégories
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/categories` | Liste toutes les catégories |
| POST | `/api/categories` | Créer une catégorie |
| GET | `/api/categories/{id}` | Détail d'une catégorie |
| PUT | `/api/categories/{id}` | Modifier une catégorie |
| DELETE | `/api/categories/{id}` | Supprimer une catégorie |

### Produits
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/products` | Liste tous les produits (avec catégorie peuplée) |
| POST | `/api/products` | Créer un produit |
| GET | `/api/products/{id}` | Détail d'un produit |
| PUT | `/api/products/{id}` | Modifier un produit |
| DELETE | `/api/products/{id}` | Supprimer un produit |
| GET | `/api/products/category/{id}` | Produits par catégorie |
| POST | `/api/products/upload` | Upload d'image |

### Devises (API externe)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/currency/rates?base=USD` | Taux de change en temps réel |
| GET | `/api/currency/convert?amount=100&from=USD&to=EUR` | Conversion de devise |

## Tests

```bash
cd backend-python

# Tous les tests (sauf connectivité)
pytest tests/ -m "not connectivity" -v

# Avec couverture de code
pytest tests/ -m "not connectivity" --cov=. --cov-report=term-missing

# Tests de connectivité (nécessite internet)
pytest tests/ -m connectivity -v

# Tests property-based uniquement
pytest tests/test_properties.py -v
```

## Variables d'environnement

Créer un fichier `.env` dans `backend-python/` :

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ecommerce
EXCHANGE_RATE_API_URL=https://open.er-api.com/v6/latest
UPLOAD_DIR=uploads/products
PORT=8000
```

## Conformité cahier des charges

- ✅ Backend Python (FastAPI)
- ✅ Frontend Angular (existant, adapté)
- ✅ API REST interne (produits, catégories)
- ✅ API REST externe (ExchangeRate API — conversion de devises)
- ✅ Conteneurisation Docker + Docker Compose
- ✅ Script de déploiement automatisé (`deploy.sh`)
- ✅ Pipeline CI/CD (`Jenkinsfile`)
- ✅ Tests automatisés (pytest + Hypothesis)
