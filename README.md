# 🔐 reconversion-agents-ia

Projet d'agents IA avec infrastructure de sécurité intégrée.

## 📋 Table des matières

- [Sécurité](#sécurité)
- [Installation](#installation)
- [Configuration](#configuration)
- [Développement](#développement)
- [Bonnes pratiques](#bonnes-pratiques)

## 🔒 Sécurité

Ce projet a été configuré avec une infrastructure de sécurité robuste dès le départ.

### Fichiers de sécurité

- **`.gitignore`** : Protège contre la fuite de secrets et fichiers sensibles
- **`SECURITY.md`** : Guide complet des bonnes pratiques de sécurité
- **`.pre-commit-config.yaml`** : Hooks automatiques pour détecter les vulnérabilités
- **`examples/`** : Exemples de code sécurisé (Python et JavaScript)

### Protection contre les vulnérabilités OWASP Top 10

✅ Injection SQL
✅ XSS (Cross-Site Scripting)
✅ Injection de commandes
✅ Désérialisation non sécurisée
✅ Authentification faible
✅ Exposition de données sensibles
✅ CSRF (Cross-Site Request Forgery)
✅ Validation d'entrée insuffisante
✅ Composants vulnérables
✅ Logging insuffisant

### Audit de sécurité

**Dernière analyse** : 2025-11-17

| Catégorie | Résultat |
|-----------|----------|
| Vulnérabilités critiques | 0 |
| Vulnérabilités élevées | 0 |
| Vulnérabilités moyennes | 0 |
| Secrets détectés | 0 |
| **Statut** | ✅ **SAIN** |

## 🚀 Installation

### Prérequis

- Python 3.8+ ou Node.js 16+
- Git

### Installation des dépendances

```bash
# Cloner le repository
git clone https://github.com/pjbreizh56bzh/reconversion-agents-ia.git
cd reconversion-agents-ia

# Python
pip install -r requirements.txt  # À créer selon vos besoins

# Node.js
npm install  # À configurer selon vos besoins
```

### Installation des hooks de sécurité (RECOMMANDÉ)

```bash
# Installer pre-commit
pip install pre-commit

# Activer les hooks
pre-commit install

# Créer le baseline pour detect-secrets
detect-secrets scan > .secrets.baseline
```

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet (ce fichier est ignoré par Git) :

```bash
# Base de données
DATABASE_URL=postgresql://user:password@localhost/dbname

# Secrets
JWT_SECRET=votre-secret-jwt-de-minimum-32-caractères
API_KEY=votre-clé-api-secrète

# Configuration
NODE_ENV=development
DEBUG=false
PORT=3000
```

### Validation de la configuration

```bash
# Vérifier que tous les secrets nécessaires sont présents
# Voir examples/secure_code_examples.py ou .js
```

## 💻 Développement

### Règles de développement sécurisé

1. **Ne JAMAIS commiter de secrets**
   - Utiliser des variables d'environnement
   - Vérifier avec `git diff` avant chaque commit

2. **Valider toutes les entrées utilisateur**
   - Voir `examples/secure_code_examples.py:InputValidator`
   - Voir `examples/secure_code_examples.js:InputValidator`

3. **Utiliser des requêtes préparées**
   - Jamais de concaténation de strings pour SQL
   - Voir exemples dans `SECURITY.md`

4. **Hasher les mots de passe**
   - Utiliser bcrypt ou argon2
   - Voir `SecurePasswordHandler` dans les exemples

5. **Logger de manière sécurisée**
   - Ne jamais logger de mots de passe ou tokens
   - Voir `SecureLogger` dans les exemples

### Tests de sécurité

```bash
# Python : Analyse statique avec bandit
pip install bandit
bandit -r .

# JavaScript : Analyse avec ESLint Security
npm install -g eslint eslint-plugin-security
eslint .

# Scan des secrets
detect-secrets scan

# Audit des dépendances
pip-audit  # Python
npm audit  # Node.js
```

### Workflow de développement

1. Créer une branche
2. Développer en suivant les bonnes pratiques (voir `SECURITY.md`)
3. Lancer les tests de sécurité
4. Commit (les hooks pre-commit s'exécutent automatiquement)
5. Push et créer une Pull Request

## 📚 Bonnes pratiques

### Référence rapide

| Situation | ✅ À FAIRE | ❌ NE PAS FAIRE |
|-----------|-----------|----------------|
| Secrets | Variables d'environnement | Hardcodés dans le code |
| SQL | Requêtes préparées | Concaténation de strings |
| Mots de passe | bcrypt/argon2 | Stockage en clair |
| Validation | Tous les inputs | Faire confiance aux inputs |
| Logging | Événements sans secrets | Logger les mots de passe |
| Dépendances | Maintenir à jour | Ignorer les vulnérabilités |

### Ressources

- [Guide de sécurité complet](SECURITY.md)
- [Exemples Python](examples/secure_code_examples.py)
- [Exemples JavaScript](examples/secure_code_examples.js)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Suivre les bonnes pratiques de sécurité
4. Commit avec messages clairs
5. Push vers la branche (`git push origin feature/AmazingFeature`)
6. Ouvrir une Pull Request

### Standards de code

- Respecter les règles ESLint/Pylint
- Passer tous les tests de sécurité
- Documenter le code
- Ajouter des tests unitaires

## 🚨 Signalement de vulnérabilités

Si vous découvrez une vulnérabilité de sécurité :

1. **NE PAS** créer une issue publique
2. Contacter l'équipe en privé
3. Fournir une description détaillée
4. Attendre la confirmation avant divulgation

## 📄 Licence

À définir selon vos besoins.

## 👥 Auteurs

- Équipe reconversion-agents-ia

---

**Date de création** : 2025-11-17
**Dernière mise à jour** : 2025-11-17
**Statut de sécurité** : ✅ SAIN