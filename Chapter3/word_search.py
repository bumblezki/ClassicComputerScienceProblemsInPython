# word_search.py
# From Classic Computer Science Problems in Python Chapter 3
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import NamedTuple, List, Dict, Optional, Tuple
from random import choice
from string import ascii_uppercase
from csp import CSP, Constraint

Grid = List[List[str]]  # type alias for grids


class GridLocation(NamedTuple):
    row: int
    column: int


def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with random letters
    return [[choice(ascii_uppercase) for c in range(columns)] for r in range(rows)]

def reverse_string(string: str) -> str:
    return string[::-1]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print(" ".join(row))


def generate_domain(word: str, grid: Grid) -> List[List[Tuple[str, GridLocation]]]:
    domain: List[List[Tuple[str, GridLocation]]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)
    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + length)
            rows: range = range(row, row + length)
            if col + length <= width:
                # left to right
                domain.append([(l, GridLocation(row, c)) for l, c in zip(word, columns)])
                domain.append([(l, GridLocation(row, c)) for l, c in zip(reverse_string(word), columns)])
                # diagonal towards bottom right
                if row + length <= height:
                    domain.append([(l, GridLocation(r, col + (r - row))) for l, r in zip(word, rows)])
                    domain.append([(l, GridLocation(r, col + (r - row))) for l, r in zip(reverse_string(word), rows)])
            if row + length <= height:
                # top to bottom
                domain.append([(l, GridLocation(r, col)) for l, r in zip(word, rows)])
                domain.append([(l, GridLocation(r, col)) for l, r in zip(reverse_string(word), rows)])
                # diagonal towards bottom left
                if col - length >= 0:
                    domain.append([(l, GridLocation(r, col - (r - row))) for l, r in zip(word, rows)])
                    domain.append([(l, GridLocation(r, col - (r - row))) for l, r in zip(reverse_string(word), rows)])

    return domain


class WordSearchConstraint(Constraint[str, List[Tuple[str, GridLocation]]]):
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words: List[str] = words

    def satisfied(self, assignment: Dict[str, List[Tuple[str, GridLocation]]]) -> bool:
        all_locations: set = set()
        all_lettered_locations: set = set()
        for locs in assignment.values():
            for letter, loc in locs:
                if loc in all_locations:
                    if (letter, loc) not in all_lettered_locations:
                        return False
                all_locations.add(loc)
                all_lettered_locations.add((letter, loc))
        return True

if __name__ == "__main__":
    grid: Grid = generate_grid(4, 9)
    words: List[str] = ["MATTHEW", "JOE", "MARY", "SARAH", "SALLY"]
    locations: Dict[str, List[List[Tuple[str, GridLocation]]]] = {}
    for word in words:
        locations[word] = generate_domain(word, grid)
    csp: CSP[str, List[Tuple[str, GridLocation]]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution: Optional[Dict[str, List[Tuple[str, GridLocation]]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for grid_locations in solution.values():
            for letter, location in grid_locations:
                (row, col) = (location.row, location.column)
                grid[row][col] = letter
        display_grid(grid)
