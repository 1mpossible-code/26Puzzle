import unittest
from main_old import PuzzleSearch, Puzzle, Directions

class TestPuzzleSearch(unittest.TestCase):
    def test_search(self):
        p = PuzzleSearch('Input1.txt')
        with open('test1.txt') as f:
            self.assertEqual(str(p), f.read())

    def test_search2(self):
        p = PuzzleSearch('Input2.txt')
        with open('test2.txt') as f:
            self.assertEqual(str(p), f.read())
    
    def test_search3(self):
        p = PuzzleSearch('Input3.txt')
        with open('test3.txt') as f:
            self.assertEqual(str(p), f.read())

if __name__ == '__main__':
    unittest.main()