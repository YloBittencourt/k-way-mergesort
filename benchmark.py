"""
Script de Benchmark e Análise de Desempenho do K-Way Merge Sort.
Avalia o impacto do número de partições K no tempo de execução e número de operações,
gerando gráficos comparativos com Matplotlib.
"""

import sys
import os
import time
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List, Dict
from k_way_mergesort import k_way_mergesort


def run_benchmark(sizes: List[int], k_values: List[int], trials: int = 3) -> Dict[int, List[float]]:
    """Mede o tempo médio de execução para diferentes valores de N e K."""
    results = {k: [] for k in k_values}

    for n in sizes:
        print(f"Executando benchmark para N = {n}...")
        for k in k_values:
            durations = []
            for _ in range(trials):
                arr = [random.randint(1, 1_000_000) for _ in range(n)]
                t0 = time.perf_counter()
                k_way_mergesort(arr, k=k)
                t1 = time.perf_counter()
                durations.append(t1 - t0)

            avg_time = sum(durations) / len(durations)
            results[k].append(avg_time * 1000)  # Converte para milissegundos

    return results


def plot_benchmark_results(sizes: List[int], results: Dict[int, List[float]], output_path: str = "assets/benchmark_comparison.png"):
    """Gera o gráfico comparativo de desempenho."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#0f172a")
    ax.set_facecolor("#1e293b")

    colors = ["#38bdf8", "#10b981", "#f59e0b", "#a855f7", "#f43f5e"]
    markers = ["o", "s", "^", "D", "v"]

    for idx, (k, times) in enumerate(results.items()):
        color = colors[idx % len(colors)]
        marker = markers[idx % len(markers)]
        ax.plot(sizes, times, label=f"K = {k} partições", color=color,
                marker=marker, linewidth=2.2, markersize=7)

    ax.set_title("Benchmark K-Way Merge Sort: Tempo de Execução vs Tamanho do Vetor (N)",
                 fontsize=13, fontweight="bold", color="#f8fafc", pad=15)
    ax.set_xlabel("Número de Elementos (N)", fontsize=11, color="#cbd5e1", labelpad=10)
    ax.set_ylabel("Tempo Médio (milissegundos)", fontsize=11, color="#cbd5e1", labelpad=10)

    ax.grid(True, linestyle="--", alpha=0.2, color="#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#334155")

    ax.tick_params(colors="#94a3b8")
    ax.legend(facecolor="#0f172a", edgecolor="#334155", fontsize=10, labelcolor="#f8fafc")

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Gráfico de benchmark gerado: {output_path}")


if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "assets/benchmark_comparison.png"
    sample_sizes = [1000, 5000, 10000, 20000, 35000]
    test_k_values = [2, 3, 5, 8]

    print("Iniciando bateria de testes comparativos...")
    res = run_benchmark(sample_sizes, test_k_values, trials=2)
    plot_benchmark_results(sample_sizes, res, out_file)

