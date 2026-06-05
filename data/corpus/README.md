# Corpus

Esta pasta contém os documentos indexados pelo pipeline RAG.

## Conteúdo atual

- `fastapi-release-notes.md` — release notes oficiais do FastAPI (versões 2025+), obtido de `docs/en/docs/release-notes.md` do repositório oficial

## Como atualizar o corpus

```bash
git clone --depth 1 https://github.com/tiangolo/fastapi /tmp/fastapi
cp /tmp/fastapi/docs/en/docs/release-notes.md data/corpus/fastapi-release-notes.md
rm -rf data/chroma/  # força re-indexação
```

## Restrições

- O pipeline suporta `.pdf`, `.md` e `.txt`
- Documentos sem direitos autorais ou com licença compatível com uso público
- O Gemini free tier aceita no máximo 100 embeddings/minuto — corpus muito grandes exigem pausas entre batches (já configurado em `rag.py`)
