#!/usr/bin/env node
/**
 * Teste de fumo de um estudo interactivo: verifica que a pagina *corre*.
 *
 * O verificar.py le o ficheiro como texto e nao sabe se o JS rebenta ao carregar,
 * se um separador fica vazio, ou se um componente nao renderiza. Isto sabe.
 *
 *   npm install jsdom
 *   node smoke.js caminho/para/estudo.html
 *
 * Opcional de proposito: precisa de node e de uma dependencia. A porta obrigatoria
 * continua a ser o verificar.py.
 */
const fs = require("fs");
const path = require("path");

// O jsdom pode estar instalado ao pe da skill ou na pasta onde se corre o comando:
// o require normal so procura a partir deste ficheiro, por isso tentamos os dois.
let JSDOM, VirtualConsole;
for (const onde of [null, path.join(process.cwd(), "node_modules", "jsdom")]) {
  try {
    ({ JSDOM, VirtualConsole } = require(onde || "jsdom"));
    break;
  } catch (e) { /* tenta o proximo */ }
}
if (!JSDOM) {
  console.error("falta o jsdom. Corre  npm install jsdom  nesta pasta, e volta a tentar.");
  process.exit(2);
}

const ficheiro = process.argv[2];
if (!ficheiro) {
  console.error("uso: node smoke.js caminho/para/estudo.html");
  process.exit(2);
}

const erros = [];
const vc = new VirtualConsole()
  .on("jsdomError", (e) => erros.push("erro de execucao: " + e.message))
  .on("error", (e) => erros.push("console.error: " + e));

const dom = new JSDOM(fs.readFileSync(ficheiro, "utf8"), {
  runScripts: "dangerously",
  virtualConsole: vc,
});
const w = dom.window;
const d = w.document;
const q = (s) => d.querySelectorAll(s);
const clique = (el) => el.dispatchEvent(new w.MouseEvent("click", { bubbles: true }));

const linhas = [];
let ok = true;
function chk(rotulo, cond, extra) {
  if (!cond) ok = false;
  linhas.push((cond ? "OK   " : "ERRO ") + rotulo + (extra ? "  " + extra : ""));
  return cond;
}
function opcional(rotulo, presente, cond, extra) {
  if (!presente) {
    linhas.push("--   " + rotulo + " (nao usado neste estudo)");
    return true;
  }
  return chk(rotulo, cond, extra);
}

/* ── o essencial ──────────────────────────────────────────────────────── */
chk("a pagina carrega sem erros de execucao", erros.length === 0, erros.join(" | "));

const botoes = q("nav button[data-tab]");
const acessos = q("section[role=tabpanel]");
chk("ha botoes de nav", botoes.length >= 7, botoes.length + " botoes");
chk("cada botao tem a sua seccao",
    [...botoes].every((b) => d.getElementById(b.dataset.tab)));
chk("exactamente uma seccao comeca aberta",
    q("section[role=tabpanel].on").length === 1);

botoes.forEach((b) => {
  clique(b);
  if (q("section[role=tabpanel].on").length !== 1)
    erros.push("o separador " + b.dataset.tab + " nao abre sozinho");
});
chk("cada separador abre exactamente uma seccao",
    q("section[role=tabpanel].on").length === 1 &&
    !erros.some((e) => e.includes("nao abre sozinho")));

/* ── auto-avaliacao ───────────────────────────────────────────────────── */
chk("o flashcard inicial esta pintado",
    (d.getElementById("fccard") || {}).textContent?.trim().length > 0);

const perguntas = q("#qlist .q");
chk("o quiz construiu as perguntas", perguntas.length >= 5, perguntas.length + " perguntas");
let quizMau = [];
perguntas.forEach((qq, i) => {
  const opts = qq.querySelectorAll(".opts button");
  if (opts.length === 0) return; // pergunta oral
  clique(opts[0]);
  if (qq.querySelectorAll(".expl").length !== 1) quizMau.push("P" + (i + 1) + " sem explicacao");
  if (qq.querySelectorAll(".opts button.good").length !== 1)
    quizMau.push("P" + (i + 1) + " sem resposta certa marcada");
});
chk("cada pergunta mc revela uma explicacao e marca a certa",
    quizMau.length === 0, quizMau.join(" | "));
q("#qlist .revbtn").forEach(clique);
chk("as perguntas orais revelam a resposta-modelo",
    q("#qlist .model").length === q("#qlist .tag.oral").length);

/* ── componentes de clique ────────────────────────────────────────────── */
let painelMau = [];
[["hot", ".hot"], ["node", ".node[data-m], .node[data-k]"]].forEach(([nome, sel]) => {
  q(sel).forEach((el) => {
    const antes = d.body.innerHTML.length;
    clique(el);
    if (d.body.innerHTML.length === antes) painelMau.push(nome + ":" + (el.dataset.k || el.dataset.m || "?"));
  });
});
opcional("cada hotspot / no de mapa abre um painel",
         q(".hot, .node[data-m], .node[data-k]").length > 0,
         painelMau.length === 0, painelMau.slice(0, 4).join(","));

/* ── leitor de codigo anotado ─────────────────────────────────────────── */
const rdbar = d.getElementById("rdbar");
if (rdbar && rdbar.querySelectorAll("button").length) {
  const semNota = [];
  [...rdbar.querySelectorAll("button")].forEach((b) => {
    clique(b);
    const todas = q("#rdsrc .l").length;
    const clicaveis = q("#rdsrc .l.c").length;
    if (todas === 0) semNota.push(b.dataset.r + ": nao renderizou");
    else if (todas !== clicaveis) semNota.push(b.dataset.r + ": " + (todas - clicaveis) + " linhas sem nota");
    q("#rdsrc .l.c").forEach((l, i) => {
      if (i % 9) return;
      clique(l);
      const n = d.getElementById("rdnote").textContent;
      if (!n || n.includes("Sem nota")) semNota.push(b.dataset.r + " linha " + l.dataset.ln);
    });
  });
  chk("os leitores de codigo abrem e todas as linhas tem nota",
      semNota.length === 0, semNota.slice(0, 3).join(" | "));
} else {
  linhas.push("--   leitor de codigo anotado (nao usado neste estudo)");
}

/* ── grelha de conceitos ──────────────────────────────────────────────── */
const cgs = q("#cgrids .cg");
if (cgs.length) {
  const maus = [];
  cgs.forEach((c) => {
    clique(c);
    if (d.getElementById("cpanel").querySelectorAll(".fld").length < 2) maus.push(c.dataset.c);
  });
  chk("cada conceito abre um painel preenchido", maus.length === 0,
      cgs.length + " conceitos" + (maus.length ? " | maus: " + maus.slice(0, 4) : ""));
} else {
  linhas.push("--   grelha de conceitos (nao usada neste estudo)");
}

/* ── simulador ────────────────────────────────────────────────────────── */
const simu = q("#simu button");
if (simu.length) {
  const maus = [];
  const vars = [...q("#simk button")].map((b) => b.dataset.k2 || b.dataset.k);
  [...simu].map((b) => b.dataset.u).forEach((u) => {
    (vars.length ? vars : [null]).forEach((k) => {
      clique(d.querySelector('#simu button[data-u="' + u + '"]'));
      if (k) clique(d.querySelector('#simk button[data-k2="' + k + '"]'));
      const saida = (d.getElementById("simout") || {}).textContent || "";
      if (saida.trim().length < 20) maus.push(u + "|" + k);
    });
  });
  chk("o simulador produz saida em todas as combinacoes", maus.length === 0,
      simu.length * Math.max(vars.length, 1) + " combinacoes" +
      (maus.length ? " | vazias: " + maus.slice(0, 4) : ""));
} else {
  linhas.push("--   simulador (nao usado neste estudo)");
}

/* ── gaveta de glossario ──────────────────────────────────────────────── */
const gbtn = d.getElementById("gbtn");
if (gbtn) {
  clique(gbtn);
  const total = q("#glist .gi").length;
  const alvo = q("#glist .gi .gt")[0]?.textContent.slice(0, 4) || "";
  const f = d.getElementById("gfilter");
  f.value = alvo;
  f.dispatchEvent(new w.Event("input", { bubbles: true }));
  chk("a gaveta de glossario abre e filtra",
      d.getElementById("gdraw").classList.contains("open") && total > 0 &&
      q("#glist .gi").length > 0 && q("#glist .gi").length <= total,
      total + " termos");
} else {
  linhas.push("--   gaveta de glossario (nao usada neste estudo)");
}

/* ── proximos niveis ──────────────────────────────────────────────────── */
chk("o backlog de Proximos niveis esta la", q(".nivel[data-slug]").length > 0,
    q(".nivel[data-slug]").length + " itens");

console.log("\n" + path.resolve(ficheiro));
console.log("-".repeat(72));
console.log(linhas.join("\n"));
console.log("-".repeat(72));
console.log(ok ? "O estudo corre.\n" : "Ha problemas a corrigir.\n");
process.exit(ok ? 0 : 1);
