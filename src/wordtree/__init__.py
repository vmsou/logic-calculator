class CharNode:
    """Representa um prefixo em uma arvore de prefixos."""

    def __init__(self, char: str):
        self.char: str = char
        self.children: dict[str, CharNode] = {}

    def __repr__(self) -> str:
        return f"CharNode(char='{self.char}', children={self.children})"

    def __eq__(self, other):
        return self.char == other

    def __hash__(self):
        return hash(self.char)

    def has(self, char: str):
        return char in self.children


class WordTree:
    """Representa uma arvore de prefixos e guarda sua raiz."""

    def __init__(self):
        self.root: CharNode = CharNode("")

    def add(self, word: str):
        node: CharNode = self.root
        for char in word:
            found = False
            if char in node.children:
                node = node.children[char]
                found = True
            if not found:
                new_node = CharNode(char)
                node.children[char] = new_node
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
    root.add("OR")
    root.add('OU')

    print(root.find("OU"))
    print(root.find("OR"))
    print(root.find("&&"))


if __name__ == '__main__':
    main()
