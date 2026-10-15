"""
Trabalho Computacional de Estatística — Primeira parte
Exercício 2

Contou-se o número de erros de impressão da primeira página de um jornal
durante 50 dias.

(a) Represente os dados graficamente.
(b) Faça um histograma e um ramo-e-folhas.

Como executar:
    pip install matplotlib numpy
    python exercicio2.py

Saídas (geradas na mesma pasta do script):
    - a_grafico_barras_frequencia.png   -> item (a)
    - a_grafico_dispersao_unidim.png    -> item (a), complementar
    - b_histograma.png                  -> item (b)
    - b_ramo_e_folhas.png               -> item (b)
    - tabelas e ramo-e-folhas também são impressos no terminal
"""

import math
import os
from collections import Counter

import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Dados (transcritos linha a linha da tabela do enunciado)
# ---------------------------------------------------------------------------
DADOS = [
    8, 11, 8, 12, 14, 13, 11, 14, 14, 15,
    6, 10, 14, 19, 6, 12, 7, 5, 8, 8,
    10, 16, 10, 12, 12, 8, 11, 6, 7, 12,
    7, 10, 14, 5, 12, 7, 9, 12, 11, 9,
    14, 8, 14, 8, 12, 10, 12, 22, 7, 15,
]

PASTA = os.path.dirname(os.path.abspath(__file__))


def salvar(fig, nome):
    caminho = os.path.join(PASTA, nome)
    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> gráfico salvo em: {caminho}")


# ---------------------------------------------------------------------------
# Item (a) — Representação gráfica
# A variável "número de erros" é quantitativa DISCRETA, então a representação
# mais adequada é um gráfico de barras das frequências de cada valor.
# Como complemento, um gráfico de dispersão unidimensional (dot plot).
# ---------------------------------------------------------------------------
def tabela_frequencias(dados):
    n = len(dados)
    freq = Counter(dados)
    print("\nTabela de frequências (variável discreta)")
    print(f"{'Erros':>6} | {'fi':>3} | {'fr':>6} | {'Fi':>3} | {'Fr':>6}")
    print("-" * 38)
    acum = 0
    for valor in sorted(freq):
        fi = freq[valor]
        acum += fi
        print(f"{valor:>6} | {fi:>3} | {fi / n:>6.2%} | {acum:>3} | {acum / n:>6.2%}")
    print("-" * 38)
    print(f"{'Total':>6} | {n:>3} | {1:>6.2%}")
    return freq


def grafico_barras(freq):
    valores = list(range(min(freq), max(freq) + 1))
    contagens = [freq.get(v, 0) for v in valores]

    fig, ax = plt.subplots(figsize=(10, 5))
    barras = ax.bar(valores, contagens, width=0.6, color="#2a78b8", edgecolor="black")
    for b, c in zip(barras, contagens):
        if c:
            ax.text(b.get_x() + b.get_width() / 2, c + 0.15, str(c), ha="center", fontsize=9)
    ax.set_xticks(valores)
    ax.set_xlabel("Número de erros de impressão")
    ax.set_ylabel("Número de dias (frequência)")
    ax.set_title("(a) Gráfico de barras — erros de impressão na 1ª página (50 dias)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    salvar(fig, "a_grafico_barras_frequencia.png")


def grafico_dispersao_unidimensional(freq):
    fig, ax = plt.subplots(figsize=(10, 3.5))
    for valor, fi in freq.items():
        ax.scatter([valor] * fi, range(1, fi + 1), s=60, color="#2a78b8", edgecolor="black")
    ax.set_xticks(range(min(freq), max(freq) + 1))
    ax.set_yticks([])
    ax.set_ylim(0, max(freq.values()) + 1)
    ax.set_xlabel("Número de erros de impressão")
    ax.set_title("(a) Gráfico de dispersão unidimensional (cada ponto = 1 dia)")
    for lado in ("left", "right", "top"):
        ax.spines[lado].set_visible(False)
    salvar(fig, "a_grafico_dispersao_unidim.png")


# ---------------------------------------------------------------------------
# Item (b) — Histograma
# Número de classes pela regra de Sturges: k = 1 + 3,3·log10(n)
# Amplitude de classe h = ceil(amplitude total / k).
# Classes fechadas à esquerda e abertas à direita: [li, ls)
# ---------------------------------------------------------------------------
def classes_sturges(dados):
    n = len(dados)
    minimo, maximo = min(dados), max(dados)
    at = maximo - minimo
    k_sturges = round(1 + 3.3 * math.log10(n))
    h = math.ceil(at / k_sturges)
    # ajusta k ao número de classes realmente necessário para cobrir [mínimo, máximo]
    # (evita classe vazia no fim e garante que o máximo caia dentro da última classe)
    k = (maximo - minimo) // h + 1
    limites = [minimo + i * h for i in range(k + 1)]
    return limites, k, h, at, k_sturges


def tabela_classes(dados, limites):
    n = len(dados)
    print("\nDistribuição de frequências por classes (para o histograma)")
    print(f"{'Classe':>10} | {'xi':>5} | {'fi':>3} | {'fr':>6} | {'Fi':>3}")
    print("-" * 40)
    acum = 0
    freqs = []
    for li, ls in zip(limites[:-1], limites[1:]):
        fi = sum(1 for x in dados if li <= x < ls)
        acum += fi
        freqs.append(fi)
        print(f"{li:>3} |-- {ls:<3} | {(li + ls) / 2:>5.1f} | {fi:>3} | {fi / n:>6.2%} | {acum:>3}")
    print("-" * 40)
    print(f"{'Total':>10} | {'':>5} | {n:>3} | {1:>6.2%}")
    return freqs


def histograma(dados):
    limites, k, h, at, k_st = classes_sturges(dados)
    print(f"\nn = {len(dados)}, mínimo = {min(dados)}, máximo = {max(dados)}, amplitude total = {at}")
    print(f"Sturges: k = 1 + 3,3·log10({len(dados)}) ≈ {1 + 3.3 * math.log10(len(dados)):.2f} "
          f"≈ {k_st} -> h = ceil({at}/{k_st}) = {h} -> {k} classes necessárias para cobrir {min(dados)} a {max(dados)}")
    freqs = tabela_classes(dados, limites)

    fig, ax = plt.subplots(figsize=(9, 5))
    # right=False -> intervalos [li, ls), coerente com a tabela
    ax.hist(dados, bins=limites, color="#5aa469", edgecolor="black")
    centros = [(a + b) / 2 for a, b in zip(limites[:-1], limites[1:])]
    for c, fi in zip(centros, freqs):
        ax.text(c, fi + 0.3, str(fi), ha="center", fontsize=10)
    ax.set_xticks(limites)
    ax.set_ylim(0, max(freqs) * 1.12)
    ax.set_xlabel("Número de erros de impressão (classes [li, ls) )")
    ax.set_ylabel("Frequência (dias)")
    ax.set_title(f"(b) Histograma — {k} classes de amplitude {h} (regra de Sturges)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    salvar(fig, "b_histograma.png")


# ---------------------------------------------------------------------------
# Item (b) — Ramo-e-folhas
# Ramo = dígito das dezenas; folha = dígito das unidades.
# Como quase todos os dados ficam entre 5 e 22 (só 3 ramos: 0, 1 e 2),
# também é feita a versão com ramos DESDOBRADOS (folhas 0–4 e 5–9),
# que mostra melhor a forma da distribuição.
# ---------------------------------------------------------------------------
def ramo_e_folhas(dados, desdobrado=False):
    linhas = []
    ramos = sorted({x // 10 for x in dados})
    for ramo in range(ramos[0], ramos[-1] + 1):
        folhas = sorted(x % 10 for x in dados if x // 10 == ramo)
        if not desdobrado:
            linhas.append((f"{ramo}", folhas))
        else:
            baixas = [f for f in folhas if f <= 4]
            altas = [f for f in folhas if f >= 5]
            linhas.append((f"{ramo}*", baixas))   # folhas 0 a 4
            linhas.append((f"{ramo}.", altas))    # folhas 5 a 9

    # remove linhas vazias do início e do fim (mantém as do meio)
    while linhas and not linhas[0][1]:
        linhas.pop(0)
    while linhas and not linhas[-1][1]:
        linhas.pop()

    texto = []
    for ramo, folhas in linhas:
        texto.append(f"{ramo:>3} | {' '.join(str(f) for f in folhas)}   ({len(folhas)})")
    return texto


def imprimir_e_salvar_ramo_e_folhas(dados):
    simples = ramo_e_folhas(dados)
    desdob = ramo_e_folhas(dados, desdobrado=True)

    print("\nRamo-e-folhas (ramo = dezena, folha = unidade)   Ex.: 1 | 4 = 14 erros")
    print("\n".join(simples))
    print("\nRamo-e-folhas com ramos desdobrados  (* = folhas 0–4, . = folhas 5–9)")
    print("\n".join(desdob))

    conteudo = (
        "Ramo-e-folhas  (1 | 4 = 14 erros)\n\n"
        + "\n".join(simples)
        + "\n\n\nRamos desdobrados\n(* = folhas 0–4,  . = folhas 5–9)\n\n"
        + "\n".join(desdob)
    )
    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.axis("off")
    ax.text(0.02, 0.98, conteudo, family="monospace", fontsize=11, va="top")
    ax.set_title("(b) Diagrama de ramo-e-folhas — erros de impressão (n = 50)")
    salvar(fig, "b_ramo_e_folhas.png")


# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Exercício 2 — Erros de impressão na 1ª página (50 dias)")
    print("=" * 60)
    print(f"Dados ordenados: {sorted(DADOS)}")

    print("\n--- Item (a) ---")
    freq = tabela_frequencias(DADOS)
    grafico_barras(freq)
    grafico_dispersao_unidimensional(freq)

    print("\n--- Item (b) ---")
    histograma(DADOS)
    imprimir_e_salvar_ramo_e_folhas(DADOS)

    plt.close("all")


if __name__ == "__main__":
    assert len(DADOS) == 50, "Deveriam ser 50 observações"
    main()
