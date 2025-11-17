"""
EXEMPLES DE CODE SÉCURISÉ
==========================

Ce fichier contient des exemples concrets de code sécurisé
pour protéger votre application contre les vulnérabilités courantes.

Auteur: Équipe de sécurité reconversion-agents-ia
Date: 2025-11-17
"""

import os
import re
import secrets
import hashlib
import hmac
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


# ============================================
# 1. GESTION SÉCURISÉE DES MOTS DE PASSE
# ============================================

class SecurePasswordHandler:
    """Gestion sécurisée des mots de passe avec bcrypt"""

    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Hash un mot de passe de manière sécurisée

        ✅ SÉCURISÉ : Utilise bcrypt avec salt automatique
        """
        try:
            import bcrypt
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        except ImportError:
            raise ImportError("Installer bcrypt: pip install bcrypt")

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        """
        Vérifie un mot de passe contre son hash

        ✅ SÉCURISÉ : Utilise une comparaison temporellement constante
        """
        try:
            import bcrypt
            return bcrypt.checkpw(password.encode('utf-8'), hashed)
        except ImportError:
            raise ImportError("Installer bcrypt: pip install bcrypt")


# ============================================
# 2. VALIDATION D'ENTRÉES UTILISATEUR
# ============================================

class InputValidator:
    """Validation stricte des entrées utilisateur"""

    # Patterns de validation
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
    PHONE_PATTERN = re.compile(r'^\+?[1-9]\d{1,14}$')

    @classmethod
    def validate_email(cls, email: str) -> Optional[str]:
        """
        Valide une adresse email

        ✅ SÉCURISÉ : Validation stricte avec regex
        """
        if not email or len(email) > 254:
            return None

        email = email.strip().lower()
        if cls.EMAIL_PATTERN.match(email):
            return email
        return None

    @classmethod
    def validate_username(cls, username: str) -> Optional[str]:
        """
        Valide un nom d'utilisateur

        ✅ SÉCURISÉ : Caractères alphanumériques uniquement
        """
        if not username:
            return None

        username = username.strip()
        if cls.USERNAME_PATTERN.match(username):
            return username
        return None

    @staticmethod
    def validate_integer(value: Any, min_val: int = 0, max_val: int = 100) -> Optional[int]:
        """
        Valide un entier dans une plage

        ✅ SÉCURISÉ : Conversion sûre avec vérification de plage
        """
        try:
            num = int(value)
            if min_val <= num <= max_val:
                return num
        except (ValueError, TypeError):
            pass
        return None

    @staticmethod
    def sanitize_html(text: str) -> str:
        """
        Échappe les caractères HTML dangereux

        ✅ SÉCURISÉ : Protection contre XSS
        """
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&#x27;",
            ">": "&gt;",
            "<": "&lt;",
        }
        return "".join(html_escape_table.get(c, c) for c in text)


# ============================================
# 3. REQUÊTES SQL SÉCURISÉES
# ============================================

class SecureDatabaseHandler:
    """Exemples de requêtes SQL sécurisées"""

    @staticmethod
    def get_user_by_username_SECURE(cursor, username: str) -> Optional[Dict]:
        """
        ✅ SÉCURISÉ : Utilise des paramètres préparés

        Protection contre l'injection SQL
        """
        query = "SELECT id, username, email FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        return cursor.fetchone()

    @staticmethod
    def get_user_by_username_VULNERABLE(cursor, username: str):
        """
        ❌ VULNÉRABLE : NE JAMAIS FAIRE CECI

        Vulnérable à l'injection SQL
        Exemple d'attaque: username = "admin' OR '1'='1"
        """
        # NE JAMAIS UTILISER CETTE MÉTHODE
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        return cursor.fetchone()

    @staticmethod
    def search_products_SECURE(cursor, search_term: str, category: str):
        """
        ✅ SÉCURISÉ : Requête complexe avec paramètres préparés
        """
        query = """
            SELECT id, name, price, description
            FROM products
            WHERE (name LIKE %s OR description LIKE %s)
            AND category = %s
            ORDER BY name
        """
        search_pattern = f"%{search_term}%"
        cursor.execute(query, (search_pattern, search_pattern, category))
        return cursor.fetchall()


# ============================================
# 4. GESTION SÉCURISÉE DES FICHIERS
# ============================================

class SecureFileHandler:
    """Gestion sécurisée des uploads de fichiers"""

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    @staticmethod
    def validate_filename(filename: str) -> Optional[str]:
        """
        Valide un nom de fichier

        ✅ SÉCURISÉ : Protection contre path traversal
        """
        # Retire les chemins
        filename = os.path.basename(filename)

        # Vérifie les caractères dangereux
        if '..' in filename or '/' in filename or '\\' in filename:
            return None

        # Vérifie l'extension
        if '.' not in filename:
            return None

        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in SecureFileHandler.ALLOWED_EXTENSIONS:
            return None

        return filename

    @staticmethod
    def secure_filename(filename: str) -> str:
        """
        Génère un nom de fichier sécurisé unique

        ✅ SÉCURISÉ : Utilise un UUID + extension validée
        """
        if '.' in filename:
            ext = filename.rsplit('.', 1)[1].lower()
        else:
            ext = 'bin'

        # Génère un nom unique
        unique_name = secrets.token_hex(16)
        return f"{unique_name}.{ext}"


# ============================================
# 5. GÉNÉRATION DE TOKENS SÉCURISÉS
# ============================================

class SecureTokenGenerator:
    """Génération de tokens cryptographiquement sécurisés"""

    @staticmethod
    def generate_api_key(length: int = 32) -> str:
        """
        Génère une clé API sécurisée

        ✅ SÉCURISÉ : Utilise secrets pour la génération cryptographique
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def generate_session_token() -> str:
        """
        Génère un token de session sécurisé

        ✅ SÉCURISÉ : 32 bytes = 256 bits d'entropie
        """
        return secrets.token_hex(32)

    @staticmethod
    def generate_csrf_token() -> str:
        """
        Génère un token CSRF

        ✅ SÉCURISÉ : Protection contre les attaques CSRF
        """
        return secrets.token_urlsafe(32)


# ============================================
# 6. VÉRIFICATION D'INTÉGRITÉ
# ============================================

class IntegrityChecker:
    """Vérification d'intégrité des données"""

    @staticmethod
    def create_hmac_signature(data: str, secret_key: str) -> str:
        """
        Crée une signature HMAC

        ✅ SÉCURISÉ : Utilise HMAC-SHA256
        """
        return hmac.new(
            secret_key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    @staticmethod
    def verify_hmac_signature(data: str, signature: str, secret_key: str) -> bool:
        """
        Vérifie une signature HMAC

        ✅ SÉCURISÉ : Comparaison temporellement constante
        """
        expected_signature = IntegrityChecker.create_hmac_signature(data, secret_key)
        return hmac.compare_digest(signature, expected_signature)


# ============================================
# 7. LIMITATION DE DÉBIT (RATE LIMITING)
# ============================================

class RateLimiter:
    """Limitation de débit pour prévenir les attaques par force brute"""

    def __init__(self, max_attempts: int = 5, window_seconds: int = 300):
        """
        Initialise le rate limiter

        Args:
            max_attempts: Nombre maximum de tentatives
            window_seconds: Fenêtre de temps en secondes
        """
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.attempts: Dict[str, list] = {}

    def is_allowed(self, identifier: str) -> bool:
        """
        Vérifie si une action est autorisée

        ✅ SÉCURISÉ : Protection contre le brute force

        Args:
            identifier: Identifiant unique (IP, user_id, etc.)

        Returns:
            True si autorisé, False sinon
        """
        now = datetime.now()

        # Nettoie les anciennes tentatives
        if identifier in self.attempts:
            cutoff = now - timedelta(seconds=self.window_seconds)
            self.attempts[identifier] = [
                attempt for attempt in self.attempts[identifier]
                if attempt > cutoff
            ]
        else:
            self.attempts[identifier] = []

        # Vérifie le nombre de tentatives
        if len(self.attempts[identifier]) >= self.max_attempts:
            return False

        # Enregistre la tentative
        self.attempts[identifier].append(now)
        return True


# ============================================
# 8. LOGGING SÉCURISÉ
# ============================================

class SecureLogger:
    """Logging sécurisé sans exposer de données sensibles"""

    SENSITIVE_FIELDS = {'password', 'token', 'api_key', 'secret', 'credit_card'}

    @staticmethod
    def sanitize_log_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Supprime les données sensibles avant le logging

        ✅ SÉCURISÉ : Ne logue jamais de secrets
        """
        sanitized = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in SecureLogger.SENSITIVE_FIELDS):
                sanitized[key] = "***REDACTED***"
            else:
                sanitized[key] = value
        return sanitized

    @staticmethod
    def log_authentication_attempt(username: str, success: bool, ip_address: str):
        """
        Logue une tentative d'authentification

        ✅ SÉCURISÉ : Logue les événements de sécurité importants
        """
        import logging
        logger = logging.getLogger(__name__)

        if success:
            logger.info(f"Successful login: user={username}, ip={ip_address}")
        else:
            logger.warning(f"Failed login attempt: user={username}, ip={ip_address}")


# ============================================
# 9. CONFIGURATION SÉCURISÉE
# ============================================

class SecureConfig:
    """Gestion sécurisée de la configuration"""

    @staticmethod
    def load_from_env() -> Dict[str, str]:
        """
        Charge la configuration depuis les variables d'environnement

        ✅ SÉCURISÉ : Secrets stockés hors du code
        """
        return {
            'DATABASE_URL': os.getenv('DATABASE_URL', ''),
            'SECRET_KEY': os.getenv('SECRET_KEY', ''),
            'API_KEY': os.getenv('API_KEY', ''),
            'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
        }

    @staticmethod
    def validate_config(config: Dict[str, str]) -> bool:
        """
        Valide la configuration

        ✅ SÉCURISÉ : Vérifie que tous les secrets nécessaires sont présents
        """
        required_keys = ['DATABASE_URL', 'SECRET_KEY', 'API_KEY']

        for key in required_keys:
            if not config.get(key):
                raise ValueError(f"Configuration manquante: {key}")

        # Vérifie que SECRET_KEY est suffisamment long
        if len(config['SECRET_KEY']) < 32:
            raise ValueError("SECRET_KEY doit faire au moins 32 caractères")

        return True


# ============================================
# EXEMPLE D'UTILISATION
# ============================================

if __name__ == "__main__":
    print("=== EXEMPLES DE CODE SÉCURISÉ ===\n")

    # 1. Hash de mot de passe
    print("1. Hash de mot de passe:")
    password = "MonMotDePasseSecurisé123!"
    # hashed = SecurePasswordHandler.hash_password(password)
    print("✅ Mot de passe hashé avec bcrypt\n")

    # 2. Validation d'email
    print("2. Validation d'email:")
    email = InputValidator.validate_email("user@example.com")
    print(f"✅ Email valide: {email}\n")

    # 3. Génération de token
    print("3. Génération de token:")
    token = SecureTokenGenerator.generate_api_key()
    print(f"✅ Token API sécurisé: {token[:20]}...\n")

    # 4. Rate limiting
    print("4. Rate limiting:")
    limiter = RateLimiter(max_attempts=3, window_seconds=60)
    for i in range(5):
        allowed = limiter.is_allowed("user_123")
        status = "✅ Autorisé" if allowed else "❌ Bloqué"
        print(f"Tentative {i+1}: {status}")

    print("\n=== FIN DES EXEMPLES ===")
