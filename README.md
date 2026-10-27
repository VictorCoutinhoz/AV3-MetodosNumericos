# AV3-MetodosNumericos

Calculadora de métodos numéricos no terminal, usando apenas a biblioteca padrão do Python 3.

Execute `python main.py`.

Os resultados são exibidos em formato decimal, sem notação científica e sem o corte de 12 algarismos. As funções trigonométricas usam radianos. Os cálculos mantêm a precisão de `float` do Python; a formatação não acrescenta precisão ao cálculo.

A saída inclui uma tabela de todas as iterações com `a`, `b`, a aproximação `p`, `f(p)` e o erro relativo entre aproximações: `abs((p_atual - p_anterior) / p_atual)`, sem porcentagem. Na primeira iteração aparece `—`; quando `p_atual = 0`, o erro relativo é indefinido. Esse erro é informativo: o critério de parada continua sendo a tolerância absoluta do intervalo ou uma raiz exata. Se o limite de iterações for atingido, as tentativas também são exibidas antes da mensagem de falha.

- `main.py` lista os métodos, recebe os dados e apresenta os resultados.
- `bisseccsao.py` contém apenas o algoritmo de bisseção, sem entrada e saída no terminal.

## Exemplo de bisseção

O método da bisseção aproxima uma raiz de `f(x) = 0` dividindo repetidamente um intervalo `[a, b]` ao meio. A função deve ser contínua nesse intervalo e ter sinais opostos nos extremos (ou já ter uma raiz em um deles).

**Use ponto (`.`) como separador decimal, nunca vírgula (`,`): digite `0.002`, e não `0,002`.** Isso vale para a função, os limites e a tolerância.

Os dados solicitados são:

- **Função:** expressão em `x` cuja raiz será calculada.
- **Limites `a` e `b`:** início e fim do intervalo, com `a < b`.
- **Tolerância `TOL`:** erro máximo aceito na aproximação da raiz. Para a precisão de `0,002` do enunciado, digite `0.002`. Quanto menor esse valor, maior a precisão e, em geral, mais iterações.
- **Máximo de iterações `N0`:** quantidade máxima de divisões permitidas. É opcional: pressione Enter para usar `1000`. Se esse limite for atingido sem alcançar a tolerância, o método informa falha.

Para resolver `f(x) = x³ + 4x² - 10 = 0`, escolha a opção `1` e informe:

```text
f(x) = x^3 + 4*x^2 - 10
Limite inferior (a): 1
Limite superior (b): 2
Tolerância (TOL): 0.002
Número máximo de iterações (N0): 100
```

Nos extremos, `f(1) = -5` e `f(2) = 14`. Como o polinômio é contínuo, existe uma raiz nesse intervalo. A aproximação retornada é `1.365234375`, com erro absoluto em x menor que `0.002`.

Digite apenas a expressão, sem `f(x) =` ou `= 0`. Use `*` para multiplicação e `^` ou `**` para potências. São permitidos parênteses, `+`, `-`, `*`, `/`, as funções `sin`, `cos`, `tan`, `sqrt`, `exp`, `log` (logaritmo natural), `abs` e as constantes `pi` e `e`. Use ponto como separador decimal.

O algoritmo para quando `f(p) == 0` ou `(b - a) / 2 < TOL`, e informa erro se atingir `N0` sem convergir. A garantia de erro exige que a função seja contínua no intervalo; a calculadora verifica os sinais dos extremos, mas não verifica continuidade.

Para adicionar outro método, coloque o algoritmo em seu módulo, crie a função de entrada e saída na `main.py` e registre-a em `METODOS`.

Execute os testes com `python -B -m unittest -v`.
