import socketio

def create_socket_manager_app():
    sio = socketio.AsyncServer(cors_allowed_origins="*", path="/socket.io")
    return sio
