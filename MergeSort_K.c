/*
Código do slide para se basear:
Mudanças: Ao inves de dividir em 5 partições, dividir em k partições

mergesort_5(A, i, f){
    if(f – i > 4){
        d = (f-i)/5; //delta

    mergesort_5(A, i, i+d);
    mergesort_5(A, i+d+1, i+2d);
    mergesort_5(A, i+2d+1, I+3d);
    mergesort_5(A, i+3d+1, I+4d);
    mergesort_5(A, i+4d+1, f);
    merge_5(A, i, f, d);
    }
}

Algoritmo de divisão e conquista
*/

#include <stdio.h>
#include <stdlib.h>
#include <limits.h> // Para usar o INT_MAX

/*
A[]: Vetor a ser ordenado
i: Índice inicial do vetor
f: Índice final do vetor
particao[]: Array com os índices de início de cada partição
k: Número de partições
*/
void merge(int A[], int i, int f, int particao[], int k)
{
    // Array temporário para armazenar a combinação das partições
    int *temp = (int *)malloc((f - i) * sizeof(int)); // f - i = número de elementos
    if(temp == NULL)
    {
        printf("Erro de alocação de memória\n");
        exit(1);
    }

    /*
    Aloca memória para um array que armazenará os índices atuais de cada partição
    Esse array é necessário para saber qual o próximo elemento a ser comparado em cada partição
    */
    int *indice_atual = (int *)malloc(k * sizeof(int));
    if(indice_atual == NULL)
    {
        printf("Erro de alocação de memória\n");
        exit(1);
    }

    // Inicializa os índices atuais de cada partição com os valores fonrcidos no array particao
    for (int j = 0; j < k; j++)
    {
        indice_atual[j] = particao[j];
    }

    int temp_index = 0; // Índice do array temporário

    /*
    Combina as partições ordenadas
    while (1) é um loop infinito que só é interrompido quando todas as partições foram totalmente percorridas
    */
    while (1)
    {
        int min_valor = INT_MAX; // Valor mínimo encontrado
        int min_indice = -1;     // Índice da partição com o menor valor

        /*
        Encontra o menor elemento entre as k partições
        1. Percorre cada partição
        2. Verifica se a partição não foi totalmente percorrida e se o valor atual é menor que o mínimo encontrado
        3. Atualiza o valor mínimo e o índice da partição com o menor valor
        */
        for (int j = 0; j < k; j++)
        {
            if (indice_atual[j] < particao[j + 1] && A[indice_atual[j]] < min_valor)
            {
                min_valor = A[indice_atual[j]];
                min_indice = j;
            }
        }

        if (min_indice == -1)
            break; // Se não encontrou nenhum valor, termina

        // Inserir o menor valor atual na posição correta do array temporário e avançando o índice para a próxima posição
        temp[temp_index++] = min_valor;

        // Avança o índice da partição de onde o menor valor foi extraído
        indice_atual[min_indice]++;
    }

    /*
    1. Percorre o array temporário até o índice temp_index (número de elementos)
    2. Copia os elementos de volta para o array original A
    */
    for (int idx = 0; idx < temp_index; idx++)
    {
        A[i + idx] = temp[idx];
    }

    // Libera a memória alocada
    free(temp);
    free(indice_atual);
}

/*
n: número de elementos do vetor
k: número de partições
i: índice inicial (para a função mergesort_k) ou 0 (para a função print_subvetores)
Retorna um array de inteiros com os índices de início de cada partição.
*/
int *calcula_particoes(int n, int k, int i)
{
    int tam_base = n / k; // Tamanho base de cada partição
    int extra = n % k;    // Número de partições com tamanho extra

    // Aloca memória para o array de partições
    int *particao = (int *)malloc((k + 1) * sizeof(int)); // k + 1 para o último índice
    if(particao == NULL)
    {
        printf("Erro de alocação de memória\n");
        exit(1);
    }

    particao[0] = i; // O primeiro índice é o início da partição

    /*
    Calcula os índices de início de cada partição
    1. Percorre cada partição
    2. Calcula o tamanho da partição (tamanho base + 1 se houver partição extra)
    3. Calcula o índice de início da partição
    */
    for (int j = 0; j < k; j++)
    {
        int size = tam_base + (j < extra ? 1 : 0);
        particao[j + 1] = particao[j] + size;
    }

    // Retorna um array onde cada elemento indica o início de uma partição
    return particao;
}

/*
A[]: Vetor a ser ordenado
i: Índice inicial do vetor
f: Índice final do vetor
k: Número de partições em que o array deve ser dividido
*/
void mergesort_k(int A[], int i, int f, int k)
{
    // Se k == 1, não há necessidade de dividir, podemos usar o merge sort normal
    if (k == 1)
    {
        // Se a diferença entre os índices for maior que 1 (ou seja, se houver mais de um elemento)
        if (i < f - 1)
        {
            int meio = (i + f) / 2;                 // Calcula o índice do meio
            mergesort_k(A, i, meio, k);             // Chama recursivamente mergesort_k para a partição à esquerda
            mergesort_k(A, meio, f, k);             // Chama recursivamente mergesort_k para a partição à direita
            merge(A, i, f, (int[]){i, meio, f}, 2); // Mesclando duas partições (à esquerda e à direita)
        }
    }
    else if ((f - i) > 1)
    {
        // Se a diferença entre os índices for maior que 1
        int n = f - i; // Número de elementos na partição
        int *particao = calcula_particoes(n, k, i); // Chama a função calcula_particoes para determinar os índices de k partições

        // Chama recursivamente mergesort_k para cada uma das k partições
        for (int j = 0; j < k; j++)
        {
            mergesort_k(A, particao[j], particao[j + 1], k);
        }

        // Combina as partições ordenadas
        merge(A, i, f, particao, k);

        free(particao); // Libera a memória alocada para partição
    }
}

/*
A[]: Vetor a ser impresso
n: Número de elementos do vetor
k: Número de partições

Printa os subvetores iniciais
*/
void print_subvetores(int A[], int n, int k)
{
    // Chama a função calcula_particoes para determinar os índices de k partições
    int *particao = calcula_particoes(n, k, 0);

    // Se k for igual a 1, só vai ser printado uma partição, se não, será printado k partições
    if (k == 1)
    {
        printf("Subvetor dividido em 1 partição:\n");
    }
    else
    {
        printf("Subvetores divididos em %d partições:\n", k);
    }

    for (int j = 0; j < k; j++)
    {
        printf("Subvetor inicial %d: ", j + 1);
        for (int l = particao[j]; l < particao[j + 1]; l++)
        {
            printf("[%d] ", A[l]);
        }
        printf("\n");
    }

    free(particao); // Libera a memória alocada para partição
}

int main()
{
    printf("----------------------ALGORITMO MERGESORT COM K PARTIÇÕES----------------------\n");
    int n, k;

    // Entrada do vetor
    printf("Digite o número de elementos do vetor: ");
    scanf("%d", &n);

    // Aloca memória para o vetor e verificação de erro
    int *A = (int *)malloc(n * sizeof(int));
    if (A == NULL)
    {
        printf("Erro de alocação de memória.\n");
        return 1;
    }

    // Preenche o vetor
    printf("Digite o vetor, separado por espaços: ");
    for (int i = 0; i < n; ++i)
    {
        scanf("%d", &A[i]);
    }

    /*
    Entrada do número de partições k
    Se for menor ou igual a 0, ou maior que n, pede para digitar novamente
    */
    do
    {
        printf("Digite o número de partições (k): ");
        scanf("%d", &k);

        if (k <= 0)
        {
            printf("O número de partições deve ser maior que 0.\n");
            printf("--------------------------------------------\n");
        }
        else if (k > n)
        {
            printf("O número de partições deve ser menor ou igual ao número de elementos do vetor.\n");
            printf("--------------------------------------------\n");
        }
    } while (k <= 0 || k > n);

    printf("--------------------------------------------\n");

    // Imprime os subvetores iniciais
    print_subvetores(A, n, k);

    // Chama o Merge Sort com k partições
    mergesort_k(A, 0, n, k);

    printf("--------------------------------------------\n");

    // Exibe o vetor ordenado
    printf("Vetor ordenado: \n");
    for (int i = 0; i < n; ++i)
    {
        printf("[%d] ", A[i]);
    }
    printf("\n");

    free(A);
    return 0;
}
