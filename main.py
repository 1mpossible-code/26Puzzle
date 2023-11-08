from typing import List, Tuple
import heapq
from enum import Enum


class Directions(Enum):
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
        res = ""
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
    class Node:
        def __init__(
            self,
            goal: 'PuzzleSearch.Node',
            state: Puzzle,
            parent: "PuzzleSearch.Node" = None,
            action: Directions = None,
            path_cost: int = 0,
        ) -> None:
            self.state = state
            self.path_cost = path_cost
            self.heuristics = state.calculate_manhattan_distance(goal)
            self.total_cost = self.path_cost + self.heuristics
            self.parent = parent
            self.action = action
            self.goal = goal

        def __lt__(self, __value: "PuzzleSearch.Node") -> bool:
            return self.total_cost < __value.total_cost

        def __eq__(self, __value: "PuzzleSearch.Node") -> bool:
            return self.state == __value.state

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

    def search(self) -> "PuzzleSearch.Node":
        goal = PuzzleSearch.Node(self.goal, self.goal)
        node = PuzzleSearch.Node(self.goal, self.initial)
        frontier = [node]
        reached = {self.initial: node}
        while len(frontier):
            node = heapq.heappop(frontier)
            if node == goal:
                return node
            for child in self.expand(node):
                s = child.state
                if s not in reached:
                    reached[s] = child
                    heapq.heappush(frontier, child)
        raise Exception("Solution is not found")

    def expand(self, node: "PuzzleSearch.Node"):
        s = node.state
        for direction in Directions:
            s_prime = s.move(direction)
            if s_prime != s:
                cost = node.path_cost + 1
                yield PuzzleSearch.Node(
                    node.goal, s_prime, parent=node, action=direction, path_cost=cost
                )


if __name__ == "__main__":
    print(PuzzleSearch("Input1.txt").search().total_cost)
