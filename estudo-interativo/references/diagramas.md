# Diagramas

**Mermaid não serve aqui.** Renderizá-lo exige carregar uma biblioteca, e o estudo tem de
abrir com duplo-clique sem rede. Todos os diagramas são **SVG inline**, escrito à mão.

Isso é menos mau do que parece: um SVG à mão diz exatamente o que queres dizer, e ganha
uma coisa que o mermaid não tem — **peças clicáveis** ligadas a um painel de explicação.

## A regra que parte tudo: cores

Nunca escrevas uma cor literal (`#333`, `black`, `white`) num SVG. O estudo tem tema claro e
tema escuro; um `stroke="#333"` fica invisível no escuro, e o leitor vê um retângulo vazio.

Usa as classes que já estão no template — `.bx`, `.node`, `.ar`, `.arl`, `.zone`, `.zlbl`,
`.flow` — que puxam as cores das variáveis CSS. Se precisares mesmo de um atributo direto,
usa `currentColor` ou `var(--fg2)`, nunca um hex.

```html
<!-- errado: desaparece no tema escuro -->
<rect fill="#f5f5f5" stroke="#333"/>
<text fill="#000">pedido</text>

<!-- certo: a classe trata do tema nos dois sentidos -->
<g class="bx"><rect x="20" y="30" width="150" height="52" rx="9"/>
  <text x="95" y="61">pedido</text></g>
```

## Convenções

- `viewBox` com origem `0 0`, largura entre 680 e 900. O template já põe
  `svg{min-width:680px;width:100%}` dentro de um `.mapbox` com scroll horizontal.
- Envolve sempre em `<div class="mapbox">`.
- `role="img"` e `aria-label` a descrever o diagrama numa frase.
- Caixas com `rx="9"`, altura 46–56, texto centrado a `y = topo + 30`.
- Setas com `marker-end="url(#ah)"` — define o marker **uma vez** por SVG.

```html
<defs>
  <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
          orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="var(--fg2)"/>
  </marker>
</defs>
```

Se tiveres mais do que um SVG no mesmo ficheiro, os `id` dos markers têm de ser diferentes
(`ah`, `ah2`, `ah3`) — `id` é global à página, e dois markers com o mesmo nome fazem o
segundo diagrama roubar a definição do primeiro.

---

## Receita 1 — pipeline horizontal

O mais usado: A → B → C, com um rótulo por seta a dizer *o que passa* ali.
Serve o separador **Como funciona**.

```html
<div class="mapbox">
<svg viewBox="0 0 860 150" role="img" aria-label="Pedido, verificação e resposta">
  <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
    orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--fg2)"/></marker></defs>

  <g class="bx"><rect x="20" y="45" width="170" height="56" rx="9"/>
    <text x="105" y="70">cliente</text><text class="s" x="105" y="88">o browser</text></g>

  <path class="ar act" d="M195 73 H285"/>
  <text class="arl act" x="240" y="63">query + JWT</text>

  <g class="bx"><rect x="290" y="45" width="170" height="56" rx="9"/>
    <text x="375" y="70">Postgres</text><text class="s" x="375" y="88">reescreve a query</text></g>

  <path class="ar act" d="M465 73 H555"/>
  <text class="arl act" x="510" y="63">+ WHERE</text>

  <g class="bx"><rect x="560" y="45" width="170" height="56" rx="9"/>
    <text x="645" y="70">tabela</text><text class="s" x="645" y="88">só as linhas dele</text></g>
</svg>
</div>
```

Espaçamento: caixa de 170 de largura a cada 270 px. Rótulo da seta a `y = caixa_y + 18`,
centrado no meio do vão.

## Receita 2 — camadas empilhadas

Para "o que está por cima do quê". Serve o separador **Como se liga**.

```html
<div class="mapbox">
<svg viewBox="0 0 700 250" role="img" aria-label="Camadas da aplicação até à base de dados">
  <rect class="zone" x="15" y="15" width="670" height="105" rx="10"/>
  <text class="zlbl" x="30" y="38">NA APLICAÇÃO — PODES CONTORNAR</text>
  <g class="bx"><rect x="35" y="52" width="290" height="50" rx="9"/>
    <text x="180" y="82">middleware de auth</text></g>
  <g class="bx"><rect x="350" y="52" width="290" height="50" rx="9"/>
    <text x="495" y="82">filtros na query</text></g>

  <rect class="zone" x="15" y="135" width="670" height="100" rx="10"/>
  <text class="zlbl" x="30" y="158">NA BASE DE DADOS — NÃO PODES</text>
  <g class="bx act"><rect x="35" y="172" width="605" height="50" rx="9"/>
    <text x="337" y="202">Row Level Security</text></g>
</svg>
</div>
```

A `.zone` (tracejada) é o que faz o trabalho: agrupa e o `.zlbl` nomeia a fronteira. Usa
`class="bx act"` para destacar a peça de que o separador fala.

## Receita 3 — mapa clicável

O upgrade que justifica escrever SVG à mão. Cada `.node` é clicável e escreve num painel.
Serve o separador **Anatomia** quando o objeto não é código mas sim um conjunto de peças.

```html
<div class="mapbox">
<svg viewBox="0 0 760 200" role="img" aria-label="Mapa clicável das peças">
  <g class="node" data-k="jwt"><rect x="30" y="60" width="180" height="58" rx="9"/>
    <text x="120" y="86">JWT</text><text class="sub" x="120" y="104">quem tu dizes que és</text></g>
  <g class="node" data-k="role"><rect x="280" y="60" width="180" height="58" rx="9"/>
    <text x="370" y="86">role</text><text class="sub" x="370" y="104">o que podes tocar</text></g>
  <g class="node" data-k="policy"><rect x="530" y="60" width="180" height="58" rx="9"/>
    <text x="620" y="86">policy</text><text class="sub" x="620" y="104">que linhas ves</text></g>
</svg>
</div>
<div class="panel" id="mpanel"><div class="ttl">Clica numa peça</div></div>
```

```js
const PECAS={
 jwt:{t:'JWT',f:[['O que é','Um bilhete assinado que o cliente traz em cada pedido.'],
                 ['Quem o lê','O Postgres, que põe o campo <code>sub</code> em <code>auth.uid()</code>.']]},
 role:{t:'role',f:[['O que é','A identidade do lado da base de dados: <code>anon</code>, <code>authenticated</code>, <code>service_role</code>.']]}
};
const mp=document.getElementById('mpanel');
document.querySelectorAll('.node').forEach(n=>{
  n.addEventListener('click',()=>{
    document.querySelectorAll('.node').forEach(x=>x.classList.remove('sel'));
    n.classList.add('sel');
    const d=PECAS[n.dataset.k]; if(!d)return;
    mp.innerHTML='<div class="ttl">'+d.t+'</div><dl class="fields">'+
      d.f.map(([k,v])=>'<div class="fld"><dt>'+k+'</dt><dd>'+v+'</dd></div>').join('')+'</dl>';
  });
});
```

## Receita 4 — ciclo

Para loops (retry, request/response, feedback). Um arco de volta com o `marker-end` no fim.

```html
<path class="ar act" d="M645 100 C700 100 700 175 645 175 H120 C65 175 65 100 120 100"/>
<text class="arl act" x="382" y="192">se falhar, tenta outra vez</text>
```

## Quando *não* fazer um diagrama

Um diagrama que só repete a lista que está por baixo dele ocupa espaço e não ensina nada.
Vale a pena quando há **posição** (o que está dentro/fora, acima/abaixo) ou **movimento**
(o que passa de onde para onde). Para "as cinco propriedades de X", uma tabela é melhor.
