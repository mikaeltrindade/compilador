#include <iostream>
using namespace std;
int main() {
    double a, b, c;
    cout << "Digite o valor de A" << endl;
    cin >> a;
    cout << "Digite o valor de B" << endl;
    cin >> b;
    c = (a + b);
    cout << "A soma de A e B é" << endl;
    cout << c << endl;
    c = (a - b);
    cout << "A diferença de A e B é" << endl;
    cout << c << endl;
    c = (a * b);
    cout << "O produto de A e B é" << endl;
    cout << c << endl;
    c = (a / b);
    cout << "A divisão de A por B é" << endl;
    cout << c << endl;
    return 0;
}