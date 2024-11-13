
class Player:
    def __init__(self, pid): 
        self.pid = f'p{pid}'

    def get_pid(self):
        return self.pid

    def to_dict(self):
        return {"pid": self.pid} 
    
    
# player = Player(1)

# print(player)

# print(player.to_dict())