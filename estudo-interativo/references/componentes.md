# Componentes

Catálogo do que existe em `assets/template.html`. O CSS de tudo isto **já lá está** — só
precisas de colar o HTML no slot certo. O JS que não está no template vem indicado por
componente; junta-o em `{{JS_EXTRA}}`.

Regra geral: um separador só com prosa falhou. Cada separador deve ter pelo menos uma coisa
que o leitor possa **clicar, percorrer ou abrir** — é isso que separa isto de um documento.

## Índice

| # | Componente | Usa quando |
|---|---|---|
| 1 | Frase-âncora | Abrir o separador "O que é" |
| 2 | Analogia | O conceito não tem paralelo no dia-a-dia do leitor |
| 3 | Details | Há um porquê/prova/caso-limite que não cabe no fio principal |
| 4 | Glosa inline | Um termo técnico precisa de uma linha, sem partir a frase |
| 5 | Anatomia clicável | O objeto tem peças nomeáveis num bloco de código/config |
| 6 | Percurso passo a passo | Há uma sequência temporal: pedido → ... → resposta |
| 7 | Camadas | Uma lista de N itens em que cada um tem detalhe próprio |
| 8 | Tabela de comparação | X vs Y vs Z sobre os mesmos eixos |
| 9 | Toggle A/B | "Assim é mau / assim é bom", lado a lado |
| 10 | Nota | Um aviso ou observação lateral |
| 11 | Flashcards | Sempre — separador Auto-avaliação |
| 12 | Quiz | Sempre — separador Auto-avaliação |
| 13 | Próximos níveis | Sempre — é o contrato de expansão |
| 14 | **Leitor de código anotado** | O objeto é código real e o objetivo é o nível 2 |
| 15 | **Grelha de conceitos** | A calibração revelou um salto de nível — é o separador Fundações |
| 16 | **Simulador de cenários reais** | O objeto corre e produz saídas diferentes conforme a entrada |
| 17 | **Cartões «onde mexer para…»** | Objetivo nível 2: o leitor tem de saber alterar |
| 18 | **Gaveta de glossário** | Mais de ~30 termos a reter |

Os 1–13 servem qualquer objeto. Os **14–18 são de estudo de código** e existem para fechar
a distância entre a explicação e o repositório — ver a secção própria mais abaixo.

---

## 1. Frase-âncora

Slot `{{EM_UMA_FRASE}}`. Uma frase, sem jargão, que alguém consegue repetir de cor depois de
ler uma vez. Se precisares de duas, o objeto de estudo está mal delimitado — volta ao passo 3
do `SKILL.md` (Enquadrar o objeto).

```html
<div class="emuma"><span class="lb">Em uma frase</span>
  Um <b>index</b> é uma segunda cópia dos teus dados, ordenada por uma coluna à escolha,
  que a base de dados consulta para não ter de ler a tabela toda.
</div>
```

## 2. Analogia

A `.quebra` não é opcional. Uma analogia sem limite declarado produz um modelo mental
confiante e errado, e o leitor só descobre isso muito mais tarde — normalmente a debugar.

```html
<div class="analog">
  <div class="ah">Analogia</div>
  <p>Um index é o índice remissivo no fim de um livro. Em vez de folheares as 600 páginas
     à procura de «mitocôndria», vais ao índice, que está por ordem alfabética, e ele
     diz-te: página 143.</p>
  <div class="quebra"><b>Onde a analogia parte:</b> o índice do livro é escrito uma vez e
    nunca mais muda. Um index de base de dados tem de ser reescrito a cada
    <code>INSERT</code> — é por isso que ter index a mais torna as escritas lentas,
    uma coisa que a imagem do livro não deixa ver.</div>
</div>
```

## 3. Details (aprofundamento)

**O contrato:** o corpo do texto carrega o modelo mental; o `<details>` carrega o *porquê*,
a prova ou o caso-limite. Quem fechar todos os `<details>` tem de sair com um modelo
correto, ainda que grosseiro. Se um `<details>` contém algo sem o qual a frase de fora
deixa de fazer sentido, esse conteúdo está no sítio errado.

O `summary` diz o que lá está dentro, não convida vagamente. `Porque é que é uma B-tree e
não uma hash table?` é bom; `Mais detalhes` é inútil — o leitor não tem como decidir se
lhe interessa abrir.

```html
<details class="mais">
  <summary>Porque é que a estrutura é uma B-tree e não uma hash table?</summary>
  <div class="corpo">
    <p>Uma hash table encontra <code>id = 42</code> mais depressa. Mas não sabe responder a
       <code>id BETWEEN 10 AND 90</code>, porque o hash destrói a ordem de propósito.</p>
    <p>A B-tree mantém as chaves ordenadas, por isso serve os dois casos: o valor exato e o
       intervalo. Como intervalos e <code>ORDER BY</code> são a maioria das consultas reais,
       é o que vem por omissão em praticamente todas as bases de dados.</p>
  </div>
</details>
```

## 4. Glosa inline

Para a primeira ocorrência de um termo que não merece um parágrafo. O `data-tip` é texto
puro — sem HTML e sem aspas duplas lá dentro.

```html
Cada linha guarda o seu <span class="t" data-tip="Identificador da versão de uma linha.
O Postgres usa-o para saber que versões cada transação pode ver.">xmin</span>.
```

## 5. Anatomia clicável

O componente mais forte do separador **Anatomia**: um bloco de código/config real à
esquerda, um painel que muda à direita. O leitor lê o objeto verdadeiro em vez de uma lista
de bullets sobre ele.

```html
<div class="anat">
  <div class="codebox" id="jsondef"><span class="jn">CREATE POLICY</span> <span class="hot" data-k="nome">"users_select_own"</span>
  <span class="jn">ON</span> <span class="hot" data-k="tabela">profiles</span>
  <span class="jn">FOR</span> <span class="hot" data-k="cmd">SELECT</span>
  <span class="jn">USING</span> (<span class="hot" data-k="using">auth.uid() = user_id</span>);</div>
  <div class="panel" id="apanel">
    <div class="ttl">Clica numa peça</div>
    <p class="hint2">Cada parte destacada tem uma função diferente.</p>
  </div>
</div>
```

JS para `{{JS_EXTRA}}` — os campos de `FIELDS` aceitam HTML:

```js
const FIELDS={
 nome:{t:'nome da policy',f:[
   ['O que é','Só uma etiqueta. Serve para a apagares depois com <code>DROP POLICY</code>.'],
   ['Armadilha','Não é único por base de dados, é único <b>por tabela</b>.']
 ]},
 cmd:{t:'FOR SELECT',f:[
   ['O que é','A que operação a regra se aplica: <code>SELECT</code>, <code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code> ou <code>ALL</code>.'],
   ['Consequência','Uma policy só de <code>SELECT</code> deixa a tabela sem regra de escrita — e sem regra, com RLS ligado, a escrita é <b>negada</b>.']
 ]}
};
const ap=document.getElementById('apanel');
document.querySelectorAll('#jsondef .hot').forEach(h=>{
  h.addEventListener('click',()=>{
    document.querySelectorAll('#jsondef .hot').forEach(x=>x.classList.remove('sel'));
    h.classList.add('sel');
    const d=FIELDS[h.dataset.k]; if(!d)return;
    ap.innerHTML='<div class="ttl">'+d.t+'</div><dl class="fields">'+
      d.f.map(([k,v])=>'<div class="fld"><dt>'+k+'</dt><dd>'+v+'</dd></div>').join('')+'</dl>';
  });
});
```

## 6. Percurso passo a passo

O componente do separador **Como funciona**. Mostra o mesmo objeto a transformar-se ao longo
dos passos — é a diferença entre listar etapas e ver a coisa acontecer.

```html
<div class="hopbar" id="hops"></div>
<div class="hopgrid">
  <div class="jsonbox" id="hopstate"></div>
  <div class="side" id="hopside"></div>
</div>
<div class="navbtns">
  <button id="hprev">← Anterior</button><button id="hnext">Seguinte →</button>
  <span class="ind" id="hind"></span>
</div>
```

```js
const HOPS=[
 {n:'pedido', t:'O cliente faz a query', who:'SELECT * FROM profiles;',
  p:'<p>Ainda não há filtro nenhum. O cliente pede a tabela toda, e acha que a vai receber toda.</p>',
  st:'sessao: role=authenticated\nauth.uid() = "u_8813"\nquery: SELECT * FROM profiles'},
 {n:'reescrita', t:'O Postgres reescreve a query', who:'+ WHERE auth.uid() = user_id',
  p:'<p>Aqui está o truque todo: a policy não é verificada <i>depois</i>, é <b>colada à query</b> antes de correr. O planeador vê uma query diferente daquela que foi enviada.</p>',
  st:'sessao: role=authenticated\nauth.uid() = "u_8813"\nquery: SELECT * FROM profiles\n       WHERE auth.uid() = user_id   <- acrescentado pelo RLS'}
];
let hi=0;
function pintaHop(){
  const h=HOPS[hi];
  document.getElementById('hops').innerHTML=HOPS.map((x,i)=>
    '<button class="'+(i===hi?'on':'')+'" data-i="'+i+'">'+x.n+'</button>').join('');
  document.getElementById('hops').querySelectorAll('button').forEach(b=>
    b.addEventListener('click',()=>{hi=+b.dataset.i;pintaHop()}));
  document.getElementById('hopstate').textContent=h.st;
  document.getElementById('hopside').innerHTML=
    '<div class="hnum">Passo '+(hi+1)+' de '+HOPS.length+'</div><h4>'+h.t+'</h4>'+
    '<div class="who">'+h.who+'</div>'+h.p;
  document.getElementById('hind').textContent=(hi+1)+' / '+HOPS.length;
  document.getElementById('hprev').disabled=hi===0;
  document.getElementById('hnext').disabled=hi===HOPS.length-1;
}
document.getElementById('hprev').addEventListener('click',()=>{if(hi>0){hi--;pintaHop()}});
document.getElementById('hnext').addEventListener('click',()=>{if(hi<HOPS.length-1){hi++;pintaHop()}});
pintaHop();
```

## 7. Camadas

Lista em que cada item abre com um clique. O JS já está no template. O `.badge` é opcional —
usa-o quando os itens se dividem em duas naturezas que vale a pena marcar (imposto vs
convenção, obrigatório vs opcional).

```html
<div class="layers">
  <div class="layer">
    <div class="n">1</div>
    <div>
      <div class="ttl2">Autenticação</div>
      <div class="sub2">quem és tu</div>
    </div>
    <span class="badge hard">imposto</span>
    <div class="exp">Verifica o JWT e põe o <code>sub</code> em <code>auth.uid()</code>.
      Sem isto, tudo o que vem a seguir não tem sobre o que decidir.</div>
  </div>
</div>
```

## 8. Tabela de comparação

Uma linha por item, uma coluna por eixo. Os eixos têm de ser os **mesmos** para todos os
itens — se um item precisa de um eixo próprio, não pertence à tabela.

```html
<table class="cmp">
  <tr><th>Mecanismo</th><th>Onde corre</th><th>Falha como</th></tr>
  <tr><td>RLS</td><td>dentro do Postgres</td><td>devolve 0 linhas, sem erro</td></tr>
  <tr><td>Middleware</td><td>no servidor, antes da query</td><td>devolve 403</td></tr>
</table>
```

## 9. Toggle A/B

Para o contraste direto entre uma versão fraca e uma forte.

```html
<div class="ab">
  <div class="abtabs">
    <button class="on" data-ab="mau">Sem RLS</button>
    <button data-ab="bom">Com RLS</button>
  </div>
  <div class="abbox" id="abtext"></div>
  <div id="abwhy"></div>
</div>
```

```js
const AB={
 mau:{txt:'SELECT * FROM profiles;   -- devolve 40 000 linhas',
      why:'<p>A tabela inteira. A segurança depende de <b>toda</b> a query da aplicação estar certa, para sempre.</p>'},
 bom:{txt:'SELECT * FROM profiles;   -- devolve 1 linha',
      why:'<p>A mesma query. A regra passou a viver na base de dados, por isso vale também para o cliente novo que alguém escreva amanhã.</p>'}
};
function drawAB(k){
  document.getElementById('abtext').textContent=AB[k].txt;
  document.getElementById('abwhy').innerHTML=AB[k].why;
}
document.querySelectorAll('.abtabs button').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.abtabs button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); drawAB(b.dataset.ab);
}));
drawAB('mau');
```

## 10. Nota

```html
<div class="note"><b>Atenção:</b> o RLS é ignorado pelo dono da tabela e por qualquer role
com <code>BYPASSRLS</code> — a <code>service_role</code> do Supabase é uma dessas.</div>
```

## 11. Flashcards (dados)

Vão para `{{DADOS_FLASHCARDS}}`. Mínimo 8. Aceitam HTML nos dois lados.

**A frente é uma pergunta, não um título.** «Index» não é um flashcard; «Porque é que um
index acelera as leituras e trava as escritas?» é. Um cartão cuja frente é um substantivo
solto testa reconhecimento, e reconhecimento não é o que precisas de conseguir fazer numa
conversa.

**O verso cabe em duas ou três linhas.** Se não cabe, a pergunta é grande demais — parte-a
em dois cartões, ou passa-a ao quiz como pergunta falada.

```js
{f:'O que é que o RLS acrescenta a uma query, mecanicamente?',
 v:'Um <code>WHERE</code>. A policy é <b>colada à query</b> antes de o planeador a ver — não é uma verificação feita depois.'},
{f:'RLS ligado numa tabela, zero policies escritas. Quem vê o quê?',
 v:'Ninguém vê nada. Sem policy não há permissão nenhuma: o default é <b>negar</b>.'},
```

## 12. Quiz (dados)

Vão para `{{DADOS_QUIZ}}`. Mínimo 5, e pelo menos uma `oral`.

As perguntas `mc` testam o **mecanismo**, não vocabulário. A boa pergunta descreve uma
situação e pergunta o que acontece; a má pergunta é «o que significa a sigla X». As opções
erradas devem ser coisas que alguém acreditaria mesmo — uma opção absurda não testa nada e
denuncia a resposta certa.

O campo `e` explica **porquê**, mesmo para quem acertou. É a parte que ensina.

A pergunta `oral` existe porque explicar em voz alta é o teste que apanha o modelo mental
incompleto — reconhecer a resposta certa entre quatro é muito mais fácil do que produzi-la.

```js
{k:'mc',q:'Ligas RLS numa tabela em produção e não escreves nenhuma policy. O que acontece às queries da app?',
 o:['Continuam iguais — o RLS só conta quando há policies',
    'Passam a devolver zero linhas, sem erro nenhum',
    'Rebentam com um erro de permissão',
    'Só as escritas são bloqueadas'],a:1,
 e:'Sem policy não há permissão. E o modo de falha é o traiçoeiro: a query <b>não dá erro</b>, devolve um conjunto vazio. A app parece funcionar e mostra uma lista vazia.'},
{k:'oral',q:'Explica em voz alta: porque é que o RLS é uma decisão de arquitetura e não só uma funcionalidade de segurança.',
 h:'Diz primeiro onde a regra passa a viver. Depois o que isso muda para quem escrever o próximo cliente.',
 m:'<p>"Sem RLS, a regra de quem-vê-o-quê vive na aplicação, e portanto vive em <b>todos</b> os sítios que falam com a base de dados."</p><p>"Com RLS, a regra desce para a base de dados e passa a haver um só sítio onde ela existe."</p>'}
```

## 13. Próximos níveis

Vai para `{{CONTEUDO_NIVEIS}}`. **É o contrato de expansão** — o `data-nivel` e o `data-slug`
são lidos por uma execução futura da skill, por isso a forma importa.

- `data-nivel` — `intermedio` ou `avancado`, sem acentos.
- `data-slug` — kebab-case, único no ficheiro. É o identificador do item.
- `data-feito` — `nao` por omissão. Passa a `sim` quando o item vira separador.

A `.destranca` responde a *porquê é que isto vale o teu tempo*. Sem ela o backlog é uma lista
de palavras e o leitor não tem como escolher o que estudar a seguir.

```html
<div class="nivel" data-nivel="intermedio" data-slug="policies-de-escrita" data-feito="nao">
  <div class="nh">
    <span class="tagn intermedio">Intermédio</span>
    <span class="nt">USING vs WITH CHECK</span>
  </div>
  <div class="nd">O <code>USING</code> filtra o que já lá está; o <code>WITH CHECK</code>
    valida o que está a entrar. Escrever só o primeiro deixa a porta aberta a alguém
    inserir uma linha em nome de outro utilizador.</div>
  <div class="destranca"><b>Destranca:</b> escreveres policies de escrita
    (<code>INSERT</code>/<code>UPDATE</code>) sem abrir buracos — que é onde quase todos os
    erros reais de RLS acontecem.</div>
</div>
```

---

# Componentes de estudo de código

Os cinco que se seguem nasceram do estudo do `Support_Ticket_assistant`, onde o problema
não era o leitor não perceber o tema — era ele não conseguir **ligar a explicação ao
código**. São os componentes que fecham essa distância. O [`montagem.md`](montagem.md)
explica como gerar os dados deles a partir do repositório real.

## 14. Leitor de código anotado

**O componente mais forte para um estudo de repositório, e a resposta à pergunta que a
citação não responde: «mostra-me».** Fonte real, numerada, com intervalos de linhas
clicáveis que abrem uma nota ao lado.

Antes disto, a única forma de apontar para código era escrever `orchestrator.py:228` —
que não mostra nada e apodrece ao primeiro refactor. Um leitor anotado mostra as linhas, e
os números que ele exibe são auto-consistentes porque vêm do ficheiro.

**A fonte nunca se transcreve à mão.** É extraída do ficheiro por um script e embutida
numa ilha JSON, que o `verificar.py --fonte` volta a conferir linha a linha:

```html
<script type="application/json" id="rdsrc-data">{
 "decide": {
   "file": "src/support_assistant/pipeline/orchestrator.py",
   "sym": "_decide",
   "first": 137,
   "src": ["def _decide(", "    ticket: Ticket,", "..."],
   "notes": [
     {"a":137,"b":150,"t":"A assinatura — e o que falta nela",
      "d":"<p>Repara no que <b>não</b> está aqui: não há parâmetro <code>repository</code>.</p>"}
   ]
 }
}</script>
```

Regras do formato, e cada uma existe por uma razão:

- `file` é o caminho **relativo à raiz do repositório**. É o que permite a conferência
  automática. Ao mostrar, o cabeçalho junta `file · sym`.
- `first` é o número da primeira linha no ficheiro real. Todos os outros são derivados
  dele, portanto não podem divergir entre si.
- As `notes` cobrem o excerto **todo**, sem buracos e sem sobreposições. O `verificar.py`
  dá erro se falharem: uma linha sem nota fica clicável e não abre nada.
- `d` é HTML. Aqui é que vive a explicação longa — não no corpo da página.

```html
<div class="rdbar" id="rdbar"></div>
<div class="rdhead" id="rdhead"></div>
<div class="rdgrid">
  <div class="rdsrc" id="rdsrc"></div>
  <div><div class="rdnote" id="rdnote"></div></div>
</div>
```

```js
const RDSRC=JSON.parse(document.getElementById('rdsrc-data').textContent);
(function(){
  const bar=document.getElementById('rdbar'), head=document.getElementById('rdhead'),
        box=document.getElementById('rdsrc'), note=document.getElementById('rdnote');
  const keys=Object.keys(RDSRC);
  let cur=keys[0], sel=0;
  const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const noteAt=n=>(RDSRC[cur].notes||[]).findIndex(x=>n>=x.a&&n<=x.b);
  function pinta(){
    const r=RDSRC[cur], ns=r.notes||[];
    bar.innerHTML=keys.map(k=>'<button data-r="'+k+'"'+(k===cur?' class="on"':'')+'>'+
      RDSRC[k].sym+'</button>').join('');
    bar.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
      cur=b.dataset.r; sel=0; pinta();}));
    head.innerHTML='<b>'+r.file+' · '+r.sym+'</b> &nbsp; linhas '+r.first+'–'+
      (r.first+r.src.length-1);
    box.innerHTML='<div class="code">'+r.src.map((ln,i)=>{
      const n=r.first+i, ni=noteAt(n);
      return '<span class="l'+(ni>=0?' c':'')+(ni===sel&&ni>=0?' sel':'')+
        '" data-ln="'+n+'"><span class="n">'+n+'</span>'+esc(ln)+'</span>';
    }).join('')+'</div>';
    box.querySelectorAll('.l.c').forEach(l=>l.addEventListener('click',()=>{
      const ni=noteAt(+l.dataset.ln); if(ni>=0){sel=ni;pinta();}}));
    const n=ns[sel];
    note.innerHTML=n?('<div class="rt">'+n.t+'</div><div class="rr">linhas '+n.a+'–'+n.b+
      '</div><div class="rb">'+n.d+'</div><div class="rdnav">'+
      '<button id="rdprev">← Bloco anterior</button><button id="rdnext">Bloco seguinte →</button>'+
      '<span class="ind">'+(sel+1)+' / '+ns.length+'</span></div>'):'<div class="rt">Sem nota</div>';
    if(!n)return;
    const p=document.getElementById('rdprev'), x=document.getElementById('rdnext');
    p.disabled=sel===0; x.disabled=sel===ns.length-1;
    p.addEventListener('click',()=>{if(sel>0){sel--;pinta();}});
    x.addEventListener('click',()=>{if(sel<ns.length-1){sel++;pinta();}});
  }
  pinta();
})();
```

**Quantos.** Cinco a sete funções. São os caminhos-chave, anotados por inteiro; o resto do
repositório cita-se por ficheiro + símbolo. Anotar tudo não é um estudo, é uma segunda
cópia do código.

**Escolher quais.** As funções onde o leitor teria de tomar uma decisão se lhe pedissem
para mudar alguma coisa. No estudo do Support Ticket foram: o orquestrador (as duas
metades), o cliente falso, o verificador, a projecção de factos, e o despacho de tools.

## 15. Grelha de conceitos

O miolo do separador **Fundações**. Cartões clicáveis agrupados por família, cada um a
abrir um painel.

**Cada conceito responde sempre a três coisas, nunca a duas:**

| Campo | O que responde |
|---|---|
| O que é | a definição, para quem nunca ouviu o termo |
| Porque aqui | porque é que **este** objeto o usa, e o que se perderia sem ele |
| No código | onde está, por ficheiro + símbolo |

A terceira é a que faz o trabalho. Sem ela isto é um manual de linguagem, e um manual de
linguagem não ajuda ninguém a ler *este* repositório.

```html
<div id="cgrids"></div>
<div class="panel" id="cpanel"><div class="ttl">Escolhe um conceito</div></div>
```

```js
const CONC=[
 {g:'Python deste repositório', items:[
   {k:'protocol',t:'typing.Protocol',s:'contrato sem herança',f:[
     ['O que é','Qualquer classe com estes métodos serve — não é preciso herdar nada.'],
     ['Porque aqui','O orquestrador depende de três protocolos e de nenhuma classe concreta.'],
     ['No código','<code>llm/protocol.py · LLMClient</code>, <code>clock.py · Clock</code>.']]}
 ]}
];
(function(){
  const wrap=document.getElementById('cgrids'), cp=document.getElementById('cpanel'), ix={};
  wrap.innerHTML=CONC.map(g=>'<div class="cgroup"><div class="cglbl">'+g.g+
    '</div><div class="cgrid">'+g.items.map(it=>{ix[it.k]=it;
      return '<div class="cg" data-c="'+it.k+'"><div class="cgt">'+it.t+
             '</div><div class="cgs">'+it.s+'</div></div>';}).join('')+'</div></div>').join('');
  wrap.querySelectorAll('.cg').forEach(c=>c.addEventListener('click',()=>{
    wrap.querySelectorAll('.cg').forEach(x=>x.classList.remove('sel'));
    c.classList.add('sel');
    const d=ix[c.dataset.c];
    cp.innerHTML='<div class="ttl">'+d.t+'</div><dl class="fields">'+
      d.f.map(([k,v])=>'<div class="fld"><dt>'+k+'</dt><dd>'+v+'</dd></div>').join('')+'</dl>';
  }));
})();
```

**Quantos.** Entre 20 e 35, em quatro ou cinco grupos. Menos do que isso e o separador não
cobre o salto; muito mais e ninguém o percorre. O `s` (subtítulo do cartão) é o que
permite escolher sem abrir — escreve-o como uma pista, não como uma repetição do título.

## 16. Simulador de cenários reais

Para objetos que **correm** e produzem saídas diferentes conforme a entrada. O leitor
escolhe as entradas e vê o percurso todo: o que foi decidido, o que se acumulou, o que
saiu.

**A regra que dá valor a isto: os desfechos são derivados, não inventados.** Correr o
objeto real contra os dados reais, despejar o resultado, e alimentar o componente com
isso. Um simulador com números plausíveis escritos à mão é pior do que não ter simulador —
parece autoridade e não é.

```html
<div class="simctl">
  <div class="simbox"><div class="sl">Entrada</div><div class="simopts" id="simu"></div></div>
  <div class="simbox"><div class="sl">Variante</div><div class="simopts" id="simk"></div></div>
</div>
<div class="simres" id="simout"></div>
<div class="simcard" id="simfinal"></div>
```

```js
/* SIM["<entrada>|<variante>"] = {passos:[{txt,bad,fin}], desfecho:'ok'|'no', ...} */
(function(){
  let u=SIMU[0].k, k=SIMK[0].k;
  const eU=document.getElementById('simu'), eK=document.getElementById('simk');
  const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  function pinta(){
    eU.innerHTML=SIMU.map(x=>'<button data-u="'+x.k+'"'+(x.k===u?' class="on"':'')+'>'+x.n+'</button>').join('');
    eK.innerHTML=SIMK.map(x=>'<button data-k2="'+x.k+'"'+(x.k===k?' class="on"':'')+'>'+x.n+'</button>').join('');
    eU.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{u=b.dataset.u;pinta();}));
    eK.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{k=b.dataset.k2;pinta();}));
    const r=SIM[u+'|'+k];
    document.getElementById('simout').innerHTML=
      '<div class="simcard"><div class="sh2">O percurso</div><div class="tr">'+
      r.passos.map(s=>'<div class="st'+(s.bad?' bad':'')+(s.fin?' fin':'')+'">'+
        esc(s.txt)+'</div>').join('')+'</div></div>';
    document.getElementById('simfinal').innerHTML='<div class="sh2">O desfecho</div>'+
      '<span class="pill '+r.desfecho+'">'+esc(r.rotulo)+'</span>'+
      '<p style="margin:12px 0 10px;font-size:14px">'+r.porque+'</p>';
  }
  pinta();
})();
```

**Quantos cenários.** Todos os que os dados suportam, e não um. Um caminho feliz sozinho
esconde precisamente aquilo que o estudo devia ensinar: o que acontece quando corre mal.
No Support Ticket eram dezoito, e os cinco modos de falha ensinam mais do que os treze
sucessos.

O `porque` de cada cenário é onde a explicação vive — uma ou duas frases a dizer **porque
é que este desfecho e não outro**, ancoradas no dado concreto que o decidiu.

## 17. Cartões-receita «onde mexer para…»

Serve directamente o objetivo de **nível 2** (encontrar e mudar qualquer linha), e é o
componente que prepara uma sessão de revisão em que alguém pede uma alteração ao vivo.

Cada cartão é um `<details class="rec">` com três partes obrigatórias:

1. Os ficheiros **pela ordem de edição**, não por ordem de importância.
2. **O teste que apanha o erro** se um passo for esquecido. Sem isto o cartão é uma lista
   de ficheiros; com isto é uma rede de segurança, e ensina que o teste existe *por causa*
   daquele esquecimento.
3. A armadilha — o passo que não dá erro nenhum quando é feito ao contrário.

```html
<div class="recs">
  <details class="rec">
    <summary>… acrescentar uma quarta tool</summary>
    <div class="rbody">
      <ol>
        <li><code>tools/loaders.py</code> — a função que lê e valida.</li>
        <li><code>domain.py</code> — o modelo, e a união em <code>ToolResult.records</code>.</li>
        <li><code>tracing/summarise.py</code> — a regra de resumo.</li>
      </ol>
      <div class="tst"><b>O teste que te apanha:</b>
        <code>test_registry.py::test_every_registered_tool_is_summarised_and_projected</code>.
        Exige, para cada tool registada, um sumarizador e uma projecção — os dois
        esquecimentos que de outra forma só apareceriam em produção.</div>
      <p><b>Cuidado:</b> uma tool a mais aproxima o loop do cap de iterações.</p>
    </div>
  </details>
</div>
```

**Quantos.** Quatro a seis, e escolhidos por uma pergunta só: *o que é que alguém pediria
numa revisão de 45 minutos?* Uma alteração que ninguém pede não vale um cartão.

## 18. Gaveta de glossário

Botão fixo, caixa de filtro, acessível de **qualquer** separador. Existe para que nenhum
termo seja um beco sem saída: o leitor encontra `FactSet` no separador 5 sem ter de voltar
ao 2 à procura da definição.

O HTML e o JS **já estão no template**, com o slot `{{DADOS_GLOSSARIO}}`. Só é preciso
preencher o array; com ele vazio, o botão remove-se sozinho.

```js
{t:'FactSet',d:'O conjunto completo de factos de que uma resposta pode ser feita. Projectado da history, e congelado.'},
{t:'handoff',d:'A entrega do ticket a uma pessoa. Sem resposta nenhuma, e sempre com um motivo.'},
```

**Quantos.** Todos os termos que o estudo usa mais do que uma vez, incluindo os do próprio
domínio. Abaixo de 30 não vale a gaveta — uma glosa `.t[data-tip]` chega. As definições são
de uma ou duas linhas: quem abre a gaveta quer relembrar-se, não estudar outra vez.

---

# Armadilhas ao escrever o JS embutido

Quatro erros que custaram tempo real e que não dão mensagem de erro útil. O ficheiro abre
em branco e não diz porquê.

**1. Apóstrofos portugueses dentro de strings de aspa simples.** `'a policy não é d'ele'`
parte o ficheiro. Escreve sem apóstrofo, ou escapa, ou usa aspas duplas nessa string.

**2. Uma string JS não pode passar de linha.** Isto é erro de sintaxe:

```js
{k:'mc', e:'O teste lê o registry
   e exige um sumarizador.'}      // ← ERRO: a string abre e nunca fecha
```

Ou fica tudo numa linha, ou concatena com `+`. É o erro mais fácil de cometer quando se
escreve texto longo, e o mais difícil de ver ao reler.

**3. `data-tab` é exclusivo do `<nav>`.** O `verificar.py` lê **qualquer** `data-tab` como
declaração de separador e dá erro de órfão. Nos outros componentes usa `data-r`, `data-c`,
`data-u`, `data-k`.

**4. Texto português gerado por script perde os acentos.** Quando o texto passa por um
script de montagem, é fácil escrevê-lo sem acentos "para não haver problemas de encoding"
— e ele chega assim à página. O `verificar.py` avisa; escreve sempre com acentos e grava em
UTF-8.

**E uma armadilha que não é de JS:** escrever ficheiros grandes de HTML/CSS através de
heredocs de bash parte-se de formas difíceis de diagnosticar. Usa a ferramenta `Write`.
