# 🍷 VinPedia - Catalogue d'Alcools Faits Maison

Une application Streamlit complète pour gérer un catalogue privé d'alcools faits maison avec authentification et système de validation.

## 🚀 Fonctionnalités

### 🔐 Authentification
- Système d'authentification simple avec liste blanche d'emails
- Distinction entre utilisateurs normaux et administrateurs
- Session sécurisée avec déconnexion

### 🏠 Galerie de Recettes
- Affichage des recettes validées uniquement
- Filtres par type d'alcool et prix maximum
- Cartes de recettes avec images et détails complets
- Interface responsive et moderne

### 📝 Proposition de Recettes
- Formulaire complet pour soumettre de nouvelles recettes
- Upload d'images avec sauvegarde automatique
- Validation des champs obligatoires
- Recettes en attente de validation par défaut

### 🔧 Interface d'Administration
- Accessible uniquement aux administrateurs
- Liste des recettes en attente de validation
- Boutons pour valider ou refuser les recettes
- Statistiques en temps réel

### 💾 Stockage et Données
- Base de données JSON pour les recettes
- Sauvegarde automatique des images uploadées
- IDs uniques pour chaque recette
- Gestion des dates de création et validation

## 🛠️ Installation

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Lancer l'application**
```bash
streamlit run src/main.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## 👥 Comptes de Test

### Administrateur
- **Email**: `admin@vinpedia.com`
- **Mot de passe**: `admin123`
- **Accès**: Toutes les fonctionnalités + administration

### Utilisateur Normal
- **Email**: `user@example.com` ou `test@test.com`
- **Mot de passe**: `user123`
- **Accès**: Galerie et proposition de recettes

## 📁 Structure du Projet

```
catalogue-alcools-streamlit/
├── src/
│   └── main.py              # Application principale
├── data/
│   ├── recipes.json         # Base de données des recettes
│   └── images/              # Dossier des images uploadées
├── requirements.txt         # Dépendances Python
└── README.md               # Documentation
```

## 🔧 Configuration

### Emails Autorisés
Modifiez la liste `ALLOWED_EMAILS` dans `src/main.py` :
```python
ALLOWED_EMAILS = ["user@example.com", "test@test.com", ADMIN_EMAIL]
```

### Compte Administrateur
Modifiez les variables dans `src/main.py` :
```python
ADMIN_EMAIL = "admin@vinpedia.com"
ADMIN_PASSWORD = "admin123"
```

**Développé avec ❤️ et Streamlit**
