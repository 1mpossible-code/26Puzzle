import unittest
from old_with_visualization import Puzzle, Directions


# 0 always present the blank tile
class TestPuzzle(unittest.TestCase):
    def test_init1(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])

        # Check if the tiles are correct
        self.assertEqual(i.get_raw(), tuple([i for i in range(27)]))

    def test_init2(self):
        # Now we test init from another puzzle
        i = Puzzle([i for i in range(27)])
        j = Puzzle(i)

        # Check if the tiles are correct
        self.assertEqual(j.get_raw(), tuple([i for i in range(27)]))

    def test_hash(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])
        j = Puzzle([i for i in range(27)])

        # Check if the hash is correct
        self.assertEqual(hash(i), hash(j))

    def test_eq(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])
        j = Puzzle([i for i in range(27)])

        # Check if the equality is correct
        self.assertEqual(i, j)

    def test_move_e(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])

        # Move the blank tile to the right
        i = i.move(Directions.E)

        # Make the list of tiles with the blank tile moved to the right
        tiles = [i for i in range(27)]
        tiles[0], tiles[1] = tiles[1], tiles[0]

        # Check if the tiles are correct
        self.assertEqual(i.get_raw(), tuple(tiles))

    def test_move_w(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([26 - i for i in range(27)])

        # Move the blank tile to the left
        i = i.move(Directions.W)

        # Make the list of tiles with the blank tile moved to the right
        tiles = [26 - i for i in range(27)]
        tiles[len(tiles) - 1], tiles[len(tiles) - 2] = (
            tiles[len(tiles) - 2],
            tiles[len(tiles) - 1],
        )

        # Check if the tiles are correct
        self.assertEqual(i.get_raw(), tuple(tiles))

    def test_move_s(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])

        # Move the blank tile to the bottom
        i = i.move(Directions.S)

        # Make the list of tiles with the blank tile moved to the right
        tiles = [i for i in range(27)]
        tiles[0], tiles[3] = tiles[3], tiles[0]

        # Check if the tiles are correct
        self.assertEqual(i.get_raw(), tuple(tiles))

    def test_move_n(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([26 - i for i in range(27)])

        # Move the blank tile to the top
        i = i.move(Directions.N)

        # Make the list of tiles with the blank tile moved to the right
        tiles = [26 - i for i in range(27)]
        tiles[len(tiles) - 1], tiles[len(tiles) - 4] = (
            tiles[len(tiles) - 4],
            tiles[len(tiles) - 1],
        )

        # Check if the tiles are correct
        self.assertEqual(i.get_raw(), tuple(tiles))

    def test_move_d(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])

        # Move the blank tile to the bottom
        i = i.move(Directions.D)

        # Make the list of tiles with the blank tile moved to the right
        tiles = [i for i in range(27)]
        tiles[0], tiles[9] = tiles[9], tiles[0]

        # Check if the tiles are correct
        self.assertEqual(i.get_raw(), tuple(tiles))

    def test_move_u(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([26 - i for i in range(27)])

        # Move the blank tile to the top
        i = i.move(Directions.U)

        # Make the list of tiles with the blank tile moved to the right
        tiles = [26 - i for i in range(27)]
        tiles[len(tiles) - 1], tiles[len(tiles) - 10] = (
            tiles[len(tiles) - 10],
            tiles[len(tiles) - 1],
        )

        # Check if the tiles are correct
        self.assertEqual(i.get_raw(), tuple(tiles))

    def test_get_xyz(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])

        # Get the x, y, z coordinates of the blank tile
        x, y, z = i.get_xyz(0)

        # Check if the coordinates are correct
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(z, 0)

    def test_get_position(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])

        # Get the position of the blank tile
        position = i.get_position(0)

        # Check if the position is correct
        self.assertEqual(position, 0)

    def test_repr(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])

        d = """0 1 2
3 4 5
6 7 8

9 10 11
12 13 14
15 16 17

18 19 20
21 22 23
24 25 26"""

        # Check if the representation is correct
        self.assertEqual(i.__repr__(), d)

    def test_repr2(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([26 - i for i in range(27)])

        d = """26 25 24
23 22 21
20 19 18

17 16 15
14 13 12
11 10 9

8 7 6
5 4 3
2 1 0"""

        # Check if the representation is correct
        self.assertEqual(i.__repr__(), d)
    
    def test_calculate_manhattan_distance(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])
        j = Puzzle([i for i in range(27)])

        # Check if the manhattan distance is correct
        self.assertEqual(i.calculate_manhattan_distance(j), 0)
    
    def test_calculate_manhattan_distance2(self):
        # Make puzzle with 27 tiles (3x3x3) 0 to 26
        i = Puzzle([i for i in range(27)])
        titles = [i for i in range(27)]
        titles[0], titles[1] = titles[1], titles[0]

        j = Puzzle(titles)

        # Check if the manhattan distance is correct
        self.assertEqual(i.calculate_manhattan_distance(j), 2)



if __name__ == "__main__":
    unittest.main()
