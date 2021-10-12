from enum import Enum
from typing import Callable

from logic.stream.exceptions import BadToken, FullBuffer
from wordtree import WordTree, PrefixNode


def reverse_map(sample_dict: dict) -> dict:
    """Inverte um mapa; os valores apontam para a chave."""
    reversed_map = {}
    for key, val in sample_dict.items():
        for i in val:
            reversed_map[i] = key
    return reversed_map


class Logic(Enum):
    """Elementos lógicos e parte de suas precedências"""
    EOF = -1
    # Operators --------
    EQUIVALENCE = 0
    IMPLICATION = 1
    OR = 2
    NOR = 3
    XOR = 4
    AND = 5
    NAND = 6
    NOT = 7
    # ------------------
    CLOSE = 8
    OPEN = 9
    VAR = 10
    CONSTANT = 11
    TRUE = 12
    FALSE = 13


"""Mapeia os Tokens com suas representações."""
logicMap: dict[Logic, list[str]] = {
    Logic.TRUE: ['V', 'T'],
    Logic.FALSE: ['F'],
    Logic.NOT: ['NOT', 'NÃO', '!', '~', '¬'],
    Logic.AND: ['AND', 'E', '&&', '&', '.', '∧', '^'],
    Logic.OR: ['OR', 'OU', '||', '|', '+', '∨', 'v'],
    Logic.IMPLICATION: ['IMPLIES', 'IMPLICA', '->', '→', '⇒'],
    Logic.EQUIVALENCE: ['EQUAL', 'IGUAL', 'EQUIVALE', '<->', '⟷', '≡', '==', '⇔'],
    Logic.XOR: ['XOR', '⊻', '⊕'],
    Logic.NAND: ['NAND', '↑'],
    Logic.NOR: ['NOR', '↓'],
    Logic.OPEN: ['('],
    Logic.CLOSE: [')'],
    Logic.VAR: ['p', 'q', 'r'],
}

logicMap[Logic.CONSTANT] = logicMap[Logic.TRUE] + logicMap[Logic.FALSE]

# Utilizado para facilitar procuras
whitespace: tuple = (' ', '\n', '\t')
equivalent: dict[str, Logic] = reverse_map(logicMap)
operators = (key for key, val in equivalent.items() if val != Logic.CONSTANT)
word_tree: WordTree = WordTree()

for word in equivalent:
    word_tree.add(word)


class ReturnString:
    """Simula um input() com texto predeterminado."""

    def __init__(self, text: str = ""):
        self.text: str = text

    def __call__(self, *args, **kwargs):
        return self.text


class Token:
    """Representa um elemento lógico dentro de uma expressão."""

    def __init__(self, kind: Logic = Logic.EOF, value: str = ""):
        self.kind: Logic = kind
        self.value = value

    def __str__(self):
        return f"{type(self).__name__}(kind={self.kind}, value='{self.value}')"

    def __repr__(self):
        return str(self)

    def __bool__(self):
        if self.kind == Logic.EOF:
            return False
        return True

    @property
    def priority(self) -> int:
        """Retorna um valor de prioridade a partir de seu valor no Enum."""
        return self.kind.value


class InputStream:
    """Nesse Stream se obtem caracteres separados pelo espaço em branco."""

    def __init__(self, source: Callable = input):
        self.source: Callable = source
        self.buffer: str = ""

    def __bool__(self):
        return bool(self.buffer)

    def get(self) -> str:
        """Retorna um caracter."""
        return self.char_tokenize()

    def putback(self, val: str) -> None:
        """Retorna o caracter para o buffer"""
        self.buffer = val + self.buffer

    def input(self) -> None:
        """Utiliza o source para pegar um input."""
        self.buffer = self.source()

    def empty(self) -> bool:
        """Verfifica se acabou o buffer."""
        return len(self.buffer) <= 0

    def char_tokenize(self) -> str:
        """Pega o primeiro caracter que não seja um espaço branco."""
        index: int = 0
        size: int = len(self.buffer)
        value: str = ""
        if self.buffer:
            while index < size and self.buffer[index] in whitespace:
                index += 1
            while index < size and self.buffer[index] not in whitespace:
                value = self.buffer[index]
                self.buffer = self.buffer[index + 1:]
                return value

        return value


class TokenStream:
    """Utiliza um InputStream para separar os tokens de uma string."""

    def __init__(self, source: InputStream):
        self.source = source
        self.full = False
        self.buffer = Token()

    def tokenize(self) -> list[Token]:
        """Retorna uma lista com os Tokens permitidos. Finaliza com um EOF (End-of-File)."""
        tokens: list[Token] = []
        t: Token = self.get()
        while t:
            tokens.append(t)
            t = self.get()

        tokens.append(Token(Logic.EOF))
        return tokens

    def match(self, ch: str) -> str:
        """Procura uma aproximação a partir de 1 caractere."""
        node: PrefixNode = word_tree.root
        matched: str = ""
        while node.has(ch):
            node = node.get(ch)
            matched += ch
            ch = self.source.get()
        self.source.putback(ch)

        return matched

    def get(self) -> Token:
        """Retorna somente um Token permitido. Utilizando uma Arvore de Palavras para se aproximar."""
        if self.full:
            self.full = False
            return self.buffer

        ch: str = self.source.get()

        if ch in logicMap[Logic.TRUE]:
            return Token(equivalent[ch], "V")

        elif ch in logicMap[Logic.FALSE]:
            return Token(equivalent[ch], "F")

        elif word_tree.root.has(ch):
            match: str = self.match(ch)
            if match in equivalent:
                return Token(equivalent[match], match)
            for c in match:
                self.source.putback(c)

        elif ch == "":
            return Token()

        raise BadToken(f"Bad Token: char='{ch}'")

    def putback(self, t: Token) -> None:
        """Retorna um Token para o buffer."""
        if self.full:
            raise FullBuffer(f"Full Buffer: {t}")
        self.buffer = t
        self.full = True

    def clean(self) -> None:
        """Limpa o buffer."""
        self.buffer = Token()
        self.full = False


def main():
    text_stream = ReturnString()
    cin = InputStream(text_stream)
    ts = TokenStream(cin)

    text_stream.text = "OU"
    print(word_tree.root.children["O"])
    cin.input()
    print(ts.match("OU"))


if __name__ == '__main__':
    main()
