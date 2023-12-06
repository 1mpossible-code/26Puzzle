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


LAST: int = 2
FIRST: int = 0



class Puzzle:
    def __init__(self, tiles: List[int]) -> None:
        if isinstance(tiles, list):
            self.__tiles: Tuple[int, ...] = tuple(map(lambda x: int(x), tiles))
        elif isinstance(tiles, Puzzle):
            self.__tiles = tiles.get_raw()

    def __hash__(self) -> int:
        return hash(self.get_raw())

    def __eq__(self, __rhs: "Puzzle") -> bool:
        return hash(self) == hash(__rhs)

    def get_raw(self) -> Tuple[int, ...]:
        return self.__tiles

    def move(self, direction: Directions) -> "Puzzle":
        tiles: List[int] = list(self.__tiles)
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

    def __repr__(self) -> str:
        res = ""
        for i in range(3):
            for j in range(3):
                line = ""
                for k in range(3):
                    line += str(self.__tiles[i * 9 + j * 3 + k]) + " "
                res += line.strip() + "\n"
            res += "\n"
        return res.strip()

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
            goal: "PuzzleSearch.Node",
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
            self.d = 0 if not parent else 1 + parent.d

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
        self.N = 1
        self.result = self.search()
        self.d = self.result.d

    def get_actions(self) -> List[str]:
        res = []
        cur = self.result
        while cur:
            if cur.action == Directions.N:
                res.insert(0, "N")
            elif cur.action == Directions.S:
                res.insert(0, "S")
            elif cur.action == Directions.E:
                res.insert(0, "E")
            elif cur.action == Directions.W:
                res.insert(0, "W")
            elif cur.action == Directions.U:
                res.insert(0, "U")
            elif cur.action == Directions.D:
                res.insert(0, "D")
            cur = cur.parent
        return res

    def get_total_costs(self) -> List[int]:
        res = []
        cur = self.result
        while cur:
            res.insert(0, cur.total_cost)
            cur = cur.parent
        return res

    def __repr__(self) -> str:
        res = ""
        res += str(self.initial)
        res += "\n\n"
        res += str(self.goal)
        res += "\n\n"
        res += f"{self.d}\n"
        res += f"{self.N}\n"
        res += f'{" ".join(self.get_actions())}\n'
        res += f'{" ".join(map(str, self.get_total_costs()))}'
        return res

    def save_file(self, filename: str) -> bool:
        with open(filename, "w") as f:
            f.write(str(self))

    def search(self) -> "PuzzleSearch.Node":
        goal = PuzzleSearch.Node(self.goal, self.goal)
        node = PuzzleSearch.Node(self.goal, self.initial)
        frontier = [node]
        reached = {self.initial: node}
        while len(frontier):
            node = heapq.heappop(frontier)
            if node == goal:
                return node
            for child in self.expand(node, reached):
                s = child.state
                self.N += 1
                reached[s] = child
                heapq.heappush(frontier, child)
        raise Exception("Solution is not found")

    def expand(self, node: "PuzzleSearch.Node", reached):
        s = node.state
        for direction in Directions:
            s_prime = s.move(direction)
            if s_prime != s and s_prime not in reached:
                cost = node.path_cost + 1
                yield PuzzleSearch.Node(
                    node.goal, s_prime, parent=node, action=direction, path_cost=cost
                )


def visualization():
    res = PuzzleSearch("Input2.txt").search()
    arr = []
    while res:
        arr.insert(0, res.state)
        res = res.parent

    # Print the path one at 3 seconds
    for i in range(len(arr)):
        print("Step: ", i)
        print(arr[i])
        input()


if __name__ == "__main__":
    visualization()
    # res = PuzzleSearch("Input1.txt")
    # print(res)
    # res2 = PuzzleSearch("Input2.txt")
    # print(res2.d, res2.N)
    # res2.save_file('test2.txt')
    # res3 = PuzzleSearch("Input3.txt")
    # print(res3.d, res3.N)
    # res3.save_file('test3.txt')
    # res.save_file('test.txt')

    # res_mine = PuzzleSearch("InputMine.txt")
    # print(res_mine.d, res_mine.N)
    # res_mine.save_file('test_mine.txt')
