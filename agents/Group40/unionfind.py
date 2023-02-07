class unionfind:

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def join(self, x, y):
        rep_x = self.find(x)
        rep_y = self.find(y)

        if rep_x == rep_y:
            return False
        if self.rank[rep_x] < self.rank[rep_y]:
            self.parent[rep_x] = rep_y
        elif self.rank[rep_x] > self.rank[rep_y]:
            self.parent[rep_y] = rep_x
        else:
            self.parent[rep_x] = rep_y
            self.rank[rep_y] += 1
        return True

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

        px = self.parent[x]
        if x == px:
            return x

        gx = self.parent[px]
        if gx == px:
            return px

        self.parent[x] = gx

        return self.find(gx)

    def connected(self, x, y):
        return self.find(x) == self.find(y)
