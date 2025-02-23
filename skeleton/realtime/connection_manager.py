"""
Gestione centralizzata delle connessioni real-time.
"""

import logging
from flask import request
from flask_socketio import disconnect, join_room

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}   # user_id -> set di sids (UI)
        self.bridge_connections = {}     # user_id -> set di sids (bridge)

    def get_token_from_request(self, req):
        token = req.cookies.get('auth_token')
        if not token:
            auth_header = req.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[len('Bearer '):]
        return token

    def add_connection(self, user_id, sid, role='ui'):
        if role == 'bridge':
            self.bridge_connections.setdefault(user_id, set()).add(sid)
            logger.info(f"[ConnectionManager] Aggiunto bridge per user_id={user_id}, sid={sid}")
        else:
            self.active_connections.setdefault(user_id, set()).add(sid)
            logger.info(f"[ConnectionManager] Aggiunta connessione UI per user_id={user_id}, sid={sid}")

    def remove_connection(self, user_id, sid, role='ui'):
        if role == 'bridge':
            if user_id in self.bridge_connections:
                self.bridge_connections[user_id].discard(sid)
                if not self.bridge_connections[user_id]:
                    del self.bridge_connections[user_id]
                logger.info(f"[ConnectionManager] Rimosso bridge per user_id={user_id}, sid={sid}")
        else:
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(sid)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
                logger.info(f"[ConnectionManager] Rimosso client UI per user_id={user_id}, sid={sid}")

    def connect_user(self, namespace_obj, role='ui'):
        sid = request.sid
        token = self.get_token_from_request(request)
        from auth.jwt_manager import verify_token
        user_data = verify_token(token)
        if not user_data:
            logger.warning("[ConnectionManager] Token non valido, disconnessione.")
            disconnect()
            return None, None
        user_id = user_data.get('user_id')
        if user_id:
            room_name = f"user_{user_id}"
            join_room(room_name, sid=sid)
            self.add_connection(user_id, sid, role=role)
            logger.info(f"[ConnectionManager] User {user_id} unito alla stanza {room_name} (sid={sid}), role={role}")
        return user_id, user_data

    def bridge_connected_for(self, user_id):
        return user_id in self.bridge_connections and bool(self.bridge_connections[user_id])

# Istanza globale
connection_manager = ConnectionManager()
