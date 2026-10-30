# AV3 — Métodos Numéricos

Trabalho da disciplina de Métodos Numéricos, desenvolvido em Python para resolver questões das notas de aula e acompanhar os cálculos passo a passo.

Até agora, estão prontos os métodos da **Bisseção**, de **Newton** e de **Euler**. Bisseção e Newton mostram as iterações, o erro relativo e a raiz encontrada. No Newton, a derivada é calculada automaticamente com o SymPy. Euler mostra a aproximação da solução de uma equação diferencial em cada passo.

Para executar, com o Python 3 instalado:

```bash
pip install -r requirements.txt
python main.py
```

Escolha o método no menu e informe os dados da questão. Exemplo:

```text
Função: x^3 - 2x^2 - 5
Intervalo: [1, 4]
Tolerância: 10^-4
```

Use ponto nos decimais, como `0.0001`. No Newton, também é possível informar apenas o ponto inicial; ao informar um intervalo, o programa usa o ponto médio. As funções `sen`, `cos` e `tan` usam radianos.

Os intervalos podem ser escritos com ou sem colchetes: `0,1` ou `[0, 1]`. A vírgula separa os extremos; para extremos decimais, use ponto: `1.2,2`.

Expressões como `cos2t + sen3t` também são aceitas e significam `cos(2*t) + sen(3*t)`. Para argumentos mais longos, use parênteses, como `sen(2*t + 1)`.

Os demais métodos pedidos no trabalho ainda serão adicionados.

Para Euler, escolha a opção `3` e informe `f(t, y)`, o intervalo, a condição inicial e o passo `h`. Exemplo: função `cos2t + sen3t`, intervalo `[0, 1]`, condição inicial `1` e `h = 0.25`. O programa calcula `N = (b - a)/h` e mostra cada passo, além da linha inicial. O passo deve dividir o intervalo em partes iguais; Euler não usa tolerância de parada.
