# agent-skills

Skills pessoais no formato [Agent Skills](https://agentskills.io) — o padrão aberto que o
GitHub Copilot (VS Code, CLI, app), o Claude Code, o Codex, o Cursor e outros leem.

## Instalar

Copia cada skill para uma localização que o teu harness varre:

- **personal, todos os projectos** — `~/.agents/skills/` ou `~/.copilot/skills/` (GitHub Copilot)
- **por projecto** — `.agents/skills/` ou `.github/skills/` dentro do repositório

## Skills

### estudo-interativo

Produz um ficheiro HTML interactivo e offline que ensina o funcionamento de uma coisa —
anatomia, percurso e como as peças se ligam — calibrado ao nível do leitor (narrar, mexer
ou decidir). Escrita em português de Portugal.

- **Runtime**: Python 3 (obrigatório, `scripts/verificar.py`); Node (opcional, `scripts/smoke.js`
  precisa de `npm install jsdom`).
- **Testes**: ver `estudo-interativo/tests/README.md` — o pacote traz o seu próprio alvo de
  regressão.

## Verificação antes de instalar

```bash
python estudo-interativo/scripts/verificar.py estudo-interativo/tests/fixture/estudo.html
```

Esperado: `Sem erros`.
