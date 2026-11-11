"""
Módulo com a implementação do K-Way Merge Sort (Merge Sort com K partições).

Fornece tanto a versão direta (algorítmica rápida) quanto a versão geradora (yield),
ideal para animações em tempo real (Pygame, Matplotlib, Web).
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Generator, Optional, Dict


@dataclass
class SortStats:
    comparisons: int = 0
    moves: int = 0
    merges: int = 0


@dataclass
class AnimationStep:
    """Representa um snapshot do estado da ordenação para renderização visual."""
    arr: List[int]
    start: int
    end: int
    partitions: List[Tuple[int, int]] = field(default_factory=list)
    active_indices: List[int] = field(default_factory=list)
    selected_idx: Optional[int] = None
    phase: str = ""
    description: str = ""
    stats: SortStats = field(default_factory=SortStats)


def calcula_particoes(n: int, k: int, start: int = 0) -> List[int]:
    """
    Calcula as fronteiras das k partições balanceadas.
    Retorna uma lista de índices de tamanho k + 1.
    """
    if k <= 0 or n <= 0:
        return [start, start + n]
    
    tam_base = n // k
    extra = n % k
    particoes = [start]
    
    for j in range(k):
        size = tam_base + (1 if j < extra else 0)
        particoes.append(particoes[-1] + size)
        
    return particoes


def k_way_mergesort(arr: List[int], k: int = 2) -> List[int]:
    """
    Versão algorítmica direta do K-Way Merge Sort.
    Ordena e retorna uma nova lista ordenada.
    """
    arr_copy = list(arr)
    _k_way_mergesort_inplace(arr_copy, 0, len(arr_copy), k)
    return arr_copy


def _k_way_mergesort_inplace(arr: List[int], i: int, f: int, k: int):
    n = f - i
    if n <= 1:
        return

    if k <= 1:
        k = 2  # Fallback seguro para divisão binária

    effective_k = min(k, n)
    particoes = calcula_particoes(n, effective_k, i)

    # Ordena recursivamente cada uma das partições
    for j in range(effective_k):
        _k_way_mergesort_inplace(arr, particoes[j], particoes[j + 1], k)

    # Intercala as partições
    _merge_inplace(arr, i, f, particoes, effective_k)


def _merge_inplace(arr: List[int], i: int, f: int, particoes: List[int], k: int):
    indices = [particoes[j] for j in range(k)]
    temp = []

    while True:
        min_val = float('inf')
        min_p = -1

        for j in range(k):
            if indices[j] < particoes[j + 1]:
                val = arr[indices[j]]
                if val < min_val:
                    min_val = val
                    min_p = j

        if min_p == -1:
            break

        temp.append(min_val)
        indices[min_p] += 1

    for idx, val in enumerate(temp):
        arr[i + idx] = val


def k_way_mergesort_visual(arr: List[int], k: int = 3) -> Generator[AnimationStep, None, None]:
    """
    Gerador passo-a-passo para K-Way Merge Sort.
    Gera instâncias de AnimationStep a cada etapa relevante.
    """
    arr_state = list(arr)
    stats = SortStats()
    n = len(arr_state)

    if n <= 1:
        yield AnimationStep(
            arr=list(arr_state),
            start=0,
            end=n,
            phase="DONE",
            description="Vetor já ordenado.",
            stats=stats
        )
        return

    def recursive_visual(i: int, f: int, current_k: int) -> Generator[AnimationStep, None, None]:
        range_n = f - i
        if range_n <= 1:
            return

        effective_k = 2 if current_k <= 1 else min(current_k, range_n)
        particoes = calcula_particoes(range_n, effective_k, i)
        partition_pairs = [(particoes[j], particoes[j + 1]) for j in range(effective_k)]

        yield AnimationStep(
            arr=list(arr_state),
            start=i,
            end=f,
            partitions=partition_pairs,
            phase="DIVIDE",
            description=f"Dividindo intervalo [{i}:{f}] em {effective_k} partições",
            stats=stats
        )

        # Recursão para cada partição
        for j in range(effective_k):
            yield from recursive_visual(particoes[j], particoes[j + 1], current_k)

        # Início do Merge das k partições
        stats.merges += 1
        indices = [particoes[j] for j in range(effective_k)]
        temp = []

        yield AnimationStep(
            arr=list(arr_state),
            start=i,
            end=f,
            partitions=partition_pairs,
            active_indices=list(indices),
            phase="MERGE_START",
            description=f"Iniciando mescla de {effective_k} partições ordenadas",
            stats=stats
        )

        while True:
            min_val = float('inf')
            min_p = -1

            for j in range(effective_k):
                if indices[j] < particoes[j + 1]:
                    stats.comparisons += 1
                    val = arr_state[indices[j]]
                    if val < min_val:
                        min_val = val
                        min_p = j

            if min_p == -1:
                break

            chosen_idx = indices[min_p]
            stats.moves += 1
            temp.append(min_val)
            indices[min_p] += 1

            yield AnimationStep(
                arr=list(arr_state),
                start=i,
                end=f,
                partitions=partition_pairs,
                active_indices=list(indices),
                selected_idx=chosen_idx,
                phase="COMPARE_MIN",
                description=f"Menor elemento atual: {min_val} (Partição {min_p + 1})",
                stats=stats
            )

        # Grava de volta no vetor original com atualização visual
        for idx, val in enumerate(temp):
            arr_state[i + idx] = val
            stats.moves += 1

            yield AnimationStep(
                arr=list(arr_state),
                start=i,
                end=f,
                partitions=partition_pairs,
                selected_idx=i + idx,
                phase="WRITE_BACK",
                description=f"Posicionando elemento mesclado {val} na posição {i + idx}",
                stats=stats
            )

        yield AnimationStep(
            arr=list(arr_state),
            start=i,
            end=f,
            partitions=[],
            phase="MERGE_DONE",
            description=f"Intervalo [{i}:{f}] mesclado com sucesso",
            stats=stats
        )

    yield from recursive_visual(0, n, k)

    yield AnimationStep(
        arr=list(arr_state),
        start=0,
        end=n,
        partitions=[],
        phase="DONE",
        description="Ordenação concluída com sucesso!",
        stats=stats
    )
