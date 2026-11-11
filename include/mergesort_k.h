/**
 * @file mergesort_k.h
 * @brief Algoritmo K-Way Merge Sort (Merge Sort com K partições)
 * 
 * Implementação parametrizada do Merge Sort capaz de dividir o vetor
 * em K partições balanceadas a cada nível da recursão.
 */

#ifndef MERGESORT_K_H
#define MERGESORT_K_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Estatísticas coletadas durante a ordenação.
 */
typedef struct {
    long long comparisons;  /**< Número total de comparações entre elementos */
    long long moves;        /**< Número de movimentações/cópias de elementos */
    long long merges;       /**< Número de operações de intercalação (merge) */
} SortStats;

/**
 * @brief Assinatura do callback de visualização / monitoramento de passos.
 * 
 * @param A Array completo em seu estado atual.
 * @param n Tamanho total do array A.
 * @param start Índice inicial do intervalo sendo processado atualmente.
 * @param end Índice final (exclusivo) do intervalo sendo processado.
 * @param particao Array com os limites das k partições (tamanho k+1), ou NULL se não aplicável.
 * @param k Número de partições ativas.
 * @param action_desc Descrição textual do passo atual.
 * @param user_data Ponteiro opcional de contexto do usuário.
 */
typedef void (*VisualizerCallback)(
    const int A[],
    int n,
    int start,
    int end,
    const int particao[],
    int k,
    const char *action_desc,
    void *user_data
);

/**
 * @brief Ordena um vetor de inteiros usando K-Way Merge Sort.
 * 
 * @param A Vetor a ser ordenado.
 * @param n Número de elementos no vetor.
 * @param k Número de partições a cada divisão recursiva (deve ser >= 1).
 */
void mergesort(int A[], int n, int k);

/**
 * @brief Versão do K-Way Merge Sort com limites explícitos e coleta de estatísticas.
 * 
 * @param A Vetor a ser ordenado.
 * @param i Índice inicial (inclusivo).
 * @param f Índice final (exclusivo).
 * @param k Número de partições.
 * @param stats Ponteiro para estrutura de estatísticas (pode ser NULL).
 */
void mergesort_k_bounds(int A[], int i, int f, int k, SortStats *stats);

/**
 * @brief Versão do K-Way Merge Sort com suporte a callback passo-a-passo para visualização.
 * 
 * @param A Vetor a ser ordenado.
 * @param n Número total de elementos.
 * @param k Número de partições.
 * @param cb Função de callback chamada a cada etapa relevante.
 * @param user_data Ponteiro opcional passado ao callback.
 * @param stats Ponteiro para coletar estatísticas (pode ser NULL).
 */
void mergesort_k_visual(
    int A[],
    int n,
    int k,
    VisualizerCallback cb,
    void *user_data,
    SortStats *stats
);

/**
 * @brief Calcula as fronteiras das k partições balanceadas para um intervalo.
 * 
 * @param n Tamanho do intervalo (f - i).
 * @param k Número de partições desejadas.
 * @param i Índice inicial no vetor original.
 * @param particao_out Array pré-alocado de tamanho mínimo (k + 1) onde serão gravados os índices.
 */
void calcula_particoes_buffer(int n, int k, int i, int particao_out[]);

#ifdef __cplusplus
}
#endif

#endif /* MERGESORT_K_H */
