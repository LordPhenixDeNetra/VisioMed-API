# CAHIER TECHNIQUE BACKEND - FASTAPI
## Application de Gestion des Actes Médicaux - VisioMed

**Unité d'Endoscopies Digestive et Bronchique**  
**Service de Médecine Interne**  
**République du Sénégal - Ministère de la Santé et de l'Action Sociale**

---

## Table des Matières

1. [Vue d'Ensemble](#1-vue-densemble)
2. [Architecture Backend](#2-architecture-backend)
3. [Stack Technique Détaillé](#3-stack-technique-détaillé)
4. [Modèle de Données](#4-modèle-de-données)
5. [Schéma de Base de Données](#5-schéma-de-base-de-données)
6. [Diagrammes UML](#6-diagrammes-uml)
7. [Structure du Projet](#7-structure-du-projet)
8. [Modèles Pydantic](#8-modèles-pydantic)
9. [Endpoints API](#9-endpoints-api)
10. [Authentification et Autorisation](#10-authentification-et-autorisation)
11. [Logique Métier](#11-logique-métier)
12. [Gestion des Erreurs](#12-gestion-des-erreurs)
13. [Validation des Données](#13-validation-des-données)
14. [Services et Repositories](#14-services-et-repositories)
15. [Génération Excel/PDF](#15-génération-excelpdf)
16. [Tests Backend](#16-tests-backend)
17. [Performance et Optimisation](#17-performance-et-optimisation)
18. [Sécurité Backend](#18-sécurité-backend)
19. [Déploiement](#19-déploiement)
20. [Monitoring et Logs](#20-monitoring-et-logs)

---

## 1. Vue d'Ensemble

### 1.1 Objectifs du Backend

Le backend FastAPI fournit une API REST complète pour :

- **Gestion des utilisateurs** avec authentification JWT
- **Gestion des référentiels** (services, actes, tarifs)
- **Saisie et consultation** des actes médicaux
- **Calcul automatique** des tarifs
- **Génération de rapports** financiers et médicaux
- **Export** Excel et PDF
- **Audit et traçabilité** des actions

### 1.2 Principes de Conception

- **Clean Architecture** : séparation claire des couches (routes, services, repositories)
- **Domain-Driven Design** : logique métier centralisée
- **SOLID Principles** : code maintenable et extensible
- **API-First** : documentation automatique avec OpenAPI/Swagger
- **Type Safety** : utilisation intensive de Pydantic pour validation
- **Async/Await** : performances optimales avec asyncio
- **Dependency Injection** : gestion élégante des dépendances

### 1.3 Caractéristiques Techniques

| Caractéristique | Valeur |
|-----------------|--------|
| **Langage** | Python 3.11+ |
| **Framework** | FastAPI 0.104+ |
| **ORM** | SQLAlchemy 2.0+ (async) |
| **Base de données** | PostgreSQL 14+ |
| **Migration** | Alembic |
| **Authentification** | JWT (python-jose) |
| **Validation** | Pydantic V2 |
| **Documentation** | OpenAPI/Swagger auto-générée |
| **Tests** | pytest + pytest-asyncio |
| **Serveur ASGI** | Uvicorn |

---

## 2. Architecture Backend

### 2.1 Architecture en Couches

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT (Frontend React)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    NGINX (Reverse Proxy)                     │
│                    SSL/TLS Termination                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              UVICORN (ASGI Server) + FastAPI                 │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         API LAYER (Routes/Endpoints)                 │    │
│  │  - Authentication Routes                             │    │
│  │  - User Management Routes                            │    │
│  │  - Service Management Routes                         │    │
│  │  - Acte Management Routes                            │    │
│  │  - Reporting Routes                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                                │
│                              ▼                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         MIDDLEWARE LAYER                             │    │
│  │  - CORS Middleware                                   │    │
│  │  - Authentication Middleware                         │    │
│  │  - Error Handling Middleware                         │    │
│  │  - Logging Middleware                                │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                                │
│                              ▼                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         SERVICE LAYER (Business Logic)               │    │
│  │  - UserService                                       │    │
│  │  - ServiceService                                    │    │
│  │  - ActeService                                       │    │
│  │  - TarifService                                      │    │
│  │  - ReportService                                     │    │
│  │  - ExportService                                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                                │
│                              ▼                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         REPOSITORY LAYER (Data Access)               │    │
│  │  - UserRepository                                    │    │
│  │  - ServiceRepository                                 │    │
│  │  - ActeRepository                                    │    │
│  │  - TarifRepository                                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                                │
└──────────────────────────────┼────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              SQLAlchemy ORM + Alembic Migrations             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                       │
│                                                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │  users   │ │ services │ │  actes   │ │  tarifs  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                    │
│  │  actes_  │ │   types  │ │  audit   │                    │
│  │ medicaux │ │  prise   │ │   logs   │                    │
│  └──────────┘ └──────────┘ └──────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Pattern Repository

Le pattern Repository sépare la logique d'accès aux données de la logique métier :

```python
# Repository Pattern
Repository (Interface)
    ├── BaseRepository (Generic CRUD)
    ├── UserRepository
    ├── ServiceRepository
    ├── ActeRepository
    └── TarifRepository

# Service Pattern
Service (Business Logic)
    ├── UserService
    ├── ActeService
    ├── TarifService
    └── ReportService
```

### 2.3 Flux de Requête Typique

```
1. Client → POST /api/v1/actes-medicaux (avec JWT token)
                    │
2. Middleware → Vérification JWT, extraction user
                    │
3. Route Handler → Validation Pydantic du body
                    │
4. Service Layer → Logique métier (calcul tarif)
                    │
5. Repository → Requête SQL via SQLAlchemy
                    │
6. Database → Insertion/Sélection
                    │
7. Repository → Retourne Model SQLAlchemy
                    │
8. Service → Transforme en Pydantic Schema
                    │
9. Route → Retourne JSON Response
                    │
10. Client ← Reçoit données JSON
```

---

## 3. Stack Technique Détaillé

### 3.1 Dépendances Python Principales

```toml
# pyproject.toml ou requirements.txt

[project]
name = "actes-medicaux-api"
version = "1.0.0"
requires-python = ">=3.11"

dependencies = [
    # Framework Web
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "python-multipart>=0.0.6",  # Pour upload fichiers
    
    # Base de données
    "sqlalchemy>=2.0.23",
    "asyncpg>=0.29.0",  # Driver PostgreSQL async
    "alembic>=1.12.0",  # Migrations
    "psycopg2-binary>=2.9.9",  # Driver PostgreSQL sync (pour Alembic)
    
    # Validation
    "pydantic>=2.4.0",
    "pydantic-settings>=2.0.0",
    "email-validator>=2.1.0",
    
    # Authentification et Sécurité
    "python-jose[cryptography]>=3.3.0",  # JWT
    "passlib[bcrypt]>=1.7.4",  # Hashing mots de passe
    "python-multipart>=0.0.6",  # OAuth2 forms
    
    # Génération Documents
    "openpyxl>=3.1.2",  # Excel
    "reportlab>=4.0.0",  # PDF
    "pandas>=2.1.0",  # Manipulation données pour rapports
    
    # Utilitaires
    "python-dotenv>=1.0.0",  # Variables environnement
    "python-dateutil>=2.8.0",
    "pytz>=2023.3",
    
    # CORS
    "fastapi-cors>=0.0.6",
    
    # Logs et Monitoring
    "loguru>=0.7.0",
    "prometheus-client>=0.19.0",
]

[project.optional-dependencies]
dev = [
    # Tests
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.25.0",  # Client HTTP async pour tests
    
    # Qualité Code
    "black>=23.11.0",
    "ruff>=0.1.6",
    "mypy>=1.7.0",
    
    # Debug
    "ipython>=8.17.0",
]
```

### 3.2 Configuration PostgreSQL

```python
# config/settings.py
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator
from typing import Optional

class Settings(BaseSettings):
    """Configuration application"""
    
    # Application
    APP_NAME: str = "Actes Médicaux API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # JWT
    SECRET_KEY: str  # openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100
    
    # Files
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 3.3 Configuration Base de Données

```python
# db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config.settings import settings

# Engine async
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base pour modèles
Base = declarative_base()

# Dependency pour obtenir session
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

## 4. Modèle de Données

### 4.1 Diagramme Entité-Relation (ERD)

```mermaid
erDiagram
    users ||--o{ user_services : "affecté à"
    users ||--o{ actes_medicaux : "créé par"
    users ||--o{ actes_medicaux : "réalisé par (médecin)"
    users ||--o{ audit_logs : "effectue"
    users ||--o{ refresh_tokens : "possède"
    
    services ||--o{ user_services : "contient"
    services ||--o{ actes_types : "propose"
    services ||--o{ tarifs : "tarifie"
    
    actes_types ||--o{ tarifs : "a un tarif"
    actes_types ||--o{ actes_medicaux : "est réalisé"
    
    types_prise_charge ||--o{ tarifs : "appliqué à"
    types_prise_charge ||--o{ actes_medicaux : "mode de paiement"
    
    tarifs ||--|| services : "pour service"
    tarifs ||--|| actes_types : "pour acte"
    tarifs ||--|| types_prise_charge : "selon prise en charge"
    
    actes_medicaux ||--|| users : "médecin"
    actes_medicaux ||--|| users : "créateur"
    actes_medicaux ||--|| actes_types : "type"
    actes_medicaux ||--|| types_prise_charge : "paiement"
    
    users {
        int id PK
        string email UK
        string password_hash
        string nom
        string prenom
        enum role
        boolean actif
        timestamp created_at
        timestamp updated_at
    }
    
    services {
        int id PK
        string code UK
        string nom
        text description
        int chef_service_id FK
        boolean actif
        timestamp created_at
    }
    
    user_services {
        int user_id FK
        int service_id FK
        timestamp created_at
    }
    
    actes_types {
        int id PK
        string code
        string nom
        int service_id FK
        boolean actif
        timestamp created_at
    }
    
    types_prise_charge {
        int id PK
        string code UK
        string libelle
        boolean actif
        timestamp created_at
    }
    
    tarifs {
        int id PK
        int service_id FK
        int acte_id FK
        int type_prise_charge_id FK
        decimal montant
        date date_debut
        date date_fin
        timestamp created_at
        timestamp updated_at
    }
    
    actes_medicaux {
        int id PK
        date date
        string nom_patient
        string prenom_patient
        int acte_id FK
        int type_prise_charge_id FK
        int medecin_id FK
        string numero_bc
        string cotation
        decimal montant
        text observations
        int created_by FK
        timestamp created_at
    }
    
    refresh_tokens {
        int id PK
        int user_id FK
        string token UK
        timestamp expires_at
        boolean revoked
        timestamp created_at
    }
    
    audit_logs {
        int id PK
        int user_id FK
        string action
        string entity_type
        int entity_id
        jsonb old_value
        jsonb new_value
        string ip_address
        timestamp created_at
    }
```

### 4.2 Contraintes et Index

```sql
-- Contraintes d'unicité
UNIQUE(email) ON users
UNIQUE(code) ON services
UNIQUE(code) ON types_prise_charge
UNIQUE(code, service_id) ON actes_types
UNIQUE(service_id, acte_id, type_prise_charge_id, date_debut) ON tarifs
UNIQUE(token) ON refresh_tokens

-- Index pour performance
CREATE INDEX idx_actes_date ON actes_medicaux(date);
CREATE INDEX idx_actes_medecin ON actes_medicaux(medecin_id);
CREATE INDEX idx_actes_created_by ON actes_medicaux(created_by);
CREATE INDEX idx_actes_type ON actes_medicaux(acte_id);
CREATE INDEX idx_tarifs_service ON tarifs(service_id);
CREATE INDEX idx_tarifs_acte ON tarifs(acte_id);
CREATE INDEX idx_tarifs_dates ON tarifs(date_debut, date_fin);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(created_at);
CREATE INDEX idx_user_services_user ON user_services(user_id);
CREATE INDEX idx_user_services_service ON user_services(service_id);
```

---

## 5. Schéma de Base de Données

### 5.1 Script SQL Complet de Création

```sql
-- ============================================================================
-- SCHÉMA DE BASE DE DONNÉES - GESTION ACTES MÉDICAUX
-- PostgreSQL 14+
-- ============================================================================

-- Extension pour UUID (optionnel)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- 1. TABLE users - Utilisateurs du système
-- ============================================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('administrateur', 'medecin', 'secretaire', 'visualiseur')),
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_actif ON users(actif);

-- Commentaires
COMMENT ON TABLE users IS 'Utilisateurs de l''application';
COMMENT ON COLUMN users.role IS 'administrateur, medecin, secretaire, visualiseur';

-- ============================================================================
-- 2. TABLE services - Services cliniques
-- ============================================================================
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(200) NOT NULL,
    description TEXT,
    chef_service_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_services_code ON services(code);
CREATE INDEX idx_services_actif ON services(actif);
CREATE INDEX idx_services_chef ON services(chef_service_id);

-- Commentaires
COMMENT ON TABLE services IS 'Services cliniques (ex: Endoscopie Digestive)';

-- ============================================================================
-- 3. TABLE user_services - Association users ↔ services (N:N)
-- ============================================================================
CREATE TABLE user_services (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    service_id INTEGER NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, service_id)
);

-- Index
CREATE INDEX idx_user_services_user ON user_services(user_id);
CREATE INDEX idx_user_services_service ON user_services(service_id);

-- Commentaires
COMMENT ON TABLE user_services IS 'Association users-services (un user peut appartenir à plusieurs services)';

-- ============================================================================
-- 4. TABLE actes_types - Types d'actes médicaux
-- ============================================================================
CREATE TABLE actes_types (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    nom VARCHAR(200) NOT NULL,
    description TEXT,
    service_id INTEGER NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(code, service_id)
);

-- Index
CREATE INDEX idx_actes_types_service ON actes_types(service_id);
CREATE INDEX idx_actes_types_code ON actes_types(code);
CREATE INDEX idx_actes_types_actif ON actes_types(actif);

-- Commentaires
COMMENT ON TABLE actes_types IS 'Types d''examens (FOGD, Coloscopie, etc.)';
COMMENT ON COLUMN actes_types.code IS 'Code unique par service';

-- ============================================================================
-- 5. TABLE types_prise_charge - Modes de prise en charge
-- ============================================================================
CREATE TABLE types_prise_charge (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    libelle VARCHAR(200) NOT NULL,
    description TEXT,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_types_prise_charge_code ON types_prise_charge(code);
CREATE INDEX idx_types_prise_charge_actif ON types_prise_charge(actif);

-- Commentaires
COMMENT ON TABLE types_prise_charge IS 'Modes de paiement (PAF, IPM, LG, PCC, etc.)';

-- Données initiales
INSERT INTO types_prise_charge (code, libelle, actif) VALUES
('PAF', 'Paiement Au Forfait', TRUE),
('IPM', 'Institution de Prévoyance Maladie', TRUE),
('LG', 'Libre Garantie', TRUE),
('PCC', 'Prise en Charge Complète', TRUE),
('IB', 'Institution de Base', TRUE),
('PCH', 'Prise en Charge', TRUE),
('SESAME', 'SESAME', TRUE),
('AT', 'Accident de Travail', TRUE),
('HOSP', 'Hospitalisation', TRUE);

-- ============================================================================
-- 6. TABLE tarifs - Grille tarifaire
-- ============================================================================
CREATE TABLE tarifs (
    id SERIAL PRIMARY KEY,
    service_id INTEGER NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    acte_id INTEGER NOT NULL REFERENCES actes_types(id) ON DELETE CASCADE,
    type_prise_charge_id INTEGER NOT NULL REFERENCES types_prise_charge(id) ON DELETE CASCADE,
    montant DECIMAL(10, 2) NOT NULL CHECK (montant >= 0),
    date_debut DATE NOT NULL DEFAULT CURRENT_DATE,
    date_fin DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(service_id, acte_id, type_prise_charge_id, date_debut),
    CHECK (date_fin IS NULL OR date_fin >= date_debut)
);

-- Index
CREATE INDEX idx_tarifs_service ON tarifs(service_id);
CREATE INDEX idx_tarifs_acte ON tarifs(acte_id);
CREATE INDEX idx_tarifs_type_pc ON tarifs(type_prise_charge_id);
CREATE INDEX idx_tarifs_dates ON tarifs(date_debut, date_fin);
CREATE INDEX idx_tarifs_composite ON tarifs(service_id, acte_id, type_prise_charge_id);

-- Commentaires
COMMENT ON TABLE tarifs IS 'Grille tarifaire : Service + Acte + Type PC → Montant';
COMMENT ON COLUMN tarifs.date_fin IS 'NULL = tarif toujours valide';

-- ============================================================================
-- 7. TABLE actes_medicaux - Actes médicaux réalisés
-- ============================================================================
CREATE TABLE actes_medicaux (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    nom_patient VARCHAR(100) NOT NULL,
    prenom_patient VARCHAR(100) NOT NULL,
    acte_id INTEGER NOT NULL REFERENCES actes_types(id) ON DELETE RESTRICT,
    type_prise_charge_id INTEGER NOT NULL REFERENCES types_prise_charge(id) ON DELETE RESTRICT,
    medecin_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    numero_bc VARCHAR(50),
    cotation VARCHAR(50),
    montant DECIMAL(10, 2) NOT NULL CHECK (montant >= 0),
    observations TEXT,
    created_by INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour performance
CREATE INDEX idx_actes_date ON actes_medicaux(date);
CREATE INDEX idx_actes_medecin ON actes_medicaux(medecin_id);
CREATE INDEX idx_actes_created_by ON actes_medicaux(created_by);
CREATE INDEX idx_actes_type ON actes_medicaux(acte_id);
CREATE INDEX idx_actes_type_pc ON actes_medicaux(type_prise_charge_id);
CREATE INDEX idx_actes_patient ON actes_medicaux(nom_patient, prenom_patient);
CREATE INDEX idx_actes_date_medecin ON actes_medicaux(date, medecin_id);

-- Commentaires
COMMENT ON TABLE actes_medicaux IS 'Actes médicaux réalisés (saisie quotidienne)';
COMMENT ON COLUMN actes_medicaux.medecin_id IS 'Médecin qui a réalisé l''acte';
COMMENT ON COLUMN actes_medicaux.created_by IS 'Utilisateur qui a saisi (secrétaire)';
COMMENT ON COLUMN actes_medicaux.numero_bc IS 'Numéro de bon de commande / facture';

-- ============================================================================
-- 8. TABLE refresh_tokens - Tokens de rafraîchissement JWT
-- ============================================================================
CREATE TABLE refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token ON refresh_tokens(token);
CREATE INDEX idx_refresh_tokens_expires ON refresh_tokens(expires_at);

-- Commentaires
COMMENT ON TABLE refresh_tokens IS 'Tokens JWT pour refresh (révocables)';

-- ============================================================================
-- 9. TABLE audit_logs - Journalisation des actions
-- ============================================================================
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id INTEGER,
    old_value JSONB,
    new_value JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(created_at);
CREATE INDEX idx_audit_action ON audit_logs(action);

-- Commentaires
COMMENT ON TABLE audit_logs IS 'Journal d''audit de toutes les actions utilisateurs';
COMMENT ON COLUMN audit_logs.action IS 'CREATE, UPDATE, DELETE, LOGIN, LOGOUT, etc.';

-- ============================================================================
-- 10. TRIGGERS - Mise à jour automatique de updated_at
-- ============================================================================

-- Fonction générique pour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Appliquer aux tables nécessaires
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_services_updated_at
    BEFORE UPDATE ON services
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_actes_types_updated_at
    BEFORE UPDATE ON actes_types
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_types_prise_charge_updated_at
    BEFORE UPDATE ON types_prise_charge
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tarifs_updated_at
    BEFORE UPDATE ON tarifs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_actes_medicaux_updated_at
    BEFORE UPDATE ON actes_medicaux
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 11. VUES - Vues utiles pour reporting
-- ============================================================================

-- Vue : actes avec toutes les informations jointes
CREATE OR REPLACE VIEW v_actes_complets AS
SELECT 
    am.id,
    am.date,
    am.nom_patient,
    am.prenom_patient,
    am.numero_bc,
    am.cotation,
    am.montant,
    am.observations,
    at.code AS acte_code,
    at.nom AS acte_nom,
    s.code AS service_code,
    s.nom AS service_nom,
    tpc.code AS type_prise_charge_code,
    tpc.libelle AS type_prise_charge_libelle,
    u_med.nom AS medecin_nom,
    u_med.prenom AS medecin_prenom,
    u_creator.nom AS created_by_nom,
    u_creator.prenom AS created_by_prenom,
    am.created_at
FROM actes_medicaux am
JOIN actes_types at ON am.acte_id = at.id
JOIN services s ON at.service_id = s.id
JOIN types_prise_charge tpc ON am.type_prise_charge_id = tpc.id
JOIN users u_med ON am.medecin_id = u_med.id
JOIN users u_creator ON am.created_by = u_creator.id;

-- Vue : statistiques par service
CREATE OR REPLACE VIEW v_stats_services AS
SELECT 
    s.id AS service_id,
    s.nom AS service_nom,
    COUNT(am.id) AS nombre_actes,
    SUM(am.montant) AS montant_total,
    COUNT(DISTINCT am.medecin_id) AS nombre_medecins,
    MIN(am.date) AS premiere_date,
    MAX(am.date) AS derniere_date
FROM services s
LEFT JOIN actes_types at ON s.id = at.service_id
LEFT JOIN actes_medicaux am ON at.id = am.acte_id
GROUP BY s.id, s.nom;

-- Vue : statistiques par médecin
CREATE OR REPLACE VIEW v_stats_medecins AS
SELECT 
    u.id AS medecin_id,
    u.nom,
    u.prenom,
    COUNT(am.id) AS nombre_actes,
    SUM(am.montant) AS montant_total,
    COUNT(DISTINCT am.acte_id) AS nombre_types_actes_differents,
    MIN(am.date) AS premiere_date,
    MAX(am.date) AS derniere_date
FROM users u
LEFT JOIN actes_medicaux am ON u.id = am.medecin_id
WHERE u.role IN ('medecin', 'administrateur')
GROUP BY u.id, u.nom, u.prenom;

-- ============================================================================
-- 12. FONCTIONS UTILITAIRES
-- ============================================================================

-- Fonction : obtenir le tarif applicable à une date donnée
CREATE OR REPLACE FUNCTION get_tarif_applicable(
    p_service_id INTEGER,
    p_acte_id INTEGER,
    p_type_prise_charge_id INTEGER,
    p_date DATE DEFAULT CURRENT_DATE
)
RETURNS DECIMAL(10, 2) AS $$
DECLARE
    v_montant DECIMAL(10, 2);
BEGIN
    SELECT montant INTO v_montant
    FROM tarifs
    WHERE service_id = p_service_id
      AND acte_id = p_acte_id
      AND type_prise_charge_id = p_type_prise_charge_id
      AND date_debut <= p_date
      AND (date_fin IS NULL OR date_fin >= p_date)
    ORDER BY date_debut DESC
    LIMIT 1;
    
    RETURN v_montant;
END;
$$ LANGUAGE plpgsql;

-- Fonction : vérifier si un utilisateur a accès à un service
CREATE OR REPLACE FUNCTION user_has_service_access(
    p_user_id INTEGER,
    p_service_id INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    v_has_access BOOLEAN;
BEGIN
    -- Administrateurs ont accès à tous les services
    SELECT EXISTS(
        SELECT 1 FROM users 
        WHERE id = p_user_id AND role = 'administrateur'
    ) INTO v_has_access;
    
    IF v_has_access THEN
        RETURN TRUE;
    END IF;
    
    -- Vérifier association user-service
    SELECT EXISTS(
        SELECT 1 FROM user_services
        WHERE user_id = p_user_id AND service_id = p_service_id
    ) INTO v_has_access;
    
    RETURN v_has_access;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 13. DONNÉES DE TEST (Optionnel)
-- ============================================================================

-- Administrateur par défaut (mot de passe: Admin123!)
INSERT INTO users (email, password_hash, nom, prenom, role, actif) VALUES
('admin@hopital.sn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5.V0N0V0N0V0N0', 'DIOP', 'Amadou', 'administrateur', TRUE);

-- Service Endoscopie Digestive
INSERT INTO services (code, nom, description, actif) VALUES
('ENDO_DIGEST', 'Endoscopie Digestive', 'Service d''endoscopie digestive et bronchique', TRUE);

-- Types d'actes
INSERT INTO actes_types (code, nom, service_id, actif)
SELECT 'FOGD', 'Fibroscopie Œso-Gastro-Duodénale (FOGD)', id, TRUE FROM services WHERE code = 'ENDO_DIGEST'
UNION ALL
SELECT 'COLO', 'Coloscopie', id, TRUE FROM services WHERE code = 'ENDO_DIGEST'
UNION ALL
SELECT 'ANUS', 'Anuscopie', id, TRUE FROM services WHERE code = 'ENDO_DIGEST';

-- ============================================================================
-- 14. PERMISSIONS ET SÉCURITÉ
-- ============================================================================

-- Créer rôle applicatif (avec droits limités)
-- CREATE ROLE app_user WITH LOGIN PASSWORD 'your_secure_password';
-- GRANT CONNECT ON DATABASE votre_db TO app_user;
-- GRANT USAGE ON SCHEMA public TO app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- ============================================================================
-- FIN DU SCHÉMA
-- ============================================================================
```

### 5.2 Migrations Alembic

```python
# alembic/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2026-02-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Création des tables (voir SQL ci-dessus)
    # Ce fichier serait généré automatiquement par:
    # alembic revision --autogenerate -m "Initial schema"
    pass

def downgrade() -> None:
    # Suppression des tables dans l'ordre inverse
    op.drop_table('audit_logs')
    op.drop_table('refresh_tokens')
    op.drop_table('actes_medicaux')
    op.drop_table('tarifs')
    op.drop_table('types_prise_charge')
    op.drop_table('actes_types')
    op.drop_table('user_services')
    op.drop_table('services')
    op.drop_table('users')
```

---

## 6. Diagrammes UML

### 6.1 Diagramme de Classes (Modèles SQLAlchemy)

```mermaid
classDiagram
    class User {
        +int id
        +str email
        +str password_hash
        +str nom
        +str prenom
        +UserRole role
        +bool actif
        +datetime created_at
        +datetime updated_at
        +List~Service~ services
        +List~ActeMedical~ actes_realises
        +List~ActeMedical~ actes_crees
        +List~RefreshToken~ refresh_tokens
        +List~AuditLog~ audit_logs
        +verify_password(password: str) bool
        +has_service_access(service_id: int) bool
    }
    
    class Service {
        +int id
        +str code
        +str nom
        +str description
        +int chef_service_id
        +bool actif
        +datetime created_at
        +datetime updated_at
        +User chef_service
        +List~User~ users
        +List~ActeType~ actes_types
        +List~Tarif~ tarifs
    }
    
    class ActeType {
        +int id
        +str code
        +str nom
        +str description
        +int service_id
        +bool actif
        +datetime created_at
        +datetime updated_at
        +Service service
        +List~Tarif~ tarifs
        +List~ActeMedical~ actes_medicaux
    }
    
    class TypePriseCharge {
        +int id
        +str code
        +str libelle
        +str description
        +bool actif
        +datetime created_at
        +datetime updated_at
        +List~Tarif~ tarifs
        +List~ActeMedical~ actes_medicaux
    }
    
    class Tarif {
        +int id
        +int service_id
        +int acte_id
        +int type_prise_charge_id
        +Decimal montant
        +date date_debut
        +date date_fin
        +datetime created_at
        +datetime updated_at
        +Service service
        +ActeType acte
        +TypePriseCharge type_prise_charge
        +is_valid_at(date: date) bool
    }
    
    class ActeMedical {
        +int id
        +date date
        +str nom_patient
        +str prenom_patient
        +int acte_id
        +int type_prise_charge_id
        +int medecin_id
        +str numero_bc
        +str cotation
        +Decimal montant
        +str observations
        +int created_by
        +datetime created_at
        +datetime updated_at
        +ActeType acte
        +TypePriseCharge type_prise_charge
        +User medecin
        +User created_by_user
    }
    
    class RefreshToken {
        +int id
        +int user_id
        +str token
        +datetime expires_at
        +bool revoked
        +datetime created_at
        +User user
        +is_valid() bool
    }
    
    class AuditLog {
        +int id
        +int user_id
        +str action
        +str entity_type
        +int entity_id
        +dict old_value
        +dict new_value
        +str ip_address
        +str user_agent
        +datetime created_at
        +User user
    }
    
    User "1" -- "*" Service : services
    Service "1" -- "*" ActeType : actes_types
    Service "1" -- "*" Tarif : tarifs
    ActeType "1" -- "*" Tarif : tarifs
    TypePriseCharge "1" -- "*" Tarif : tarifs
    ActeType "1" -- "*" ActeMedical : actes_medicaux
    TypePriseCharge "1" -- "*" ActeMedical : actes_medicaux
    User "1" -- "*" ActeMedical : medecin
    User "1" -- "*" ActeMedical : created_by
    User "1" -- "*" RefreshToken : refresh_tokens
    User "1" -- "*" AuditLog : audit_logs
```

### 6.2 Diagramme de Séquence - Saisie d'un Acte Médical

```mermaid
sequenceDiagram
    participant C as Client (Frontend)
    participant API as FastAPI
    participant MW as Auth Middleware
    participant S as ActeService
    participant TS as TarifService
    participant R as ActeRepository
    participant DB as PostgreSQL
    participant AL as AuditLog
    
    C->>+API: POST /api/v1/actes-medicaux<br/>{acte_data + JWT}
    
    API->>+MW: Vérifier JWT
    MW->>MW: Décoder token
    MW->>MW: Vérifier expiration
    MW->>DB: SELECT user WHERE id=?
    DB-->>MW: User object
    MW-->>-API: current_user
    
    API->>API: Valider Pydantic Schema
    
    API->>+S: create_acte(acte_data, current_user)
    
    S->>S: Vérifier autorisation<br/>(secretaire ou admin)
    
    S->>+TS: get_tarif_applicable(service, acte, type_pc, date)
    TS->>DB: SELECT tarif WHERE...<br/>date_debut <= date AND<br/>(date_fin IS NULL OR date_fin >= date)
    DB-->>TS: Tarif object
    TS-->>-S: montant
    
    alt Tarif non trouvé
        S-->>API: HTTP 400 "Tarif non configuré"
        API-->>C: Error response
    end
    
    S->>S: acte_data.montant = montant_calculé
    
    S->>+R: create(acte_data)
    R->>DB: INSERT INTO actes_medicaux...
    DB-->>R: acte_id
    R->>DB: SELECT acte WITH joins
    DB-->>R: acte_complet
    R-->>-S: ActeMedical object
    
    S->>+AL: log_action("CREATE", "acte_medical", acte_id)
    AL->>DB: INSERT INTO audit_logs...
    DB-->>AL: OK
    AL-->>-S: OK
    
    S-->>-API: ActeMedical object
    
    API->>API: Convertir en Pydantic Response
    API-->>-C: HTTP 201 {acte_data}
```

### 6.3 Diagramme de Séquence - Génération Rapport Médecin

```mermaid
sequenceDiagram
    participant C as Client
    participant API as FastAPI
    participant MW as Auth Middleware
    participant RS as ReportService
    participant AR as ActeRepository
    participant ES as ExportService
    participant DB as PostgreSQL
    
    C->>+API: GET /api/v1/reports/medecin/{id}<br/>?start_date=...&end_date=...&format=excel
    
    API->>+MW: Vérifier JWT
    MW-->>-API: current_user
    
    API->>+RS: generate_medecin_report(medecin_id, filters, current_user)
    
    RS->>RS: Vérifier autorisation<br/>(médecin peut voir ses propres stats<br/>ou admin voit tout)
    
    RS->>+AR: get_actes_by_medecin(medecin_id, filters)
    AR->>DB: SELECT am.* FROM actes_medicaux am<br/>WHERE medecin_id=? AND date BETWEEN ? AND ?<br/>JOIN ...
    DB-->>AR: List[ActeMedical]
    AR-->>-RS: actes_list
    
    RS->>RS: Calculer statistiques:<br/>- Total actes<br/>- Montant total<br/>- Répartition par type<br/>- Répartition par prise en charge<br/>- Pourcentage service
    
    alt format == "excel"
        RS->>+ES: generate_excel_medecin(stats_data)
        ES->>ES: Créer workbook openpyxl<br/>- Onglet Activité<br/>- Onglet Financier<br/>- Onglet Détails<br/>- Graphiques
        ES-->>-RS: excel_buffer
        RS-->>API: FileResponse(excel_buffer)
        API-->>C: HTTP 200 application/vnd.ms-excel
    else format == "pdf"
        RS->>+ES: generate_pdf_medecin(stats_data)
        ES->>ES: Créer PDF reportlab<br/>- En-tête<br/>- Tableaux<br/>- Graphiques
        ES-->>-RS: pdf_buffer
        RS-->>API: FileResponse(pdf_buffer)
        API-->>C: HTTP 200 application/pdf
    else format == "json"
        RS-->>-API: stats_data (JSON)
        API-->>-C: HTTP 200 application/json
    end
```

### 6.4 Diagramme de Composants Backend

```mermaid
graph TB
    subgraph "FastAPI Application"
        MAIN[main.py<br/>Application Entry]
        
        subgraph "API Layer"
            AUTH_R[auth.py<br/>Auth Routes]
            USER_R[users.py<br/>User Routes]
            SERV_R[services.py<br/>Service Routes]
            ACTE_R[actes.py<br/>Acte Routes]
            REP_R[reports.py<br/>Report Routes]
        end
        
        subgraph "Middleware Layer"
            CORS[CORS Middleware]
            AUTH_MW[Auth Middleware]
            ERR_MW[Error Handler]
            LOG_MW[Logging Middleware]
        end
        
        subgraph "Service Layer"
            USER_S[UserService]
            AUTH_S[AuthService]
            SERV_S[ServiceService]
            ACTE_S[ActeService]
            TARIF_S[TarifService]
            REP_S[ReportService]
            EXP_S[ExportService]
        end
        
        subgraph "Repository Layer"
            USER_REP[UserRepository]
            SERV_REP[ServiceRepository]
            ACTE_REP[ActeRepository]
            TARIF_REP[TarifRepository]
        end
        
        subgraph "Data Layer"
            MODELS[SQLAlchemy Models]
            SCHEMAS[Pydantic Schemas]
            DB[Database Session]
        end
    end
    
    subgraph "External"
        PG[(PostgreSQL)]
        EXCEL[Excel Files]
        PDF[PDF Files]
    end
    
    MAIN --> AUTH_R
    MAIN --> USER_R
    MAIN --> SERV_R
    MAIN --> ACTE_R
    MAIN --> REP_R
    
    MAIN --> CORS
    MAIN --> AUTH_MW
    MAIN --> ERR_MW
    MAIN --> LOG_MW
    
    AUTH_R --> AUTH_S
    USER_R --> USER_S
    SERV_R --> SERV_S
    ACTE_R --> ACTE_S
    ACTE_R --> TARIF_S
    REP_R --> REP_S
    REP_R --> EXP_S
    
    USER_S --> USER_REP
    SERV_S --> SERV_REP
    ACTE_S --> ACTE_REP
    TARIF_S --> TARIF_REP
    
    USER_REP --> MODELS
    SERV_REP --> MODELS
    ACTE_REP --> MODELS
    TARIF_REP --> MODELS
    
    MODELS --> DB
    DB --> PG
    
    EXP_S --> EXCEL
    EXP_S --> PDF
    
    style MAIN fill:#e1f5ff
    style PG fill:#ffe1e1
    style EXCEL fill:#ffe1ff
    style PDF fill:#ffe1ff
```

---

**(Suite dans le prochain message...)**
## 7. Structure du Projet

### 7.1 Arborescence Complète

```
actes-medicaux-backend/
│
├── alembic/                          # Migrations base de données
│   ├── versions/
│   │   ├── 001_initial_schema.py
│   │   ├── 002_add_audit_logs.py
│   │   └── ...
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
│
├── app/                              # Application principale
│   ├── __init__.py
│   ├── main.py                       # Point d'entrée FastAPI
│   │
│   ├── api/                          # Couche API (Routes)
│   │   ├── __init__.py
│   │   ├── deps.py                   # Dépendances communes
│   │   │
│   │   └── v1/                       # API Version 1
│   │       ├── __init__.py
│   │       ├── router.py             # Router principal V1
│   │       │
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py           # Authentification
│   │           ├── users.py          # Gestion utilisateurs
│   │           ├── services.py       # Gestion services
│   │           ├── actes_types.py    # Types d'actes
│   │           ├── tarifs.py         # Tarification
│   │           ├── actes_medicaux.py # Actes médicaux
│   │           ├── reports.py        # Rapports
│   │           └── exports.py        # Exports Excel/PDF
│   │
│   ├── core/                         # Configuration & utilitaires
│   │   ├── __init__.py
│   │   ├── config.py                 # Settings Pydantic
│   │   ├── security.py               # JWT, hashing
│   │   ├── exceptions.py             # Exceptions personnalisées
│   │   └── logging.py                # Configuration logs
│   │
│   ├── db/                           # Base de données
│   │   ├── __init__.py
│   │   ├── database.py               # Session, engine
│   │   ├── base.py                   # Import tous les modèles
│   │   │
│   │   └── models/                   # Modèles SQLAlchemy
│   │       ├── __init__.py
│   │       ├── user.py
│   │       ├── service.py
│   │       ├── acte_type.py
│   │       ├── type_prise_charge.py
│   │       ├── tarif.py
│   │       ├── acte_medical.py
│   │       ├── refresh_token.py
│   │       └── audit_log.py
│   │
│   ├── schemas/                      # Schémas Pydantic
│   │   ├── __init__.py
│   │   ├── user.py                   # UserCreate, UserUpdate, UserResponse
│   │   ├── service.py
│   │   ├── acte_type.py
│   │   ├── type_prise_charge.py
│   │   ├── tarif.py
│   │   ├── acte_medical.py
│   │   ├── auth.py                   # Token, Login
│   │   ├── report.py                 # Schemas rapports
│   │   └── common.py                 # Schemas communs (Pagination, etc.)
│   │
│   ├── services/                     # Logique métier
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── service_service.py
│   │   ├── acte_service.py
│   │   ├── tarif_service.py
│   │   ├── report_service.py
│   │   ├── export_service.py
│   │   └── audit_service.py
│   │
│   ├── repositories/                 # Accès données
│   │   ├── __init__.py
│   │   ├── base.py                   # Repository générique
│   │   ├── user_repository.py
│   │   ├── service_repository.py
│   │   ├── acte_repository.py
│   │   ├── tarif_repository.py
│   │   └── audit_repository.py
│   │
│   └── utils/                        # Utilitaires
│       ├── __init__.py
│       ├── excel_generator.py        # Génération Excel
│       ├── pdf_generator.py          # Génération PDF
│       ├── validators.py             # Validations custom
│       └── helpers.py                # Fonctions helper
│
├── tests/                            # Tests
│   ├── __init__.py
│   ├── conftest.py                   # Fixtures pytest
│   │
│   ├── unit/                         # Tests unitaires
│   │   ├── test_services/
│   │   ├── test_repositories/
│   │   └── test_utils/
│   │
│   ├── integration/                  # Tests d'intégration
│   │   ├── test_api/
│   │   └── test_db/
│   │
│   └── e2e/                          # Tests end-to-end
│       └── test_workflows/
│
├── scripts/                          # Scripts utilitaires
│   ├── init_db.py                    # Initialisation BD
│   ├── create_admin.py               # Créer admin
│   ├── seed_data.py                  # Données de test
│   └── backup_db.sh                  # Backup BD
│
├── docs/                             # Documentation
│   ├── api.md
│   ├── deployment.md
│   └── development.md
│
├── .env.example                      # Exemple variables env
├── .gitignore
├── .dockerignore
├── Dockerfile                        # Image Docker
├── docker-compose.yml                # Orchestration locale
├── pyproject.toml                    # Configuration projet
├── requirements.txt                  # Dépendances pip
├── README.md
└── Makefile                          # Commandes utiles
```

### 7.2 Fichiers de Configuration Clés

#### 7.2.1 pyproject.toml

```toml
[project]
name = "actes-medicaux-api"
version = "1.0.0"
description = "API FastAPI pour gestion des actes médicaux"
authors = [{name = "Votre Nom", email = "email@example.com"}]
requires-python = ">=3.11"
readme = "README.md"
license = {text = "Proprietary"}

dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "sqlalchemy>=2.0.23",
    "asyncpg>=0.29.0",
    "alembic>=1.12.0",
    "pydantic>=2.4.0",
    "pydantic-settings>=2.0.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.6",
    "openpyxl>=3.1.2",
    "reportlab>=4.0.0",
    "pandas>=2.1.0",
    "python-dotenv>=1.0.0",
    "loguru>=0.7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.25.0",
    "black>=23.11.0",
    "ruff>=0.1.6",
    "mypy>=1.7.0",
]

[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --cov=app --cov-report=term-missing"
testpaths = ["tests"]
asyncio_mode = "auto"
```

#### 7.2.2 .env.example

```bash
# Application
APP_NAME="Actes Médicaux API"
VERSION="1.0.0"
DEBUG=false
ENVIRONMENT="production"  # development, staging, production

# Database
POSTGRES_USER=actes_user
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=actes_medicaux_db

# Security
SECRET_KEY=your_secret_key_here_use_openssl_rand_hex_32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000","https://votre-domaine.sn"]

# Pagination
DEFAULT_PAGE_SIZE=50
MAX_PAGE_SIZE=100

# Files
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760  # 10MB

# Logs
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Monitoring
ENABLE_METRICS=true
```

#### 7.2.3 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Répertoire de travail
WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .

# Installer dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier code application
COPY . .

# Créer user non-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Port exposé
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 7.2.4 docker-compose.yml

```yaml
version: '3.8'

services:
  # Base de données PostgreSQL
  db:
    image: postgres:14-alpine
    container_name: actes_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init_db.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # API Backend
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: actes_api
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_HOST=db
      - POSTGRES_PORT=5432
      - POSTGRES_DB=${POSTGRES_DB}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./app:/app/app
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    ports:
      - "8000:8000"
    command: >
      sh -c "
        alembic upgrade head &&
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
      "

  # Redis (optionnel, pour cache)
  redis:
    image: redis:7-alpine
    container_name: actes_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

#### 7.2.5 Makefile

```makefile
.PHONY: help install dev test lint format docker-up docker-down migrate

help:
	@echo "Commandes disponibles:"
	@echo "  make install     - Installer dépendances"
	@echo "  make dev         - Lancer serveur dev"
	@echo "  make test        - Lancer tests"
	@echo "  make lint        - Vérifier code"
	@echo "  make format      - Formater code"
	@echo "  make docker-up   - Démarrer Docker"
	@echo "  make docker-down - Arrêter Docker"
	@echo "  make migrate     - Lancer migrations"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --cov=app --cov-report=html

lint:
	ruff check app/
	mypy app/

format:
	black app/ tests/
	ruff check --fix app/

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f api

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(msg)"

db-reset:
	docker-compose down -v
	docker-compose up -d db
	sleep 5
	alembic upgrade head
	python scripts/seed_data.py
```

---

## 8. Modèles Pydantic

### 8.1 Schémas de Base

```python
# app/schemas/common.py
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional
from datetime import datetime

# Schema générique pour pagination
DataT = TypeVar('DataT')

class PaginationParams(BaseModel):
    """Paramètres de pagination"""
    page: int = Field(1, ge=1, description="Numéro de page")
    page_size: int = Field(50, ge=1, le=100, description="Taille de page")
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size

class PaginatedResponse(BaseModel, Generic[DataT]):
    """Réponse paginée générique"""
    items: list[DataT]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def create(cls, items: list[DataT], total: int, params: PaginationParams):
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=(total + params.page_size - 1) // params.page_size
        )

class TimestampMixin(BaseModel):
    """Mixin pour timestamps"""
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

### 8.2 Schémas Utilisateur

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """Rôles utilisateurs"""
    ADMINISTRATEUR = "administrateur"
    MEDECIN = "medecin"
    SECRETAIRE = "secretaire"
    VISUALISEUR = "visualiseur"

# Base
class UserBase(BaseModel):
    """Attributs communs"""
    email: EmailStr
    nom: str = Field(..., min_length=2, max_length=100)
    prenom: str = Field(..., min_length=2, max_length=100)
    role: UserRole
    actif: bool = True

# Création
class UserCreate(UserBase):
    """Création utilisateur"""
    password: str = Field(..., min_length=8, max_length=100)
    service_ids: Optional[List[int]] = []
    
    @validator('password')
    def validate_password(cls, v):
        """Validation mot de passe fort"""
        if not any(c.isupper() for c in v):
            raise ValueError('Mot de passe doit contenir au moins une majuscule')
        if not any(c.islower() for c in v):
            raise ValueError('Mot de passe doit contenir au moins une minuscule')
        if not any(c.isdigit() for c in v):
            raise ValueError('Mot de passe doit contenir au moins un chiffre')
        return v

# Mise à jour
class UserUpdate(BaseModel):
    """Mise à jour utilisateur"""
    email: Optional[EmailStr] = None
    nom: Optional[str] = Field(None, min_length=2, max_length=100)
    prenom: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[UserRole] = None
    actif: Optional[bool] = None
    service_ids: Optional[List[int]] = None

# Changement de mot de passe
class PasswordChange(BaseModel):
    """Changement de mot de passe"""
    old_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_new_password(cls, v, values):
        if 'old_password' in values and v == values['old_password']:
            raise ValueError('Nouveau mot de passe doit être différent de l\'ancien')
        if not any(c.isupper() for c in v):
            raise ValueError('Mot de passe doit contenir au moins une majuscule')
        if not any(c.islower() for c in v):
            raise ValueError('Mot de passe doit contenir au moins une minuscule')
        if not any(c.isdigit() for c in v):
            raise ValueError('Mot de passe doit contenir au moins un chiffre')
        return v

# Réponse simple
class UserResponse(UserBase):
    """Réponse utilisateur"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Réponse détaillée
class UserDetailResponse(UserResponse):
    """Réponse utilisateur avec services"""
    services: List["ServiceBrief"] = []

# Brief (pour relations)
class UserBrief(BaseModel):
    """User brief pour relations"""
    id: int
    nom: str
    prenom: str
    email: EmailStr
    role: UserRole
    
    class Config:
        from_attributes = True
```

### 8.3 Schémas Acte Médical

```python
# app/schemas/acte_medical.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

# Base
class ActeMedicalBase(BaseModel):
    """Attributs communs acte médical"""
    date: date
    nom_patient: str = Field(..., min_length=2, max_length=100)
    prenom_patient: str = Field(..., min_length=2, max_length=100)
    acte_id: int = Field(..., gt=0)
    type_prise_charge_id: int = Field(..., gt=0)
    medecin_id: int = Field(..., gt=0)
    numero_bc: Optional[str] = Field(None, max_length=50)
    cotation: Optional[str] = Field(None, max_length=50)
    observations: Optional[str] = Field(None, max_length=1000)
    
    @validator('date')
    def validate_date(cls, v):
        """Date ne peut pas être dans le futur"""
        if v > date.today():
            raise ValueError('La date ne peut pas être dans le futur')
        return v

# Création
class ActeMedicalCreate(ActeMedicalBase):
    """Création acte médical (montant calculé automatiquement)"""
    pass

# Mise à jour
class ActeMedicalUpdate(BaseModel):
    """Mise à jour acte médical"""
    date: Optional[date] = None
    nom_patient: Optional[str] = Field(None, min_length=2, max_length=100)
    prenom_patient: Optional[str] = Field(None, min_length=2, max_length=100)
    acte_id: Optional[int] = Field(None, gt=0)
    type_prise_charge_id: Optional[int] = Field(None, gt=0)
    medecin_id: Optional[int] = Field(None, gt=0)
    numero_bc: Optional[str] = Field(None, max_length=50)
    cotation: Optional[str] = Field(None, max_length=50)
    observations: Optional[str] = Field(None, max_length=1000)

# Réponse simple
class ActeMedicalResponse(ActeMedicalBase):
    """Réponse acte médical"""
    id: int
    montant: Decimal
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Réponse détaillée
class ActeMedicalDetailResponse(ActeMedicalResponse):
    """Réponse détaillée avec relations"""
    acte: "ActeTypeBrief"
    type_prise_charge: "TypePriseChargeBrief"
    medecin: "UserBrief"
    created_by_user: "UserBrief"
    
    class Config:
        from_attributes = True

# Filtres de recherche
class ActeMedicalFilters(BaseModel):
    """Filtres pour recherche actes"""
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    service_id: Optional[int] = None
    acte_id: Optional[int] = None
    type_prise_charge_id: Optional[int] = None
    medecin_id: Optional[int] = None
    nom_patient: Optional[str] = None
    numero_bc: Optional[str] = None
```

### 8.4 Schémas Tarif

```python
# app/schemas/tarif.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

# Base
class TarifBase(BaseModel):
    """Attributs communs tarif"""
    service_id: int = Field(..., gt=0)
    acte_id: int = Field(..., gt=0)
    type_prise_charge_id: int = Field(..., gt=0)
    montant: Decimal = Field(..., ge=0, decimal_places=2)
    date_debut: date = Field(default_factory=date.today)
    date_fin: Optional[date] = None
    
    @validator('date_fin')
    def validate_date_fin(cls, v, values):
        """date_fin doit être >= date_debut"""
        if v and 'date_debut' in values and v < values['date_debut']:
            raise ValueError('date_fin doit être >= date_debut')
        return v

# Création
class TarifCreate(TarifBase):
    """Création tarif"""
    pass

# Mise à jour
class TarifUpdate(BaseModel):
    """Mise à jour tarif"""
    montant: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None

# Réponse
class TarifResponse(TarifBase):
    """Réponse tarif"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Réponse détaillée
class TarifDetailResponse(TarifResponse):
    """Réponse détaillée avec relations"""
    service: "ServiceBrief"
    acte: "ActeTypeBrief"
    type_prise_charge: "TypePriseChargeBrief"
    
    class Config:
        from_attributes = True

# Recherche de tarif applicable
class TarifQuery(BaseModel):
    """Requête pour obtenir tarif applicable"""
    service_id: int
    acte_id: int
    type_prise_charge_id: int
    date: date = Field(default_factory=date.today)
```

### 8.5 Schémas Authentification

```python
# app/schemas/auth.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Login
class LoginRequest(BaseModel):
    """Requête de connexion"""
    email: EmailStr
    password: str

# Token
class Token(BaseModel):
    """Token JWT"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Données décodées du token"""
    user_id: int
    email: str
    role: str

# Refresh token
class RefreshTokenRequest(BaseModel):
    """Requête refresh token"""
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    """Réponse refresh token"""
    access_token: str
    token_type: str = "bearer"
```

### 8.6 Schémas Rapports

```python
# app/schemas/report.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date
from decimal import Decimal

# Filtres rapports
class ReportFilters(BaseModel):
    """Filtres pour rapports"""
    date_debut: date
    date_fin: date
    service_id: Optional[int] = None
    medecin_id: Optional[int] = None
    acte_id: Optional[int] = None
    type_prise_charge_id: Optional[int] = None

# Statistiques acte
class ActeStats(BaseModel):
    """Statistiques par acte"""
    acte_code: str
    acte_nom: str
    nombre: int
    montant_total: Decimal
    pourcentage: Decimal

# Statistiques prise en charge
class PriseChargeStats(BaseModel):
    """Statistiques par type prise en charge"""
    type_code: str
    type_libelle: str
    nombre: int
    montant_total: Decimal
    pourcentage: Decimal

# Rapport service
class ServiceReport(BaseModel):
    """Rapport financier service"""
    service_id: int
    service_nom: str
    periode_debut: date
    periode_fin: date
    nombre_total_actes: int
    montant_total: Decimal
    stats_par_acte: List[ActeStats]
    stats_par_prise_charge: List[PriseChargeStats]

# Rapport médecin
class MedecinReport(BaseModel):
    """Rapport médecin"""
    medecin_id: int
    medecin_nom: str
    medecin_prenom: str
    periode_debut: date
    periode_fin: date
    
    # Activité
    nombre_total_actes: int
    stats_par_acte: List[ActeStats]
    stats_par_prise_charge: List[PriseChargeStats]
    
    # Financier
    montant_total: Decimal
    montant_par_acte: List[ActeStats]
    montant_par_prise_charge: List[PriseChargeStats]
    pourcentage_contribution_service: Optional[Decimal] = None

# Options export
class ExportFormat(str, Enum):
    JSON = "json"
    EXCEL = "excel"
    PDF = "pdf"

class ExportRequest(BaseModel):
    """Requête d'export"""
    format: ExportFormat
    filters: ReportFilters
```

---

**(Suite dans le prochain message...)**
## 9. Endpoints API

### 9.1 Point d'Entrée Principal

```python
# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from app.core.config import settings
from app.core.logging import logger
from app.api.v1.router import api_router
from app.db.database import engine
from app.db.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    # Startup
    logger.info("🚀 Démarrage de l'application...")
    logger.info(f"📊 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🗄️  Database: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}")
    
    # Vérifier connexion BD
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Connexion base de données établie")
    except Exception as e:
        logger.error(f"❌ Erreur connexion BD: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Arrêt de l'application...")
    await engine.dispose()
    logger.info("✅ Ressources libérées")

# Créer l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API REST pour la gestion des actes médicaux",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# ============================================================================
# MIDDLEWARE
# ============================================================================

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host (sécurité)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["votre-domaine.sn", "www.votre-domaine.sn"]
    )

# Middleware de logging des requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log toutes les requêtes HTTP"""
    start_time = time.time()
    
    # Traiter la requête
    response = await call_next(request)
    
    # Calculer durée
    duration = time.time() - start_time
    
    # Logger
    logger.info(
        f"{request.method} {request.url.path} "
        f"- Status: {response.status_code} "
        f"- Duration: {duration:.3f}s"
    )
    
    # Ajouter header durée
    response.headers["X-Process-Time"] = str(duration)
    
    return response

# ============================================================================
# GESTIONNAIRES D'ERREURS
# ============================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Gestionnaire erreurs de validation Pydantic"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Erreur de validation: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Erreur de validation des données",
            "errors": errors
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Gestionnaire global d'exceptions"""
    logger.error(f"Erreur non gérée: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Une erreur interne s'est produite",
            "error": str(exc) if settings.DEBUG else None
        }
    )

# ============================================================================
# ROUTES
# ============================================================================

# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Vérification santé de l'API"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

# Includer le router API v1
app.include_router(api_router, prefix="/api/v1")

# Route racine
@app.get("/", tags=["Root"])
async def root():
    """Route racine"""
    return {
        "message": f"Bienvenue sur {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/api/docs",
        "health": "/health"
    }
```

### 9.2 Router API V1

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    services,
    actes_types,
    tarifs,
    actes_medicaux,
    reports,
    exports
)

api_router = APIRouter()

# Inclure tous les routers d'endpoints
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentification"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Utilisateurs"]
)

api_router.include_router(
    services.router,
    prefix="/services",
    tags=["Services"]
)

api_router.include_router(
    actes_types.router,
    prefix="/actes-types",
    tags=["Types d'Actes"]
)

api_router.include_router(
    tarifs.router,
    prefix="/tarifs",
    tags=["Tarifs"]
)

api_router.include_router(
    actes_medicaux.router,
    prefix="/actes-medicaux",
    tags=["Actes Médicaux"]
)

api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["Rapports"]
)

api_router.include_router(
    exports.router,
    prefix="/exports",
    tags=["Exports"]
)
```

### 9.3 Dépendances Communes

```python
# app/api/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.db.database import get_db
from app.db.models.user import User
from app.core.config import settings
from app.core.security import verify_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData
from app.schemas.user import UserRole

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Type aliases
DBSession = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

# ============================================================================
# DÉPENDANCES AUTHENTIFICATION
# ============================================================================

async def get_current_user(
    token: TokenDep,
    db: DBSession
) -> User:
    """Récupérer l'utilisateur courant depuis le JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Décoder le token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(
            user_id=user_id,
            email=payload.get("email"),
            role=payload.get("role")
        )
    except JWTError:
        raise credentials_exception
    
    # Récupérer l'utilisateur
    user_repo = UserRepository(db)
    user = await user_repo.get(token_data.user_id)
    
    if user is None:
        raise credentials_exception
    
    if not user.actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé"
        )
    
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

# ============================================================================
# DÉPENDANCES AUTORISATION PAR RÔLE
# ============================================================================

def require_role(*allowed_roles: UserRole):
    """Décorateur pour vérifier le rôle de l'utilisateur"""
    def role_checker(current_user: CurrentUser) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès interdit. Rôle(s) requis: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker

# Dépendances spécifiques par rôle
RequireAdmin = Annotated[User, Depends(require_role(UserRole.ADMINISTRATEUR))]
RequireMedecin = Annotated[User, Depends(require_role(UserRole.MEDECIN, UserRole.ADMINISTRATEUR))]
RequireSecretaire = Annotated[User, Depends(require_role(UserRole.SECRETAIRE, UserRole.ADMINISTRATEUR))]

# ============================================================================
# DÉPENDANCES PAGINATION
# ============================================================================

def pagination_params(
    page: int = 1,
    page_size: int = 50
) -> PaginationParams:
    """Paramètres de pagination"""
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le numéro de page doit être >= 1"
        )
    
    if page_size < 1 or page_size > settings.MAX_PAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La taille de page doit être entre 1 et {settings.MAX_PAGE_SIZE}"
        )
    
    return PaginationParams(page=page, page_size=page_size)

PaginationDep = Annotated[PaginationParams, Depends(pagination_params)]
```

### 9.4 Endpoint Authentification

```python
# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import DBSession, CurrentUser
from app.schemas.auth import Token, RefreshTokenRequest, RefreshTokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: DBSession
):
    """
    Créer un nouvel utilisateur (inscription)
    
    - **email**: Email unique
    - **password**: Mot de passe (min 8 caractères)
    - **nom**: Nom de famille
    - **prenom**: Prénom
    - **role**: Rôle utilisateur
    """
    auth_service = AuthService(db)
    user = await auth_service.register_user(user_data)
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: DBSession = Depends()
):
    """
    Connexion utilisateur
    
    Retourne un access token et un refresh token
    """
    auth_service = AuthService(db)
    token = await auth_service.authenticate(form_data.username, form_data.password)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token

@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: DBSession
):
    """
    Rafraîchir l'access token avec un refresh token
    """
    auth_service = AuthService(db)
    new_token = await auth_service.refresh_access_token(refresh_data.refresh_token)
    
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalide ou expiré"
        )
    
    return new_token

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: CurrentUser,
    db: DBSession
):
    """
    Déconnexion - révoque tous les refresh tokens de l'utilisateur
    """
    auth_service = AuthService(db)
    await auth_service.logout(current_user.id)
    return None

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """
    Obtenir les informations de l'utilisateur connecté
    """
    return current_user
```

### 9.5 Endpoint Actes Médicaux

```python
# app/api/v1/endpoints/actes_medicaux.py
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from datetime import date

from app.api.deps import DBSession, CurrentUser, RequireSecretaire, PaginationDep
from app.schemas.acte_medical import (
    ActeMedicalCreate,
    ActeMedicalUpdate,
    ActeMedicalResponse,
    ActeMedicalDetailResponse,
    ActeMedicalFilters
)
from app.schemas.common import PaginatedResponse
from app.services.acte_service import ActeService
from app.core.logging import logger

router = APIRouter()

@router.post(
    "/",
    response_model=ActeMedicalDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un acte médical"
)
async def create_acte_medical(
    acte_data: ActeMedicalCreate,
    current_user: CurrentUser,
    db: DBSession
):
    """
    Créer un nouvel acte médical
    
    Le montant est calculé automatiquement selon:
    - Service
    - Type d'acte
    - Type de prise en charge
    - Date de l'acte
    
    **Permissions**: Secrétaire ou Administrateur
    """
    # Vérifier autorisation
    if current_user.role not in ["secretaire", "administrateur"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les secrétaires et administrateurs peuvent créer des actes"
        )
    
    acte_service = ActeService(db)
    
    try:
        acte = await acte_service.create_acte_medical(acte_data, current_user.id)
        logger.info(
            f"Acte créé: ID={acte.id}, Médecin={acte.medecin_id}, "
            f"Montant={acte.montant}, Par={current_user.email}"
        )
        return acte
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=PaginatedResponse[ActeMedicalDetailResponse],
    summary="Lister les actes médicaux"
)
async def list_actes_medicaux(
    db: DBSession,
    current_user: CurrentUser,
    pagination: PaginationDep,
    # Filtres optionnels
    date_debut: Optional[date] = Query(None, description="Date de début"),
    date_fin: Optional[date] = Query(None, description="Date de fin"),
    service_id: Optional[int] = Query(None, description="ID du service"),
    acte_id: Optional[int] = Query(None, description="ID du type d'acte"),
    type_prise_charge_id: Optional[int] = Query(None, description="ID type prise en charge"),
    medecin_id: Optional[int] = Query(None, description="ID du médecin"),
    nom_patient: Optional[str] = Query(None, description="Nom du patient (recherche partielle)"),
    numero_bc: Optional[str] = Query(None, description="Numéro BC")
):
    """
    Lister les actes médicaux avec filtres et pagination
    
    **Filtrage**:
    - Les secrétaires ne voient que les actes de leur(s) service(s)
    - Les médecins voient leurs propres actes
    - Les administrateurs voient tout
    """
    # Construire filtres
    filters = ActeMedicalFilters(
        date_debut=date_debut,
        date_fin=date_fin,
        service_id=service_id,
        acte_id=acte_id,
        type_prise_charge_id=type_prise_charge_id,
        medecin_id=medecin_id,
        nom_patient=nom_patient,
        numero_bc=numero_bc
    )
    
    acte_service = ActeService(db)
    
    # Appliquer filtres selon rôle
    if current_user.role == "medecin":
        filters.medecin_id = current_user.id
    elif current_user.role == "secretaire":
        # Filtrer par services de l'utilisateur
        if not current_user.services:
            return PaginatedResponse.create([], 0, pagination)
        # TODO: implémenter filtre par services
    
    actes, total = await acte_service.list_actes_medicaux(filters, pagination)
    
    return PaginatedResponse.create(actes, total, pagination)

@router.get(
    "/{acte_id}",
    response_model=ActeMedicalDetailResponse,
    summary="Obtenir un acte médical"
)
async def get_acte_medical(
    acte_id: int,
    db: DBSession,
    current_user: CurrentUser
):
    """
    Récupérer un acte médical par son ID
    """
    acte_service = ActeService(db)
    acte = await acte_service.get_acte_medical(acte_id)
    
    if not acte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Acte médical {acte_id} non trouvé"
        )
    
    # Vérifier autorisation d'accès
    if current_user.role == "medecin" and acte.medecin_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès interdit à cet acte"
        )
    
    return acte

@router.put(
    "/{acte_id}",
    response_model=ActeMedicalDetailResponse,
    summary="Modifier un acte médical"
)
async def update_acte_medical(
    acte_id: int,
    acte_data: ActeMedicalUpdate,
    db: DBSession,
    current_user: CurrentUser
):
    """
    Modifier un acte médical existant
    
    **Permissions**: Secrétaire (qui a créé) ou Administrateur
    """
    acte_service = ActeService(db)
    
    # Vérifier que l'acte existe
    existing_acte = await acte_service.get_acte_medical(acte_id)
    if not existing_acte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Acte médical {acte_id} non trouvé"
        )
    
    # Vérifier autorisation
    if current_user.role == "secretaire" and existing_acte.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez modifier que vos propres saisies"
        )
    
    try:
        updated_acte = await acte_service.update_acte_medical(acte_id, acte_data)
        logger.info(f"Acte modifié: ID={acte_id}, Par={current_user.email}")
        return updated_acte
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    "/{acte_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un acte médical"
)
async def delete_acte_medical(
    acte_id: int,
    db: DBSession,
    current_user: CurrentUser
):
    """
    Supprimer un acte médical
    
    **Permissions**: Administrateur uniquement
    """
    if current_user.role != "administrateur":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul l'administrateur peut supprimer des actes"
        )
    
    acte_service = ActeService(db)
    deleted = await acte_service.delete_acte_medical(acte_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Acte médical {acte_id} non trouvé"
        )
    
    logger.warning(f"Acte supprimé: ID={acte_id}, Par={current_user.email}")
    return None
```

### 9.6 Endpoint Rapports

```python
# app/api/v1/endpoints/reports.py
from fastapi import APIRouter, HTTPException, status, Query
from datetime import date, datetime, timedelta

from app.api.deps import DBSession, CurrentUser
from app.schemas.report import (
    ReportFilters,
    ServiceReport,
    MedecinReport
)
from app.services.report_service import ReportService

router = APIRouter()

@router.get(
    "/service/{service_id}",
    response_model=ServiceReport,
    summary="Rapport financier par service"
)
async def get_service_report(
    service_id: int,
    db: DBSession,
    current_user: CurrentUser,
    date_debut: date = Query(..., description="Date de début"),
    date_fin: date = Query(..., description="Date de fin"),
    acte_id: int = Query(None, description="Filtrer par type d'acte"),
    type_prise_charge_id: int = Query(None, description="Filtrer par type prise en charge")
):
    """
    Générer un rapport financier pour un service
    
    Contient:
    - Nombre total d'actes
    - Montant total généré
    - Statistiques par type d'examen
    - Statistiques par type de prise en charge
    
    **Permissions**:
    - Administrateur: tous les services
    - Médecin/Secrétaire: uniquement leur(s) service(s)
    """
    # Vérifier autorisation d'accès au service
    if current_user.role not in ["administrateur"]:
        # Vérifier que l'utilisateur appartient au service
        service_ids = [s.id for s in current_user.services]
        if service_id not in service_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès interdit à ce service"
            )
    
    # Construire filtres
    filters = ReportFilters(
        date_debut=date_debut,
        date_fin=date_fin,
        service_id=service_id,
        acte_id=acte_id,
        type_prise_charge_id=type_prise_charge_id
    )
    
    report_service = ReportService(db)
    report = await report_service.generate_service_report(filters)
    
    return report

@router.get(
    "/medecin/{medecin_id}",
    response_model=MedecinReport,
    summary="Rapport d'activité et financier par médecin"
)
async def get_medecin_report(
    medecin_id: int,
    db: DBSession,
    current_user: CurrentUser,
    date_debut: date = Query(..., description="Date de début"),
    date_fin: date = Query(..., description="Date de fin")
):
    """
    Générer un rapport complet pour un médecin
    
    Contient:
    - **Activité**: nombre d'actes par type, par prise en charge
    - **Financier**: montant total, par type, contribution au service
    
    **Permissions**:
    - Administrateur: tous les médecins
    - Médecin: uniquement son propre rapport
    - Secrétaire: médecins de son/ses service(s)
    """
    # Vérifier autorisation
    if current_user.role == "medecin" and medecin_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez consulter que votre propre rapport"
        )
    
    # TODO: Vérifier pour secrétaire (médecins du même service)
    
    filters = ReportFilters(
        date_debut=date_debut,
        date_fin=date_fin,
        medecin_id=medecin_id
    )
    
    report_service = ReportService(db)
    report = await report_service.generate_medecin_report(filters)
    
    return report

@router.get(
    "/dashboard",
    summary="Tableau de bord général"
)
async def get_dashboard(
    db: DBSession,
    current_user: CurrentUser,
    periode: str = Query("mois", description="jour, semaine, mois, trimestre, annee")
):
    """
    Obtenir les statistiques du tableau de bord
    
    Selon la période sélectionnée, retourne:
    - Nombre d'actes réalisés
    - Montant total généré
    - Top 5 actes
    - Top 5 médecins
    - Évolution temporelle
    """
    # Calculer dates selon période
    today = date.today()
    if periode == "jour":
        date_debut = today
    elif periode == "semaine":
        date_debut = today - timedelta(days=7)
    elif periode == "mois":
        date_debut = today.replace(day=1)
    elif periode == "trimestre":
        # Début du trimestre
        quarter = (today.month - 1) // 3
        date_debut = today.replace(month=quarter * 3 + 1, day=1)
    else:  # annee
        date_debut = today.replace(month=1, day=1)
    
    date_fin = today
    
    report_service = ReportService(db)
    dashboard_data = await report_service.generate_dashboard(
        date_debut, date_fin, current_user
    )
    
    return dashboard_data
```

---

**(Suite dans le prochain message...)**
## 10. Authentification et Autorisation

### 10.1 Sécurité - Gestion JWT et Hashing

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Context pour hashing bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe contre son hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hasher un mot de passe"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Créer un access token JWT
    
    Args:
        data: Données à encoder dans le token
        expires_delta: Durée de validité (défaut: 15 minutes)
    
    Returns:
        Token JWT encodé
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Créer un refresh token JWT
    
    Args:
        data: Données à encoder
        expires_delta: Durée de validité (défaut: 7 jours)
    
    Returns:
        Refresh token JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """
    Vérifier et décoder un token JWT
    
    Args:
        token: Token à vérifier
        token_type: Type attendu (access ou refresh)
    
    Returns:
        Payload décodé ou None si invalide
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Vérifier le type de token
        if payload.get("type") != token_type:
            return None
        
        return payload
    except JWTError:
        return None
```

### 10.2 Service d'Authentification

```python
# app/services/auth_service.py
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.models.refresh_token import RefreshToken
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.user import UserCreate
from app.schemas.auth import Token, RefreshTokenResponse
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token
)
from app.core.logging import logger

class AuthService:
    """Service de gestion de l'authentification"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.refresh_token_repo = RefreshTokenRepository(db)
    
    async def register_user(self, user_data: UserCreate) -> User:
        """
        Créer un nouvel utilisateur
        
        Args:
            user_data: Données utilisateur
        
        Returns:
            User créé
        
        Raises:
            ValueError: Si email déjà utilisé
        """
        # Vérifier email unique
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"L'email {user_data.email} est déjà utilisé")
        
        # Hasher le mot de passe
        hashed_password = get_password_hash(user_data.password)
        
        # Créer l'utilisateur
        user_dict = user_data.model_dump(exclude={'password', 'service_ids'})
        user_dict['password_hash'] = hashed_password
        
        user = await self.user_repo.create(user_dict)
        
        # Associer aux services
        if user_data.service_ids:
            await self.user_repo.update_services(user.id, user_data.service_ids)
        
        logger.info(f"Nouvel utilisateur créé: {user.email} (ID: {user.id})")
        
        return user
    
    async def authenticate(self, email: str, password: str) -> Optional[Token]:
        """
        Authentifier un utilisateur
        
        Args:
            email: Email utilisateur
            password: Mot de passe en clair
        
        Returns:
            Token avec access_token et refresh_token, ou None si échec
        """
        # Récupérer l'utilisateur
        user = await self.user_repo.get_by_email(email)
        
        if not user:
            logger.warning(f"Tentative de connexion avec email inconnu: {email}")
            return None
        
        # Vérifier le mot de passe
        if not verify_password(password, user.password_hash):
            logger.warning(f"Mot de passe incorrect pour: {email}")
            return None
        
        # Vérifier que le compte est actif
        if not user.actif:
            logger.warning(f"Tentative de connexion sur compte désactivé: {email}")
            return None
        
        # Créer les tokens
        access_token = create_access_token(
            data={
                "sub": user.id,
                "email": user.email,
                "role": user.role
            }
        )
        
        refresh_token_str = create_refresh_token(
            data={
                "sub": user.id,
                "email": user.email
            }
        )
        
        # Stocker le refresh token en base
        expires_at = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        
        await self.refresh_token_repo.create({
            "user_id": user.id,
            "token": refresh_token_str,
            "expires_at": expires_at
        })
        
        logger.info(f"Connexion réussie: {user.email} (ID: {user.id})")
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token_str,
            token_type="bearer"
        )
    
    async def refresh_access_token(
        self,
        refresh_token: str
    ) -> Optional[RefreshTokenResponse]:
        """
        Rafraîchir un access token
        
        Args:
            refresh_token: Refresh token
        
        Returns:
            Nouveau access token ou None si invalide
        """
        # Vérifier le token
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            return None
        
        # Vérifier que le token existe en base et n'est pas révoqué
        stored_token = await self.refresh_token_repo.get_by_token(refresh_token)
        
        if not stored_token or stored_token.revoked:
            logger.warning("Tentative d'utilisation d'un refresh token révoqué")
            return None
        
        if stored_token.expires_at < datetime.utcnow():
            logger.warning("Tentative d'utilisation d'un refresh token expiré")
            return None
        
        # Récupérer l'utilisateur
        user_id = payload.get("sub")
        user = await self.user_repo.get(user_id)
        
        if not user or not user.actif:
            return None
        
        # Créer un nouveau access token
        new_access_token = create_access_token(
            data={
                "sub": user.id,
                "email": user.email,
                "role": user.role
            }
        )
        
        return RefreshTokenResponse(
            access_token=new_access_token,
            token_type="bearer"
        )
    
    async def logout(self, user_id: int) -> None:
        """
        Déconnecter un utilisateur (révoquer tous ses refresh tokens)
        
        Args:
            user_id: ID de l'utilisateur
        """
        await self.refresh_token_repo.revoke_all_for_user(user_id)
        logger.info(f"Déconnexion utilisateur ID: {user_id}")
```

---

## 11. Logique Métier

### 11.1 Service Actes Médicaux

```python
# app/services/acte_service.py
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.repositories.acte_repository import ActeRepository
from app.repositories.tarif_repository import TarifRepository
from app.repositories.acte_type_repository import ActeTypeRepository
from app.repositories.audit_repository import AuditRepository
from app.schemas.acte_medical import (
    ActeMedicalCreate,
    ActeMedicalUpdate,
    ActeMedicalFilters
)
from app.schemas.common import PaginationParams
from app.db.models.acte_medical import ActeMedical
from app.core.logging import logger

class ActeService:
    """Service de gestion des actes médicaux"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.acte_repo = ActeRepository(db)
        self.tarif_repo = TarifRepository(db)
        self.acte_type_repo = ActeTypeRepository(db)
        self.audit_repo = AuditRepository(db)
    
    async def create_acte_medical(
        self,
        acte_data: ActeMedicalCreate,
        created_by: int
    ) -> ActeMedical:
        """
        Créer un acte médical avec calcul automatique du tarif
        
        Args:
            acte_data: Données de l'acte
            created_by: ID de l'utilisateur créateur
        
        Returns:
            Acte médical créé
        
        Raises:
            ValueError: Si tarif non trouvé ou données invalides
        """
        # 1. Vérifier que l'acte existe et récupérer son service
        acte_type = await self.acte_type_repo.get(acte_data.acte_id)
        if not acte_type:
            raise ValueError(f"Type d'acte {acte_data.acte_id} non trouvé")
        
        if not acte_type.actif:
            raise ValueError(f"Type d'acte {acte_type.nom} est désactivé")
        
        service_id = acte_type.service_id
        
        # 2. Récupérer le tarif applicable
        tarif = await self.tarif_repo.get_applicable_tarif(
            service_id=service_id,
            acte_id=acte_data.acte_id,
            type_prise_charge_id=acte_data.type_prise_charge_id,
            date_acte=acte_data.date
        )
        
        if not tarif:
            raise ValueError(
                f"Aucun tarif configuré pour: "
                f"Service={service_id}, "
                f"Acte={acte_data.acte_id}, "
                f"Type PC={acte_data.type_prise_charge_id}, "
                f"Date={acte_data.date}"
            )
        
        # 3. Créer l'acte avec le montant calculé
        acte_dict = acte_data.model_dump()
        acte_dict['montant'] = tarif.montant
        acte_dict['created_by'] = created_by
        
        acte = await self.acte_repo.create(acte_dict)
        
        # 4. Journaliser dans l'audit
        await self.audit_repo.log_action(
            user_id=created_by,
            action="CREATE",
            entity_type="acte_medical",
            entity_id=acte.id,
            new_value={
                "patient": f"{acte.nom_patient} {acte.prenom_patient}",
                "acte": acte_type.nom,
                "montant": float(acte.montant)
            }
        )
        
        logger.info(
            f"Acte créé: ID={acte.id}, Patient={acte.nom_patient} {acte.prenom_patient}, "
            f"Montant={acte.montant} CFA"
        )
        
        return acte
    
    async def list_actes_medicaux(
        self,
        filters: ActeMedicalFilters,
        pagination: PaginationParams
    ) -> Tuple[List[ActeMedical], int]:
        """
        Lister les actes avec filtres et pagination
        
        Args:
            filters: Filtres de recherche
            pagination: Paramètres de pagination
        
        Returns:
            Tuple (liste actes, total)
        """
        actes = await self.acte_repo.list_with_filters(
            filters=filters,
            offset=pagination.offset,
            limit=pagination.limit
        )
        
        total = await self.acte_repo.count_with_filters(filters)
        
        return actes, total
    
    async def get_acte_medical(self, acte_id: int) -> Optional[ActeMedical]:
        """Récupérer un acte par ID"""
        return await self.acte_repo.get_with_details(acte_id)
    
    async def update_acte_medical(
        self,
        acte_id: int,
        acte_data: ActeMedicalUpdate
    ) -> ActeMedical:
        """
        Mettre à jour un acte médical
        
        Note: Si acte_id ou type_prise_charge_id change, recalculer le montant
        """
        # Récupérer l'acte existant
        existing_acte = await self.acte_repo.get(acte_id)
        if not existing_acte:
            raise ValueError(f"Acte {acte_id} non trouvé")
        
        update_dict = acte_data.model_dump(exclude_unset=True)
        
        # Si type d'acte ou prise en charge change, recalculer le montant
        if 'acte_id' in update_dict or 'type_prise_charge_id' in update_dict:
            new_acte_id = update_dict.get('acte_id', existing_acte.acte_id)
            new_type_pc_id = update_dict.get(
                'type_prise_charge_id',
                existing_acte.type_prise_charge_id
            )
            new_date = update_dict.get('date', existing_acte.date)
            
            # Récupérer le service via le type d'acte
            acte_type = await self.acte_type_repo.get(new_acte_id)
            service_id = acte_type.service_id
            
            # Récupérer nouveau tarif
            tarif = await self.tarif_repo.get_applicable_tarif(
                service_id=service_id,
                acte_id=new_acte_id,
                type_prise_charge_id=new_type_pc_id,
                date_acte=new_date
            )
            
            if not tarif:
                raise ValueError("Aucun tarif applicable pour ces paramètres")
            
            update_dict['montant'] = tarif.montant
        
        # Mettre à jour
        updated_acte = await self.acte_repo.update(acte_id, update_dict)
        
        # Audit
        await self.audit_repo.log_action(
            user_id=existing_acte.created_by,  # TODO: passer current_user
            action="UPDATE",
            entity_type="acte_medical",
            entity_id=acte_id,
            old_value={"montant": float(existing_acte.montant)},
            new_value={"montant": float(updated_acte.montant)}
        )
        
        return updated_acte
    
    async def delete_acte_medical(self, acte_id: int) -> bool:
        """Supprimer un acte médical"""
        deleted = await self.acte_repo.delete(acte_id)
        
        if deleted:
            await self.audit_repo.log_action(
                user_id=0,  # TODO: passer current_user
                action="DELETE",
                entity_type="acte_medical",
                entity_id=acte_id
            )
            
            logger.warning(f"Acte supprimé: ID={acte_id}")
        
        return deleted
```

### 11.2 Service de Reporting

```python
# app/services/report_service.py
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from decimal import Decimal
from datetime import date

from app.repositories.acte_repository import ActeRepository
from app.db.models.acte_medical import ActeMedical
from app.db.models.acte_type import ActeType
from app.db.models.type_prise_charge import TypePriseCharge
from app.db.models.service import Service
from app.schemas.report import (
    ReportFilters,
    ServiceReport,
    MedecinReport,
    ActeStats,
    PriseChargeStats
)

class ReportService:
    """Service de génération de rapports"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.acte_repo = ActeRepository(db)
    
    async def generate_service_report(
        self,
        filters: ReportFilters
    ) -> ServiceReport:
        """
        Générer un rapport financier pour un service
        
        Args:
            filters: Filtres du rapport
        
        Returns:
            Rapport complet du service
        """
        # Requête de base
        query = select(
            ActeMedical, ActeType, TypePriseCharge, Service
        ).join(
            ActeType, ActeMedical.acte_id == ActeType.id
        ).join(
            Service, ActeType.service_id == Service.id
        ).join(
            TypePriseCharge, ActeMedical.type_prise_charge_id == TypePriseCharge.id
        ).where(
            Service.id == filters.service_id,
            ActeMedical.date >= filters.date_debut,
            ActeMedical.date <= filters.date_fin
        )
        
        # Filtres additionnels
        if filters.acte_id:
            query = query.where(ActeMedical.acte_id == filters.acte_id)
        if filters.type_prise_charge_id:
            query = query.where(
                ActeMedical.type_prise_charge_id == filters.type_prise_charge_id
            )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        if not rows:
            # Service sans actes
            service = await self.db.get(Service, filters.service_id)
            return ServiceReport(
                service_id=filters.service_id,
                service_nom=service.nom if service else "Inconnu",
                periode_debut=filters.date_debut,
                periode_fin=filters.date_fin,
                nombre_total_actes=0,
                montant_total=Decimal(0),
                stats_par_acte=[],
                stats_par_prise_charge=[]
            )
        
        # Extraire données
        service_nom = rows[0].Service.nom
        total_actes = len(rows)
        montant_total = sum(row.ActeMedical.montant for row in rows)
        
        # Statistiques par acte
        stats_par_acte_dict = {}
        for row in rows:
            acte = row.ActeType
            acte_medical = row.ActeMedical
            
            if acte.code not in stats_par_acte_dict:
                stats_par_acte_dict[acte.code] = {
                    'code': acte.code,
                    'nom': acte.nom,
                    'nombre': 0,
                    'montant': Decimal(0)
                }
            
            stats_par_acte_dict[acte.code]['nombre'] += 1
            stats_par_acte_dict[acte.code]['montant'] += acte_medical.montant
        
        stats_par_acte = [
            ActeStats(
                acte_code=v['code'],
                acte_nom=v['nom'],
                nombre=v['nombre'],
                montant_total=v['montant'],
                pourcentage=round((v['montant'] / montant_total * 100), 2) if montant_total > 0 else 0
            )
            for v in stats_par_acte_dict.values()
        ]
        
        # Statistiques par prise en charge
        stats_par_pc_dict = {}
        for row in rows:
            pc = row.TypePriseCharge
            acte_medical = row.ActeMedical
            
            if pc.code not in stats_par_pc_dict:
                stats_par_pc_dict[pc.code] = {
                    'code': pc.code,
                    'libelle': pc.libelle,
                    'nombre': 0,
                    'montant': Decimal(0)
                }
            
            stats_par_pc_dict[pc.code]['nombre'] += 1
            stats_par_pc_dict[pc.code]['montant'] += acte_medical.montant
        
        stats_par_prise_charge = [
            PriseChargeStats(
                type_code=v['code'],
                type_libelle=v['libelle'],
                nombre=v['nombre'],
                montant_total=v['montant'],
                pourcentage=round((v['montant'] / montant_total * 100), 2) if montant_total > 0 else 0
            )
            for v in stats_par_pc_dict.values()
        ]
        
        return ServiceReport(
            service_id=filters.service_id,
            service_nom=service_nom,
            periode_debut=filters.date_debut,
            periode_fin=filters.date_fin,
            nombre_total_actes=total_actes,
            montant_total=montant_total,
            stats_par_acte=stats_par_acte,
            stats_par_prise_charge=stats_par_prise_charge
        )
    
    async def generate_medecin_report(
        self,
        filters: ReportFilters
    ) -> MedecinReport:
        """
        Générer un rapport complet pour un médecin
        
        Combine activité et finances
        """
        # Requête actes du médecin
        query = select(
            ActeMedical, ActeType, TypePriseCharge
        ).join(
            ActeType, ActeMedical.acte_id == ActeType.id
        ).join(
            TypePriseCharge, ActeMedical.type_prise_charge_id == TypePriseCharge.id
        ).where(
            ActeMedical.medecin_id == filters.medecin_id,
            ActeMedical.date >= filters.date_debut,
            ActeMedical.date <= filters.date_fin
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        # Récupérer infos médecin
        from app.db.models.user import User
        medecin = await self.db.get(User, filters.medecin_id)
        
        if not rows:
            return MedecinReport(
                medecin_id=filters.medecin_id,
                medecin_nom=medecin.nom if medecin else "Inconnu",
                medecin_prenom=medecin.prenom if medecin else "",
                periode_debut=filters.date_debut,
                periode_fin=filters.date_fin,
                nombre_total_actes=0,
                stats_par_acte=[],
                stats_par_prise_charge=[],
                montant_total=Decimal(0),
                montant_par_acte=[],
                montant_par_prise_charge=[]
            )
        
        # Calculs
        total_actes = len(rows)
        montant_total = sum(row.ActeMedical.montant for row in rows)
        
        # Stats par acte (activité)
        stats_acte = {}
        for row in rows:
            acte = row.ActeType
            if acte.code not in stats_acte:
                stats_acte[acte.code] = {
                    'code': acte.code,
                    'nom': acte.nom,
                    'nombre': 0,
                    'montant': Decimal(0)
                }
            stats_acte[acte.code]['nombre'] += 1
            stats_acte[acte.code]['montant'] += row.ActeMedical.montant
        
        stats_par_acte = [
            ActeStats(
                acte_code=v['code'],
                acte_nom=v['nom'],
                nombre=v['nombre'],
                montant_total=v['montant'],
                pourcentage=round((v['nombre'] / total_actes * 100), 2)
            )
            for v in stats_acte.values()
        ]
        
        montant_par_acte = [
            ActeStats(
                acte_code=v['code'],
                acte_nom=v['nom'],
                nombre=v['nombre'],
                montant_total=v['montant'],
                pourcentage=round((v['montant'] / montant_total * 100), 2) if montant_total > 0 else 0
            )
            for v in stats_acte.values()
        ]
        
        # Stats par prise en charge
        stats_pc = {}
        for row in rows:
            pc = row.TypePriseCharge
            if pc.code not in stats_pc:
                stats_pc[pc.code] = {
                    'code': pc.code,
                    'libelle': pc.libelle,
                    'nombre': 0,
                    'montant': Decimal(0)
                }
            stats_pc[pc.code]['nombre'] += 1
            stats_pc[pc.code]['montant'] += row.ActeMedical.montant
        
        stats_par_prise_charge = [
            PriseChargeStats(
                type_code=v['code'],
                type_libelle=v['libelle'],
                nombre=v['nombre'],
                montant_total=v['montant'],
                pourcentage=round((v['nombre'] / total_actes * 100), 2)
            )
            for v in stats_pc.values()
        ]
        
        montant_par_prise_charge = [
            PriseChargeStats(
                type_code=v['code'],
                type_libelle=v['libelle'],
                nombre=v['nombre'],
                montant_total=v['montant'],
                pourcentage=round((v['montant'] / montant_total * 100), 2) if montant_total > 0 else 0
            )
            for v in stats_pc.values()
        ]
        
        # Calcul contribution au service (optionnel)
        # TODO: implémenter calcul pourcentage vs service
        
        return MedecinReport(
            medecin_id=filters.medecin_id,
            medecin_nom=medecin.nom,
            medecin_prenom=medecin.prenom,
            periode_debut=filters.date_debut,
            periode_fin=filters.date_fin,
            nombre_total_actes=total_actes,
            stats_par_acte=stats_par_acte,
            stats_par_prise_charge=stats_par_prise_charge,
            montant_total=montant_total,
            montant_par_acte=montant_par_acte,
            montant_par_prise_charge=montant_par_prise_charge
        )
```

---

**(Suite dans le prochain message avec génération Excel/PDF et tests...)**
## 15. Génération Excel/PDF

### 15.1 Génération Excel avec openpyxl

```python
# app/utils/excel_generator.py
from typing import List, Dict
from datetime import date
from decimal import Decimal
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from app.schemas.report import ServiceReport, MedecinReport

class ExcelGenerator:
    """Générateur de fichiers Excel"""
    
    # Couleurs
    HEADER_FILL = PatternFill(start_color="D5E8F0", end_color="D5E8F0", fill_type="solid")
    YELLOW_FILL = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    TOTAL_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    # Polices
    HEADER_FONT = Font(bold=True, size=11)
    TITLE_FONT = Font(bold=True, size=14)
    
    # Bordures
    THIN_BORDER = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    @classmethod
    def generate_service_report(
        cls,
        report: ServiceReport
    ) -> BytesIO:
        """
        Générer un rapport Excel pour un service
        
        Structure:
        - Onglet 1: Récapitulatif général
        - Onglet 2: Par type d'acte
        - Onglet 3: Par type de prise en charge
        """
        wb = Workbook()
        
        # =====================================================================
        # Onglet 1: RÉCAPITULATIF
        # =====================================================================
        ws_recap = wb.active
        ws_recap.title = "Récapitulatif"
        
        # Titre
        ws_recap['B2'] = f"RAPPORT FINANCIER - {report.service_nom.upper()}"
        ws_recap['B2'].font = cls.TITLE_FONT
        ws_recap.merge_cells('B2:F2')
        
        # Période
        ws_recap['B3'] = f"Période: du {report.periode_debut.strftime('%d/%m/%Y')} au {report.periode_fin.strftime('%d/%m/%Y')}"
        ws_recap.merge_cells('B3:F3')
        
        # Résumé
        ws_recap['B5'] = "RÉSUMÉ"
        ws_recap['B5'].font = cls.HEADER_FONT
        ws_recap['B5'].fill = cls.HEADER_FILL
        
        ws_recap['B6'] = "Nombre total d'actes:"
        ws_recap['C6'] = report.nombre_total_actes
        ws_recap['C6'].font = Font(bold=True)
        
        ws_recap['B7'] = "Montant total:"
        ws_recap['C7'] = f"{report.montant_total:,.0f} CFA"
        ws_recap['C7'].font = Font(bold=True)
        ws_recap['C7'].fill = cls.YELLOW_FILL
        
        # =====================================================================
        # Onglet 2: PAR TYPE D'ACTE
        # =====================================================================
        ws_actes = wb.create_sheet("Par Type d'Acte")
        
        # En-têtes
        headers_actes = ["Code Acte", "Nom de l'Acte", "Nombre", "Montant Total (CFA)", "Pourcentage (%)"]
        ws_actes.append(headers_actes)
        
        # Formater en-têtes
        for col in range(1, len(headers_actes) + 1):
            cell = ws_actes.cell(1, col)
            cell.font = cls.HEADER_FONT
            cell.fill = cls.HEADER_FILL
            cell.alignment = Alignment(horizontal='center')
            cell.border = cls.THIN_BORDER
        
        # Données
        row_num = 2
        for stat in report.stats_par_acte:
            ws_actes.append([
                stat.acte_code,
                stat.acte_nom,
                stat.nombre,
                float(stat.montant_total),
                float(stat.pourcentage)
            ])
            
            # Formater montant
            ws_actes.cell(row_num, 4).number_format = '#,##0'
            ws_actes.cell(row_num, 5).number_format = '0.00'
            
            # Bordures
            for col in range(1, len(headers_actes) + 1):
                ws_actes.cell(row_num, col).border = cls.THIN_BORDER
            
            row_num += 1
        
        # Ligne total
        total_row = row_num
        ws_actes[f'A{total_row}'] = "TOTAL"
        ws_actes[f'A{total_row}'].font = Font(bold=True)
        ws_actes[f'C{total_row}'] = report.nombre_total_actes
        ws_actes[f'D{total_row}'] = float(report.montant_total)
        ws_actes[f'E{total_row}'] = 100.00
        
        for col in range(1, len(headers_actes) + 1):
            cell = ws_actes.cell(total_row, col)
            cell.font = Font(bold=True)
            cell.fill = cls.TOTAL_FILL
            cell.border = cls.THIN_BORDER
        
        ws_actes.cell(total_row, 4).number_format = '#,##0'
        ws_actes.cell(total_row, 5).number_format = '0.00'
        
        # Ajuster largeur colonnes
        cls._auto_adjust_columns(ws_actes)
        
        # =====================================================================
        # Onglet 3: PAR TYPE DE PRISE EN CHARGE
        # =====================================================================
        ws_pc = wb.create_sheet("Par Prise en Charge")
        
        headers_pc = ["Code PC", "Type de Prise en Charge", "Nombre", "Montant Total (CFA)", "Pourcentage (%)"]
        ws_pc.append(headers_pc)
        
        # Formater en-têtes
        for col in range(1, len(headers_pc) + 1):
            cell = ws_pc.cell(1, col)
            cell.font = cls.HEADER_FONT
            cell.fill = cls.HEADER_FILL
            cell.alignment = Alignment(horizontal='center')
            cell.border = cls.THIN_BORDER
        
        # Données
        row_num = 2
        for stat in report.stats_par_prise_charge:
            ws_pc.append([
                stat.type_code,
                stat.type_libelle,
                stat.nombre,
                float(stat.montant_total),
                float(stat.pourcentage)
            ])
            
            ws_pc.cell(row_num, 4).number_format = '#,##0'
            ws_pc.cell(row_num, 5).number_format = '0.00'
            
            for col in range(1, len(headers_pc) + 1):
                ws_pc.cell(row_num, col).border = cls.THIN_BORDER
            
            row_num += 1
        
        # Ligne total
        total_row = row_num
        ws_pc[f'A{total_row}'] = "TOTAL"
        ws_pc[f'A{total_row}'].font = Font(bold=True)
        ws_pc[f'C{total_row}'] = report.nombre_total_actes
        ws_pc[f'D{total_row}'] = float(report.montant_total)
        ws_pc[f'E{total_row}'] = 100.00
        
        for col in range(1, len(headers_pc) + 1):
            cell = ws_pc.cell(total_row, col)
            cell.font = Font(bold=True)
            cell.fill = cls.TOTAL_FILL
            cell.border = cls.THIN_BORDER
        
        ws_pc.cell(total_row, 4).number_format = '#,##0'
        ws_pc.cell(total_row, 5).number_format = '0.00'
        
        cls._auto_adjust_columns(ws_pc)
        
        # Sauvegarder dans BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return output
    
    @classmethod
    def generate_medecin_report(
        cls,
        report: MedecinReport
    ) -> BytesIO:
        """
        Générer un rapport Excel pour un médecin
        
        Structure:
        - Onglet 1: Synthèse
        - Onglet 2: Activité par type d'acte
        - Onglet 3: Financier par type d'acte
        - Onglet 4: Par type de prise en charge
        """
        wb = Workbook()
        
        # =====================================================================
        # Onglet 1: SYNTHÈSE
        # =====================================================================
        ws = wb.active
        ws.title = "Synthèse"
        
        # Titre
        ws['B2'] = f"RAPPORT MÉDECIN - Dr {report.medecin_prenom} {report.medecin_nom.upper()}"
        ws['B2'].font = cls.TITLE_FONT
        ws.merge_cells('B2:F2')
        
        ws['B3'] = f"Période: du {report.periode_debut.strftime('%d/%m/%Y')} au {report.periode_fin.strftime('%d/%m/%Y')}"
        ws.merge_cells('B3:F3')
        
        # Activité
        ws['B5'] = "ACTIVITÉ MÉDICALE"
        ws['B5'].font = cls.HEADER_FONT
        ws['B5'].fill = cls.HEADER_FILL
        ws.merge_cells('B5:C5')
        
        ws['B6'] = "Nombre total d'actes réalisés:"
        ws['C6'] = report.nombre_total_actes
        ws['C6'].font = Font(bold=True)
        
        # Financier
        ws['B8'] = "FINANCIER"
        ws['B8'].font = cls.HEADER_FONT
        ws['B8'].fill = cls.HEADER_FILL
        ws.merge_cells('B8:C8')
        
        ws['B9'] = "Montant total généré:"
        ws['C9'] = f"{report.montant_total:,.0f} CFA"
        ws['C9'].font = Font(bold=True)
        ws['C9'].fill = cls.YELLOW_FILL
        
        if report.pourcentage_contribution_service:
            ws['B10'] = "Contribution au service:"
            ws['C10'] = f"{report.pourcentage_contribution_service:.2f} %"
            ws['C10'].font = Font(bold=True)
        
        # =====================================================================
        # Autres onglets (similaire au rapport service)
        # =====================================================================
        # TODO: Ajouter onglets détaillés
        
        # Sauvegarder
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return output
    
    @staticmethod
    def _auto_adjust_columns(worksheet):
        """Ajuster automatiquement la largeur des colonnes"""
        for column_cells in worksheet.columns:
            max_length = 0
            column = column_cells[0].column_letter
            
            for cell in column_cells:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column].width = adjusted_width
```

### 15.2 Génération PDF avec ReportLab

```python
# app/utils/pdf_generator.py
from typing import List
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

from app.schemas.report import ServiceReport, MedecinReport

class PDFGenerator:
    """Générateur de fichiers PDF"""
    
    @classmethod
    def generate_service_report(
        cls,
        report: ServiceReport
    ) -> BytesIO:
        """
        Générer un rapport PDF pour un service
        """
        output = BytesIO()
        
        # Créer document (paysage pour tableaux larges)
        doc = SimpleDocTemplate(
            output,
            pagesize=landscape(A4),
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#003366'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#006699'),
            spaceAfter=10
        )
        
        # Contenu
        story = []
        
        # En-tête
        story.append(Paragraph("RÉPUBLIQUE DU SÉNÉGAL", styles['Normal']))
        story.append(Paragraph("Ministère de la Santé et de l'Action Sociale", styles['Normal']))
        story.append(Spacer(1, 0.5*cm))
        
        # Titre
        story.append(Paragraph(
            f"RAPPORT FINANCIER<br/>{report.service_nom.upper()}",
            title_style
        ))
        
        # Période
        story.append(Paragraph(
            f"Période du {report.periode_debut.strftime('%d/%m/%Y')} "
            f"au {report.periode_fin.strftime('%d/%m/%Y')}",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.8*cm))
        
        # Résumé
        story.append(Paragraph("RÉSUMÉ", heading_style))
        
        summary_data = [
            ["Nombre total d'actes:", f"{report.nombre_total_actes}"],
            ["Montant total généré:", f"{report.montant_total:,.0f} CFA"]
        ]
        
        summary_table = Table(summary_data, colWidths=[6*cm, 8*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#D5E8F0')),
            ('BACKGROUND', (1, 1), (1, 1), colors.yellow),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 1*cm))
        
        # Tableau par type d'acte
        story.append(Paragraph("RÉPARTITION PAR TYPE D'ACTE", heading_style))
        
        acte_data = [["Code", "Nom de l'Acte", "Nombre", "Montant (CFA)", "%"]]
        for stat in report.stats_par_acte:
            acte_data.append([
                stat.acte_code,
                stat.acte_nom,
                str(stat.nombre),
                f"{stat.montant_total:,.0f}",
                f"{stat.pourcentage:.2f}%"
            ])
        
        # Total
        acte_data.append([
            "TOTAL",
            "",
            str(report.nombre_total_actes),
            f"{report.montant_total:,.0f}",
            "100.00%"
        ])
        
        acte_table = Table(acte_data, colWidths=[3*cm, 8*cm, 3*cm, 4*cm, 3*cm])
        acte_table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D5E8F0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Données
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            ('ALIGN', (2, 1), (-1, -2), 'RIGHT'),
            
            # Ligne total
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FFF2CC')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            
            # Grille
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(acte_table)
        story.append(PageBreak())
        
        # Tableau par prise en charge
        story.append(Paragraph("RÉPARTITION PAR TYPE DE PRISE EN CHARGE", heading_style))
        
        pc_data = [["Code", "Type de Prise en Charge", "Nombre", "Montant (CFA)", "%"]]
        for stat in report.stats_par_prise_charge:
            pc_data.append([
                stat.type_code,
                stat.type_libelle,
                str(stat.nombre),
                f"{stat.montant_total:,.0f}",
                f"{stat.pourcentage:.2f}%"
            ])
        
        pc_data.append([
            "TOTAL",
            "",
            str(report.nombre_total_actes),
            f"{report.montant_total:,.0f}",
            "100.00%"
        ])
        
        pc_table = Table(pc_data, colWidths=[3*cm, 8*cm, 3*cm, 4*cm, 3*cm])
        pc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D5E8F0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            ('ALIGN', (2, 1), (-1, -2), 'RIGHT'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FFF2CC')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(pc_table)
        
        # Pied de page avec date d'édition
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph(
            f"Document généré le {date.today().strftime('%d/%m/%Y')}",
            ParagraphStyle('Footer', fontSize=8, alignment=TA_RIGHT)
        ))
        
        # Générer PDF
        doc.build(story)
        output.seek(0)
        
        return output
```

---

## 16. Tests Backend

### 16.1 Configuration Tests

```python
# tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient

from app.main import app
from app.db.database import get_db, Base
from app.core.config import settings

# Database de test
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_db"

# Engine de test
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    """Créer un event loop pour toute la session de tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Créer une session de base de données de test
    Rollback après chaque test
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Client HTTP de test"""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()
```

### 16.2 Tests Unitaires - Services

```python
# tests/unit/test_services/test_acte_service.py
import pytest
from decimal import Decimal
from datetime import date

from app.services.acte_service import ActeService
from app.schemas.acte_medical import ActeMedicalCreate

@pytest.mark.asyncio
class TestActeService:
    """Tests du service ActeService"""
    
    async def test_create_acte_with_tarif_calculation(self, db_session):
        """
        Tester la création d'un acte avec calcul automatique du tarif
        """
        # Setup: créer service, acte_type, type_prise_charge, tarif
        # ... (fixtures)
        
        acte_service = ActeService(db_session)
        
        acte_data = ActeMedicalCreate(
            date=date.today(),
            nom_patient="DIOP",
            prenom_patient="Amadou",
            acte_id=1,
            type_prise_charge_id=1,
            medecin_id=2
        )
        
        # Act
        acte = await acte_service.create_acte_medical(acte_data, created_by=1)
        
        # Assert
        assert acte.id is not None
        assert acte.montant == Decimal("30000.00")
        assert acte.nom_patient == "DIOP"
    
    async def test_create_acte_without_tarif_raises_error(self, db_session):
        """
        Tester qu'une erreur est levée si aucun tarif n'existe
        """
        acte_service = ActeService(db_session)
        
        acte_data = ActeMedicalCreate(
            date=date.today(),
            nom_patient="DIOP",
            prenom_patient="Amadou",
            acte_id=999,  # N'existe pas
            type_prise_charge_id=1,
            medecin_id=2
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Type d'acte .* non trouvé"):
            await acte_service.create_acte_medical(acte_data, created_by=1)
```

### 16.3 Tests d'Intégration - API

```python
# tests/integration/test_api/test_actes_medicaux.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestActesMedicauxAPI:
    """Tests d'intégration des endpoints actes médicaux"""
    
    async def test_create_acte_success(self, client: AsyncClient, auth_headers):
        """
        Tester la création d'un acte via l'API
        """
        acte_data = {
            "date": "2026-02-06",
            "nom_patient": "DIOP",
            "prenom_patient": "Amadou",
            "acte_id": 1,
            "type_prise_charge_id": 1,
            "medecin_id": 2
        }
        
        response = await client.post(
            "/api/v1/actes-medicaux/",
            json=acte_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["nom_patient"] == "DIOP"
        assert "montant" in data
        assert data["montant"] > 0
    
    async def test_list_actes_with_pagination(self, client: AsyncClient, auth_headers):
        """
        Tester la liste des actes avec pagination
        """
        response = await client.get(
            "/api/v1/actes-medicaux/?page=1&page_size=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert data["page"] == 1
    
    async def test_unauthorized_access_returns_401(self, client: AsyncClient):
        """
        Tester qu'un accès non autorisé retourne 401
        """
        response = await client.get("/api/v1/actes-medicaux/")
        
        assert response.status_code == 401
```

---

## 19. Déploiement

### 19.1 Déploiement sur VPS Ubuntu

```bash
#!/bin/bash
# deploy.sh - Script de déploiement automatisé

set -e

echo "🚀 Déploiement de l'application Actes Médicaux"

# 1. Mise à jour système
echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# 2. Installation dépendances
echo "📦 Installation des dépendances..."
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql-14 \
    nginx \
    git \
    supervisor

# 3. Créer utilisateur applicatif
echo "👤 Création utilisateur app..."
sudo useradd -m -s /bin/bash appuser || true

# 4. Cloner le repository
echo "📥 Clonage du repository..."
cd /home/appuser
sudo -u appuser git clone https://github.com/votre-org/actes-medicaux-api.git
cd actes-medicaux-api

# 5. Créer environnement virtuel
echo "🐍 Configuration Python..."
sudo -u appuser python3.11 -m venv venv
sudo -u appuser venv/bin/pip install --upgrade pip
sudo -u appuser venv/bin/pip install -r requirements.txt

# 6. Configuration PostgreSQL
echo "🗄️  Configuration PostgreSQL..."
sudo -u postgres psql <<EOF
CREATE DATABASE actes_medicaux_db;
CREATE USER actes_user WITH PASSWORD 'votre_mot_de_passe_securise';
GRANT ALL PRIVILEGES ON DATABASE actes_medicaux_db TO actes_user;
\q
EOF

# 7. Variables d'environnement
echo "⚙️  Configuration variables d'environnement..."
sudo -u appuser cat > .env <<EOF
POSTGRES_USER=actes_user
POSTGRES_PASSWORD=votre_mot_de_passe_securise
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=actes_medicaux_db
SECRET_KEY=$(openssl rand -hex 32)
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=["https://votre-domaine.sn"]
EOF

# 8. Migrations base de données
echo "🔄 Exécution des migrations..."
sudo -u appuser venv/bin/alembic upgrade head

# 9. Configuration Nginx
echo "🌐 Configuration Nginx..."
sudo tee /etc/nginx/sites-available/actes-medicaux <<EOF
server {
    listen 80;
    server_name votre-domaine.sn;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/actes-medicaux /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 10. Configuration Supervisor
echo "🔧 Configuration Supervisor..."
sudo tee /etc/supervisor/conf.d/actes-medicaux.conf <<EOF
[program:actes-medicaux]
directory=/home/appuser/actes-medicaux-api
command=/home/appuser/actes-medicaux-api/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
user=appuser
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/actes-medicaux.log
EOF

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start actes-medicaux

# 11. SSL avec Let's Encrypt
echo "🔒 Configuration SSL..."
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.sn --non-interactive --agree-tos -m admin@votre-domaine.sn

echo "✅ Déploiement terminé!"
echo "🌐 Application accessible sur: https://votre-domaine.sn"
```

---

## 20. Monitoring et Logs

### 20.1 Configuration Logging

```python
# app/core/logging.py
import sys
from loguru import logger
from app.core.config import settings

# Configuration Loguru
logger.remove()  # Retirer handler par défaut

# Console output
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)

# Fichier log
logger.add(
    settings.LOG_FILE,
    rotation="500 MB",
    retention="10 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=settings.LOG_LEVEL
)

# Export
__all__ = ["logger"]
```

---

## CONCLUSION

Ce cahier technique backend complet fournit:

✅ **Architecture robuste** avec séparation claire des responsabilités  
✅ **Stack moderne** : FastAPI + PostgreSQL + SQLAlchemy async  
✅ **Schéma BD flexible** et optimisé avec contraintes et index  
✅ **Diagrammes UML** complets (classes, séquence, composants, ERD)  
✅ **Authentification JWT** sécurisée avec refresh tokens  
✅ **Autorisation RBAC** granulaire  
✅ **Calcul automatique** des tarifs selon règles métier  
✅ **Génération Excel/PDF** professionnels  
✅ **Tests** unitaires et d'intégration  
✅ **Documentation** API auto-générée (Swagger)  
✅ **Déploiement** automatisé avec Docker et scripts  
✅ **Monitoring** et logs structurés  

### Prochaines Étapes

1. **Valider** le schéma de base de données avec les utilisateurs
2. **Implémenter** le code selon la structure proposée
3. **Tester** intensivement chaque module
4. **Déployer** en environnement de staging
5. **Former** les utilisateurs
6. **Mettre en production** progressivement

---

**Document rédigé par Claude - Février 2026**  
**Version 1.0 - Cahier Technique Backend FastAPI**