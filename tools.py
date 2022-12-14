import socket
import uuid

def getip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]

def genuuid():
    return str(uuid.uuid4())
