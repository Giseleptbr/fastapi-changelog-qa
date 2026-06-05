"""Function-calling / tool-use — registro de tools usadas pelo agente."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable


def check_compat(lib: str, from_version: str, to_version: str) -> str:
    """Retorna breaking changes entre duas versões do FastAPI listados no changelog."""
    corpus_path = Path("data/corpus/fastapi-release-notes.md")
    if not corpus_path.exists():
        return "Arquivo de release notes não encontrado em data/corpus/."

    content = corpus_path.read_text(encoding="utf-8", errors="ignore")

    try:
        from_tuple = tuple(int(x) for x in from_version.split("."))
        to_tuple = tuple(int(x) for x in to_version.split("."))
    except ValueError:
        return f"Versões inválidas: {from_version}, {to_version}. Use formato X.Y.Z."

    # Extrai seções de versão do changelog
    sections = re.split(r'\n(?=## \d)', content)
    breaking: list[str] = []

    for section in sections:
        match = re.match(r'## (\d+\.\d+\.\d+)', section)
        if not match:
            continue
        ver_tuple = tuple(int(x) for x in match.group(1).split("."))
        if from_tuple < ver_tuple <= to_tuple:
            # Filtra linhas com "breaking" ou "deprecat" ou "removed"
            lines = [
                line.strip()
                for line in section.splitlines()
                if re.search(r'breaking|deprecat|removed|incompatible', line, re.IGNORECASE)
            ]
            if lines:
                breaking.append(f"**{match.group(1)}:**\n" + "\n".join(f"  - {l}" for l in lines))

    if not breaking:
        return f"Nenhum breaking change encontrado entre {from_version} e {to_version} no changelog do {lib}."
    return "\n\n".join(breaking)


TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "check_compat",
            "description": "Verifica breaking changes entre duas versões do FastAPI consultando o changelog oficial. Use quando o usuário perguntar sobre compatibilidade ou mudanças entre versões.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lib": {
                        "type": "string",
                        "description": "Nome da biblioteca (ex: 'fastapi')",
                    },
                    "from_version": {
                        "type": "string",
                        "description": "Versão de origem (ex: '0.100.0')",
                    },
                    "to_version": {
                        "type": "string",
                        "description": "Versão de destino (ex: '0.110.0')",
                    },
                },
                "required": ["lib", "from_version", "to_version"],
            },
        },
    },
]


TOOL_REGISTRY: dict[str, Callable[..., str]] = {
    "check_compat": check_compat,
}


def run_tool_call(name: str, arguments_json: str) -> str:
    """Executa uma tool call e retorna o resultado como string."""
    if name not in TOOL_REGISTRY:
        return f"ERROR: tool '{name}' nao registrada"
    try:
        kwargs = json.loads(arguments_json)
        return TOOL_REGISTRY[name](**kwargs)
    except Exception as e:
        return f"ERROR ao executar {name}: {e}"
