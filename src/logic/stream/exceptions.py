class BadToken(Exception):
    """Representa um Token não permitido."""
    pass


class FullBuffer(Exception):
    """Problema de lógica no programa. Foi colocado um Token no Buffer antes de ser resgatado."""
    pass
