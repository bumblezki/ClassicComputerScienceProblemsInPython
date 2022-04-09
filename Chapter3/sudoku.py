from nntplib import GroupInfo
from re import S
from typing import NamedTuple, List, Dict, Optional, Tuple
from csp import CSP, Constraint
from enum import Enum
from itertools import combinations

ZERO = 0
THREE = 3
SIX = 6
NINE = 9

Grid = List[List[str]]  # type alias for grids

class GridLocation(NamedTuple):
    row: int
    column: int

class SudokuNumber(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


class Sudoku:
    starting_numbers: Dict[GridLocation, SudokuNumber] = {}

    def __init__(self):
        self.grid: Grid = self.generate_grid()
        
    def generate_grid(self) -> Grid:
        return [["." for _ in range(NINE)] for _ in range(NINE)]

    @staticmethod
    def on_same_row(here: GridLocation, there: GridLocation) -> bool:
        return here.row == there.row

    @staticmethod
    def in_same_column(here: GridLocation, there: GridLocation) -> bool:
        return here.column == there.column

    @staticmethod
    def in_same_square(here: GridLocation, there: GridLocation) -> bool:
        return (
            here.column // THREE == there.column // THREE and 
            here.row    // THREE == there.row    // THREE
        )

    def insert_number(self, number: SudokuNumber, location: GridLocation):
        if location.row >= NINE or location.column >= NINE:
            raise ValueError(f"Tried to insert a {number.value} into a GridLocation not on the sudoku grid.")
        self.grid[location.row][location.column] = str(number.value)

    def display(self) -> None:
        for i, row in enumerate(self.grid):
            if i != ZERO and i % THREE == ZERO:
                print("------+-------+------")
            row.insert(SIX, '|')
            row.insert(THREE, '|')
            print(" ".join(row))

    def add_starting_number(self, loc: GridLocation, number: SudokuNumber) -> None:
        self.starting_numbers[loc] = number


def get_connected_grid_locations(all_locs: List[GridLocation], loc: GridLocation) -> List[GridLocation]:
    connected_locs: List[GridLocation] = []
    for other_loc in all_locs:
        if loc != other_loc and (
            Sudoku.in_same_column(loc, other_loc) or
            Sudoku.on_same_row(loc, other_loc) or
            Sudoku.in_same_square(loc, other_loc)
        ):
            connected_locs.append(other_loc)
    return connected_locs


class SudokuConstraint(Constraint[GridLocation, SudokuNumber]):
    def __init__(self, grid_locations: List[GridLocation]) -> None:
        super().__init__(grid_locations)
        self.grid_locations: List[GridLocation] = grid_locations

    def satisfied(self, assignment: Dict[GridLocation, SudokuNumber]) -> bool:        
        all_locs: List[GridLocation] = [GridLocation(row, col) for row in range(NINE) for col in range(NINE)]
        for loc, number in assignment.items():
            connected_locs: List[GridLocation] = get_connected_grid_locations(all_locs, loc)
            if loc in Sudoku.starting_numbers and assignment[loc] != sudoku.starting_numbers[loc]:
                return False
            for loc in connected_locs:
                if loc in assignment and assignment[loc] == number:
                    return False
        return True


if __name__ == "__main__":
    sudoku: Sudoku = Sudoku()
    sudoku.add_starting_number(GridLocation(0,0), SudokuNumber.EIGHT)
    sudoku.add_starting_number(GridLocation(3,6), SudokuNumber.FIVE)
    numbers: Dict[GridLocation, List[SudokuNumber]] = {}
    all_locs: List[GridLocation] = [GridLocation(row, col) for row in range(NINE) for col in range(NINE)]
    for loc in all_locs:
        numbers[loc] = [number for number in SudokuNumber]
    csp: CSP[GridLocation, SudokuNumber] = CSP(all_locs, numbers)
    csp.add_constraint(SudokuConstraint(all_locs))
    solution: Optional[Dict[GridLocation, SudokuNumber]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for loc, number in solution.items():
            sudoku.insert_number(number, loc)
        sudoku.display()
