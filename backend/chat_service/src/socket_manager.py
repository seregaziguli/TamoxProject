from fastapi_socketio import SocketManager

def create_socket_manager_app(app):
    sio = SocketManager(app, path="/chat/ws/chat")
    return sio
