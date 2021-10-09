class CharNode:
    def __init__(self, char: str):
        self.char: str = char
        self.children: dict[CharNode] = {}
        self.finished: bool = False
        self.counter: int = 1

    def __eq__(self, other):
        return self.char == other.char

    def __hash__(self):
        return hash(self.char)


class WordTree:
    def __init__(self):
        self.root = CharNode("")

    def add(self, word: str):
        node: CharNode = self.root
        for char in word:
            found = False
            node2 = CharNode(char)
            if node2 in node.children:
                node.children[node2].counter += 1
                node = node.children[node2]
                found = True
                break
            if not found:
                new_node = CharNode(char)
                node.children[new_node] = new_node
                node = new_node
        node.finished = True

    def find(self, word: str):
        node: CharNode = self.root
        if not node.children:
            return False
        for char in word:
            found = False
            node2 = CharNode(char)
            if node2 in node.children:
                found = True
                node = node.children[node2]
            if not found:
                return False
        return node.finished

def main():
    root = WordTree()
    root.add("word")
    root.add('&')

    print(root.find("word"))
    print(root.find("&"))



if __name__ == '__main__':
    main()
