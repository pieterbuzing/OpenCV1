class Node:
    def __init__(self, elem):
        self.elem = elem
        self.children = []

    def insert(self, new_elem):
        new_node = Node(new_elem)
        self.__insert(new_node)

    def __insert(self, new_node):
        for child in self.children:
            if child.elem.contains(new_node.elem):
                child.__insert(new_node)
                break
            elif new_node.elem.contains(child.elem):
                old_children = self.children
                self.children = [new_node]
                for old_child in old_children:
                    self.__insert(old_child)
                break
        else:
            self.children.append(new_node)

    def findmaxchildren (self):
        node, count = self, len(self.children)
        for child in self.children:
            nod, cnt = child.findmaxchildren()
            if cnt >= count:
                node, count = nod, cnt
        return node, count

    def __repr__(self):
        return "(%d, %d, %d, %d)" % \
               (self.elem.x, self.elem.y,
                self.elem.width, self.elem.height)
