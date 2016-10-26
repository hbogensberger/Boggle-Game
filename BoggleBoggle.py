'''
Boggle Boggle
'''
import random
import re

# Standard boggle game has the following 96 letter tiles
letters = ['A', 'A', 'E', 'E', 'G', 'N', 'E', 'L', 'R',
            'T', 'T', 'Y', 'A', 'O', 'O', 'T', 'T', 'W',
            'A', 'B', 'B', 'J', 'O', 'O', 'E', 'H', 'R',
            'T', 'V', 'W', 'C', 'I', 'M', 'O', 'T', 'U',
            'D', 'I', 'S', 'T', 'T', 'Y', 'E', 'I', 'O',
            'S', 'S', 'T', 'D', 'E', 'L', 'R', 'V', 'Y',
            'A', 'C', 'H', 'O', 'P', 'S', 'H', 'I', 'M',
            'N', 'QU', 'E', 'E', 'I', 'N', 'S', 'U', 'E',
            'E', 'G', 'H', 'N', 'W', 'A', 'F', 'F', 'K',
            'P', 'S', 'H', 'L', 'N', 'N', 'R', 'Z', 'D',
            'E', 'I', 'L', 'R', 'X']

# Randomly selects 16 letters to start game
boggle_letters = ""
while len(boggle_letters) != 16:
    boggle_letters += random.choice(letters)

# Creates 4x4 Boggle Board
grid = re.findall('....?', boggle_letters.lower())
nrows, ncols = len(grid), len(grid[0])

# Displays board visually as a 4x4 grid
def pretty_grid(grid):
    s = [[str(e) for e in row] for row in grid]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '  '.join('{{:{}}}'.format(x) for x in lens)
    pretty_table = [fmt.format(*row) for row in s]
    return '  \n\n'.join(pretty_table)

dictfile = '/Users/Bogensberger/Python/Boggle/boggledictionary.txt'

# Trie to store dictionary
class TrieNode:
    def __init__(self, parent, value):
        self.parent = parent
        self.children = [None] * 26
        self.isWord = False
        if parent is not None:
            parent.children[ord(value) - 97] = self

def MakeTrie(dictfile):
    dict = open(dictfile)
    root = TrieNode(None, '')
    for word in dict:
        curNode = root
        for letter in word.lower():
            if 97 <= ord(letter) < 123:
                nextNode = curNode.children[ord(letter) - 97]
                if nextNode is None:
                    nextNode = TrieNode(curNode, letter)
                curNode = nextNode
        curNode.isWord = True
    return root

# BFS Algorithm to search for all words in grid and checking them against trie dictionary
def BoggleWords(grid, dict):
    rows = len(grid)
    cols = len(grid[0])
    queue = []
    words = []
    for y in range(cols):
        for x in range(rows):
            c = grid[y][x]
            node = dict.children[ord(c) - 97]
            if node is not None:
                queue.append((x, y, c, node))
    while queue:
        x, y, s, node = queue.pop(0)
        for dx, dy in ((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)):
            x2, y2 = x + dx, y + dy
            if 0 <= x2 < cols and 0 <= y2 < rows:
                s2 = s + grid[y2][x2]
                node2 = node.children[ord(grid[y2][x2]) - 97]
                if node2 is not None:
                    if node2.isWord and len(s2) >= 3 and s2 not in words:
                        words.append(s2)
                    queue.append((x2, y2, s2, node2))

    return '\n'.join(words)


# Sets up game
welcome = """Welcome to Boggle! Are you ready to play?!\n
You must find as many words as possible in the grid.\nHere are the rules:\n
1.) Letters must be adjacent.\n
2.) Words must contain at least three letters.\n
3.) No letter may be used more than once within a single word."""

def display_words(dictionary):
    print '\nWould you like to see all possible words? (yes or no)\n'
    if raw_input().lower().startswith('y'):
        print 'Here are all the valid words:\n'
        print BoggleWords(grid, dictionary)
    else:
        quit()
        

dictionary = MakeTrie(dictfile)

print welcome

print pretty_grid(grid)

print display_words(dictionary)



 

