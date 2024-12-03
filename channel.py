import json
import threading
import socket
from event import Event

def receive_message(sock):
    length_bytes = sock.recv(4)
    
    if len(length_bytes) == 0:
        return
    
    if len(length_bytes) < 4:
        raise ValueError(f"Length prefix not receive correctly {len(length_bytes)}")
    
    message_length = int.from_bytes(length_bytes, 'big')
    
    message_data = b''
    while len(message_data) < message_length:
        packet = sock.recv(message_length - len(message_data))
        if not packet:
            raise ValueError("Socket connection broken")
        message_data += packet
        
    # return message_data.decode('utf-8')
    try:
        return message_data.decode('utf-8')
    except UnicodeDecodeError:
        print("Error decoding message:", message_data)
        return None


send_message_lock = threading.Lock()
def send_message(sock, message):
    with send_message_lock:
        json_message = json.dumps(message)
        
        packed_message = json_message.encode('utf-8')
        message_length = len(packed_message)
        
        sock.sendall(message_length.to_bytes(4, 'big'))
        sock.sendall(packed_message)
    
    
class ServerChannel():
    def __init__(self, conn, handle):
        self.conn = conn
        self.handle = handle
        self.is_close = False
        
    def recv(self):
        t = threading.Thread(target = self._recv)
        t.start()
        self.t = t
        
    def _recv(self):
        while not self.is_close:
            json_message = receive_message(self.conn)
            if json_message:
                data = json.loads(json_message)
                event = Event(id = data['id'], data = data['data'])
                self.handle(self, event)

    def send(self, data):
        send_message(self.conn, data)
                
    def close(self):
        self.is_close = True
        
        
class Channel():
    def __init__(self, handle):
        self.handle = handle
        self.is_close = False
        
    def recv(self):
        t = threading.Thread(target = self._recv)
        t.start()
        
    def _recv(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 5000))
        self.socket = s
        while not self.is_close:
            json_message = receive_message(s)
            if json_message:
                data = json.loads(json_message)
                event = Event(id = data['id'], data = data['data'])
                self.handle(event)
                
    def send(self, data):
        send_message(self.socket, data)
        
    def close(self):
        self.is_close = True
    
    
    