/**
 * @file mergesort_k.c
 * @brief Implementação modular e robusta do K-Way Merge Sort.
 */

#include "mergesort_k.h"
#include <stdlib.h>
#include <stdio.h>
#include <limits.h>

void calcula_particoes_buffer(int n, int k, int i, int particao_out[])
{
    if (k <= 0 || n <= 0) {
        particao_out[0] = i;
        return;
    }

    int tam_base = n / k;
    int extra = n % k;

    particao_out[0] = i;
    for (int j = 0; j < k; j++) {
        int size = tam_base + (j < extra ? 1 : 0);
        particao_out[j + 1] = particao_out[j] + size;
    }
}

/**
 * @brief Mescla k partições ordenadas adjacentes em um único intervalo [i, f).
 */
static void merge_internal(
    int A[],
    int total_n,
    int i,
    int f,
    const int particao[],
    int k,
    VisualizerCallback cb,
    void *user_data,
    SortStats *stats
) {
    int total_elementos = f - i;
    if (total_elementos <= 1 || k <= 1) {
        return;
    }

    int *temp = (int *)malloc(total_elementos * sizeof(int));
    int *indice_atual = (int *)malloc(k * sizeof(int));

    if (!temp || !indice_atual) {
        fprintf(stderr, "Erro: Falha na alocação de memória no merge.\n");
        free(temp);
        free(indice_atual);
        exit(EXIT_FAILURE);
    }

    for (int j = 0; j < k; j++) {
        indice_atual[j] = particao[j];
    }

    if (stats) stats->merges++;

    int temp_index = 0;

    // K-way merge: busca o menor elemento ativo entre as k partições
    while (1) {
        int min_valor = INT_MAX;
        int min_particao = -1;

        for (int j = 0; j < k; j++) {
            // Se a partição j ainda tem elementos
            if (indice_atual[j] < particao[j + 1]) {
                if (stats) stats->comparisons++;

                if (min_particao == -1 || A[indice_atual[j]] < min_valor) {
                    min_valor = A[indice_atual[j]];
                    min_particao = j;
                }
            }
        }

        // Se todas as partições foram esgotadas
        if (min_particao == -1) {
            break;
        }

        temp[temp_index++] = min_valor;
        indice_atual[min_particao]++;
        if (stats) stats->moves++;
    }

    // Copia os elementos ordenados de volta para o vetor original A
    for (int idx = 0; idx < temp_index; idx++) {
        A[i + idx] = temp[idx];
        if (stats) stats->moves++;

        // Notifica visualizador de atualização periódica no vetor durante o merge
        if (cb) {
            cb(A, total_n, i, i + idx + 1, particao, k, "Copiando elemento mesclado de volta para o vetor", user_data);
        }
    }

    free(temp);
    free(indice_atual);
}

/**
 * @brief Função recursiva principal para o K-Way Merge Sort.
 */
static void mergesort_recursive(
    int A[],
    int total_n,
    int i,
    int f,
    int k,
    VisualizerCallback cb,
    void *user_data,
    SortStats *stats
) {
    int n = f - i;

    // Caso base: 0 ou 1 elemento já está ordenado
    if (n <= 1) {
        return;
    }

    // Caso especial k=1: divide ao meio (Merge Sort binário padrão)
    if (k == 1) {
        int meio = i + n / 2;
        mergesort_recursive(A, total_n, i, meio, 1, cb, user_data, stats);
        mergesort_recursive(A, total_n, meio, f, 1, cb, user_data, stats);

        int particao2[3] = {i, meio, f};
        if (cb) {
            cb(A, total_n, i, f, particao2, 2, "Mesclando 2 partições", user_data);
        }
        merge_internal(A, total_n, i, f, particao2, 2, cb, user_data, stats);
        return;
    }

    // Ajusta o número efetivo de partições para não exceder a quantidade de elementos
    int effective_k = (k > n) ? n : k;

    int *particao = (int *)malloc((effective_k + 1) * sizeof(int));
    if (!particao) {
        fprintf(stderr, "Erro de alocação de memória para partições.\n");
        exit(EXIT_FAILURE);
    }

    calcula_particoes_buffer(n, effective_k, i, particao);

    if (cb) {
        cb(A, total_n, i, f, particao, effective_k, "Dividindo intervalo em K partições", user_data);
    }

    // Chamadas recursivas para cada uma das k partições
    for (int j = 0; j < effective_k; j++) {
        mergesort_recursive(A, total_n, particao[j], particao[j + 1], k, cb, user_data, stats);
    }

    if (cb) {
        cb(A, total_n, i, f, particao, effective_k, "Iniciando mescla das K partições", user_data);
    }

    // Mescla as k partições
    merge_internal(A, total_n, i, f, particao, effective_k, cb, user_data, stats);

    if (cb) {
        cb(A, total_n, i, f, NULL, 0, "Subvetor mesclado e ordenado", user_data);
    }

    free(particao);
}

void mergesort(int A[], int n, int k)
{
    if (!A || n <= 1) return;
    if (k <= 0) k = 2; // fallback padrão seguro
    mergesort_recursive(A, n, 0, n, k, NULL, NULL, NULL);
}

void mergesort_k_bounds(int A[], int i, int f, int k, SortStats *stats)
{
    if (!A || (f - i) <= 1) return;
    if (k <= 0) k = 2;
    if (stats) {
        stats->comparisons = 0;
        stats->moves = 0;
        stats->merges = 0;
    }
    mergesort_recursive(A, f, i, f, k, NULL, NULL, stats);
}

void mergesort_k_visual(
    int A[],
    int n,
    int k,
    VisualizerCallback cb,
    void *user_data,
    SortStats *stats
) {
    if (!A || n <= 1) return;
    if (k <= 0) k = 2;
    if (stats) {
        stats->comparisons = 0;
        stats->moves = 0;
        stats->merges = 0;
    }
    mergesort_recursive(A, n, 0, n, k, cb, user_data, stats);
}

