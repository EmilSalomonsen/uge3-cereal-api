# Cereal API

En RESTful API til håndtering af cerealprodukt-data med authentication og billedhåndtering.

## Features

- CRUD operationer for cerealprodukter
- Bruger authentication med JWT tokens
- Billedhåndtering for produkter
- Filtrering af produkter baseret på forskellige kriterier

## Installation

1. Klon repository'et
```bash
git clone <repository-url>
```

2. Opret virtuelt miljø og installer dependencies
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Start MongoDB

4. Start serveren
```bash
python -m uvicorn src.main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/auth/signup`: Opret ny bruger
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password123"
  }
  ```

- `POST /api/auth/login`: Log ind
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

### Products
- `GET /api/products/`: Hent alle produkter
  - Query parametre:
    - `calories`: Filter på kalorier
    - `manufacturer`: Filter på producent
    - `skip`: Antal at skippe
    - `limit`: Maks antal at returnere

- `GET /api/products/{id}`: Hent specifikt produkt

- `POST /api/products/`: Opret nyt produkt (kræver auth)
  ```json
  {
    "name": "New Cereal",
    "mfr": "K",
    "type": "C",
    "calories": 100,
    ...
  }
  ```

- `PUT /api/products/{id}`: Opdater produkt (kræver auth)
- `DELETE /api/products/{id}`: Slet produkt (kræver auth)

### Images
- `GET /api/products/{id}/image`: Hent produktbillede
- `POST /api/products/{id}/image`: Upload/opdater produktbillede (kræver auth)

## Design Beslutninger

1. **Authentication**
   - JWT tokens bruges for stateless authentication
   - Passwords hashes med bcrypt for sikkerhed
   - Protected endpoints for data modification

2. **Database**
   - MongoDB valgt for fleksibel datahåndtering
   - Separate collections for users og products

3. **Billedhåndtering**
   - Billeder gemmes i filesystem med produktnavn
   - URL'er gemmes i databasen for nem reference

4. **API Design**
   - RESTful principper følges
   - Separate modeller for input/output (ProductCreate vs ProductResponse)
   - Konsistent fejlhåndtering
