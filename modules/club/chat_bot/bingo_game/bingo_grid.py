
from data_model import CellCheckResult, BingoCell

class BingoGrid:
    def __init__(self, dimension: int, cells: str) -> None:
        self.dimension = dimension
        self.connections = 0
        self.grid = []
        self.init_grid_from_str(cells)

    def init_grid_from_str(self, cells: str) -> None:
        cell_values = [x.strip() for x in cells.split(',')]
        self.validate_number_count(cell_values)
        self.validate_duplication(cell_values)
        for i in range(self.dimension):
            row = []
            for j in range(self.dimension):
                cell_index = i * self.dimension + j
                number = int(cell_values[cell_index])
                row.append(BingoCell(number, False))
            self.grid.append(row)

    def validate_number_count(self, cell_values: list) -> None:
        number_count = len(cell_values)
        if number_count != self.dimension * self.dimension:
            raise ValueError(f"賓果的數字必須是 {self.dimension} * {self.dimension}")

    def validate_duplication(self, cell_values: list) -> None:
        temp_dict = {}
        for v in cell_values:
            temp_dict[v] = 0
        if len(cell_values) != len(temp_dict.keys()):
            raise ValueError("賓果的數字有重複")

    def check_cell_by_number(self, number: int) -> CellCheckResult:
        for i in range(self.dimension):
            for j in range(self.dimension):
                cell = self.grid[i][j]
                if cell.number == number:
                    if cell.checked == False:
                        cell.checked = True
                        self.update_connections()
                        return CellCheckResult.OK
                    else:
                        return CellCheckResult.AlreadyChecked
        return CellCheckResult.NotFound

    def update_connections(self) -> None:
        rows = self.get_connected_rows()
        columns = self.get_connected_columns()
        diagonals = self.get_connected_diagonals()
        self.connections = rows + columns + diagonals

    def get_connected_rows(self) -> int:
        connected_rows = 0
        for row in range(self.dimension):
            checked_count = 0
            for col in range(self.dimension):
                if self.grid[row][col].checked == True:
                    checked_count += 1
            if checked_count == self.dimension:
                connected_rows += 1
        return connected_rows

    def get_connected_columns(self) -> int:
        connected_columns = 0
        for col in range(self.dimension):
            checked_count = 0
            for row in range(self.dimension):
                if self.grid[row][col].checked == True:
                    checked_count += 1
            if checked_count == self.dimension:
                connected_columns += 1
        return connected_columns

    def get_connected_diagonals(self):
        connected_diagonals = 0
        if self.is_forward_diagonal_connnected():
            connected_diagonals += 1
        if self.is_backward_diagonal_connnected():
            connected_diagonals += 1
        return connected_diagonals
   
    def is_forward_diagonal_connnected(self):
        checked_cells = 0
        for i in range(self.dimension):
            if self.grid[i][i].checked == True:
                checked_cells += 1
        if checked_cells == self.dimension:
            return True

    def is_backward_diagonal_connnected(self):
        checked_cells = 0
        for row in range(self.dimension):
            col = self.dimension - row - 1
            if self.grid[row][col].checked == True:
                checked_cells += 1
        if checked_cells == self.dimension:
            return True
