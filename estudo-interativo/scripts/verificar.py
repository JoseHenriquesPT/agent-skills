#!/usr/bin/env python3
"""Verifica um estudo interactivo produzido pela skill estudo-interativo.

As regras aqui sao as que nao se podem confirmar a olho: se o ficheiro abre offline,
se a espinha esta toda la, se o contrato de expansao (Proximos niveis) continua
legivel por uma execucao futura da skill, e -- com `--fonte` -- se cada excerto de
codigo embutido bate certo com o ficheiro de origem.

    python verificar.py caminho/para/estudo.html
    python verificar.py caminho/para/estudo.html --fonte C:/caminho/para/o/repo
    python verificar.py caminho/para/estudo.html --ignorar-caminho

ERROS fazem falhar. AVISOS nao -- sao pontos de qualidade a olhar, nao regressoes.
Sai com 1 se houver erros.
"""

import argparse
import json
import pathlib
import re
import sys

SEPARADORES = [
    ("oquee", "O que e"),
    ("anatomia", "Anatomia"),
    ("funciona", "Como funciona"),
    ("liga", "Como se liga"),
    ("confusoes", "Confusoes"),
    ("avaliacao", "Auto-avaliacao"),
    ("niveis", "Proximos niveis"),
]

#: Separadores cuja estrutura interactiva ja e imposta por outras verificacoes.
ISENTOS_DE_COMPONENTE = {"avaliacao", "niveis"}

MIN_FLASHCARDS = 8
MIN_QUIZ = 5
MIN_DETAILS = 3

#: Marcas que contam como "o leitor pode clicar, percorrer ou abrir isto".
#: Cada uma corresponde a um componente do references/componentes.md.
MARCAS_COMPONENTE = (
    "<svg",              # diagrama
    "<details",          # aprofundamento e cartoes-receita
    'class="hot"',       # anatomia clicavel
    'class="layer"',     # camadas
    'class="emuma"',     # frase-ancora
    'class="abtabs"',    # toggle A/B
    'class="hopbar"',    # percurso passo a passo
    'class="cgrid"',     # grelha de conceitos
    'id="cgrids"',       # grelha de conceitos (construida por JS)
    'id="rdbar"',        # leitor de codigo anotado
    'class="simopts"',   # simulador
    'id="simu"',         # simulador (construido por JS)
    'class="cmp"',       # tabela de comparacao
)

#: Palavras portuguesas que so existem sem acento por engano. Lista curta e de alto
#: sinal de proposito: e um aviso para ir olhar, nao um corrector ortografico.
SEM_ACENTO = """
nao entao sao tambem decisao decisoes excepcao excepcoes validacao execucao
iteracao iteracoes observacao observacoes intencao razao razoes unico unica
proprio propria apos alem possivel numero numeros ultimo ultima minimo maximo
pratica basico publico estatico generico especifico proximo construcao
verificacao classificacao funcao funcoes seccao seccoes sessao sessoes opcao
opcoes condicao operacao informacao aplicacao duracao ordenacao declaracao
violacao violacoes clausula clausulas variavel variaveis memoria proposito
atencao referencia experiencia sequencia consequencia importacao importacoes
implementacao configuracao transaccao projeccao sumarizacao
""".split()

erros: list[str] = []
avisos: list[str] = []


def erro(msg: str) -> None:
    erros.append(msg)


def aviso(msg: str) -> None:
    avisos.append(msg)


def bloco(html: str, nome: str) -> str:
    """Devolve o miolo de `const <nome>=[ ... ];` ou string vazia."""
    m = re.search(r"const\s+" + nome + r"\s*=\s*\[(.*?)\n\];", html, re.S)
    return m.group(1) if m else ""


def seccoes(html: str) -> dict[str, str]:
    """O HTML de cada <section role=tabpanel>, indexado por id."""
    out: dict[str, str] = {}
    for m in re.finditer(
        r'<section[^>]*\brole\s*=\s*["\']tabpanel["\'][^>]*>(.*?)</section>', html, re.S
    ):
        tag = m.group(0)[: m.group(0).index(">") + 1]
        sid = re.search(r'id\s*=\s*["\']([\w-]+)["\']', tag)
        if sid:
            out[sid.group(1)] = m.group(1)
    return out


def sem_codigo(html: str) -> str:
    """O documento sem style, sem as ilhas JSON e sem os blocos de codigo embutido.

    O que sobra e prosa (incluindo a que vive dentro de strings de JS, que e onde a
    geracao por script costuma introduzir erros).
    """
    out = re.sub(r"<style>.*?</style>", " ", html, flags=re.S)
    out = re.sub(
        r'<script[^>]+type\s*=\s*["\']application/json["\'].*?</script>', " ", out, flags=re.S
    )
    out = re.sub(r'<div class="codebox".*?</div>', " ", out, flags=re.S)
    return out


# --------------------------------------------------------------------------- #
# 1. offline: nenhuma referencia externa
# --------------------------------------------------------------------------- #
def check_offline(html: str) -> None:
    # xmlns e um identificador de namespace XML, nao um pedido de rede.
    padroes = [
        (r'<script[^>]+src\s*=\s*["\']https?://', "<script src> para um URL externo"),
        (r'<link[^>]+href\s*=\s*["\']https?://', "<link href> para um URL externo"),
        (r'<img[^>]+src\s*=\s*["\']https?://', "<img src> para um URL externo"),
        (r"@import\s+(url\()?[\"']?https?://", "@import de uma folha de estilo externa"),
        (r"url\(\s*[\"']?https?://", "url() de CSS a apontar para fora"),
        (r"\bfetch\s*\(\s*[\"']https?://", "chamada fetch() para a rede"),
        (r"new\s+WebSocket\s*\(", "ligacao WebSocket"),
        (r"XMLHttpRequest", "XMLHttpRequest"),
    ]
    for pad, desc in padroes:
        for m in re.finditer(pad, html, re.I):
            linha = html[: m.start()].count("\n") + 1
            erro(
                f"linha {linha}: {desc}. O estudo tem de abrir com duplo-clique sem rede "
                f"- embute o recurso ou tira-o."
            )


# --------------------------------------------------------------------------- #
# 2. lingua e tema
# --------------------------------------------------------------------------- #
def check_lingua_tema(html: str) -> None:
    if not re.search(r'<html[^>]+lang\s*=\s*["\']pt-PT["\']', html, re.I):
        erro('falta lang="pt-PT" no <html>.')

    blocos_tema = [
        (r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark", "@media (prefers-color-scheme:dark)"),
        (r':root\[data-theme\s*=\s*["\']dark["\']\]', ':root[data-theme="dark"]'),
        (r':root\[data-theme\s*=\s*["\']light["\']\]', ':root[data-theme="light"]'),
    ]
    for pad, nome in blocos_tema:
        if not re.search(pad, html, re.I):
            erro(
                f"falta o bloco de tema {nome}. Sem os tres, o botao de tema deixa de "
                f"funcionar num dos sentidos."
            )

    if 'id="themeBtn"' not in html:
        erro("falta o botao de tema (#themeBtn).")


# --------------------------------------------------------------------------- #
# 3. espinha
# --------------------------------------------------------------------------- #
def check_espinha(html: str) -> None:
    ids = set(seccoes(html))
    tabs = set(re.findall(r'data-tab\s*=\s*["\']([\w-]+)["\']', html))

    for sid, nome in SEPARADORES:
        if sid not in ids:
            erro(f'falta o separador "{nome}" (<section id="{sid}">). A espinha e fixa.')
        elif sid not in tabs:
            erro(f'o separador "{nome}" existe mas nao tem botao no nav (data-tab="{sid}").')

    orfaos = tabs - ids
    for o in sorted(orfaos):
        erro(f'ha um botao data-tab="{o}" sem <section id="{o}"> - o separador nao abre.')

    ligados = re.findall(r'<section[^>]*class\s*=\s*["\'][^"\']*\bon\b', html)
    if len(ligados) != 1:
        erro(
            f"{len(ligados)} separadores comecam com class=\"on\" - tem de ser exactamente 1 "
            f"(o primeiro)."
        )

    # `data-tab` e exclusivo do nav: o check acima le qualquer ocorrencia como separador.
    nav = re.search(r"<nav\b.*?</nav>", html, re.S)
    if nav:
        dentro = len(re.findall(r"data-tab\s*=", nav.group(0)))
        total = len(re.findall(r"data-tab\s*=", html))
        if total > dentro:
            aviso(
                f"ha {total - dentro} atributo(s) data-tab fora do <nav>. Esse atributo e "
                f"exclusivo da navegacao - usa data-r / data-c / data-u nos outros "
                f"componentes, senao este verificador le-os como separadores."
            )


# --------------------------------------------------------------------------- #
# 4. auto-avaliacao
# --------------------------------------------------------------------------- #
def check_avaliacao(html: str) -> None:
    cards = bloco(html, "CARDS")
    if not cards.strip():
        erro("nao encontrei o array CARDS (flashcards).")
    else:
        n = len(re.findall(r"\{\s*f\s*:", cards))
        if n < MIN_FLASHCARDS:
            erro(f"so {n} flashcards; o minimo e {MIN_FLASHCARDS}.")
        if re.search(r"\{\s*f\s*:\s*['\"][^'\"]{0,25}['\"]\s*,", cards):
            aviso(
                "ha flashcards com a frente muito curta. A frente e uma pergunta, nao um "
                "titulo - um substantivo solto testa reconhecimento, nao compreensao."
            )

    qs = bloco(html, "QS")
    if not qs.strip():
        erro("nao encontrei o array QS (quiz).")
    else:
        n = len(re.findall(r"\{\s*k\s*:", qs))
        orais = len(re.findall(r"k\s*:\s*['\"]oral['\"]", qs))
        if n < MIN_QUIZ:
            erro(f"so {n} perguntas de quiz; o minimo e {MIN_QUIZ}.")
        if orais < 1:
            erro(
                "o quiz nao tem nenhuma pergunta 'oral'. Explicar em voz alta e o que apanha "
                "o modelo mental incompleto - reconhecer a opcao certa entre quatro nao apanha."
            )
        for m in re.finditer(r"k\s*:\s*['\"]mc['\"](.*?)(?=\{\s*k\s*:|$)", qs, re.S):
            if not re.search(r"\be\s*:", m.group(1)):
                aviso("ha uma pergunta de escolha multipla sem campo 'e' (explicacao).")
                break


# --------------------------------------------------------------------------- #
# 5. contrato de expansao
# --------------------------------------------------------------------------- #
def check_niveis(html: str) -> None:
    itens = re.findall(r'<div[^>]+class\s*=\s*["\']nivel["\'][^>]*>', html)
    if not itens:
        erro(
            'o separador "Proximos niveis" nao tem nenhum <div class="nivel">. E este '
            "separador que permite a skill ser chamada outra vez para aprofundar - sem ele "
            "o estudo e um beco sem saida."
        )
        return

    slugs: list[str] = []
    for tag in itens:
        nivel = re.search(r'data-nivel\s*=\s*["\']([\w-]+)["\']', tag)
        slug = re.search(r'data-slug\s*=\s*["\']([\w-]+)["\']', tag)
        feito = re.search(r'data-feito\s*=\s*["\']([\w-]+)["\']', tag)

        if not nivel:
            erro(f"item de Proximos niveis sem data-nivel: {tag[:80]}")
        elif nivel.group(1) not in ("intermedio", "avancado"):
            erro(
                f'data-nivel="{nivel.group(1)}" invalido - so "intermedio" ou "avancado" '
                f"(sem acentos)."
            )
        if not slug:
            erro(f"item de Proximos niveis sem data-slug: {tag[:80]}")
        else:
            slugs.append(slug.group(1))
        if not feito:
            erro(f"item de Proximos niveis sem data-feito: {tag[:80]}")
        elif feito.group(1) not in ("sim", "nao"):
            erro(f'data-feito="{feito.group(1)}" invalido - so "sim" ou "nao".')

    repetidos = {s for s in slugs if slugs.count(s) > 1}
    for s in sorted(repetidos):
        erro(f'data-slug="{s}" aparece mais do que uma vez; os slugs identificam o item.')

    por_fazer = [t for t in itens if 'data-feito="nao"' in t.replace("'", '"')]
    if not por_fazer:
        aviso(
            "todos os itens de Proximos niveis estao marcados como feitos. Se o objeto ainda "
            "da para aprofundar, acrescenta itens novos; se nao da, diz isso no texto."
        )

    if "destranca" not in html:
        aviso(
            'nenhum item tem a linha "Destranca:". Sem ela o backlog e uma lista de palavras '
            "e o leitor nao tem como escolher o que estudar a seguir."
        )


# --------------------------------------------------------------------------- #
# 6. interactividade e diagramas
# --------------------------------------------------------------------------- #
def check_interactividade(html: str) -> None:
    n_det = len(re.findall(r"<details", html, re.I))
    if n_det < MIN_DETAILS:
        erro(
            f"so {n_det} seccoes <details>; o minimo e {MIN_DETAILS}. O corpo do texto carrega "
            f"o modelo mental e o <details> carrega o porque - sem eles o estudo ou fica raso "
            f"ou fica pesado."
        )

    svgs = re.findall(r"<svg\b.*?</svg>", html, re.S | re.I)
    if not svgs:
        erro("nao ha nenhum diagrama <svg>. Pelo menos a anatomia ou o fluxo pedem um.")

    for i, svg in enumerate(svgs, 1):
        maus = re.findall(
            r'(?:fill|stroke)\s*=\s*["\'](#[0-9a-fA-F]{3,8}|black|white|red|blue|green|gray|grey)["\']',
            svg,
        )
        if maus:
            erro(
                f"diagrama {i}: cor fixa em SVG ({', '.join(sorted(set(maus))[:4])}). "
                f"No tema oposto isso fica invisivel - usa as classes .bx/.node/.ar ou "
                f"var(--fg2)/currentColor."
            )
        check_geometria_svg(i, svg)

    ids_marker = re.findall(r'<marker[^>]+id\s*=\s*["\']([\w-]+)["\']', html)
    dups = {m for m in ids_marker if ids_marker.count(m) > 1}
    for d in sorted(dups):
        erro(
            f'ha dois <marker id="{d}"> - o id e global a pagina, por isso o segundo diagrama '
            f"fica a usar a definicao do primeiro."
        )

    # So atributos dentro de uma tag contam: o exemplo literal de marker-end que o CSS do
    # template documenta (dentro de um comentario /* */) nao e uma referencia real.
    usados = set(re.findall(r"<[^>]*\bmarker-end\s*=\s*[\"']url\(#([\w-]+)\)", html))
    for u in sorted(usados - set(ids_marker)):
        erro(f'um path usa marker-end="url(#{u})" mas nao ha nenhum <marker id="{u}">.')


def check_geometria_svg(i: int, svg: str) -> None:
    """Caixas e rotulos fora do viewBox: um diagrama cortado, sem o abrir no browser."""
    vb = re.search(r'viewBox\s*=\s*["\']\s*0\s+0\s+(\d+)\s+(\d+)', svg)
    if not vb:
        return
    W, H = int(vb.group(1)), int(vb.group(2))
    fora = []
    for r in re.finditer(
        r'<rect[^>]*\bx="(-?\d+)"[^>]*\by="(-?\d+)"[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"', svg
    ):
        x, y, w, h = map(int, r.groups())
        if x < 0 or y < 0 or x + w > W or y + h > H:
            fora.append(f"rect {x},{y} {w}x{h}")
    for t in re.finditer(r'<text[^>]*\bx="(-?\d+)"[^>]*\by="(-?\d+)"', svg):
        x, y = map(int, t.groups())
        if x < 0 or y < 0 or x > W or y > H:
            fora.append(f"text {x},{y}")
    if fora:
        aviso(
            f"diagrama {i}: {len(fora)} elemento(s) fora do viewBox {W}x{H} "
            f"({', '.join(fora[:3])}). Ficam cortados - alarga o viewBox ou move-os."
        )


# --------------------------------------------------------------------------- #
# 7. qualidade: cada separador abre com um componente
# --------------------------------------------------------------------------- #
def check_componentes(html: str) -> None:
    for sid, nome in SEPARADORES:
        if sid in ISENTOS_DE_COMPONENTE:
            continue
        corpo = seccoes(html).get(sid)
        if corpo is None:
            continue

        pos = [corpo.find(m) for m in MARCAS_COMPONENTE if m in corpo]
        if not pos:
            aviso(
                f'o separador "{nome}" nao tem nenhum componente interactivo. Um separador so '
                f"com prosa falhou - poe-lhe uma coisa que o leitor possa clicar, percorrer "
                f"ou abrir (references/componentes.md)."
            )
            continue

        primeiro = min(pos)
        # Um <p class="lead"> conta como legenda do componente, nao como prosa.
        prosa = [
            m.start()
            for m in re.finditer(r"<p(?![^>]*class=[\"']lead)", corpo)
            if m.start() < primeiro
        ]
        if prosa:
            aviso(
                f'o separador "{nome}" abre com prosa: ha {len(prosa)} paragrafo(s) antes do '
                f"primeiro componente. Cada separador abre com uma coisa que se ve ou se "
                f"clica; a explicacao vem depois, ou dentro do painel de clique."
            )


# --------------------------------------------------------------------------- #
# 8. qualidade: politica de citacao e acentos
# --------------------------------------------------------------------------- #
def check_citacoes(html: str) -> None:
    """Numeros de linha em prosa apodrecem ao primeiro refactor."""
    texto = sem_codigo(html)
    achados = set(
        re.findall(
            r"\b([\w./-]+\.(?:py|ts|tsx|js|jsx|md|sql|go|rs|java|rb|php|c|h|cpp|ya?ml|json|toml|sh):\d+)\b",
            texto,
        )
    )
    if achados:
        aviso(
            f"ha {len(achados)} citacao(oes) com numero de linha em prosa "
            f"({', '.join(sorted(achados)[:3])}). Numeros de linha so dentro dos blocos de "
            f"codigo embutidos, onde sao auto-consistentes; em prosa, ancora por ficheiro + "
            f"simbolo (orchestrator.py - _decide)."
        )


def check_acentos(html: str) -> None:
    """Portugues gerado por script perde acentos com facilidade."""
    texto = re.sub(r"<[^>]*>", " ", sem_codigo(html))
    achados: dict[str, int] = {}
    for palavra in SEM_ACENTO:
        for m in re.finditer(r"(?<![0-9A-Za-zÀ-ÿ_-])" + palavra + r"(?![0-9A-Za-zÀ-ÿ_-])", texto):
            antes = texto[max(0, m.start() - 1) : m.start()]
            depois = texto[m.end() : m.end() + 1]
            # chaves e valores de objectos JS: {k:'ambiguo'}, {ambiguo:...}
            if depois == ":" or (antes in "\"'" and depois in "\"'"):
                continue
            achados[palavra] = achados.get(palavra, 0) + 1
    if achados:
        top = ", ".join(f"{p} ({n})" for p, n in sorted(achados.items(), key=lambda x: -x[1])[:5])
        aviso(
            f"{sum(achados.values())} palavra(s) portuguesas sem acento no texto visivel: "
            f"{top}. Confirma - texto gerado por script e onde isto costuma acontecer."
        )


# --------------------------------------------------------------------------- #
# 9. leitor de codigo anotado: notas completas, e (com --fonte) excertos fieis
# --------------------------------------------------------------------------- #
def ilha_rdsrc(html: str) -> dict | None:
    # `rdsrc-data` e nao `rdsrc`: o segundo e o id da <div> que renderiza a fonte.
    m = re.search(
        r'<script[^>]+id\s*=\s*["\']rdsrc-data["\'][^>]*>(.*?)</script>', html, re.S
    )
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as exc:
        erro(f"a ilha JSON #rdsrc-data nao e JSON valido: {exc}")
        return None


def check_leitor(html: str, fonte: pathlib.Path | None) -> None:
    dados = ilha_rdsrc(html)
    if dados is None:
        if fonte is not None:
            erro(
                "pediste --fonte mas o estudo nao tem a ilha "
                '<script type="application/json" id="rdsrc-data">. Ver references/montagem.md.'
            )
        return

    for chave, e in dados.items():
        faltam = {"file", "sym", "first", "src"} - set(e)
        if faltam:
            erro(f"leitor '{chave}': faltam os campos {sorted(faltam)}.")
            continue

        primeira, linhas = e["first"], e["src"]
        ultima = primeira + len(linhas) - 1

        # As notas tem de cobrir o excerto todo, sem buracos nem sobreposicoes:
        # uma linha sem nota e uma linha clicavel que nao abre nada.
        notas = e.get("notes", [])
        if not notas:
            aviso(f"leitor '{chave}': sem notas. O excerto fica sem nada a explica-lo.")
        else:
            coberto: set[int] = set()
            sobrepostas = set()
            for n in notas:
                intervalo = set(range(n["a"], n["b"] + 1))
                sobrepostas |= coberto & intervalo
                coberto |= intervalo
            buracos = sorted(set(range(primeira, ultima + 1)) - coberto)
            extra = sorted(coberto - set(range(primeira, ultima + 1)))
            if buracos:
                erro(
                    f"leitor '{chave}': as linhas {buracos[:6]} nao pertencem a nota nenhuma "
                    f"- ficam clicaveis e nao abrem nada."
                )
            if sobrepostas:
                erro(f"leitor '{chave}': as linhas {sorted(sobrepostas)[:6]} tem duas notas.")
            if extra:
                erro(f"leitor '{chave}': ha notas para linhas fora do excerto: {extra[:6]}.")

        if fonte is None:
            continue

        caminho = fonte / e["file"]
        if not caminho.is_file():
            erro(f"leitor '{chave}': nao encontrei {caminho}.")
            continue
        reais = caminho.read_text(encoding="utf-8").split("\n")
        fatia = reais[primeira - 1 : primeira - 1 + len(linhas)]
        if fatia != linhas:
            difs = [
                f"linha {primeira + i}: fonte={a!r} != estudo={b!r}"
                for i, (a, b) in enumerate(zip(fatia, linhas))
                if a != b
            ]
            erro(
                f"leitor '{chave}' ({e['file']} - {e['sym']}): o excerto nao bate certo com a "
                f"origem. {difs[0] if difs else 'o excerto tem outro tamanho'}. Um excerto "
                f"que nao bate certo e pior do que nenhum - regenera-o a partir do ficheiro."
            )


# --------------------------------------------------------------------------- #
# 10. placeholders e caminho
# --------------------------------------------------------------------------- #
def check_placeholders(html: str) -> None:
    for m in set(re.findall(r"\{\{[A-Z_0-9]+\}\}", html)):
        erro(f"sobrou o placeholder {m} por preencher.")


def check_caminho(p: pathlib.Path) -> None:
    """A convencao e <area>/<tema>/estudo.html.

    `materiais/<area>/<tema>/` continua aceite: foi a convencao documentada durante um
    tempo e ha estudos arrumados assim.
    """
    partes = [x.lower() for x in p.parts]
    if p.name != "estudo.html":
        aviso(f'o ficheiro chama-se "{p.name}"; a convencao e "estudo.html".')

    if "materiais" in partes:
        i = partes.index("materiais")
        if len(p.parts) - i != 4:
            erro(
                f"caminho fora da convencao de legado. Esperado "
                f"materiais/<area>/<tema>/estudo.html, obtido {'/'.join(p.parts[i:])}."
            )
        return

    # <area>/<tema>/estudo.html: a pasta de tema nomeia o objeto concreto, e o nome dela
    # e o que uma execucao futura procura para saber se ja existe estudo deste objeto.
    tema = p.resolve().parent.name
    if not re.fullmatch(r"[a-z0-9]+(?:[-_][a-z0-9]+)*", tema):
        aviso(
            f'a pasta de tema chama-se "{tema}"; a convencao e <area>/<tema>/estudo.html '
            f"com o tema em minusculas e hifens. E por este nome que uma execucao futura "
            f"encontra o estudo em vez de criar um duplicado."
        )


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica um estudo interactivo.")
    ap.add_argument("ficheiro")
    ap.add_argument(
        "--fonte",
        metavar="RAIZ",
        help="raiz do repositorio de origem: confere cada excerto embutido linha a linha",
    )
    ap.add_argument(
        "--ignorar-caminho",
        action="store_true",
        help="nao verificar a convencao <area>/<tema>/estudo.html",
    )
    args = ap.parse_args()

    p = pathlib.Path(args.ficheiro)
    if not p.is_file():
        print(f"nao encontrei o ficheiro: {p}")
        return 1

    fonte = None
    if args.fonte:
        fonte = pathlib.Path(args.fonte)
        if not fonte.is_dir():
            print(f"--fonte: nao encontrei a pasta {fonte}")
            return 1

    html = p.read_text(encoding="utf-8", errors="replace")

    check_offline(html)
    check_lingua_tema(html)
    check_espinha(html)
    check_avaliacao(html)
    check_niveis(html)
    check_interactividade(html)
    check_componentes(html)
    check_citacoes(html)
    check_acentos(html)
    check_leitor(html, fonte)
    check_placeholders(html)
    if not args.ignorar_caminho:
        check_caminho(p)

    print(f"\n{p}  ({len(html):,} bytes)".replace(",", " "))
    print("-" * 72)

    for a in avisos:
        print(f"  AVISO  {a}")
    for e in erros:
        print(f"  ERRO   {e}")

    print("-" * 72)
    if erros:
        print(f"{len(erros)} erro(s), {len(avisos)} aviso(s). Corrige os erros.\n")
        return 1
    print(f"Sem erros, {len(avisos)} aviso(s). O estudo passa.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
