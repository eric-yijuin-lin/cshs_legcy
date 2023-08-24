from uuid import uuid4
from data_model import Player, RoomJoinResult
from bingo_set import PlayerBingoSet

class GameRoom:
    def __init__(self, id: str, grid_dimension: int, max_player: int) -> None:
        self.id = id
        self.max_player = max_player
        self.grid_dimension = grid_dimension
        self.players = []

    def join(self, player_set: PlayerBingoSet) -> RoomJoinResult:
        if len(self.players) == self.max_player:
            return RoomJoinResult.RoomFull
        self.players.append(player_set)
        return RoomJoinResult.OK

class GameManager:
    def __init__(self) -> None:
        self.game_rooms = {}
        self.rooms_locked = False

    def create_room(self, grid_dimension: int, max_player: int) -> str:
        room_id = self.generate_room_id()
        room = GameRoom(room_id, grid_dimension, max_player)
        self.game_rooms[room.id] = room

    def generate_room_id(self) -> str:
        while True:
            uuid = uuid4()
            short_id = str(uuid)[0:5]
            if short_id not in self.game_rooms.keys():
                return short_id

    def register_plyaer(self, name: str, bingo_numbers: str, room_id = None):
        player = Player(name)
        self.join_room(player, bingo_numbers, room_id)

    def join_room(self, player: Player, bingo_numbers: str, room_id = None) -> RoomJoinResult:
        if self.rooms_locked == True:
            return RoomJoinResult.Locking

        join_result = None
        if room_id:
            join_result = self.join_random_room(player, bingo_numbers)
        else:
            join_result = self.join_room_by_id(player, room_id, bingo_numbers)

        self.rooms_locked = False
        return join_result

    def join_random_room(self, player: Player, bingo_numbers: str) -> RoomJoinResult:
        available_rooms = [x for x in self.game_rooms.values()]
        if len(available_rooms) == 0:
            return RoomJoinResult.RoomFull

        selected_room: GameRoom = available_rooms[0]
        bingo_set = PlayerBingoSet(player, selected_room.grid_dimension, bingo_numbers)
        join_result = selected_room.join(bingo_set)
        return join_result


    def join_room_by_id(self, player: Player, room_id: str, bingo_numbers: str) -> RoomJoinResult:
        if room_id not in self.game_rooms:
            return RoomJoinResult.NotFound
        selected_room: GameRoom = self.game_rooms[room_id]
        bingo_set = PlayerBingoSet(player, selected_room.grid_dimension, bingo_numbers)
        join_result = selected_room.join(bingo_set)
        return join_result
