class CharNode:
    def __init__(self, char: str):
        self.char: str = char
        self.children: dict[CharNode] = {}

    def __repr__(self) -> str:
        return f"CharNode(char='{self.char}', children={self.children})"

    def __eq__(self, other):
        return self.char == other

    def __hash__(self):
        return hash(self.char)


class WordTree:
    def __init__(self):
        self.root = CharNode("")

    def add(self, word: str):
        node: CharNode = self.root
        for char in word:
            found = False
            if char in node.children:
                node = node.children[char]
                found = True
                break
            if not found:
                new_node = CharNode(char)
                node.children[new_node] = new_node
                node = new_node

    def find(self, word: str):
        node: CharNode = self.root
        if not node.children:
            return False
        for char in word:
            found = False
            if char in node.children:
                found = True
                node = node.children[char]
            if not found:
                return False

        return True

def main():
    root = WordTree()
    root.add("NOR")
    root.add('&')

    print(root.find("NOR"))
    print(root.find("&"))
    print(root.find("&&"))


if __name__ == '__main__':
    main()
