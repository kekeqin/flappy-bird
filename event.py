
READY = 0
START = 1
JOIN = 2
JUMP = 3
SCORE = 4
DEAD = 5
QUIT = 6
PLAYER_LIST = 7
PIPE_DATA = 8

PID = 9
BIRD_STATE_UPDATE = 10

class Event:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        
    def is_event(self, target):
        return self.id == target
        
    def to_dict(self):
        return {"id": self.id, "data": self.data}
    
    
    
# event = Event(id = QUIT, data = 3)
# print(event.is_event(JOIN))

# print(event.to_dict())