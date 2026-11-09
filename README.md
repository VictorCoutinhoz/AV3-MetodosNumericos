# AV3 — Métodos Numéricos

Trabalho da disciplina de Métodos Numéricos, desenvolvido em Python para resolver questões das notas de aula e acompanhar os cálculos passo a passo.

## Métodos disponíveis

| Opção | Método | O que faz |
| :---: | --- | --- |
| 1 | Bisseção | Encontra uma raiz dividindo o intervalo ao meio. |
| 2 | Newton | Encontra uma raiz usando regras de derivação programadas no projeto. |
| 3 | Euler | Aproxima a solução de uma equação diferencial passo a passo. |
| 4 | Ponto médio | Runge-Kutta de segunda ordem com a inclinação no meio do passo. |
| 5 | Euler modificado | Runge-Kutta de segunda ordem com a média de duas inclinações. |

As contas aparecem em tabelas. Bisseção e Newton também mostram o erro relativo entre as aproximações.

## Como executar

Com o **Python 3.9 ou superior** instalado, rode no terminal (não precisa instalar bibliotecas):

```bash
python main.py
```

Depois, escolha o método no menu e informe os dados da questão.

## Exemplo com Euler

```text
Função: cos2t + sen3t
Intervalo: [0, 1]
Condição inicial: 1
Passo h: 0.25
```

Nesse caso, o programa calcula **4 passos** e mostra os valores de `t` e a aproximação de `y` em cada um deles. O passo `h` deve dividir o intervalo em partes iguais.

## Na hora de digitar

- **Decimais:** use ponto, como `0.25`.
- **Intervalos:** `0,1` ou `[0, 1]`. A vírgula separa os extremos.
- **Potências:** `x^2` ou `x**2`. Para a tolerância, pode usar `10^-4`.
- **Trigonometria:** `sen`, `cos` e `tan`, sempre em radianos. Aceita `cos2t`; para argumentos compostos, use `cos(2*t + 1)`.
- **Newton:** informe um ponto inicial ou um intervalo; o intervalo usa seu ponto médio como chute inicial.
- **Euler:** informe o passo `h`, sem tolerância de parada.
- **Ponto médio e Euler modificado:** usam os mesmos dados de Euler: `f(t, y)`, intervalo, condição inicial e passo `h`.

## Runge-Kutta de segunda ordem

As fórmulas seguem as notas de aula (seção 5.4, páginas numeradas 45–47).
Em cada passo, `w` aproxima `y(t)` e `k1 = f(t, w)`:

```text
Ponto médio:
    k2 = f(t + h/2, w + h*k1/2)
    próximo w = w + h*k2

Euler modificado:
    k2 = f(t + h, w + h*k1)
    próximo w = w + h*(k1 + k2)/2
```

Por exemplo, para `y' = y - t^2 + 1`, intervalo `[0, 2]`, `y(0) = 0.5`
e `h = 0.2`, as duas primeiras aproximações são:

| t | Ponto médio | Euler modificado |
| --- | --- | --- |
| 0.2 | 0.828 | 0.826 |
| 0.4 | 1.21136 | 1.20692 |

Os dois métodos mostram a tabela completa, incluindo a condição inicial na linha 0.

## Como a derivada é calculada

As regras estão em `expressoes/derivada.py`, com comentários indicando as fórmulas:

- Constante e variável: `c' = 0` e `x' = 1`.
- Soma e subtração: deriva cada termo.
- Produto: `(u*v)' = u'*v + u*v'`.
- Quociente: `(u/v)' = (u'*v - u*v') / v^2`.
- Potência com expoente constante: `(u^c)' = c*u^(c-1)*u'`.
- Potência com expoente variável: usa a regra com logaritmo, para base positiva.
- Regra da cadeia para `sen`, `cos`, `tan`, `sqrt`, `exp`, `ln`/`log` e `abs`.

O módulo `ast` do Python apenas identifica a estrutura da expressão. As regras
matemáticas são implementadas pelo projeto, sem SymPy e sem aproximação por
diferenças finitas. Por exemplo, `x^3 + 4*x^2 - 10` gera uma expressão equivalente
a `3*x^2 + 8*x`.

Para usar Newton, o ponto precisa pertencer ao domínio da função e da fórmula da
derivada. Por exemplo, `abs(x)` não tem derivada em zero e `log(x)` exige `x > 0`.

## Organização

```text
AV3-MetodosNumericos/
├── main.py
├── metodos/
│   ├── __init__.py
│   ├── bissecao.py
│   ├── newton.py
│   ├── euler.py
│   ├── ponto_medio.py
│   └── euler_modificado.py
├── expressoes/
│   ├── __init__.py
│   ├── funcoes.py
│   └── derivada.py
├── README.md
├── requirements.txt
└── .gitignore
```

- `main.py`: interface com menu, entradas e tabelas.
- `metodos/`: algoritmos numéricos; recebem dados e devolvem resultados, sem `input()` ou `print()`.
- `expressoes/`: leitura e cálculo das expressões matemáticas e regras de derivação.

Cada método tem seu algoritmo completo no próprio arquivo.

*Os demais métodos do trabalho serão adicionados ao longo do projeto.*
