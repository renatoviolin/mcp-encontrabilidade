"""Servidor MCP mínimo — duas tools de exemplo.

Rode com:
    uv sync
    uv run python app.py

O servidor sobe via HTTP em http://127.0.0.1:8000/mcp.
"""

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("aula-mcp")

PRODUTOS = [
    {"id": "fone-a", "nome": "Fone Pulse Air", "preco": 199.90, "estoque": 12},
    {"id": "fone-b", "nome": "Fone Run Pro", "preco": 249.90, "estoque": 0},
    {"id": "fone-c", "nome": "Fone Lit Basic", "preco": 129.90, "estoque": 30},
]


@mcp.tool()
def somar(a: float, b: float) -> float:
    """Soma dois números e devolve o resultado."""
    print(f"[somar] a={a} b={b}", flush=True)
    return a + b


@mcp.tool()
def repetir_nome(nome: str) -> str:
    """Retorna o nome do usuário em caixa alta"""
    return nome.upper()


@mcp.tool()
def buscar_produtos(termo: str | None = None, preco_max: float | None = None) -> list[dict]:
    """Busca produtos pelo nome e, se informado, limita pelo preço máximo.
       Se termo não informado, retorna todos os produtos da base
    """
    if termo == None:
        return PRODUTOS
    print(f"[buscar_produtos] termo={termo!r} preco_max={preco_max}", flush=True)
    termo = termo.strip().lower()
    return [
        produto
        for produto in PRODUTOS
        if termo in produto["nome"].lower()
        and (preco_max is None or produto["preco"] <= preco_max)
    ]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
