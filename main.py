class Puzzle:
    def __init__(self, puzzle_array: list) -> None:
        self.__puzzle = list(map(lambda x: int(x), puzzle_array))

    def display(self) -> None:
        for i in range(3):
            for j in range(3):
                line = ""
                for k in range(3):
                    line += str(self.__puzzle[i * 9 + j * 3 + k]) + " "
                print(line.strip())
            print()

    def calculate_manhattan_distance(self, goal: object) -> int:
        pass

    def get_position(self, value: int) -> int:
        return self.__puzzle.index(value)

    def get_xyz(self, value: int) -> tuple:
        idx = self.get_position(value)
        z = idx // 9
        idx %= 9
        y = idx // 3
        idx %= 3
        x = idx
        return x, y, z

class PuzzleSearch:
    def __init__(self, filename) -> None:
        with open(filename, "r") as f:
            content = f.read()
            blocks = content.split()
            self.initial = Puzzle(blocks[:27])
            self.final = Puzzle(blocks[27:])


if __name__ == "__main__":
    PuzzleSearch("Input1.txt")
