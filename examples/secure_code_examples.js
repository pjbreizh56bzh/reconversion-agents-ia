/**
 * EXEMPLES DE CODE SÉCURISÉ - JAVASCRIPT/NODE.JS
 * ================================================
 *
 * Ce fichier contient des exemples concrets de code sécurisé
 * pour protéger votre application Node.js contre les vulnérabilités courantes.
 *
 * Auteur: Équipe de sécurité reconversion-agents-ia
 * Date: 2025-11-17
 */

// ============================================
// DÉPENDANCES RECOMMANDÉES POUR LA SÉCURITÉ
// ============================================
/*
npm install --save helmet express-rate-limit bcrypt validator
npm install --save jsonwebtoken crypto dotenv
npm install --save-dev eslint eslint-plugin-security
*/

// ============================================
// 1. CONFIGURATION EXPRESS SÉCURISÉE
// ============================================

const express = require('express');
const helmet = require('helmet');

function createSecureExpressApp() {
  const app = express();

  // ✅ SÉCURISÉ : Headers de sécurité avec Helmet
  app.use(helmet());

  // ✅ SÉCURISÉ : Configuration CSP (Content Security Policy)
  app.use(
    helmet.contentSecurityPolicy({
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", 'data:', 'https:'],
        connectSrc: ["'self'"],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],
        mediaSrc: ["'self'"],
        frameSrc: ["'none'"],
      },
    })
  );

  // ✅ SÉCURISÉ : Désactive le header X-Powered-By
  app.disable('x-powered-by');

  // ✅ SÉCURISÉ : Parse JSON avec limite de taille
  app.use(express.json({ limit: '10mb' }));

  // ✅ SÉCURISÉ : Protection contre les attaques de pollution de paramètres
  app.use(express.urlencoded({ extended: true, limit: '10mb' }));

  return app;
}

// ============================================
// 2. RATE LIMITING
// ============================================

const rateLimit = require('express-rate-limit');

// ✅ SÉCURISÉ : Limite le nombre de requêtes
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 tentatives maximum
  message: 'Trop de tentatives de connexion, réessayez plus tard',
  standardHeaders: true,
  legacyHeaders: false,
});

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requêtes maximum
  message: 'Trop de requêtes, réessayez plus tard',
});

// Utilisation :
// app.post('/api/login', loginLimiter, loginHandler);
// app.use('/api/', apiLimiter);

// ============================================
// 3. GESTION SÉCURISÉE DES MOTS DE PASSE
// ============================================

const bcrypt = require('bcrypt');

class SecurePasswordHandler {
  /**
   * Hash un mot de passe de manière sécurisée
   * ✅ SÉCURISÉ : Utilise bcrypt avec salt automatique
   */
  static async hashPassword(password) {
    const saltRounds = 12; // Plus c'est élevé, plus c'est sécurisé (mais lent)
    return await bcrypt.hash(password, saltRounds);
  }

  /**
   * Vérifie un mot de passe contre son hash
   * ✅ SÉCURISÉ : Utilise une comparaison temporellement constante
   */
  static async verifyPassword(password, hashedPassword) {
    return await bcrypt.compare(password, hashedPassword);
  }

  /**
   * Valide la force d'un mot de passe
   * ✅ SÉCURISÉ : Exige complexité minimale
   */
  static validatePasswordStrength(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    return (
      password.length >= minLength &&
      hasUpperCase &&
      hasLowerCase &&
      hasNumbers &&
      hasSpecialChar
    );
  }
}

// ============================================
// 4. VALIDATION D'ENTRÉES UTILISATEUR
// ============================================

const validator = require('validator');

class InputValidator {
  /**
   * Valide et nettoie une adresse email
   * ✅ SÉCURISÉ : Validation stricte
   */
  static validateEmail(email) {
    if (!email || typeof email !== 'string') {
      return null;
    }

    const sanitized = validator.trim(email.toLowerCase());

    if (validator.isEmail(sanitized)) {
      return sanitized;
    }
    return null;
  }

  /**
   * Valide un nom d'utilisateur
   * ✅ SÉCURISÉ : Caractères alphanumériques uniquement
   */
  static validateUsername(username) {
    if (!username || typeof username !== 'string') {
      return null;
    }

    const sanitized = validator.trim(username);

    if (
      validator.isAlphanumeric(sanitized, 'en-US', { ignore: '_-' }) &&
      validator.isLength(sanitized, { min: 3, max: 20 })
    ) {
      return sanitized;
    }
    return null;
  }

  /**
   * Valide une URL
   * ✅ SÉCURISÉ : Protocoles autorisés uniquement
   */
  static validateURL(url) {
    if (!url || typeof url !== 'string') {
      return null;
    }

    const options = {
      protocols: ['http', 'https'],
      require_protocol: true,
    };

    if (validator.isURL(url, options)) {
      return url;
    }
    return null;
  }

  /**
   * Échappe les caractères HTML dangereux
   * ✅ SÉCURISÉ : Protection contre XSS
   */
  static sanitizeHTML(text) {
    if (!text || typeof text !== 'string') {
      return '';
    }
    return validator.escape(text);
  }

  /**
   * Valide un entier dans une plage
   * ✅ SÉCURISÉ : Conversion sûre avec vérification
   */
  static validateInteger(value, min = 0, max = 100) {
    const num = parseInt(value, 10);

    if (isNaN(num) || num < min || num > max) {
      return null;
    }
    return num;
  }
}

// ============================================
// 5. REQUÊTES SQL SÉCURISÉES
// ============================================

/**
 * Exemple avec PostgreSQL (pg)
 */
class SecureDatabaseHandler {
  /**
   * ✅ SÉCURISÉ : Utilise des paramètres préparés
   * Protection contre l'injection SQL
   */
  static async getUserByUsername(pool, username) {
    const query = 'SELECT id, username, email FROM users WHERE username = $1';
    const result = await pool.query(query, [username]);
    return result.rows[0] || null;
  }

  /**
   * ❌ VULNÉRABLE : NE JAMAIS FAIRE CECI
   * Vulnérable à l'injection SQL
   */
  static async getUserByUsername_VULNERABLE(pool, username) {
    // NE JAMAIS UTILISER CETTE MÉTHODE
    const query = `SELECT * FROM users WHERE username = '${username}'`;
    const result = await pool.query(query);
    return result.rows[0];
  }

  /**
   * ✅ SÉCURISÉ : Requête complexe avec paramètres
   */
  static async searchProducts(pool, searchTerm, category) {
    const query = `
      SELECT id, name, price, description
      FROM products
      WHERE (name ILIKE $1 OR description ILIKE $1)
      AND category = $2
      ORDER BY name
    `;
    const searchPattern = `%${searchTerm}%`;
    const result = await pool.query(query, [searchPattern, category]);
    return result.rows;
  }
}

// ============================================
// 6. GESTION SÉCURISÉE DES JWT
// ============================================

const jwt = require('jsonwebtoken');
const crypto = require('crypto');

class SecureJWTHandler {
  /**
   * Génère un token JWT sécurisé
   * ✅ SÉCURISÉ : Expiration courte + secret fort
   */
  static generateToken(payload, expiresIn = '1h') {
    const secret = process.env.JWT_SECRET;

    if (!secret || secret.length < 32) {
      throw new Error('JWT_SECRET doit faire au moins 32 caractères');
    }

    return jwt.sign(payload, secret, {
      expiresIn,
      algorithm: 'HS256',
    });
  }

  /**
   * Vérifie un token JWT
   * ✅ SÉCURISÉ : Validation stricte
   */
  static verifyToken(token) {
    try {
      const secret = process.env.JWT_SECRET;
      return jwt.verify(token, secret, {
        algorithms: ['HS256'],
      });
    } catch (error) {
      return null;
    }
  }

  /**
   * Génère un refresh token sécurisé
   * ✅ SÉCURISÉ : Utilise crypto pour génération aléatoire
   */
  static generateRefreshToken() {
    return crypto.randomBytes(32).toString('hex');
  }
}

// ============================================
// 7. GESTION SÉCURISÉE DES FICHIERS
// ============================================

const path = require('path');
const fs = require('fs').promises;

class SecureFileHandler {
  static ALLOWED_EXTENSIONS = new Set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']);
  static MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

  /**
   * Valide un nom de fichier
   * ✅ SÉCURISÉ : Protection contre path traversal
   */
  static validateFilename(filename) {
    // Retire les chemins
    const basename = path.basename(filename);

    // Vérifie les caractères dangereux
    if (basename.includes('..') || basename.includes('/') || basename.includes('\\')) {
      return null;
    }

    // Vérifie l'extension
    const ext = path.extname(basename).slice(1).toLowerCase();
    if (!this.ALLOWED_EXTENSIONS.has(ext)) {
      return null;
    }

    return basename;
  }

  /**
   * Génère un nom de fichier sécurisé unique
   * ✅ SÉCURISÉ : UUID + extension validée
   */
  static generateSecureFilename(originalFilename) {
    const ext = path.extname(originalFilename).toLowerCase();
    const uniqueName = crypto.randomBytes(16).toString('hex');
    return `${uniqueName}${ext}`;
  }

  /**
   * Lit un fichier de manière sécurisée
   * ✅ SÉCURISÉ : Validation du chemin
   */
  static async readFileSecurely(filename, baseDir) {
    const safePath = path.join(baseDir, path.basename(filename));

    // Vérifie que le chemin ne sort pas du répertoire de base
    if (!safePath.startsWith(baseDir)) {
      throw new Error('Accès interdit');
    }

    return await fs.readFile(safePath, 'utf8');
  }
}

// ============================================
// 8. PROTECTION CONTRE LES ATTAQUES XSS
// ============================================

class XSSProtection {
  /**
   * Échappe les caractères HTML
   * ✅ SÉCURISÉ : Protection contre XSS
   */
  static escapeHTML(text) {
    const htmlEscapeMap = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#x27;',
      '/': '&#x2F;',
    };

    return text.replace(/[&<>"'/]/g, (char) => htmlEscapeMap[char]);
  }

  /**
   * Nettoie une URL pour prévenir les attaques javascript:
   * ✅ SÉCURISÉ : Bloque les protocoles dangereux
   */
  static sanitizeURL(url) {
    const dangerous = /^(javascript|data|vbscript):/i;
    if (dangerous.test(url)) {
      return '';
    }
    return url;
  }
}

// ============================================
// 9. PROTECTION CSRF
// ============================================

class CSRFProtection {
  /**
   * Génère un token CSRF
   * ✅ SÉCURISÉ : Génération cryptographique
   */
  static generateCSRFToken() {
    return crypto.randomBytes(32).toString('hex');
  }

  /**
   * Middleware de vérification CSRF
   * ✅ SÉCURISÉ : Valide le token CSRF
   */
  static csrfMiddleware(req, res, next) {
    if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(req.method)) {
      const token = req.headers['x-csrf-token'] || req.body._csrf;
      const sessionToken = req.session?.csrfToken;

      if (!token || token !== sessionToken) {
        return res.status(403).json({ error: 'Token CSRF invalide' });
      }
    }
    next();
  }
}

// ============================================
// 10. LOGGING SÉCURISÉ
// ============================================

class SecureLogger {
  static SENSITIVE_FIELDS = ['password', 'token', 'api_key', 'secret', 'credit_card'];

  /**
   * Supprime les données sensibles avant le logging
   * ✅ SÉCURISÉ : Ne logue jamais de secrets
   */
  static sanitizeLogData(data) {
    const sanitized = { ...data };

    for (const key in sanitized) {
      const lowerKey = key.toLowerCase();
      if (this.SENSITIVE_FIELDS.some((field) => lowerKey.includes(field))) {
        sanitized[key] = '***REDACTED***';
      }
    }

    return sanitized;
  }

  /**
   * Logue une tentative d'authentification
   * ✅ SÉCURISÉ : Logue les événements de sécurité importants
   */
  static logAuthenticationAttempt(username, success, ipAddress) {
    const timestamp = new Date().toISOString();
    const status = success ? 'SUCCESS' : 'FAILED';

    console.log(
      JSON.stringify({
        timestamp,
        event: 'authentication',
        status,
        username,
        ip: ipAddress,
      })
    );
  }
}

// ============================================
// 11. CONFIGURATION SÉCURISÉE
// ============================================

require('dotenv').config();

class SecureConfig {
  /**
   * Charge et valide la configuration
   * ✅ SÉCURISÉ : Validation des variables d'environnement
   */
  static loadConfig() {
    const requiredEnvVars = ['DATABASE_URL', 'JWT_SECRET', 'API_KEY'];

    for (const envVar of requiredEnvVars) {
      if (!process.env[envVar]) {
        throw new Error(`Variable d'environnement manquante: ${envVar}`);
      }
    }

    // Vérifie que JWT_SECRET est suffisamment long
    if (process.env.JWT_SECRET.length < 32) {
      throw new Error('JWT_SECRET doit faire au moins 32 caractères');
    }

    return {
      databaseUrl: process.env.DATABASE_URL,
      jwtSecret: process.env.JWT_SECRET,
      apiKey: process.env.API_KEY,
      nodeEnv: process.env.NODE_ENV || 'development',
      port: parseInt(process.env.PORT || '3000', 10),
    };
  }
}

// ============================================
// 12. EXEMPLE D'API ROUTE SÉCURISÉE
// ============================================

function createSecureLoginRoute() {
  return async (req, res) => {
    try {
      // ✅ Validation des entrées
      const email = InputValidator.validateEmail(req.body.email);
      const password = req.body.password;

      if (!email || !password) {
        return res.status(400).json({ error: 'Email ou mot de passe invalide' });
      }

      // ✅ Récupération sécurisée de l'utilisateur
      // const user = await SecureDatabaseHandler.getUserByEmail(pool, email);

      // ✅ Vérification sécurisée du mot de passe
      // const isValid = await SecurePasswordHandler.verifyPassword(password, user.password_hash);

      // ✅ Génération de token JWT
      // const token = SecureJWTHandler.generateToken({ userId: user.id, email: user.email });

      // ✅ Logging sécurisé
      SecureLogger.logAuthenticationAttempt(email, true, req.ip);

      // ✅ Retour sécurisé
      return res.json({
        // token,
        user: {
          // id: user.id,
          // email: user.email,
          // Ne jamais retourner le hash du mot de passe !
        },
      });
    } catch (error) {
      // ✅ Gestion d'erreur sécurisée
      SecureLogger.logAuthenticationAttempt(req.body.email, false, req.ip);

      // Ne pas révéler d'informations sur l'erreur
      return res.status(401).json({ error: 'Authentification échouée' });
    }
  };
}

// ============================================
// EXPORTS
// ============================================

module.exports = {
  createSecureExpressApp,
  loginLimiter,
  apiLimiter,
  SecurePasswordHandler,
  InputValidator,
  SecureDatabaseHandler,
  SecureJWTHandler,
  SecureFileHandler,
  XSSProtection,
  CSRFProtection,
  SecureLogger,
  SecureConfig,
  createSecureLoginRoute,
};

// ============================================
// EXEMPLE D'UTILISATION
// ============================================

if (require.main === module) {
  console.log('=== EXEMPLES DE CODE SÉCURISÉ (NODE.JS) ===\n');

  // 1. Validation d'email
  console.log('1. Validation d\'email:');
  const email = InputValidator.validateEmail('user@example.com');
  console.log(`✅ Email valide: ${email}\n`);

  // 2. Génération de token JWT
  console.log('2. Génération de token:');
  process.env.JWT_SECRET = crypto.randomBytes(32).toString('hex');
  const token = SecureJWTHandler.generateToken({ userId: 123 });
  console.log(`✅ Token JWT: ${token.substring(0, 20)}...\n`);

  // 3. Échappement HTML
  console.log('3. Protection XSS:');
  const userInput = '<script>alert("XSS")</script>';
  const safe = XSSProtection.escapeHTML(userInput);
  console.log(`❌ Entrée dangereuse: ${userInput}`);
  console.log(`✅ Sortie sécurisée: ${safe}\n`);

  // 4. Token CSRF
  console.log('4. Token CSRF:');
  const csrfToken = CSRFProtection.generateCSRFToken();
  console.log(`✅ Token CSRF: ${csrfToken.substring(0, 20)}...\n`);

  console.log('=== FIN DES EXEMPLES ===');
}
