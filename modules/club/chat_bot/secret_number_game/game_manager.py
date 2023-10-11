import random
from enum import Enum
from attr import dataclass

class GameStatusEnum(Enum):
    Error = -1
    Ok = 0
    Hit = 1
    Missed = 2

@dataclass
class ProcessGameResult:
    status: GameStatusEnum
    message: str

class SecretNumberGameManager:
    def __init__(self) -> None:
        self.min_number = 0
        self.max_number = 0
        self.secret_number =0
        self.players = {}
        self.turn_list = []
        self.turn_index = 0
        self.action_dict = {}
        self.is_room_open = False
        self.init_action_dict()
        self.is_debugging = False

    def init_action_dict(self) -> dict:
        self.action_dict["create"] = self.create_room
        self.action_dict["建立"] = self.create_room
        self.action_dict["join"] = self.join_room
        self.action_dict["加入"] = self.join_room
        self.action_dict["close"] = self.close_room
        self.action_dict["關閉"] = self.close_room
        self.action_dict["guess"] = self.guess
        self.action_dict["猜"] = self.guess
        self.action_dict["debug"] = self.set_debug_mode


    def process_command(self, player_id: str, name: str, arguments: list) -> ProcessGameResult:
        command_obj = {
            "player_id": player_id,
            "name": name,
            "game": arguments[0],
            "action": arguments[1],
            "arguments": arguments[2:]
        }
        command_action = command_obj["action"]
        if command_action not in self.action_dict:
            return ProcessGameResult(GameStatusEnum.Error, f"當前版本不支援 {command_action} 指令")
        acion_delegate = self.action_dict[command_action]
        action_result = acion_delegate(command_obj)
        return action_result

    # def create_room(self, min_number: int, max_number: int):
    def create_room(self, command_obj: dict) -> ProcessGameResult:
        arguments = command_obj["arguments"]
        try:
            min_number = int(arguments[0])
            max_number = int(arguments[1])
        except (ValueError, IndexError):
            return ProcessGameResult(GameStatusEnum.Error, "無法建立房間，無效的最小範圍或最大範圍")
        if max_number - min_number < 2:
            return ProcessGameResult(GameStatusEnum.Error, "最大範圍至少需大於最小範圍 + 2")
        self.min_number = min_number
        self.max_number = max_number
        self.secret_number = random.randint(min_number, max_number)
        self.is_room_open = True
        return ProcessGameResult(GameStatusEnum.Ok, f"房間已建立，最小數字: {min_number}；最大數字: {max_number}")

    def close_room(self, command_obj: dict) -> ProcessGameResult:
        self.is_room_open = False
        self.init_turn_list()
        return ProcessGameResult(GameStatusEnum.Ok, f"房間已關閉，不再開放加入。本次猜數字順序為：{self.turn_list}")
    
    def init_turn_list(self) -> None:
        self.turn_list = list(self.players.values())
        random.shuffle(self.turn_list)

    def join_room(self, command_obj: dict) -> ProcessGameResult:
        player_id = command_obj["player_id"]
        name = command_obj["name"]
        if self.is_debugging:
            rand_num = "debug-" + str(random.randint(1, 100)).rjust(3, '0')
            player_id += rand_num
            name += rand_num
        if not self.is_room_open:
            return ProcessGameResult(GameStatusEnum.Error, f"{name} 你好，房間已關閉，下次請早喔~")
        if player_id in self.players:
            return ProcessGameResult(GameStatusEnum.Ok, f"{name} 你好，你已經在房間裡囉")
        self.players[player_id] = name
        return ProcessGameResult(GameStatusEnum.Ok, f"{name} 加入房間")

    def guess(self, command_obj: dict) -> ProcessGameResult:
        player_id = command_obj["player_id"]
        name = command_obj["name"]
        if self.is_room_open:
            return ProcessGameResult(GameStatusEnum.Error, "房間尚未關閉，必須先關閉才能開始猜")
        if not player_id in self.players and not self.is_debugging:
            return ProcessGameResult(GameStatusEnum.Error, f"{name} 你好，想要加入我們嗎？請先加入房間喔")
        if command_obj["arguments"] is None or len(command_obj["arguments"]) == 0:
            return ProcessGameResult(GameStatusEnum.Error, f"{name} 你好，必須猜一個整數")
        
        num_text: str = command_obj["arguments"][0]
        if not num_text or not num_text.isdigit():
            return ProcessGameResult(GameStatusEnum.Error, f"{name} 你好，必須猜一個整數")
        guess_number = int(num_text)
        if guess_number < self.min_number or guess_number > self.max_number:
            return ProcessGameResult(GameStatusEnum.Error, f"{name} 你好，請猜一個 {self.min_number} 至 {self.max_number} 之間的數字")
        if guess_number == self.secret_number:
            return ProcessGameResult(GameStatusEnum.Hit, f"恭喜!! {name} 猜中了，答案是 {self.secret_number}")
        elif guess_number > self.secret_number:
            self.max_number = guess_number
        else:
            self.min_number = guess_number
        return ProcessGameResult(GameStatusEnum.Missed, f"沒中!! 數字的範圍是 {self.min_number} 至 {self.max_number}")

    def set_debug_mode(self, arguments: dict) -> None:
        self.is_debugging = True
        return ProcessGameResult(GameStatusEnum.Ok, "啟動 debug 模式")
        
