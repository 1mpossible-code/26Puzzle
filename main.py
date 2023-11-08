import heapq
from enum import Enum
from typing import List, Tuple

LAST: int = 2
FIRST: int = 0


# Enum for direction which a tile can move
class Directions(Enum):
    N, S, E, W, U, D = range(6)


# Abstraction for PuzzleState
class PuzzleState:
    def __init__(self, tiles: List[int]) -> None:
        self.tiles: Tuple[int, ...] = tuple(tiles)

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __eq__(self, other: "PuzzleState") -> bool:
        return self.tiles == other.tiles

    def move(self, direction: Directions) -> "PuzzleState":
        tiles: List[int] = list(self.tiles)
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

        return PuzzleState(tiles)

    def __repr__(self) -> str:
        res = ""
        for i in range(3):
            for j in range(3):
                line = ""
                for k in range(3):
                    line += str(self.tiles[i * 9 + j * 3 + k]) + " "
                res += line.strip() + "\n"
            res += "\n"
        return res.strip()

    def get_position(self, value: int) -> int:
        return self.tiles.index(value)

    def get_xyz(self, value: int) -> Tuple[int, int, int]:
        idx = self.get_position(value)
        z = idx // 9
        idx %= 9
        y = idx // 3
        idx %= 3
        x = idx
        return x, y, z


# Abstraction for Manhattan Distance Heuristic
class ManhattanDistance:
    @staticmethod
    def calculate(state: "PuzzleState", goal: "PuzzleState") -> int:
        distance = 0
        for i in range(27):
            t1 = state.get_xyz(i)
            t2 = goal.get_xyz(i)
            for j in range(3):
                distance += abs(t1[j] - t2[j])
        return distance


# A node in the search space
class SearchNode:
    def __init__(self,
                 state: PuzzleState,
                 goal: PuzzleState,
                 parent=None,
                 action: Directions = None,
                 path_cost: int = 0,
                 ) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristics = ManhattanDistance.calculate(state, goal)
        self.total_cost = self.path_cost + self.heuristics

    def __lt__(self, other) -> bool:
        return self.total_cost < other.total_cost

    def __eq__(self, other: "SearchNode") -> bool:
        return self.state == other.state


# A* Search Algorithm Implementation
class AStarSearch:
    def __init__(self, initial: PuzzleState, goal: PuzzleState) -> None:
        self.initial = initial
        self.goal = goal
        self.N = 1

    def search(self) -> SearchNode:
        goal = SearchNode(self.goal, self.goal)
        node = SearchNode(self.initial, self.goal)
        frontier = [node]
        reached = {self.initial: node}
        while len(frontier):
            node = heapq.heappop(frontier)
            if node == goal:
                return node
            for child in self.expand(node, reached):
                s = child.state
                reached[s] = child
                heapq.heappush(frontier, child)
        raise Exception("No solution found")

    def expand(self, node: SearchNode, reached):
        s = node.state
        for direction in Directions:
            s_prime = s.move(direction)
            if s_prime != s and s_prime not in reached:
                cost = node.path_cost + 1
                self.N += 1
                yield SearchNode(s_prime, self.goal, node, direction, cost)


# Solution for Puzzle
class Solution:
    def __init__(self, result: SearchNode, N: int) -> None:
        self.result = result

        self.d = self.get_depth(result)
        self.N = N
        self.actions = self.get_actions()
        self.costs = self.get_costs()
        self.initial = self.get_initial()
        self.goal = self.result.state

    def get_initial(self) -> PuzzleState:
        cur = self.result
        while cur.parent:
            cur = cur.parent
        return cur.state

    def get_actions(self) -> List[str]:
        actions = []
        cur = self.result
        while cur:
            if cur.action == Directions.N:
                actions.insert(0, "N")
            elif cur.action == Directions.S:
                actions.insert(0, "S")
            elif cur.action == Directions.E:
                actions.insert(0, "E")
            elif cur.action == Directions.W:
                actions.insert(0, "W")
            elif cur.action == Directions.U:
                actions.insert(0, "U")
            elif cur.action == Directions.D:
                actions.insert(0, "D")
            cur = cur.parent
        return actions

    def get_costs(self) -> List[int]:
        costs = []
        cur = self.result
        while cur:
            costs.insert(0, cur.total_cost)
            cur = cur.parent
        return costs

    def __repr__(self) -> str:
        res = str(self.initial)
        res += "\n\n"
        res += str(self.goal)
        res += "\n\n"
        res += f"{self.d}\n"
        res += f"{self.N}\n"
        res += f'{" ".join(self.actions)}\n'
        res += f'{" ".join(map(str, self.costs))}'
        return res

    @staticmethod
    def get_depth(result: SearchNode) -> int:
        cur = result
        depth = 0
        while cur.parent:
            cur = cur.parent
            depth += 1
        return depth


# File operations for Puzzle
class PuzzleFileIO:
    @staticmethod
    def read_puzzle_from_file(filename: str) -> Tuple[PuzzleState, PuzzleState]:
        with open(filename, "r") as f:
            blocks = f.read().split()
        blocks = list(map(int, blocks))
        return PuzzleState(blocks[:27]), PuzzleState(blocks[27:])

    @staticmethod
    def write_solution_to_file(filename: str, solution: Solution) -> None:
        with open(filename, "w") as f:
            f.write(str(solution))


def solve(filename: str) -> Solution:
    initial, goal = PuzzleFileIO.read_puzzle_from_file(filename)
    a_star = AStarSearch(initial, goal)
    result = a_star.search()
    return Solution(result, a_star.N)


if __name__ == "__main__":
    res = solve("Input1.txt")
    PuzzleFileIO.write_solution_to_file("Input1_solution.txt", res)
    res2 = solve("Input2.txt")
    PuzzleFileIO.write_solution_to_file("Input2_solution.txt", res2)
    res3 = solve("Input3.txt")
    PuzzleFileIO.write_solution_to_file("Input3_solution.txt", res3)

    resMine = solve("InputMine.txt")
    PuzzleFileIO.write_solution_to_file("InputMine_solution.txt", resMine)
