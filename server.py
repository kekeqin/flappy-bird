import socket
from player import Player
from channel import send_message, ServerChannel
from event import Event, PLAYER_LIST, QUIT,  READY, PIPE_DATA, START, SCORE, JUMP, PID, DEAD,BIRD_STATE_UPDATE
import random
from asserts import Asserts
from bird import Bird
import time
import threading


class Server:
    def __init__(self):
        self.port = 5000
        self.host = "127.0.0.1"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []
        self.conns = []
        self.channels = []
        
        self.ready_players = 0
        
        self.birds= []
        self.asserts = Asserts()

    def start(self):
        self.get_socket_ready()
        self.handle_connection()

    def get_socket_ready(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print("服务器已准备接收客户端连接")

    def handle_connection(self):
        while True:
            conn, addr = self.sock.accept()
            self.conns.append(conn)
            print(f"接收到来自{addr}的连接 , Players: {len(self.players)}")

            player = Player(len(self.players) + 1)
            self.players.append(player)
            
            bird = Bird(60, 200, player.get_pid())
            self.birds.append(bird)
          
            player_list = self._get_play_list()
            player_list_event = Event(id=PLAYER_LIST, data=player_list)
            pipe_data_event = Event(id=PIPE_DATA, data=self.gen_pipe_data())
            self.broadcast(data=player_list_event.to_dict())
            self.broadcast(data=pipe_data_event.to_dict())

            # 初始化 chnnel 并回显 pid
            channel = ServerChannel(conn, self.client_event_handler)
            channel.send(Event(id=PID, data={"pid": player.get_pid()}).to_dict())
            channel.recv()
            self.channels.append(channel)


    # 处理客户端事件
    # TODO 使用 match
    def client_event_handler(self, channel, event):
        # match event.id:
        #     case "QUIT":
        #         self.handle_quit_event(channel)
        #     case "START":
        #         self.handle_start_event()
        #     case"READY":
        #         self.handle_ready_event()
        #     case "JUMP":
        #         pid = event.data["pid"]
        #         for bird in self.birds:
        #             if bird.id == pid:
        #                 bird.jump()
        #     case "DEAD":
        #         pid = event.data["pid"]
        #         for bird in self.birds:
        #             if bird.id == pid:
        #                 bird.dead = True
        #                 dead_event = Event(id=DEAD, data={"pid": bird.id})
        #                 self.broadcast(data=dead_event.to_dict())
        if event.is_event(QUIT):
            self.handle_quit_event(channel)
        elif event.is_event(START):
            self.handle_start_event()
        elif event.is_event(READY):
            self.handle_ready_event()
        elif event.is_event(JUMP):
            pid = event.data["pid"]
            for bird in self.birds:
                if bird.id == pid:
                    bird.jump()
        elif event.is_event(DEAD):
            pid = event.data["pid"]
            for bird in self.birds:
                if bird.id == pid:
                    bird.dead = True
                    dead_event = Event(id=DEAD, data={"pid": bird.id})
                    self.broadcast(data=dead_event.to_dict())

            
    def handle_start_event(self):
        game_start_event = Event(id=START, data=None)
        self.broadcast(data=game_start_event.to_dict())
        t = threading.Thread(target=self.update_birds_per_60c_each_1s, args=[])
        t.start()


    def update_birds_per_60c_each_1s(self):
        # 使用 time 模块的 time() 函数。该函数返回一个浮点数，表示自纪元以来的秒数，包含小数部分表示毫秒。
        next_timestamp = time.time() * 1000
        while not self.is_birds_dead():
            now =  time.time() * 1000
            if now >= next_timestamp:
                # print(now, next_timestamp)
                self.update_birds()
                next_timestamp = next_timestamp + 16.7


    # 应该在计算后掉用
    def is_birds_dead(self):
        for bird in self.birds:
            if not bird.dead:
                return False
        return True

    # 什么情况下可以调用？
    # 答：在游戏开始之后可以调用
    # 调用多少次？
    # 答：假设按照每秒调用 60 次计算（平滑的 60 次计算，将 60次计算平均到一秒中）
    # 在哪里调用？
    # 答：在游戏开始之后。
    # 在什么时候结束调用？
    # 答：在所有 birds 死亡之后
    def update_birds(self):
        for bird in self.birds:
            if bird.is_jump and bird.velocity >= 0:
                bird.is_jump = False
                # self.asserts.get_audios("flap").play()
                bird.velocity = bird.y_vel
            bird.velocity += bird.gravity
            bird.rect.y += bird.velocity
            bird.update_indx_state()

            # print("bird.rect.top", bird.rect.top, "bird.rect.bottom", bird.rect.bottom)

            # if bird.rect.top < 0 or bird.rect.bottom > 400:
            #     bird.died()
                
        # 广播所有小鸟状态更新
        all_bird_states = []
        for bird in self.birds:
            bird_state = self.get_bird_state(bird)
            all_bird_states.append(bird_state)
        state_update_event = Event(id=BIRD_STATE_UPDATE, data=all_bird_states)
        self.broadcast(data=state_update_event.to_dict())
        
    def get_bird_state(self, bird):
        return {
                "pid": bird.id,
                "x": bird.rect.x,
                "y": bird.rect.y,
                "velocity": bird.velocity,
                "dead": bird.dead,
                "score": bird.score
            }
            
    def gen_pipe_data(self):
        pipes = []
        H = 512
        gap = 130
        for i in range(1000):
            y1 = random.randint(int(H * 0.3), int(H * 0.7))
            pipes.append(
                [
                    y1, # 0
                    y1 - gap # 1          
                ]
            )
        return pipes

    def handle_ready_event(self):
        self.ready_players += 1
        if self.ready_players == len(self.players):
            self.handle_start_event()

    
    def handle_quit_event(self, channel):
        self.remove(channel.conn)

        quit_event = Event(id=QUIT, data=None)
        self.broadcast(quit_event.to_dict())
        
        player_list = self._get_play_list()
        player_list_event = Event(id=PLAYER_LIST, data=player_list)
        self.broadcast(data=player_list_event.to_dict())

    def broadcast(self, data):
        for connection in self.conns:
            send_message(connection, data)

    def remove(self, conn):
        for i, c in enumerate(self.conns):
            if str(id(c)) == str(id(conn)):
                self.conns.pop(i)
                self.players.pop(i)
                self.channels[i].close()
                self.channels.pop(i)
                break
        conn.close()

    def _get_play_list(self):
        player_list = []
        for p in self.players:
            player_list.append(p.to_dict())
        
        return player_list


if __name__ == '__main__':
    server = Server()
    server.start()


