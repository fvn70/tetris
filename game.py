import numpy as np


class Field:
    pieces = []
    saved = []

    def __init__(self, cols, rows):
        self.n = rows
        self.m = cols

    def add_piece(self, p):
        self.pieces = []
        self.pieces.append(p)

    def down(self, p):
        return p.down(self, self.m, self.n)

    def rotate(self, p):
        p.rotate()

    def left(self, p):
        p.left(self.m)

    def right(self, p):
        p.right(self.m)

    def draw(self):
        lst = []
        for p in self.pieces:
            if p.live:
                lst += p.shapes[p.idx]
        lst += self.saved
        k = 0
        print()
        for i in range(self.n):
            s =''
            for j in range(self.m):
                s += '0 ' if k in lst else '- '
                k += 1
            print(s.strip())

    def down_all(self):
        vmax = (self.n - 1) * self.m
        while np.intersect1d(self.saved, range(vmax, vmax + self.m)).size == self.m:
            self.saved = [v + self.m for v in self.saved if v < vmax]

class Piese:

    def __init__(self, name, sh):
        self.name = name
        self.shapes = sh
        self.turns = len(sh)
        self.turn = 0
        self.idx = 0
        self.live = True

    def left(self, m):
        if self.live:
            v0 = min([v % m for v in self.shapes[self.idx]])
            if v0 > 0:
                self.shapes = [[p[j] - 1 for j in range(4)] for p in self.shapes]

    def right(self, m):
        if self.live:
            v0 = max([v % m for v in self.shapes[self.idx]])
            if v0 < m - 1:
                self.shapes = [[p[j] + 1 for j in range(4)] for p in self.shapes]

    def rotate(self):
        if self.live:
            self.turn += 1
            self.idx = self.turn % self.turns

    def down(self, g, m, n):
        row0 = m
        if self.live:
            p = self.shapes[self.idx]
            v0 = max([v // m for v in p])
            p1 = [x + m for x in p]
            if np.intersect1d(p1, g.saved).size == 0:
                if v0 < n - 1:
                    self.shapes = [[p[j] + m for j in range(4)] for p in self.shapes]
                if v0 == n - 2:
                    self.live = False
                    g.saved += p1
            else:
                self.live = False
                g.saved += p
            if len(g.saved) > 0:
                row0 = min(g.saved) // m
        return row0

O = [[4, 14, 15, 5]]
I = [[4, 14, 24, 34], [3, 4, 5, 6]]
S = [[5, 4, 14, 13], [4, 14, 15, 25]]
Z = [[4, 5, 15, 16], [5, 15, 14, 24]]
L = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
J = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
T = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]

dic = {'O': O, 'I': I, 'S': S, 'Z': Z, 'L': L, 'J': J, 'T': T, }

cmd = input()
m, n = cmd.split()
g = Field(int(m), int(n))
g.draw()
p = None
while True:
    # cmd = input('\nInput command: ')
    cmd = input('\n')
    if cmd == 'exit':
        break
    elif cmd == 'piece':
        cmd = input()
        lst = dic[cmd].copy()
        p = Piese(cmd, lst)
        g.add_piece(p)
        g.draw()
        continue
    elif cmd == 'down':
        pass
    elif cmd == 'break':
        g.down_all()
    elif cmd == 'left':
        g.left(p)
    elif cmd == 'right':
        g.right(p)
    elif cmd == 'rotate':
        g.rotate(p)
    row = g.down(p)
    g.draw()
    if row < 1:
        print('\nGame Over!')
        break

