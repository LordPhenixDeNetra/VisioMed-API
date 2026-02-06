# VisioMed - Gestion des Actes Médicaux

**VisioMed** est une API Backend moderne et robuste développée avec **FastAPI** pour la gestion des actes médicaux, spécifiquement conçue pour l'Unité d'Endoscopies Digestive et Bronchique et le Service de Médecine Interne.

Elle permet la gestion complète des patients, des actes médicaux, de la tarification, ainsi que la génération de rapports financiers et médicaux.

---

## 🚀 Fonctionnalités Clés

*   **Authentification & Sécurité** : Gestion des utilisateurs (Admin, Médecin, Secrétaire, Visualiseur), Authentification JWT (Access & Refresh Tokens), et Contrôle d'accès basé sur les rôles (RBAC).
*   **Gestion des Actes Médicaux** : Enregistrement, suivi et historique des actes (Endoscopie, Coloscopie, etc.).
*   **Tarification Dynamique** : Gestion des tarifs par acte et par type de prise en charge (IPM, Lettre de Garantie, etc.), avec support de la temporalité.
*   **Reporting & Export** : Génération de rapports financiers, export des données en Excel et PDF.
*   **Audit & Traçabilité** : Journalisation complète des actions critiques pour la sécurité et la conformité.
*   **Architecture Robuste** : Clean Architecture, Async SQLAlchemy, Pydantic v2, et Migrations Alembic.

---

## 🛠 Stack Technique

*   **Langage** : Python 3.11+
*   **Framework** : FastAPI
*   **Base de Données** : PostgreSQL
*   **ORM** : SQLAlchemy (Async)
*   **Migrations** : Alembic
*   **Authentification** : Python-Jose (JWT), Passlib (Bcrypt)
*   **Validation** : Pydantic
*   **Tests** : Pytest, Pytest-Asyncio
*   **Outils** : Uvicorn, Black, Ruff, Loguru

---

## ⚙️ Prérequis

Avant de commencer, assurez-vous d'avoir installé :
*   Python 3.11 ou supérieur
*   PostgreSQL
*   Git

---

## 📦 Installation

1.  **Cloner le projet**

    ```bash
    git clone https://github.com/votre-utilisateur/visiomed.git
    cd visiomed
    ```

2.  **Créer un environnement virtuel**

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/MacOS
    source .venv/bin/activate
    ```

3.  **Installer les dépendances**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration de l'environnement**

    Créez un fichier `.env` à la racine du projet en vous basant sur `.env.example`.

    ```env
    # Exemple de configuration .env
    APP_NAME=VisioMed
    DEBUG=True
    
    # Base de données
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=votre_mot_de_passe
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_DB=visiomed_db

    # Sécurité
    SECRET_KEY=votre_cle_secrete_tres_longue_et_aleatoire
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

---

## 🗄️ Base de Données

1.  **Appliquer les migrations**

    Créez les tables dans la base de données :

    ```bash
    alembic upgrade head
    ```

2.  **Initialiser les données (Seeding)**

    Peuplez la base avec les données de référence (Rôles, Services, Types d'actes, Utilisateurs par défaut) :

    ```bash
    python -m app.initial_data
    ```

    *Comptes par défaut créés :*
    *   **Admin** : `admin@visiomed.com` / `admin123`
    *   **Médecin** : `aminata.kane@visiomed.com` / `medecin123`
    *   **Secrétaire** : `fatou.ndiaye@visiomed.com` / `secretaire123`

---

## ▶️ Démarrage

Lancez le serveur de développement :

```bash
uvicorn main:app --reload
```

L'application sera accessible sur :
*   **API** : http://127.0.0.1:8000
*   **Documentation Swagger** : http://127.0.0.1:8000/docs
*   **Documentation ReDoc** : http://127.0.0.1:8000/redoc

---

## 🧪 Tests

Pour exécuter la suite de tests unitaires et d'intégration :

```bash
pytest
```

---

## 📂 Structure du Projet

```
VisioMed/
├── alembic/              # Scripts de migration DB
├── app/
│   ├── api/              # Endpoints API (Routes)
│   ├── core/             # Configuration, Sécurité, Logging
│   ├── db/               # Configuration DB et Modèles
│   ├── repositories/     # Couche d'accès aux données (CRUD)
│   ├── schemas/          # Modèles Pydantic (DTOs)
│   ├── services/         # Logique métier
│   └── initial_data.py   # Script de seed
├── tests/                # Tests automatisés
├── .env                  # Variables d'environnement
├── main.py               # Point d'entrée de l'application
└── requirements.txt      # Dépendances Python
```

---

## 📝 Auteurs

*   **VisioMed Team** - *Développement Backend*

---

## 📄 Licence

Ce projet est sous licence propriétaire - Voir le fichier LICENSE pour plus de détails.


<!-- uvicorn main:app --reload -->