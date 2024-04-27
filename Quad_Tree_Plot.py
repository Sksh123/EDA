import matplotlib.pyplot as plt
import mplcursors

# Define constants
BUCKET_SIZE = 4  # Maximum number of data points in each leaf node
TILE_SIZE = 10   # Size of each quadrant (arbitrary value for demonstration)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class QuadTreeNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = [None] * 4  # Four quadrants
        self.data = []

    def is_leaf(self):
        return all(child is None for child in self.children)

    def insert(self, point):
        if self.is_leaf():
            self.data.append(point)
            if len(self.data) > BUCKET_SIZE:
                self.subdivide()
        else:
            quadrant = self.get_quadrant(point)
            if self.children[quadrant] is None:
                self.children[quadrant] = self.create_child(quadrant)
            self.children[quadrant].insert(point)

    def subdivide(self):
        half_width = self.width / 2
        half_height = self.height / 2
        self.children[0] = QuadTreeNode(self.x, self.y, half_width, half_height)
        self.children[1] = QuadTreeNode(self.x + half_width, self.y, half_width, half_height)
        self.children[2] = QuadTreeNode(self.x + half_width, self.y + half_height, half_width, half_height)
        self.children[3] = QuadTreeNode(self.x, self.y + half_height, half_width, half_height)
        for point in self.data:
            quadrant = self.get_quadrant(point)
            self.children[quadrant].insert(point)
        self.data = []

    def get_quadrant(self, point):
        mid_x = self.x + self.width / 2
        mid_y = self.y + self.height / 2
        if point.x <= mid_x:
            if point.y <= mid_y:
                return 0
            else:
                return 3
        else:
            if point.y <= mid_y:
                return 1
            else:
                return 2
            
    def range_query(self, range, point=None):
        if point is None:
            # This is the case when only the range is provided
            # result = []
            # if not self.intersect(range):
            #     return result
            # if self.is_leaf():
            #     result.extend(self.data)
            # else:
            #     for child in self.children:
            #         result.extend(child.range_query(range))
            # return result
            result = []
            if not self.intersect(range):
                return result
            if self.is_leaf():
                # Filter out points inside the range
                result.extend(point for point in self.data if self.point_inside_range(point, range))
            else:
                for child in self.children:
                    result.extend(child.range_query(range))
            return result
        else:
            # This is the case when both range and point are provided
            if not self.intersect(range):
                return "Outside"
            if self.is_leaf():
                return self.get_relative_position(point, range)
            else:
                for child in self.children:
                    result = child.range_query(range, point)
                    if result != "Outside":
                        return result
                return "Inside"
            
    def point_inside_range(self, point, query_range):
        return (query_range.x <= point.x <= query_range.x + query_range.width) and \
           (query_range.y <= point.y <= query_range.y + query_range.height)

    def intersect(self, range):
        return not (range.x + range.width < self.x or
                    range.x > self.x + self.width or
                    range.y + range.height < self.y or
                    range.y > self.y + self.height)

    def get_relative_position(self, point, range):
        if point.x < range.x:
            if point.y < range.y:
                return "Southwest"
            elif point.y > range.y + range.height:
                return "Northwest"
            else:
                return "West"
        elif point.x > range.x + range.width:
            if point.y < range.y:
                return "Southeast"
            elif point.y > range.y + range.height:
                return "Northeast"
            else:
                return "East"
        else:
            if point.y < range.y:
                return "South"
            elif point.y > range.y + range.height:
                return "North"
            else:
                return "Inside"

class Range:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def visualize_quadtree(node, ax):
    if node.is_leaf():
        ax.add_patch(plt.Rectangle((node.x, node.y), node.width, node.height, fill=False, edgecolor='black'))
    else:
        for child in node.children:
            visualize_quadtree(child, ax)



def visualize_points(points, color, ax):
    x = [point.x for point in points]
    y = [point.y for point in points]
    ax.plot(x, y, 'o', color=color) 
    points_plot = ax.scatter(x, y, color=color)  # Use scatter plot instead of plot
    mplcursors.cursor(points_plot, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"({sel.target[0]:.2f}, {sel.target[1]:.2f})"))

def visualize_range_query(query_range, result, ax):
    ax.add_patch(plt.Rectangle((query_range.x, query_range.y), query_range.width, query_range.height, fill=False, edgecolor='red'))
    if isinstance(result, list):
        visualize_points(result, "blue", ax)
    else:
        ax.text(query_range.x + query_range.width / 2, query_range.y + query_range.height / 2, result, ha='center', va='center')

def main():
    # Create a root node for the quadtree
    root = QuadTreeNode(0, 0, 100, 100)

    # Insert some sample data points
    points = [Point(20, 20), Point(80, 80), Point(30, 70), Point(50, 50),
              Point(10, 30), Point(90, 20), Point(70, 40), Point(40, 60),
              Point(60, 90), Point(20, 80), Point(70, 10), Point(10, 60),
              Point(30, 20), Point(80, 30), Point(50, 70), Point(40, 10),
              Point(90, 60), Point(60, 40), Point(20, 50), Point(70, 80), Point(60, 80)]

    for point in points:
        root.insert(point)

    # Define a range for range query
    query_range = Range(0, 0, 100, 100)

    query_result = root.range_query(query_range)
    print("Points within range:")
    for point in query_result:
        print("({}, {})".format(point.x, point.y))

    # Define a point to check its relative position
    check_point = Point(5, 20)

    # Perform range query
    result = root.range_query(query_range, check_point)
    print(f"Relative position of the point ({check_point.x}, {check_point.y}) with respect to the range:", result)

    # Plotting
    fig, ax = plt.subplots()
    visualize_quadtree(root, ax)
    visualize_range_query(query_range, query_result, ax)
    visualize_points([check_point], 'red', ax)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    main()
