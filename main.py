# Built-in heapq module to implement priority queue (Min Heap) for the frontier.
import heapq
# Enum is for creating enumerations of possible directions in which a tile can move in a 3D puzzle grid.
from enum import Enum
# Typing is for type hints and type safety. As well, it improves readability.
from typing import List, Tuple

# Constants for indicating positions within the puzzle grid
LAST: int = 2  # Used to indicate the last index in a dimension
FIRST: int = 0  # Used to indicate the first index in a dimension


class Directions(Enum):
    """
    Enumeration for possible directions in which a tile can move in a 3D puzzle grid.
    Includes North (N), South (S), East (E), West (W), Up (U), and Down (D).
    """
    N, S, E, W, U, D = range(6)


class PuzzleState:
    """
    Represents a state of a sliding puzzle. Each state is defined by the positions of the tiles.
    """

    def __init__(self, tiles: List[int]) -> None:
        """
        Initializes a new PuzzleState with a given list of tiles.
        :param tiles: A list of integers representing the tiles in the puzzle.
        """
        self.tiles: Tuple[int, ...] = tuple(tiles)

    def __hash__(self) -> int:
        """
        Hashing is used to make the class hashable and to allow it to be used as a key in a dictionary.
        :return: The hash of the PuzzleState.
        """
        return hash(self.tiles)

    def __eq__(self, other: "PuzzleState") -> bool:
        """
        Equality is used to compare two PuzzleStates.
        :param other: The other PuzzleState to compare to.
        :return: True if the two PuzzleStates are equal, False otherwise.
        """
        return self.tiles == other.tiles

    def move(self, direction: Directions) -> "PuzzleState":
        """
        Moves the blank tile in the given direction. It does not modify the current PuzzleState, but instead returns
        a new PuzzleState with the blank tile moved in the given direction.
        :param direction: The direction in which to move the blank tile. It must be one of the Directions enum values.
        :return: A new PuzzleState with the blank tile moved in the given direction.
        """
        tiles: List[int] = list(self.tiles)
        x, y, z = self.get_xyz(0)
        idx = self.get_position(0)

        # We can move the blank tile in the given direction if the blank tile is not at the edge of the puzzle grid.
        # The tiles are stored in a 1D list, so we need to calculate the index of the tile in the list.
        # We can then swap the blank tile with the tile in the calculated index.
        # If we need to move x direction, we need to swap the blank tile with the tile to the left or right of it, so
        # we need to subtract or add 1 to the index respectively.
        # If we need to move y direction, we need to swap the blank tile with the tile above or below it, so we need to
        # subtract or add 3 to the index respectively.
        # If we need to move z direction, we need to swap the blank tile with the tile in front of or behind it, so we
        # need to subtract or add 9 to the index respectively.
        #
        # Each time we need to check if the blank tile is at the edge of the puzzle grid, so we need to check if the
        # x, y, or z coordinate of the blank tile is equal to the first or last index in the dimension. If it is, then
        # we cannot move the blank tile in that direction and as result we silently fail and return the current state
        # duplicate.
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
        """
        :return: A string representation of the PuzzleState.
        """
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
        """
        Gets the position of a tile with specific value in the puzzle grid.
        :param value: The value of the tile to get the position of. Blank tile is represented by 0.
        :return: The position of the tile with the given value.
        """
        return self.tiles.index(value)

    def get_xyz(self, value: int) -> Tuple[int, int, int]:
        """
        Gets the x, y, z coordinates of a tile with specific value in the puzzle grid.
        :param value: The value of the tile to get the coordinates of. Blank tile is represented by 0.
        :return: The x, y, z coordinates of the tile with the given value. It can be an int from 0 to 2 depending on
        the position of the tile in the puzzle grid.
        """
        idx = self.get_position(value)
        return idx % 3, idx // 3 % 3, idx // 9


class ManhattanDistance:
    """
    Provides a method to calculate the Manhattan distance heuristic for a 3D puzzle.
    This heuristic estimates the cost to reach the goal from the current state.
    """

    @staticmethod
    def calculate(state: "PuzzleState", goal: "PuzzleState") -> int:
        """
        Calculates the Manhattan Distance between two PuzzleStates.
        :param state: The current PuzzleState.
        :param goal: The goal PuzzleState.
        :return: The Manhattan Distance between the two PuzzleStates.
        """
        distance = 0
        for i in range(27):
            t1 = state.get_xyz(i)
            t2 = goal.get_xyz(i)
            for j in range(3):
                distance += abs(t1[j] - t2[j])
        return distance


# A node in the search space
class SearchNode:
    """
    Represents a node in the search space of the A* algorithm.
    Each node contains the current state, a reference to the parent node,
    the action that was taken to reach this state, the path cost, and the total cost.
    """

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
        """
        Comparison is used mainly for Min Heap provided by python's heapq module.
        :param other: The other SearchNode to compare to.
        :return: True if the total cost of this SearchNode is less than the total cost of the other SearchNode, False
        """
        return self.total_cost < other.total_cost

    def __eq__(self, other: "SearchNode") -> bool:
        """
        Equality is used to compare two SearchNodes.
        :param other: The other SearchNode to compare to.
        :return: True if the two SearchNodes are equal, False otherwise.
        """
        return self.state == other.state


class AStarSearch:
    """
    Implements the A* search algorithm for finding the shortest path to the goal state in a 3D puzzle.
    """

    def __init__(self, initial: PuzzleState, goal: PuzzleState) -> None:
        # Initial and goal states
        self.initial = initial
        self.goal = goal
        # Number of nodes expanded
        self.N = 1

    def search(self) -> SearchNode:
        """
        Modified Best First Search algorithm to find the shortest path to the goal state in a 3D puzzle. Using a
        priority queue (Min Heap) to store the nodes in the frontier, the algorithm expands the node with the lowest
        total cost. The total cost is the sum of the path cost and the heuristic cost. The heuristic cost is the
        Manhattan distance between the current state and the goal state. The path cost is the number of actions taken
        to reach the current state from the initial state. The algorithm terminates when the goal state is reached or
        when the frontier is empty. If the frontier is empty, then there is no solution to the puzzle, which results in
        an exception being thrown.
        :return: The goal node with history (parent nodes) of the path pointing back to the first (initial) node.
        """
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
        """
        Expands the given node by generating all possible states that can be reached from the current state.
        Here we yield the nodes and only then the node is considered generated.
        I moved the check if the state is in reached, so we do not need to check it in the search function and yield
        the node that is already in reached. Otherwise, we would have to have an additional check (if else condition)
        in the search function.
        :param node:  The node to expand.
        :param reached:  The hashmap of reached states.
        :return:  A generator of all possible states that can be reached from the current state.
        """
        s = node.state
        for direction in Directions:
            s_prime = s.move(direction)
            if s_prime != s and s_prime not in reached:
                cost = node.path_cost + 1
                self.N += 1
                yield SearchNode(s_prime, self.goal, node, direction, cost)


class Solution:
    """
    Represents a solution to the puzzle, containing the result node, the depth of the solution,
    the number of nodes expanded, the sequence of actions taken, and the costs associated with each action.
    """

    def __init__(self, result: SearchNode, nodes_generated: int) -> None:
        """
        Initializes a new Solution with the given result node and the number of nodes expanded.
        :param result: The result node.
        :param nodes_generated: As result node does not contain the number of nodes expanded, we need to pass it as a
        parameter. This was my decision, since in my understanding responsibility for keeping track is in the search
        algorithm, not in the node by itself.
        """
        self.result = result

        # Depth of the solution (shallowest node since A* search is used)
        self.d = self.get_depth(result)
        self.N = nodes_generated
        # Sequence of actions taken
        self.actions = self.get_actions()
        # Costs associated with each action
        self.costs = self.get_costs()
        # Initial and goal states
        self.initial = self.get_initial()
        self.goal = self.result.state

    def get_initial(self) -> PuzzleState:
        """
        Gets the initial state of the puzzle.
        :return:  The initial state of the puzzle.
        """
        cur = self.result
        while cur.parent:
            cur = cur.parent
        return cur.state

    def get_actions(self) -> List[str]:
        """
        Gets the sequence of actions taken to reach the goal state.
        :return:  The sequence of actions taken to reach the goal state.
        """
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
        """
        Gets the costs associated with each action.
        :return:  The costs associated with each action.
        """
        costs = []
        cur = self.result
        while cur:
            costs.insert(0, cur.total_cost)
            cur = cur.parent
        return costs

    def __repr__(self) -> str:
        """
        :return: A string representation of the Solution. As specified in the assignment. Also used to save in file.
        """
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
        """
        Gets the depth of the solution.
        :param result:  The result node.
        :return:  The depth of the solution.
        """
        cur = result
        depth = 0
        while cur.parent:
            cur = cur.parent
            depth += 1
        return depth


class PuzzleFileIO:
    """
    Provides static methods for reading a puzzle state from a file and writing the solution back to a file.
    """

    @staticmethod
    def read_puzzle_from_file(filename: str) -> Tuple[PuzzleState, PuzzleState]:
        with open(filename, "r") as f:
            # It will automatically split by whitespaces and newlines, which is exactly what we want
            blocks = f.read().split()
        # Convert the list of strings to a list of integers for type safety
        blocks = list(map(int, blocks))
        # Return the initial and goal states
        return PuzzleState(blocks[:27]), PuzzleState(blocks[27:])

    @staticmethod
    def write_solution_to_file(filename: str, solution: Solution) -> None:
        with open(filename, "w") as f:
            # Use the __repr__ method of the Solution class to get the string representation of the solution.
            f.write(str(solution))


def solve(filename: str) -> Solution:
    """
    Main usability function since it combines all the steps of solving the puzzle and makes the process simpler.
    After we can print or save our solution to the file since it will return the Solution class dedicated to serve
    this purpose.
    :param filename:  The name of the file with the puzzle.
    :return:  The solution to the puzzle.
    """
    initial, goal = PuzzleFileIO.read_puzzle_from_file(filename)
    a_star = AStarSearch(initial, goal)
    result = a_star.search()
    return Solution(result, a_star.N)


if __name__ == "__main__":
    # Driver code that solves puzzles from files and writes solutions to new files.
    res = solve("Input1.txt")
    PuzzleFileIO.write_solution_to_file("Input1_solution.txt", res)
    res2 = solve("Input2.txt")
    PuzzleFileIO.write_solution_to_file("Input2_solution.txt", res2)
    res3 = solve("Input3.txt")
    PuzzleFileIO.write_solution_to_file("Input3_solution.txt", res3)
