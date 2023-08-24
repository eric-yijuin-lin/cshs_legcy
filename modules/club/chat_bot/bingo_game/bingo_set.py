from data_model import Player, CellCheckResult
from bingo_grid import BingoGrid

class PlayerBingoSet:
    def __init__(self, player: Player, dimension: int, cells: str) -> None:
        self.player = player
        self.grid = BingoGrid(dimension, cells)
    def check_bingo(self, number: int):
        check_result = self.grid.check_cell_by_number(number)
        if check_result == CellCheckResult.OK:
            print("OK")
        elif check_result == CellCheckResult.NotFound:
            print("NotFound")
        elif check_result == CellCheckResult.AlreadyChecked:
            print("AlreadyChecked")

debug_player = Player("debug-name")
game_control = PlayerBingoSet(debug_player, 4, "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16")
for i in range(18):
    game_control.check_bingo(i)
    print(f"checked {i}")
    print(f"connection: {game_control.grid.connections}")
aaa = 0
