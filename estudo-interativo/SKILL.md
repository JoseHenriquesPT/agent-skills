---
name: estudo-interativo
description: "Produz um ficheiro HTML interactivo e offline (tema claro/escuro) que ensina o funcionamento de uma coisa — anatomia, percurso e como as peças se ligam — calibrado ao nível do leitor: narrar, mexer ou decidir. Usa quando o utilizador pede para explicar como algo funciona, «ensina-me X», «como funciona X», «estudo interactivo», ou para aprofundar um estudo já existente. Distinta de case-study (que decide); esta skill explica."
---

# Estudo interactivo

Produz **um ficheiro HTML** que ensina o funcionamento de uma coisa: a anatomia, o percurso,
e como as peças se ligam. Abre com duplo-clique, funciona sem rede, e tem tema claro e
escuro.

O alvo **não é fixo — é calibrado**, e é a primeira coisa a decidir:

| Nível | O leitor sai capaz de… | O que isso obriga |
|---|---|---|
| **1 · Narrar** | desenhar o diagrama e narrar o percurso de uma peça à outra | a espinha; sem código embutido |
| **2 · Mexer** | encontrar e mudar qualquer linha | + leitor de código anotado, cartões «onde mexer para…», e o teste que apanha cada erro |
| **3 · Decidir** | defender as escolhas e propor alternativas | + os trade-offs, o que foi rejeitado, e o que se perde em cada decisão |

O nível 1 é o alvo por omissão e chega para a maioria dos temas. O que os três têm em comum
é o limite: **um estudo que tenta ensinar tudo não é lido.** O que fica de fora não se
perde — vai para o separador **Próximos níveis**, que é também o que permite chamar a skill
outra vez para aprofundar.

---

## Passo 1 — Procurar antes de criar

**Nunca comeces a escrever sem procurar primeiro.** Sem este passo cada execução produz um
duplicado ligeiramente diferente do anterior, e o caminho de expansão nunca chega a ser
encontrado.

Procura no repositório de trabalho — tipicamente `DevPractice/` — por material que já cubra
este objeto. Compara pelo **objeto e pelos seus sinónimos e siglas**, não pelo slug exacto:
`RLS` ↔ `row level security`, `LLM` ↔ `large language model`, `k8s` ↔ `kubernetes`.

| O que encontras | O que fazes |
|---|---|
| Um `estudo.html` do mesmo objeto | **Não crias nada.** Vai para o [Modo expansão](#modo-expansão). |
| Material relacionado mas diferente — os `.md` que já lá estão, um estudo vizinho | Diz o que encontraste e **pergunta**: aprofundar o existente ou criar novo? Se for novo, esse material entra como **fonte** e ficam com links um para o outro. |
| Nada próximo | Cria a estrutura e segue. |

### Onde o ficheiro vive

```
<area>/<tema>/estudo.html
```

Duas camadas: a pasta de **área** nomeia o campo ou a tecnologia, a subpasta nomeia o
**objeto concreto**, em minúsculas e com hífenes.

O `DevPractice/` já tem áreas — `AI_Pratical/`, `AI_Projects/`, `AI_Theoretical/`,
`infraestrutura/`, `cybersecurity/`, `offensive-security/`, `entrevistas/`. **Escolhe de
entre as que existem** sempre que alguma sirva; uma área nova pede confirmação ao
utilizador. Os `.md` soltos que já vivem nas pastas de área não se tocam nem se movem.

(`materiais/<area>/<tema>/` foi a convenção documentada durante um tempo e continua aceite
onde já existe.)

---

## Passo 2 — Calibrar

**Duas perguntas ao utilizador, sempre, numa `AskUserQuestion`, antes de escrever fosse o
que for.** Este passo existe por uma razão específica: a execução que o introduziu tinha
falhado antes, e o diagnóstico do leitor foi *"só entendo metade do que está a ser explicado
e também não consigo ligar isso ao código"*. Um estudo tecnicamente correcto para o leitor
errado é um estudo que não é lido.

**Pergunta 1 — a partir de quê?** Do zero · a partir de *X* (a linguagem ou tecnologia que
ele já tem) · já domina a área. Não perguntes «qual é o teu nível»: pergunta o que ele já
sabe, com opções concretas ao objeto.

**Pergunta 2 — para conseguir fazer o quê?** Os três níveis da tabela lá em cima, escritos
como capacidades, não como rótulos.

As respostas mandam no resto:

| Resposta | Consequência |
|---|---|
| Do zero, ou «a partir de X» com salto grande | Nasce o separador **Fundações** (2º), com a grelha de conceitos. Tudo o que não for X explica-se do zero |
| Já domina a área | Sem Fundações; o vocabulário do domínio pode ser assumido |
| Nível 1 · Narrar | A espinha, e mais nada. Sem código embutido |
| Nível 2 · Mexer | **Obrigatórios**: leitor de código anotado (5–7 funções) e cartões «onde mexer para…», cada um com o teste que apanha o erro |
| Nível 3 · Decidir | + um separador ou uma camada de `<details>` por decisão: o que foi rejeitado e porquê |

Anota as duas respostas no bloco de proveniência. Quem reler o estudo daqui a um ano precisa
de saber para quem ele foi escrito.

---

## Passo 3 — Enquadrar o objeto

Decide o que é o objeto e corta-o à espinha. Aqui a regra da parcimónia mantém-se: faz **no
máximo uma pergunta** sobre o *recorte*, e só se duas leituras razoáveis do pedido dariam
estudos genuinamente diferentes ("Docker" — o que é um container, ou como escrever um
Dockerfile?). Fora isso, escolhe a leitura mais útil e diz qual escolheste.

Teste de delimitação: consegues escrever a frase-âncora — uma frase, sem jargão, que alguém
repete de cor depois de a ler uma vez? Se precisas de duas, o objeto é grande demais.

## Passo 4 — Recolher e verificar

Lê `references/fontes.md`. A regra é uma: **nunca escrever de memória o que tem fonte
verificável à mão.** O que é estável (o que é, que problema resolve, a intuição) escreve-se à
vontade; o que é volátil (nomes de pacotes, assinaturas, flags, defaults, limites) verifica-se
sempre. Quando não conseguires verificar alguma coisa, **di-lo no texto**.

Sobre código: lê os ficheiros, não deduzas a arquitectura pelo nome das pastas. Quando o
código contradiz o README, **o código ganha** — e essa contradição é das coisas mais
interessantes que o estudo pode mostrar.

### Política de citação

Esta regra nasceu de um estudo que citava `orchestrator.py:228` sem nunca mostrar essas
linhas — e cujo número já estava errado no commit seguinte.

- Números de linha **só dentro de blocos de código embutidos**, onde são auto-consistentes
  porque vêm do ficheiro.
- Em prosa, âncora por **ficheiro + símbolo**: `orchestrator.py · _decide`, nunca `:205`.
- O bloco de proveniência **fixa o commit** e diz que as linhas embutidas são desse commit.

Uma citação que aponta para código sem o mostrar não é verificável pelo leitor — é só um
número que ele tem de acreditar. Se vale a pena apontar, vale a pena embutir.

## Passo 5 — Mapear a espinha

A espinha são sete separadores fixos. Fixá-la é o que torna "perceber o básico" um alvo
verificável em vez de uma sensação, e é o que faz dois estudos diferentes serem navegáveis
da mesma maneira.

| # | Separador | O que responde |
|---|---|---|
| 1 | **O que é** | Para que serve isto, para alguém que nunca ouviu o termo. Analogia primeiro, termo depois. |
| 2 | **Anatomia** | De que peças é feito, e como se chamam. |
| 3 | **Como funciona** | O percurso: o que entra, o que acontece, o que sai. |
| 4 | **Como se liga** | Onde encaixa no resto do mundo; os vizinhos e as fronteiras. |
| 5 | **Confusões** | Os quase-iguais: X vs Y, e o que separa mesmo os dois. |
| 6 | **Auto-avaliação** | Flashcards e quiz. |
| 7 | **Próximos níveis** | O que ficou por dizer, e o que cada coisa destranca. |

**Separadores extra são permitidos**, e entram sempre antes de *Auto-avaliação*. O
`verificar.py` aceita-os desde que os 7 ids da espinha existam com botão no nav e haja
exactamente um `class="on"`. O caso previsto é o **`fundacoes`**, em 2º lugar, quando a
calibração revelou um salto de nível.

Os `<h2>` de 1 a 5 usam o vocabulário do próprio objeto, não a etiqueta genérica: "Anatomia
de uma policy", não "Anatomia". Os botões do nav ficam como estão — são a navegação, e
mantê-los estáveis é o que faz os estudos parecerem uma coleção.

O separador **Confusões** é o mais subestimado. Costuma ser o atalho de cinco minutos para
quem chega: a maior parte da confusão real não é sobre o que uma coisa é, é sobre em que
difere daquela outra parecida.

## Passo 6 — Escrever

As regras estão em [Regras de escrita](#regras-de-escrita), mais abaixo. Lê-as antes de
começar a produzir texto — são a parte da skill que determina a qualidade do resultado.

## Passo 7 — Montar

Copia `assets/template.html` para o destino e preenche os slots `{{...}}`. O CSS e o JS de
tabs, tema, flashcards, quiz e gaveta de glossário **já lá estão** — não os reescrevas.

Consulta `references/componentes.md` para escolher os componentes e `references/diagramas.md`
para os SVG. Para um estudo de nível 2 ou 3, lê também `references/montagem.md`: montagem
por partes, extracção do código real, e dados derivados de correr o objeto.

**Um separador só com prosa falhou.** Cada um dos cinco primeiros **abre** com uma coisa que
o leitor possa clicar, percorrer ou abrir. É isso que separa isto de um documento — e é
metade da razão pela qual o formato é HTML e não markdown.

### Que componente, quando

| Separador | Escolha natural |
|---|---|
| O que é | frase-âncora + toggle A/B (o mau contra o bom), ou o objeto real anotado |
| Fundações | **grelha de conceitos** (§15) |
| Anatomia | mapa SVG clicável, ou anatomia clicável sobre código/config real |
| Como funciona | **leitor de código anotado** (§14) e/ou **simulador** (§16); percurso passo a passo se não houver código |
| Como se liga | SVG de camadas + `.layer`, e **cartões «onde mexer para…»** (§17) no nível 2 |
| Confusões | tabelas `cmp` + um toggle A/B para o par mais consequente |

E, transversal a todos: a **gaveta de glossário** (§18) quando houver mais de ~30 termos —
já está no template, é só preencher o array.

## Passo 8 — Auto-avaliação e Próximos níveis

Mínimo 8 flashcards e 5 perguntas de quiz, das quais pelo menos uma `oral`. Num estudo de
nível 2, pelo menos **duas** perguntas do tipo *«onde é que mexias para…»* — é a forma da
pergunta que uma revisão de código faz.

A pergunta falada não é um extra. Reconhecer a resposta certa entre quatro é muito mais fácil
do que produzi-la — a pergunta `oral` é a que apanha o modelo mental incompleto, e é o
formato mais próximo de ter de explicar a coisa a outra pessoa.

**O backlog de Próximos níveis não se escreve no fim: colhe-se.** Cada vez que, no passo 6,
empurraste um detalhe para fora, esse detalhe é um item candidato. Por isso este separador
sai naturalmente bem se o limite de profundidade foi respeitado, e sai vazio ou inventado se
não foi — o que é, em si, um sinal útil.

Cada item leva `data-nivel` (`intermedio` ou `avancado`), um `data-slug` único, `data-feito`,
e a linha **Destranca:** que diz o que a pessoa passa a conseguir fazer. A forma exacta está
em `references/componentes.md`, secção 13.

## Passo 9 — Verificar

Cinco portas, por ordem de custo. As três primeiras são obrigatórias num estudo com código
embutido; a primeira é obrigatória sempre.

```bash
# 1 · estrutura, offline, espinha, contrato de expansão, diagramas
python <skill>/scripts/verificar.py <area>/<tema>/estudo.html

# 2 · sintaxe do JS — apanha a string partida a meio e o apóstrofo
node --check <script extraído>

# 3 · fidelidade dos excertos contra o repositório de origem
python <skill>/scripts/verificar.py <ficheiro> --fonte <raiz-do-repo>

# 5 · a página corre mesmo (opcional: precisa de node + npm install jsdom)
node <skill>/scripts/smoke.js <ficheiro>
```

Esperado: **0 erros**. A porta 4 é ler os avisos — não fazem falhar, mas cada um é um ponto
a olhar: português sem acento no texto visível, elementos de SVG fora do `viewBox`, um
separador que abre com prosa, uma citação com número de linha. O `montagem.md` tem os
comandos completos e explica o que cada porta apanha.

Corrige e volta a correr. Depois diz ao utilizador o caminho do ficheiro e sugere um ou dois
itens do backlog que valha a pena aprofundar a seguir.

---

## Modo expansão

Quando o passo 1 encontra um `estudo.html` do mesmo objeto, ou quando o utilizador pede para
aprofundar:

1. **Lê o ficheiro** e extrai os itens de `<div class="nivel">` — slug, nível, título, descrição.
2. **Mostra o backlog** ao utilizador e pergunta o que quer aprofundar, a não ser que ele já
   tenha dito. Se ele pedir um tema que não está no backlog, aceita — o backlog é uma
   proposta, não um menu fechado.
3. **Escreve o separador novo**, com o mesmo cuidado dos outros: um `<h2>` no vocabulário do
   objeto, a abrir com um componente, e `<details>` para o que aprofunda. Entra no nav
   **antes** de Auto-avaliação.
4. **Acrescenta 2 a 4 flashcards e 1 a 2 perguntas** ao `CARDS` e ao `QS` sobre o que
   acabaste de escrever. Um separador novo sem avaliação nova fica por verificar.
5. **Marca o item** com `data-feito="sim"` — não o apagues. Um backlog que mostra o que já foi
   coberto é um mapa de progresso; um que só mostra o que falta perde essa informação.
6. **Recalcula o backlog**: o separador novo abriu portas que antes não faziam sentido.
7. Corre as portas de verificação do Passo 9.

A expansão é **aditiva**. Não reescrevas separadores existentes sem o utilizador pedir — ele
pode ter anotado ou editado o ficheiro à mão, e uma reescrita silenciosa apaga esse trabalho.
Se um separador antigo estiver mesmo errado, diz qual e porquê, e pergunta.

**Reescrita** (quando o utilizador pede mesmo) é outra coisa: aí vale a pena voltar ao Passo
2 e recalibrar, porque a razão mais provável para uma reescrita ser precisa é o estudo ter
sido escrito para um leitor diferente daquele que o vai ler.

---

## Regras de escrita

### Profundidade — o teste do modelo mental

Perante cada detalhe que apetece acrescentar, pergunta: **remover isto parte o modelo mental
do leitor?**

Se parte, fica. Se não parte, **não se corta — migra** para Próximos níveis, com uma linha a
dizer o que destranca. É esta migração que faz o limite de profundidade produzir uma coisa
útil em vez de só produzir omissões.

O outro teste, aplicado à frase: se uma frase só faz sentido para quem já sabe o tema, ou é
reescrita, ou o termo que ela usa merece um cartão na grelha de conceitos.

### Cada separador abre com um componente

Nunca com prosa. Um `<p class="lead">` de uma linha conta como legenda do componente que vem
a seguir — «Clica em qualquer conceito» — e não como prosa. As explicações longas vivem
**dentro** dos painéis de clique, não no HTML corrido: é isso que mantém um ficheiro de 250
KB navegável em vez de cansativo.

### Língua

Prosa em **português de Portugal**: `ficheiro`, `utilizador`, `ecrã`, `a correr` (nunca
`arquivo`, `usuário`, `tela`, `rodando`). Trata o leitor por **tu**.

Termos e identificadores técnicos ficam em **inglês** e nunca se traduzem: *policy*, *tool
use*, *middleware*, *garbage collector*, `SELECT`, `useEffect`. Traduzir um termo técnico
tira ao leitor a palavra que ele precisa de reconhecer na documentação e numa conversa.

A primeira ocorrência de cada termo leva uma glosa de uma linha — inline, ou num
`.t[data-tip]`, ou uma entrada na gaveta de glossário.

**Escreve com acentos, sempre, inclusive dentro de strings de JS e de texto gerado por
script.** É aí que eles se perdem, e o `verificar.py` avisa quando isso acontece. As únicas
excepções são os valores de contrato lidos por regex — `data-nivel="avancado"`,
`data-feito="nao"`, `data-slug` — que são identificadores, não prosa.

### Analogias

Usa-as quando o conceito não tem paralelo nenhum na experiência do leitor. Mas **toda a
analogia declara onde parte**, no `.quebra`.

Isto não é escrúpulo. Uma analogia sem limite declarado produz um modelo mental confiante e
errado, e o leitor só descobre isso muito mais tarde, normalmente a debugar. A analogia com o
ponto de rutura ensina duas coisas de uma vez: a intuição, e a fronteira dela.

### Secções expansíveis

O corpo do texto carrega o **modelo mental**. O `<details>` carrega o **porquê**, a prova, o
caso-limite, o número exacto.

O teste: quem fechar todos os `<details>` tem de sair com um modelo correcto, ainda que
grosseiro. Se um `<details>` contém algo sem o qual a frase de fora deixa de fazer sentido,
esse conteúdo está no sítio errado — o `<details>` não é um esconderijo para conteúdo
essencial que não coube.

O `summary` diz o que lá está dentro. `Porque é que é uma B-tree e não uma hash table?` é
bom; `Mais detalhes` é inútil, porque o leitor não tem como decidir se lhe interessa abrir.

### Proveniência

O ficheiro fecha com o bloco `{{PROVENIENCIA}}`: quando foi escrito, **para quem** (as duas
respostas da calibração), de onde veio o conteúdo, **de que commit** são as linhas embutidas,
e o que não foi verificado. Quem ler isto daqui a um ano precisa de saber o que ainda pode
confiar.

---

## Ficheiros da skill

| Ficheiro | Quando o ler |
|---|---|
| `assets/template.html` | Sempre, no passo 7. É a base do ficheiro. |
| `references/componentes.md` | Passo 7 — que componente usar e o HTML/JS de cada um. Os 14–18 são de estudo de código. |
| `references/diagramas.md` | Passo 7, ao fazer SVG. Mermaid não serve: não renderiza offline. |
| `references/montagem.md` | Passo 7, em estudos de nível 2 ou 3 — montar por partes, extrair código real, derivar dados, e as cinco portas de verificação. |
| `references/fontes.md` | Passo 4 — como recolher e verificar por tipo de fonte. |
| `scripts/verificar.py` | Passo 9, e outra vez depois de corrigir. `--fonte` confere os excertos. |
| `scripts/smoke.js` | Passo 9, porta 5. Opcional: precisa de `npm install jsdom`. |
