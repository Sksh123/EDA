class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Item:
    def __init__(self, position, data):
        self.position = position
        self.data = data

class QuadTree:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.item = None
        
        self.top_left_tree = None
        self.top_right_tree = None
        self.bottom_left_tree = None
        self.bottom_right_tree = None

    def insert(self, item):
        if item is None:
            return
        
        if not self.in_boundary(item.position):
            return

        if abs(self.top_left.x - self.bottom_right.x) <= 1 and abs(self.top_left.y - self.bottom_right.y) <= 1:
            if self.item is None:
                self.item = item
            return

        if (self.top_left.x + self.bottom_right.x) / 2 >= item.position.x:
            if (self.top_left.y + self.bottom_right.y) / 2 >= item.position.y:
                if self.top_left_tree is None:
                    self.top_left_tree = QuadTree(self.top_left, Point((self.top_left.x + self.bottom_right.x) / 2, (self.top_left.y + self.bottom_right.y) / 2))
                self.top_left_tree.insert(item)
            else:
                if self.bottom_left_tree is None:
                    self.bottom_left_tree = QuadTree(Point(self.top_left.x, (self.top_left.y + self.bottom_right.y) / 2), Point((self.top_left.x + self.bottom_right.x) / 2, self.bottom_right.y))
                self.bottom_left_tree.insert(item)
        else:
            if (self.top_left.y + self.bottom_right.y) / 2 >= item.position.y:
                if self.top_right_tree is None:
                    self.top_right_tree = QuadTree(Point((self.top_left.x + self.bottom_right.x) / 2, self.top_left.y), Point(self.bottom_right.x, (self.top_left.y + self.bottom_right.y) / 2))
                self.top_right_tree.insert(item)
            else:
                if self.bottom_right_tree is None:
                    self.bottom_right_tree = QuadTree(Point((self.top_left.x + self.bottom_right.x) / 2, (self.top_left.y + self.bottom_right.y) / 2), self.bottom_right)
                self.bottom_right_tree.insert(item)

    def search(self, point):
        if not self.in_boundary(point):
            return None

        if self.item is not None:
            return self.item

        if (self.top_left.x + self.bottom_right.x) / 2 >= point.x:
            if (self.top_left.y + self.bottom_right.y) / 2 >= point.y:
                if self.top_left_tree is None:
                    return None
                return self.top_left_tree.search(point)
            else:
                if self.bottom_left_tree is None:
                    return None
                return self.bottom_left_tree.search(point)
        else:
            if (self.top_left.y + self.bottom_right.y) / 2 >= point.y:
                if self.top_right_tree is None:
                    return None
                return self.top_right_tree.search(point)
            else:
                if self.bottom_right_tree is None:
                    return None
                return self.bottom_right_tree.search(point)

    def in_boundary(self, point):
        return point.x >= self.top_left.x and point.x <= self.bottom_right.x and point.y >= self.top_left.y and point.y <= self.bottom_right.y

# Driver program
root = QuadTree(Point(0, 0), Point(10, 10))
item1 = Item(Point(2, 2), "A")
item2 = Item(Point(6, 8), "B")
item3 = Item(Point(9, 5), "C")
root.insert(item1)
root.insert(item2)
root.insert(item3)

print("Item at (2, 2):", root.search(Point(2, 2)).data)
print("Item at (6, 8):", root.search(Point(6, 8)).data)
print("Item at (9, 5):", root.search(Point(9, 5)).data)
print("Non-existing item:", root.search(Point(5, 5)))
