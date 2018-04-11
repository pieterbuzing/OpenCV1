import unittest

from detect_shapes import Rectangle
from rectangle_tree import Node


class TestStringMethods(unittest.TestCase):

    def test_tree(self):
        a = Rectangle(None, 0, 0, 100, 100)
        b = Rectangle(None, 10, 10, 30, 90)
        c = Rectangle(None, 30, 10, 60, 30)
        d = Rectangle(None, 15, 15, 20, 60)
        e = Rectangle(None, 20, 60, 10, 25)
        root = Node(a)
        root.insert(b)
        root.insert(c)
        root.insert(d)
        root.insert(e)
        max_node, max_count = root.findmaxchildren()
        assert max_count == 2
        assert max_node.elem.x == 10
        assert max_node.elem.y == 10
        assert max_node.elem == b
        assert root.elem == a
        assert len(root.children) == 2


if __name__ == '__main__':
    unittest.main()
