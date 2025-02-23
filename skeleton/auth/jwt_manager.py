"""
Gestione dei token JWT per l'autenticazione.
"""

import jwt
from datetime import datetime, timedelta
from config.default import CONFIG  # Assicurati che il percorso sia corretto
import logging

logger = logging.getLogger(__name__)

def create_token(user):
    payload = {
        'user_id': user['id'],
        'username': user['username'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, CONFIG["module_name"] + "_secret", algorithm='HS256')
    return token

def verify_token(token):
    if not token:
        return None
    try:
        payload = jwt.decode(token, CONFIG["module_name"] + "_secret", algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token scaduto.")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Token non valido.")
        return None
