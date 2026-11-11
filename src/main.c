/**
 * @file main.c
 * @brief Interface de linha de comando para o K-Way Merge Sort em C.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "mergesort_k.h"

static void print_vetor(const char *label, const int A[], int n) {
    printf("%s: [", label);
    for (int i = 0; i < n; i++) {
        printf("%d%s", A[i], (i == n - 1) ? "" : ", ");
    }
    printf("]\n");
}

static void print_ajuda(const char *prog) {
    printf("Uso: %s [OPCOES]\n\n", prog);
    printf("Opções:\n");
    printf("  -n <tamanho>     Número de elementos no vetor (padrão: 20)\n");
    printf("  -k <particoes>   Número de partições a cada divisão (padrão: 3)\n");
    printf("  -r               Gera valores aleatórios automaticamente\n");
    printf("  -b               Executa benchmark comparando diferentes valores de K\n");
    printf("  -h, --help       Exibe esta mensagem de ajuda\n\n");
}

static void executar_benchmark(int n) {
    int k_testes[] = {2, 3, 4, 5, 8, 10};
    int num_k = sizeof(k_testes) / sizeof(k_testes[0]);

    printf("\n=== BENCHMARK K-WAY MERGE SORT (N = %d elementos) ===\n", n);
    printf("%-6s | %-15s | %-15s | %-12s | %-12s\n", "K", "Comparacoes", "Movimentacoes", "Merges", "Tempo (ms)");
    printf("-----------------------------------------------------------------------\n");

    for (int idx = 0; idx < num_k; idx++) {
        int k = k_testes[idx];
        if (k > n) continue;

        int *arr = (int *)malloc(n * sizeof(int));
        for (int i = 0; i < n; i++) {
            arr[i] = rand() % 100000;
        }

        SortStats stats;
        clock_t t0 = clock();
        mergesort_k_bounds(arr, 0, n, k, &stats);
        clock_t t1 = clock();
        double ms = ((double)(t1 - t0) / CLOCKS_PER_SEC) * 1000.0;

        printf("%-6d | %-15lld | %-15lld | %-12lld | %-12.3f\n",
               k, stats.comparisons, stats.moves, stats.merges, ms);

        free(arr);
    }
    printf("-----------------------------------------------------------------------\n\n");
}

int main(int argc, char *argv[]) {
    int n = 0;
    int k = 0;
    int modo_aleatorio = 0;
    int modo_benchmark = 0;

    srand((unsigned int)time(NULL));

    // Parse de argumentos
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-n") == 0 && i + 1 < argc) {
            n = atoi(argv[++i]);
        } else if (strcmp(argv[i], "-k") == 0 && i + 1 < argc) {
            k = atoi(argv[++i]);
        } else if (strcmp(argv[i], "-r") == 0) {
            modo_aleatorio = 1;
        } else if (strcmp(argv[i], "-b") == 0) {
            modo_benchmark = 1;
        } else if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_ajuda(argv[0]);
            return 0;
        }
    }

    if (modo_benchmark) {
        if (n <= 0) n = 100000;
        executar_benchmark(n);
        return 0;
    }

    // Modo interativo caso argumentos não tenham sido fornecidos
    if (n <= 0) {
        printf("------------------------------------------------------------------\n");
        printf("            ALGORITMO K-WAY MERGE SORT (EM LINGUAGEM C)           \n");
        printf("------------------------------------------------------------------\n");
        printf("Digite o tamanho do vetor (N): ");
        if (scanf("%d", &n) != 1 || n <= 0) {
            fprintf(stderr, "Tamanho inválido.\n");
            return 1;
        }
    }

    int *A = (int *)malloc(n * sizeof(int));
    if (!A) {
        fprintf(stderr, "Erro de alocação de memória.\n");
        return 1;
    }

    if (modo_aleatorio) {
        for (int i = 0; i < n; i++) {
            A[i] = rand() % 100;
        }
    } else {
        printf("Deseja preencher com valores aleatórios? (1=Sim, 0=Digitar manualmente): ");
        int opcao = 1;
        if (scanf("%d", &opcao) == 1 && opcao == 1) {
            for (int i = 0; i < n; i++) {
                A[i] = rand() % 100;
            }
        } else {
            printf("Digite os %d números separados por espaço:\n", n);
            for (int i = 0; i < n; i++) {
                if (scanf("%d", &A[i]) != 1) {
                    fprintf(stderr, "Entrada inválida.\n");
                    free(A);
                    return 1;
                }
            }
        }
    }

    if (k <= 0) {
        do {
            printf("Digite o número de partições (K) [2..%d]: ", n);
            if (scanf("%d", &k) != 1) {
                fprintf(stderr, "Entrada inválida.\n");
                free(A);
                return 1;
            }
            if (k <= 0 || k > n) {
                printf("K deve ser entre 1 e %d.\n", n);
            }
        } while (k <= 0 || k > n);
    }

    printf("\n");
    print_vetor("Vetor Original", A, n);

    SortStats stats;
    clock_t inicio = clock();
    mergesort_k_bounds(A, 0, n, k, &stats);
    clock_t fim = clock();
    double ms = ((double)(fim - inicio) / CLOCKS_PER_SEC) * 1000.0;

    print_vetor("Vetor Ordenado ", A, n);

    printf("\n=== Estatísticas da Execução ===\n");
    printf("Elementos (N):       %d\n", n);
    printf("Partições (K):       %d\n", k);
    printf("Comparações:         %lld\n", stats.comparisons);
    printf("Movimentações:       %lld\n", stats.moves);
    printf("Merges executados:   %lld\n", stats.merges);
    printf("Tempo total:         %.4f ms\n", ms);
    printf("================================\n\n");

    free(A);
    return 0;
}

