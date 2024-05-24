if __name__ == '__main__':
    i = 0
    n = 0
    fatorial = 0.0
    print("Digite um número para calcular o fatorial")
    n = float(input())
    fatorial = 1.0
    i = 1
    while (i <= n):
        fatorial = (fatorial * i)
        i = (i + 1)
    print("O fatorial de ")
    print(n)
    print(" é ")
    print(fatorial)