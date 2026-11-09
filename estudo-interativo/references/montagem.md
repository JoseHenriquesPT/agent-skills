# Montagem

Como se constrói um estudo grande sem ele apodrecer. Este ficheiro só é preciso quando o
estudo **embute código real** ou **mostra saídas de um sistema que corre** — ou seja, nos
objetivos de nível 2 e 3. Para um estudo de nível 1 basta o `componentes.md`.

A regra que governa tudo o resto:

> **Nada do que é verificável se escreve à mão.** Código embutido extrai-se do ficheiro.
> Saídas de um sistema obtêm-se a correr o sistema. O que se escreve à mão são as
> explicações — e essas não têm como estar «desactualizadas».

---

## 1. Montar por partes

Um estudo de nível 2 chega facilmente a 200–250 KB. Não cabe bem num `Write` só, e uma
sequência de edições sobre um ficheiro enorme perde-se depressa.

Convenção, no scratchpad da sessão:

```
p1_head.html          <head>, CSS, <header> com o nav
p2_oquee.html         um ficheiro por separador
p3_fundacoes.html
...
p9_js_base.html       tabs, tema, CARDS, QS e os motores respectivos
p10_js_paineis.html   os painéis de clique
p11_js_conceitos.html a grelha de conceitos
p12_js_leitor.html    o leitor de código
p13_js_sim.html       o simulador, o glossário, e o fecho </script></body></html>
build.py              concatena, e gera o que é derivado
```

O `build.py` concatena por ordem e substitui os marcadores dos dados gerados:

```python
PARTES = ["p1_head.html", "p2_oquee.html", ...]
html = "".join((SP / p).read_text(encoding="utf-8") for p in PARTES)
# marcador de comentário HTML, porque a ilha é um <script> no corpo da página;
# para dados que vão para dentro do <script> do estudo, usa /*__NOME__*/
assert "<!--__RDSRC__-->" in html
html = html.replace("<!--__RDSRC__-->", ilha_rdsrc(REPO, NOTAS))
OUT.write_text(html, encoding="utf-8")
```

**Escreve as partes com a ferramenta `Write`, não com heredocs de bash.** Heredocs
partem-se com CSS e HTML de formas que só se descobrem quando o shell dá um erro de sintaxe
sem relação nenhuma com o problema.

Vantagem que só se nota depois: quando é preciso corrigir uma coisa em todas as partes
(acentos, um facto que mudou), corrige-se na parte e volta-se a correr o `build.py`. O
ficheiro final é sempre descartável.

---

## 2. Extrair o código, nunca transcrevê-lo

O `build.py` lê os ficheiros de origem e emite os excertos. Uma transcrição à mão é uma
citação errada à espera de acontecer.

```python
LEITORES = [
    ("decide", "src/support_assistant/pipeline/orchestrator.py", "_decide", 137, 212),
    ("run",    "src/support_assistant/pipeline/orchestrator.py", "run_pipeline", 82, 134),
]

def ilha_rdsrc(repo: pathlib.Path, notas: dict) -> str:
    dados = {}
    for chave, rel, sym, a, b in LEITORES:
        linhas = (repo / rel).read_text(encoding="utf-8").split("\n")
        excerto = linhas[a - 1 : b]
        assert len(excerto) == b - a + 1, chave
        dados[chave] = {"file": rel, "sym": sym, "first": a,
                        "src": excerto, "notes": notas[chave]}
    # `<` escapado: senão um `</script>` no código fecharia a ilha a meio.
    corpo = json.dumps(dados, ensure_ascii=False).replace("<", "\\u003c")
    return f'<script type="application/json" id="rdsrc-data">{corpo}</script>'
```

**Porquê uma ilha JSON e não um objecto JS.** Três razões, e as três apareceram na prática:
o `JSON.parse` dispensa escapes à mão; o `verificar.py --fonte` consegue lê-la com
`json.loads` e conferir cada linha contra o disco; e o `file` fica como caminho relativo à
raiz do repositório, que é o que torna essa conferência possível.

**Escolher os intervalos.** Função completa, do `def` à última linha do corpo. Um excerto
que começa a meio obriga o leitor a imaginar o contexto — que é exactamente o que o
componente existe para evitar.

**Fixar o commit.** O bloco de proveniência diz de que commit são as linhas. Sem isso,
daqui a seis meses ninguém sabe se os números ainda valem.

---

## 3. As notas escrevem-se à mão, à parte

As notas são a parte que ensina, e são a única coisa deste componente que uma pessoa
escreve. Vivem num dicionário separado no `build.py`, indexado pela mesma chave, para a
fonte poder ser regenerada sem lhes tocar.

```python
NOTAS = {
 "decide": [
   {"a": 137, "b": 150, "t": "A assinatura — e o que falta nela",
    "d": "<p>Repara no que <b>não</b> está aqui: não há <code>repository</code>…</p>"},
   {"a": 151, "b": 153, "t": "…", "d": "…"},
 ],
}
```

**Invariante que o `verificar.py` impõe:** cada linha do excerto pertence a **exactamente
uma** nota. Sem buracos — uma linha sem nota fica clicável e não abre nada — e sem
sobreposições.

Uma nota boa responde a *porquê assim*, não a *o que faz*. O que a linha faz o leitor lê na
linha; o que ele não consegue ler é a decisão que a pôs ali, a alternativa que foi
rejeitada, e o que se parte se ela mudar.

---

## 4. Dados derivados de correr o objeto

Para o simulador, e para qualquer número que apareça no estudo.

O procedimento é sempre o mesmo: um script que corre o objeto real contra os dados reais e
despeja o resultado em JSON; o `build.py` transforma esse JSON no formato do componente.
No estudo do Support Ticket foi literalmente correr o `run_pipeline` de produção com um
relógio congelado, para as dezoito combinações, e guardar os registos que saíram.

```python
# sim.py — corre o objeto, despeja o resultado
for entrada in ENTRADAS:
    resultado = correr_a_serio(entrada)
    saida[entrada] = {"passos": resultado.trace, "desfecho": resultado.status}
print(json.dumps(saida, indent=1, ensure_ascii=False))
```

**O que isto compra**, além da exactidão: descobre-se o que o sistema faz mesmo. Nesta
execução, quatro dos dezoito desfechos não eram os que se esperavam a olhar para o código,
e três detalhes do registo (contagens de literais, mensagens de erro) só se souberam assim.

Se o objeto **não** corre — um tema abstracto, documentação — este componente não se usa. O
que não se faz é inventar saídas plausíveis: um número plausível escrito à mão tem o mesmo
peso na cabeça do leitor que um verdadeiro, e é indistinguível dele até ao dia em que
falha.

---

## 5. Verificar

Cinco portas, por ordem de custo. As três primeiras são obrigatórias num estudo com código.

**1 · O verificador.** Estrutura, offline, espinha, contrato de expansão, diagramas.

```bash
python <skill>/scripts/verificar.py <area>/<tema>/estudo.html
```

Esperado: **0 erros**. Os avisos leem-se um a um — são pontos de qualidade, não regressões.

**2 · Sintaxe do JS.** Apanha a string partida a meio e o apóstrofo, que fazem a página
abrir em branco sem dizer porquê.

```bash
python -c "import re,pathlib; h=pathlib.Path('estudo.html').read_text(encoding='utf-8'); \
pathlib.Path('check.js').write_text(re.search(r'<script>(.*)</script>',h,re.S).group(1),encoding='utf-8')"
node --check check.js
```

**3 · Fidelidade dos excertos.** Confere cada linha embutida contra o ficheiro de origem, e
a cobertura das notas.

```bash
python <skill>/scripts/verificar.py <ficheiro> --fonte <raiz-do-repositorio>
```

Um excerto que não bate certo é pior do que nenhum: dá autoridade a uma citação errada.

**4 · Os avisos de acento e de geometria.** O verificador assinala português sem acento no
texto visível — o erro típico de texto gerado por script — e elementos de SVG fora do
`viewBox`, que é um diagrama cortado sem ninguém o abrir.

**5 · Teste de fumo (opcional).** Se a página *corre*: se os separadores abrem, se os
componentes renderizam, se cada linha clicável do leitor abre nota.

```bash
npm install jsdom && node <skill>/scripts/smoke.js <ficheiro>
```

---

## 6. Conferir os factos que o verificador não alcança

O verificador confirma que um excerto bate certo com o ficheiro. Não confirma que a frase
*sobre* o excerto é verdadeira. Essa parte é manual, e vale a pena fazê-la em bloco no fim:

- Nomes de testes citados — que existam mesmo, com aquele nome (`grep`).
- Contagens («onze módulos», «262 linhas», «quinze ADRs») — contar.
- Afirmações sobre o que um teste garante. Foi aqui que esta execução escorregou: uma
  afirmação de que um teste de *layering* garantia uma dependência externa, quando ele só
  analisa importações internas. Ler o teste antes de dizer o que ele impede.
