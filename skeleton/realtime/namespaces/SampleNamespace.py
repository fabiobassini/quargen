"""
Namespace generico per la gestione delle connessioni real-time.
"""

from flask_socketio import Namespace, emit, join_room, leave_room
from flask import request
import logging
from realtime.connection_manager import connection_manager
from auth.jwt_manager import verify_token

logger = logging.getLogger(__name__)

class SampleNamespace(Namespace):
    def on_connect(self):
        logger.info("[SampleNamespace] Connessione stabilita.")
        user_id, user_data = connection_manager.connect_user(self)
        if not user_id:
            return False
        room = f"user_{user_id}"
        join_room(room)
        emit("connected", {"message": "Connesso con successo"}, room=room)

    def on_disconnect(self):
        logger.info("[SampleNamespace] Disconnessione.")
        token = connection_manager.get_token_from_request(request)
        user_data = verify_token(token)
        if user_data:
            user_id = user_data.get('user_id')
            room = f"user_{user_id}"
            connection_manager.remove_connection(user_id, request.sid)
            leave_room(room, sid=request.sid)
            emit("disconnected", {"user_id": user_id}, room=room)
