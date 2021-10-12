from __future__ import annotations


class PrefixNode:
    """Representa um prefixo em uma arvore de prefixos."""

    def __init__(self, char: str):
        self.char: str = char
        self.children: dict[str, PrefixNode] = {}

    def __repr__(self) -> str:
        return f"CharNode(char='{self.char}', children={self.children})"

    def __eq__(self, other) -> bool:
        return self.char == other

    def __hash__(self) -> int:
        return hash(self.char)

    def has(self, char: str) -> bool:
        return char in self.children

    def get(self, char: str) -> PrefixNode:
        return self.children[char]

    def set(self, char: str, node) -> None:
        self.children[char] = node


class WordTree:
    """Representa uma arvore de prefixos e guarda sua raiz."""

    def __init__(self):
        self.root: PrefixNode = PrefixNode("")

    def add(self, word: str) -> None:
        node: PrefixNode = self.root
        for char in word:
            found: bool = False
            if node.has(char):
                node = node.get(char)
                found = True
            if not found:
                new_node: PrefixNode = PrefixNode(char)
                node.set(char, new_node)
                node = new_node

    def find(self, word: str) -> bool:
        node: PrefixNode = self.root
        if not node.children:
            return False
        for char in word:
            found: bool = False
            if node.has(char):
                found = True
                node = node.get(char)
            if not found:
                return False
        return True

def main() -> None:
    root: WordTree = WordTree()
    root.add("OR")
    root.add('OU')

    print(root.find("OU"))
    print(root.find("OR"))
    print(root.find("&&"))


if __name__ == '__main__':
    main()
