/**
 * @file test_mergesort.c
 * @brief Bateria de testes unitários automatizados para o K-Way Merge Sort.
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "mergesort_k.h"

static int is_sorted(const int A[], int n) {
    for (int i = 0; i < n - 1; i++) {
        if (A[i] > A[i + 1]) return 0;
    }
    return 1;
}

static void test_casos_borda() {
    printf("[TEST] Casos de borda (vazio, 1 elemento, 2 elementos)...\n");
    int empty[] = {0};
    mergesort(empty, 0, 3);

    int single[] = {42};
    mergesort(single, 1, 3);
    assert(single[0] == 42);

    int pair[] = {9, 2};
    mergesort(pair, 2, 2);
    assert(is_sorted(pair, 2));
    printf("  -> OK!\n");
}

static void test_vetores_ordenados_e_invertidos() {
    printf("[TEST] Vetores já ordenados e invertidos...\n");
    int sorted[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    mergesort(sorted, 10, 3);
    assert(is_sorted(sorted, 10));

    int reversed[] = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
    mergesort(reversed, 10, 4);
    assert(is_sorted(reversed, 10));
    printf("  -> OK!\n");
}

static void test_elementos_duplicados() {
    printf("[TEST] Vetor com elementos duplicados e todos iguais...\n");
    int identical[] = {5, 5, 5, 5, 5, 5, 5};
    mergesort(identical, 7, 3);
    assert(is_sorted(identical, 7));

    int duplicates[] = {4, 2, 4, 1, 3, 2, 1, 4, 3};
    mergesort(duplicates, 9, 3);
    assert(is_sorted(duplicates, 9));
    printf("  -> OK!\n");
}

static void test_variacoes_de_k() {
    printf("[TEST] Variações de K (k=1, k=2, k=3, k=5, k=11, k > n)...\n");
    int n = 37; // Número primo
    int *A = (int *)malloc(n * sizeof(int));

    int k_values[] = {1, 2, 3, 5, 7, 11, n, n + 5};
    for (size_t i = 0; i < sizeof(k_values) / sizeof(k_values[0]); i++) {
        int k = k_values[i];
        for (int j = 0; j < n; j++) {
            A[j] = rand() % 500;
        }
        mergesort(A, n, k);
        assert(is_sorted(A, n));
    }

    free(A);
    printf("  -> OK!\n");
}

int main() {
    printf("===========================================\n");
    printf("   EXECUTANDO TESTES UNITÁRIOS (C ENGINE)  \n");
    printf("===========================================\n");

    test_casos_borda();
    test_vetores_ordenados_e_invertidos();
    test_elementos_duplicados();
    test_variacoes_de_k();

    printf("\n>>> TODOS OS TESTES PASSARAM COM SUCESSO! <<<\n");
    return 0;
}
