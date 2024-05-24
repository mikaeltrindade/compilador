#include <stdio.h>
int main() {
    int i, n;
    double fatorial;
    printf("Digite um número para calcular o fatorial");
    scanf("%d", &n);
    fatorial = 1.0;
    for (None; (i <= n); None) {
        fatorial = (fatorial * i);
    }
    printf("O fatorial de ");
    printf("%d\n", n);
    printf(" é ");
    printf("%lf\n", fatorial);
    return 0;
}