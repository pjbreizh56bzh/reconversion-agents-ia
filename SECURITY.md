# 🔒 GUIDE DE SÉCURITÉ - RECONVERSION AGENTS IA

## Table des matières
1. [Principes de sécurité](#principes-de-sécurité)
2. [Gestion des secrets](#gestion-des-secrets)
3. [Protection contre les vulnérabilités OWASP Top 10](#protection-contre-les-vulnérabilités-owasp-top-10)
4. [Bonnes pratiques par langage](#bonnes-pratiques-par-langage)
5. [Audit et monitoring](#audit-et-monitoring)
6. [Checklist avant commit](#checklist-avant-commit)

---

## Principes de sécurité

### 🎯 Règles d'or

1. **Principe du moindre privilège** : Donner uniquement les accès nécessaires
2. **Défense en profondeur** : Plusieurs couches de sécurité
3. **Sécurité par défaut** : Configuration sécurisée dès le début
4. **Validation stricte** : Ne jamais faire confiance aux entrées utilisateur
5. **Fail securely** : En cas d'erreur, échouer de manière sécurisée

---

## Gestion des secrets

### ✅ À FAIRE

```bash
# Utiliser des variables d'environnement
export API_KEY="votre-clé-secrète"
export DATABASE_URL="postgresql://user:pass@localhost/db"

# Dans le code (Python)
import os
api_key = os.getenv('API_KEY')

# Dans le code (JavaScript/Node.js)
const apiKey = process.env.API_KEY;
```

### ❌ NE JAMAIS FAIRE

```python
# ❌ DANGER : Secrets en dur dans le code
API_KEY = "sk-1234567890abcdef"  # NE JAMAIS FAIRE
PASSWORD = "motdepasse123"       # NE JAMAIS FAIRE
```

### 🛠️ Outils recommandés

- **Python** : `python-dotenv`, `keyring`
- **Node.js** : `dotenv`, `node-vault`
- **Général** : `git-secrets`, `detect-secrets`, `truffleHog`

---

## Protection contre les vulnérabilités OWASP Top 10

### 1️⃣ Injection SQL

#### ❌ Code vulnérable
```python
# DANGER : Vulnérable à l'injection SQL
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

#### ✅ Code sécurisé
```python
# SÉCURISÉ : Requêtes préparées
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))

# OU avec ORM (SQLAlchemy)
user = User.query.filter_by(username=username).first()
```

### 2️⃣ Cross-Site Scripting (XSS)

#### ❌ Code vulnérable (JavaScript)
```javascript
// DANGER : Vulnérable à XSS
element.innerHTML = userInput;
```

#### ✅ Code sécurisé
```javascript
// SÉCURISÉ : Échappement automatique
element.textContent = userInput;

// OU avec React (échappe automatiquement)
return <div>{userInput}</div>;
```

### 3️⃣ Injection de commandes

#### ❌ Code vulnérable
```python
# DANGER : Vulnérable à l'injection de commandes
import os
os.system(f"ping {user_input}")
```

#### ✅ Code sécurisé
```python
# SÉCURISÉ : Utiliser subprocess avec liste
import subprocess
subprocess.run(["ping", "-c", "1", user_input], check=True, capture_output=True)
```

### 4️⃣ Désérialisation non sécurisée

#### ❌ Code vulnérable
```python
# DANGER : pickle peut exécuter du code arbitraire
import pickle
data = pickle.loads(user_input)
```

#### ✅ Code sécurisé
```python
# SÉCURISÉ : Utiliser JSON pour les données non fiables
import json
data = json.loads(user_input)
```

### 5️⃣ Authentification faible

#### ✅ Code sécurisé
```python
# SÉCURISÉ : Hashage de mot de passe avec bcrypt
import bcrypt

# Hashage lors de l'inscription
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Vérification lors de la connexion
if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
    # Authentification réussie
    pass
```

### 6️⃣ Exposition de données sensibles

#### ❌ Code vulnérable
```python
# DANGER : Logging de données sensibles
logger.info(f"User {username} logged in with password {password}")
```

#### ✅ Code sécurisé
```python
# SÉCURISÉ : Ne jamais logger les mots de passe
logger.info(f"User {username} logged in successfully")
```

### 7️⃣ CSRF (Cross-Site Request Forgery)

#### ✅ Code sécurisé (Flask)
```python
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
```

### 8️⃣ Validation d'entrée insuffisante

#### ✅ Code sécurisé (Python)
```python
from typing import Optional
import re

def validate_email(email: str) -> Optional[str]:
    """Valide une adresse email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return email
    return None

def validate_integer(value: str, min_val: int = 0, max_val: int = 100) -> Optional[int]:
    """Valide un entier dans une plage"""
    try:
        num = int(value)
        if min_val <= num <= max_val:
            return num
    except ValueError:
        pass
    return None
```

### 9️⃣ Utilisation de composants vulnérables

```bash
# Vérifier les vulnérabilités des dépendances

# Python
pip install safety
safety check

# Node.js
npm audit
npm audit fix

# Yarn
yarn audit
```

### 🔟 Logging et monitoring insuffisant

#### ✅ Code sécurisé
```python
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Logger les événements de sécurité
logger = logging.getLogger(__name__)

def login(username: str, password: str):
    try:
        # Tentative de connexion
        user = authenticate(username, password)
        logger.info(f"Successful login for user: {username}")
        return user
    except AuthenticationError:
        logger.warning(f"Failed login attempt for user: {username}")
        raise
```

---

## Bonnes pratiques par langage

### 🐍 Python

```python
# ✅ Bonnes pratiques
1. Utiliser type hints
2. Valider toutes les entrées
3. Utiliser des ORM (SQLAlchemy, Django ORM)
4. Éviter eval(), exec(), pickle avec données non fiables
5. Utiliser secrets pour générer des tokens
6. Implémenter rate limiting
7. Utiliser des bibliothèques de sécurité :
   - bcrypt / argon2 pour les mots de passe
   - cryptography pour le chiffrement
   - pydantic pour la validation de données
```

### 📜 JavaScript/TypeScript

```javascript
// ✅ Bonnes pratiques
1. Utiliser TypeScript pour la sécurité des types
2. Sanitiser toutes les entrées utilisateur
3. Configurer les headers de sécurité (helmet.js)
4. Implémenter CSP (Content Security Policy)
5. Utiliser des ORM (Prisma, TypeORM, Sequelize)
6. Éviter eval(), Function(), innerHTML
7. Valider avec des bibliothèques : joi, yup, zod
```

---

## Audit et monitoring

### 📊 Outils d'analyse statique

```bash
# Python
pip install bandit pylint
bandit -r .
pylint **/*.py

# JavaScript/TypeScript
npm install -g eslint
eslint .

# SonarQube pour tous les langages
```

### 🔍 Tests de sécurité

```bash
# Scan des secrets
pip install detect-secrets
detect-secrets scan > .secrets.baseline

# Scan des dépendances vulnérables
npm audit
pip-audit
```

---

## Checklist avant commit

### ✅ Vérifications obligatoires

- [ ] Aucun secret en dur dans le code
- [ ] Toutes les entrées utilisateur sont validées
- [ ] Les requêtes SQL utilisent des paramètres préparés
- [ ] Les mots de passe sont hashés (bcrypt, argon2)
- [ ] Les erreurs ne révèlent pas d'informations sensibles
- [ ] Les logs ne contiennent pas de données sensibles
- [ ] Les dépendances sont à jour et sans vulnérabilités
- [ ] Les headers de sécurité sont configurés
- [ ] HTTPS est activé en production
- [ ] Les tokens CSRF sont implémentés
- [ ] Rate limiting est en place
- [ ] Tests de sécurité passent

---

## 🚨 Signalement de vulnérabilités

Si vous découvrez une vulnérabilité de sécurité :

1. **NE PAS** créer une issue publique
2. Contacter l'équipe de sécurité en privé
3. Fournir une description détaillée
4. Attendre la confirmation avant de divulguer

---

## 📚 Ressources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

**Dernière mise à jour** : 2025-11-17
**Maintenu par** : Équipe de sécurité reconversion-agents-ia
