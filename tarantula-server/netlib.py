import socket

def get_my_ip_address():
    _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _socket.connect(("8.8.8.8", 80))
    ip = _socket.getsockname()[0]
    _socket.close()
    return ip