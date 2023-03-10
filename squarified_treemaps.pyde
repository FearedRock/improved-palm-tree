import math
from S4P import *


def parse6(file_name):
    data = loadStrings(file_name)
    
    num_int = []
    num_list = []
    for count, num in enumerate(data):
        num = num.split(' ')
        mini_list = []
        for non_integers in num:
            non_integers = non_integers.strip('\n')
            if non_integers.isnumeric():
                mini_list.append(int(non_integers))
        num_list.append(mini_list)

    num_values = []
    num_parents = []
    parent_child_list = []

    for count, num in enumerate(num_list):
        #dedicated for creating the values list by using the format of the file
        if count == 0 and len(num) == 1:
            for second_count, values in enumerate(num_list[:num[0] + 1]):
                if second_count == 0:
                    pass
                else:
                    num_values.append(values)

        #if the count is greater than 0, then that means that single number represents the parent child
        #relationships
        elif len(num) == 1:
            for third_count, values in enumerate(num_list[count:]):
                if third_count == 0:
                    pass
                else:
                    num_parents.append(values)

    num_parents = sorted(num_parents, key= lambda x: x[0])
    num_values = sorted(num_values, key= lambda x: x[0])
    return(num_parents, num_values)

class Node:
    def __init__(self, id, value, x=0, y=0, width=0, height=0):
        self.id = id
        self.value = value
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.parent = None
        self.children = []
        self.depth = 1
        self.max_depth = 1

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def get_id(self):
        return self.id

    def calculate_value(self):
        value = self.value
        for child in self.children:
            child.calculate_value()
            value += child.value
        self.value = value

        return self.value

def create_tree(parent_child_list, child_value_list):
    nodes = {}
    for parent, child in parent_child_list:
        #Creates the parent and child nodes
        if parent not in nodes:
            nodes[parent] = Node(parent, 0)
        if child not in nodes:
            nodes[child] = Node(child, 0)
        nodes[parent].add_child(nodes[child])
    #Associates the values with the children
    for child, value in child_value_list:
        nodes[child].value = value

    root = None
    for node in nodes.values():
        # No parent means that the node is the root node
        if node.get_parent() is None:
            root = node
            break

    def calculate_depths(node, depth=0):
        node.depth = depth
        for child in node.children:
            calculate_depths(child, depth + 1)

    calculate_depths(root)
    root.max_depth = max([node.depth for node in nodes.values()])
    root.calculate_value()

    def assign_coordinates(node, x, y, dx, dy):
        sizes = [child.value for child in node.children]
        if not sizes:
            node.x = x
            node.y = y
            node.width = dx
            node.height = dy
        else:
            rects = padded_squarify(sizes, x, y, dx, dy)
            for i, child in enumerate(node.children):
                rect = rects[i]
                assign_coordinates(child, abs(rect["x"]), abs(rect["y"]), abs(rect["dx"]), abs(rect["dy"]))

    assign_coordinates(root, 0, 0, 1, 1)
    return root

def assign_node_dimensions(node, x, y, width, height):
    node.x = x
    node.y = y
    node.width = width
    node.height = height
    rectangles = padded_squarify([child.value for child in node.children], x, y, width, height)
    for i, child in enumerate(node.children):
        assign_node_dimensions(child, rectangles[i]["x"], rectangles[i]["y"], rectangles[i]["dx"], rectangles[i]["dy"])

def print_tree(node, level=0):
    print("  " * level + str(node.get_id()) + ": " + str(node.value))
    for child in node.get_children():
        print_tree(child, level + 1)

def print_node_info(node):
    print("Node id:", node.id)
    print("Node value:", node.value)
    print("Node x:", node.x)
    print("Node y:", node.y)
    print("Node width:", node.width)
    print("Node height:", node.height)
    print("Node parent:", node.parent.id if node.parent else None)
    print("Node children:", [child.id for child in node.children])
    print("Node depth:", node.depth)
    print("Node max_depth:", node.max_depth)
    print()

    for child in node.children:
        print_node_info(child)

def flatten_tree(root):
    nodes = [root]
    flattened_tree = [root]
    while nodes:
        node = nodes.pop(0)
        children = node.get_children()
        for child in children:
            nodes.append(child)
            flattened_tree.append(child)
    flattened_tree.sort(key=lambda x: x.value, reverse=True)
    return flattened_tree

def draw_treemap(mega_list):
    for node in mega_list:
        fill(node.value % 255, 0, 0)
        rect(node.x, node.y, node.width, node.height)
                
def setup():
    size(1200, 800)
    parents_list, values_list = parse6('W1-hierarchy2.shf')
    root = create_tree(parents_list, values_list)
    print_tree(root)
    assign_node_dimensions(root, 0, 0, 1200, 800)
    mega_list = flatten_tree(root)
    draw_treemap(mega_list)
    #print_node_info(root)
    #print(mega_list)
    print('parents_list = ', parents_list)
    print('values_list = ', values_list)
    
#def draw():

    
    
    
