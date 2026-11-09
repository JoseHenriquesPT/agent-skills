# Testes do pacote

O alvo destes testes é o **próprio pacote**: o `SKILL.md`, o `template.html` e os scripts têm
de continuar a produzir estudos que passam as portas de verificação da skill (Passo 9).

## Fixture

`fixture/estudo.html` é um estudo de nível 1 escrito de propósito para exercitar cada ponto
do contrato: os sete separadores, componentes nos cinco primeiros, um diagrama SVG por
secção de mecanismo, três `<details>`, oito flashcards, cinco perguntas de quiz (uma oral),
o contrato de expansão em `Próximos níveis`, e o bloco de proveniência. **Não é um estudo de
trabalho** — é o alvo de regressão dos scripts.

## Correr

```bash
# porta 1 · estrutura, offline, espinha, contrato de expansão (obrigatória)
python ../scripts/verificar.py fixture/estudo.html

# porta 5 · a página corre mesmo (opcional: precisa de node + jsdom)
npm install jsdom   # numa pasta à parte; o smoke.js procura em ./node_modules
node ../scripts/smoke.js fixture/estudo.html
```

Esperado: **0 erros** nas duas portas.

Depois de tocar no `SKILL.md`, no `template.html` ou nos scripts, volta a correr isto antes
de considerar o pacote pronto. Se mudares o contrato (novos campos, novos mínimos),
atualiza o fixture para o representar.
