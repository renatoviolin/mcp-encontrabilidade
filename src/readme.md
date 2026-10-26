# aula-mcp — servidor MCP mínimo em Python

Template de sala: um servidor MCP via **HTTP (Streamable HTTP)** com duas tools.

- `somar(a, b)` — soma dois números.
- `buscar_produtos(termo, preco_max?)` — filtra uma lista de produtos em memória.

Biblioteca: [MCP Python SDK](https://py.sdk.modelcontextprotocol.io/) (`mcp`), que já traz a classe `MCPServer` (a antiga `FastMCP`).

## Estrutura

```
aula-mcp/src/
  app.py            <- servidor e tools
  pyproject.toml    <- dependências
  uv.lock           <- versões travadas
  readme.md
```

## 1. Instalar

Pré-requisito: [uv](https://docs.astral.sh/uv/). O uv também baixa o Python 3.11+ se precisar.

```bash
cd aula-mcp/src
uv sync
```

## 2. Rodar

```bash
uv run python app.py
```

O servidor sobe em `http://127.0.0.1:8000/mcp` e fica rodando até `Ctrl+C`. Deixe este terminal aberto: o opencode e o Inspector se conectam a ele por HTTP.

Cada tool imprime no terminal os dados que chegaram, por exemplo:

```
[somar] a=17.0 b=25.0
[buscar_produtos] termo='fone' preco_max=200.0
```

### Testar no Inspector

Precisa de Node.js com `npx`.

Listar as tools:

```bash
npx -y @modelcontextprotocol/inspector --cli http://127.0.0.1:8000/mcp --method tools/list
```

Chamar `somar`:

```bash
npx -y @modelcontextprotocol/inspector --cli http://127.0.0.1:8000/mcp \
  --method tools/call --tool-name somar --tool-arg a=17 --tool-arg b=25
```

Para usar a interface visual:

```bash
npx -y @modelcontextprotocol/inspector
```

Na tela, escolha **Transport = Streamable HTTP**, informe `http://127.0.0.1:8000/mcp` e clique em **Connect**.

> Não renomeie `app.py` para `mcp.py`: o nome do arquivo sombreia o pacote `mcp` e o Python passa a importar o próprio script no lugar da biblioteca.

## 3. Configurar no opencode

Adicione ao `opencode.json` do projeto ou ao global `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "aula-mcp": {
      "type": "remote",
      "url": "http://127.0.0.1:8000/mcp",
      "enabled": true
    }
  }
}
```

1. Suba o servidor com `uv run python app.py`.
2. Reinicie o opencode (ou abra-o depois do servidor).
3. Teste no chat:

> Use a tool `somar` para calcular 17 + 25.

> Use `buscar_produtos` para listar fones até R$ 200.

Se o agente chamar as tools, o MCP está conectado. O opencode não inicia servidores remotos: o `app.py` precisa estar rodando.

## 4. Como as tools são criadas

- `@mcp.tool()` registra a função como tool.
- O nome da função vira o nome da tool.
- Os tipos dos parâmetros (`a: float`, `preco_max: float | None`) viram o JSON Schema que o agente vê.
- A docstring vira a descrição que ajuda o agente a decidir quando chamar.
- O retorno é serializado automaticamente.

Para criar uma tool nova:

```python
@mcp.tool()
def ola(nome: str) -> str:
    """Cumprimenta a pessoa pelo nome."""
    return f"Olá, {nome}!"
```

## 5. Regras do HTTP

- O servidor escuta apenas em `127.0.0.1:8000` por padrão (mesma máquina do opencode).
- O endpoint do MCP é `/mcp`; abrir `http://127.0.0.1:8000/` no navegador não mostra a loja nem as tools.
- Para mudar host/porta, altere a chamada final do `app.py` e o `url` do `opencode.json`:

```python
mcp.run(transport="streamable-http", host="127.0.0.1", port=8080)
```

- O template não tem autenticação. Não exponha em `0.0.0.0` ou na internet sem colocar auth na frente.
- Como o transporte é HTTP, `print()` no servidor é seguro e aparece no terminal. Se um dia trocar para stdio, use `logging` (stderr): o stdout fica reservado ao protocolo.

## 6. Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Connection refused` no Inspector/opencode | servidor não está rodando | `uv run python app.py` em outro terminal |
| `Address already in use` | porta 8000 ocupada | pare o outro processo ou use outra porta |
| opencode não lista as tools | URL errada ou servidor parado | confira `http://127.0.0.1:8000/mcp` e reinicie |
| `ModuleNotFoundError: No module named 'mcp.server'` | arquivo renomeado para `mcp.py` | mantenha o nome `app.py` |
| Inspector não abre | Node/npx ausente | instale Node 20+ |
