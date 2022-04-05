from typing import NamedTuple, List, Dict, Optional, Tuple
from csp import CSP, Constraint
from enum import Enum
from itertools import combinations

THREE = 3
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
        for row in self.grid:
            print(" ".join(row))


def generate_domain() -> List[List[GridLocation]]:
    return [[GridLocation(row, col) for row in range(NINE) for col in range(NINE)]]


class SudokuConstraint(Constraint[SudokuNumber, List[GridLocation]]):
    def __init__(self, numbers: List[SudokuNumber]) -> None:
        super().__init__(numbers)
        self.numbers: List[SudokuNumber] = numbers

    def satisfied(self, assignment: Dict[SudokuNumber, List[GridLocation]]) -> bool:        
        assigned_locs: set = set()
        for locs in assignment.values():
            for loc in locs:
                if loc in assigned_locs:
                    return False
            for loc1, loc2 in combinations(locs, 2):
                if (
                    Sudoku.in_same_column(loc1, loc2) or
                    Sudoku.in_same_square(loc1, loc2) or 
                    Sudoku.on_same_row(loc1, loc2)
                ): 
                    return False
            for loc in locs:
                assigned_locs.add(loc)
        return True


if __name__ == "__main__":
    sudoku: Sudoku = Sudoku()
    locations: Dict[SudokuNumber, List[GridLocation]] = {}
    numbers = [number for number in SudokuNumber]
    for number in numbers:
        locations[number] = generate_domain()
    csp: CSP[SudokuNumber, List[List[GridLocation]]] = CSP(numbers, locations)
    csp.add_constraint(SudokuConstraint(numbers))
    solution: Optional[Dict[SudokuNumber, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for number, locs in solution.items():
            for loc in locs:
                sudoku.insert_number(number, loc)
        sudoku.display()
