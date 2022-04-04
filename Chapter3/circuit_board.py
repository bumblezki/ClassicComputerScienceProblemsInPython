from typing import NamedTuple, List, Dict, Optional
from random import choice
from enum import Enum
from csp import CSP, Constraint

Grid = List[List[str]]  # type alias for grids

class GridLocation(NamedTuple):
    row: int
    column: int

class ChipColor(Enum):
    BLUE = "B "
    GREEN = "G "
    PURPLE = "P "
    RED = "R "
    YELLOW = "Y "


class Chip(NamedTuple):
    m: int
    n: int
    color: ChipColor 


def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with periods
    return [[". " for _ in range(columns)] for _ in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))


def generate_domain(chip: Chip, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    for row in range(height):
        for col in range(width):
            if col + chip.m <= width and row + chip.n <= height:
                domain.append(
                    [GridLocation(r, c) for c in range(col, col + chip.m) for r in range(row, row + chip.n)]
                )
            if chip.n != chip.m:
                if col + chip.n <= width and row + chip.m <= height:
                    domain.append(
                        [GridLocation(r, c) for c in range(col, col + chip.n) for r in range(row, row + chip.m)]
                    )          
    return domain


class CircuitBoardConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, chips: List[Chip]) -> None:
        super().__init__(chips)
        self.chips: List[Chip] = chips

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        # if there are any duplicates grid locations then there is an overlap
        all_locations = [locs for values in assignment.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)


if __name__ == "__main__":
    grid: Grid = generate_grid(10,10)
    chips: List[Chip] = [
        Chip(1, 6, ChipColor.BLUE),
        Chip(3, 4, ChipColor.GREEN),
        Chip(5, 5, ChipColor.PURPLE),
        Chip(2, 8, ChipColor.RED),
        Chip(3, 3, ChipColor.YELLOW)
    ]
    locations: Dict[str, List[List[GridLocation]]] = {}
    for chip in chips:
        locations[chip] = generate_domain(chip, grid)
    csp: CSP[str, List[GridLocation]] = CSP(chips, locations)
    csp.add_constraint(CircuitBoardConstraint(chips))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for chip, grid_locations in solution.items():
            for loc in grid_locations:
                try:
                    grid[loc.row][loc.column] = chip.color.value
                except IndexError:
                    print(f"\nFailed with {chip.color.value} at {loc.column}, {loc.row} \n")
        display_grid(grid)
