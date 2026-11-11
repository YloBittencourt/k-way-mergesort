"""
Visualizador e gerador de gráficos explicativos com Matplotlib para o K-Way Merge Sort.
Gera ilustrações estáticas de alta resolução e animações explicativas do algoritmo.
"""

import sys
import os
import matplotlib
matplotlib.use("Agg")  # Backend não interativo para geração headless de alta resolução
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from k_way_mergesort import calcula_particoes, k_way_mergesort


# Configuração estética moderna para Matplotlib (Dark Theme)
plt.style.use("dark_background")
PALETTE = ["#10b981", "#0ea5e9", "#f59e0b", "#a855f7", "#f43f5e", "#06b6d4"]


def generate_explanation_diagram(output_path: str = "assets/matplotlib_explanation.png", n: int = 24, k: int = 3):
    """
    Gera um painel com 4 fases explicando visualmente a essência do K-Way Merge Sort:
    1. Vetor Original
    2. Divisão em K Partições
    3. Partições Ordenadas Independentemente
    4. Vetor Final Mesclado
    """
    np.random.seed(42)
    original = np.random.randint(15, 95, size=n)

    # Calcula as partições
    particoes = calcula_particoes(n, k, 0)
    
    # Cria estado intermediário: cada partição ordenada isoladamente
    sub_sorted = np.copy(original)
    for j in range(k):
        start, end = particoes[j], particoes[j + 1]
        sub_sorted[start:end] = np.sort(sub_sorted[start:end])

    # Estado final: totalmente ordenado
    fully_sorted = np.sort(original)

    fig, axes = plt.subplots(4, 1, figsize=(11, 8.5), facecolor="#0f172a")
    fig.suptitle(f"Como Funciona o K-Way Merge Sort (N = {n}, K = {k})", fontsize=16, fontweight="bold", color="#f8fafc", y=0.98)

    stages = [
        ("1. Vetor Inicial Desordenado", original, ["#64748b"] * n, "Entrada original antes da divisão recursiva"),
        (f"2. Divisão em K = {k} Partições", original, None, "Array particionado em blocos balanceados"),
        ("3. Subvetores Ordenados (Pós-Recursão)", sub_sorted, None, "Cada partição foi recursivamente ordenada"),
        ("4. Mescla Final (K-Way Merge)", fully_sorted, ["#22c55e"] * n, "Intercalação das K partições em tempo O(n · k)")
    ]

    for idx, (title, data, custom_colors, subtitle) in enumerate(stages):
        ax = axes[idx]
        ax.set_facecolor("#1e293b")
        for spine in ax.spines.values():
            spine.set_color("#334155")
            spine.set_linewidth(1)

        # Determina cores por partição
        if custom_colors is not None:
            colors = custom_colors
        else:
            colors = []
            for i in range(n):
                for p_idx in range(k):
                    if particoes[p_idx] <= i < particoes[p_idx + 1]:
                        colors.append(PALETTE[p_idx % len(PALETTE)])
                        break

        x = np.arange(n)
        bars = ax.bar(x, data, color=colors, edgecolor="#0f172a", width=0.85, alpha=0.92)

        # Adiciona rótulos de valores no topo das barras
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 2, f"{int(h)}",
                    ha="center", va="bottom", fontsize=7.5, color="#cbd5e1", fontweight="bold")

        ax.set_title(f"{title}  —  {subtitle}", loc="left", fontsize=11, color="#38bdf8", pad=8, fontweight="semibold")
        ax.set_ylim(0, 115)
        ax.set_xlim(-0.8, n - 0.2)
        ax.set_xticks(x)
        ax.set_xticklabels([f"[{i}]" for i in range(n)], fontsize=7, color="#94a3b8")
        ax.tick_params(axis="y", labelsize=8, colors="#94a3b8")
        ax.grid(axis="y", linestyle="--", alpha=0.15, color="#ffffff")

        # Linhas divisórias entre as partições nas etapas 2 e 3
        if idx in (1, 2):
            for p in particoes[1:-1]:
                ax.axvline(p - 0.5, color="#f8fafc", linestyle=":", linewidth=1.5, alpha=0.7)

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Diagrama explicativo gerado com sucesso: {output_path}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/matplotlib_explanation.png"
    generate_explanation_diagram(out)
