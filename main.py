from typing import List, Tuple


class Directions:
    N = 0
    S = 1
    E = 2
    W = 3
    U = 4
    D = 5


LAST = 2
FIRST = 0


class Puzzle:
    def __init__(self, tiles: List) -> None:
        if isinstance(tiles, list):
            self.__tiles = tuple(map(lambda x: int(x), tiles))
        elif isinstance(tiles, Puzzle):
            self.__tiles = tiles.get_raw()

    def __hash__(self) -> int:
        return hash(self.get_raw())

    def __eq__(self, __rhs: "Puzzle") -> bool:
        return hash(self) == hash(__rhs)

    def get_raw(self) -> tuple:
        return self.__tiles

    def move(self, direction: Directions) -> "Puzzle":
        tiles: list = list(self.__tiles)
        x, y, z = self.get_xyz(0)
        idx = self.get_position(0)

        if direction == Directions.W and x != FIRST:
            tiles[idx], tiles[idx - 1] = tiles[idx - 1], tiles[idx]
        elif direction == Directions.E and x != LAST:
            tiles[idx], tiles[idx + 1] = tiles[idx + 1], tiles[idx]
        elif direction == Directions.N and y != FIRST:
            tiles[idx], tiles[idx - 3] = tiles[idx - 3], tiles[idx]
        elif direction == Directions.S and y != LAST:
            tiles[idx], tiles[idx + 3] = tiles[idx + 3], tiles[idx]
        elif direction == Directions.U and z != FIRST:
            tiles[idx], tiles[idx - 9] = tiles[idx - 9], tiles[idx]
        elif direction == Directions.D and z != LAST:
            tiles[idx], tiles[idx + 9] = tiles[idx + 9], tiles[idx]

        return Puzzle(tiles)

    def __repr__(self) -> None:
        res = ''
        for i in range(3):
            for j in range(3):
                line = ""
                for k in range(3):
                    line += str(self.__tiles[i * 9 + j * 3 + k]) + " "
                res += line.strip() + "\n"
            res += "\n"
        return res

    def calculate_manhattan_distance(self, goal: "Puzzle") -> int:
        res = 0
        for i in range(27):
            t1 = self.get_xyz(i)
            t2 = goal.get_xyz(i)
            for j in range(3):
                res += abs(t1[j] - t2[j])
        return res

    def get_position(self, value: int) -> int:
        return self.__tiles.index(value)

    def get_xyz(self, value: int) -> Tuple[int, int, int]:
        idx = self.get_position(value)
        z = idx // 9
        idx %= 9
        y = idx // 3
        idx %= 3
        x = idx
        return x, y, z


class PuzzleSearch:
    class Node():
        def __init__(self, state: Puzzle, parent: Puzzle = None) -> None:
            self.state = state
            
    def __init__(self, filename) -> None:
        try:
            with open(filename, "r") as f:
                content = f.read()
                blocks = content.split()
        except FileNotFoundError as e:
            print("File not found")
            exit(1)

        self.initial = Puzzle(blocks[:27])
        self.goal = Puzzle(blocks[27:])
        self.frontier = []
        self.reached = {}


if __name__ == "__main__":
    PuzzleSearch("Input1.txt")
