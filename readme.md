##### Exemplo de conta:
programa
inteiro a, b, c;
decimal d;
escreva("Programa Teste");
escreva("Digite A");
leia(a);
escreva("Digite B");
leia(b);
se (a < b) {
    c = a + b;
} senao {
    c = a - b;
}
escreva("C e igual a ");
escreva(c);
d = c / (a + b);
escreva("D e igual a ");
escreva(d);
fimprog
##### If aninhado:
programa
inteiro x, y, z;
escreva("Digite o valor de X");
leia(x);
escreva("Digite o valor de Y");
leia(y);
se (x < y) {
    z = x + y;
    se (z > 10) {
        escreva("A soma é maior que 10");
    } senao {
        escreva("A soma é menor ou igual a 10");
    }
} senao {
    z = x - y;
    se (z < 0) {
        escreva("A diferença é negativa");
    } senao {
        escreva("A diferença é zero ou positiva");
    }
}
escreva("O valor de Z é");
escreva(z);
fimprog
##### Média numeros:
programa
decimal a, b, c;
escreva("Digite o valor de A");
leia(a);
escreva("Digite o valor de B");
leia(b);
c = a + b;
escreva("A soma de A e B é");
escreva(c);
c = a - b;
escreva("A diferença de A e B é");
escreva(c);
c = a * b;
escreva("O produto de A e B é");
escreva(c);
c = a / b;
escreva("A divisão de A por B é");
escreva(c);
fimprog

##### While loop:
programa
inteiro contador;
decimal soma;
contador = 0;
soma = 0.0;
enquanto (contador < 5) {
    decimal valor;
    escreva("Digite um valor");
    leia(valor);
    soma = soma + valor;
    contador = contador + 1;
}
escreva("A soma dos valores é");
escreva(soma);
fimprog

##### For loop:
programa
inteiro i, n;
decimal fatorial;
escreva("Digite um número para calcular o fatorial");
leia(n);
fatorial = 1.0;
para (i = 1; i <= n; i = i + 1) {
    fatorial = fatorial * i;
}
escreva("O fatorial de ");
escreva(n);
escreva(" é ");
escreva(fatorial);
fimprog