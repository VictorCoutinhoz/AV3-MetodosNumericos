# AV3 — Métodos Numéricos

Trabalho da disciplina de Métodos Numéricos, desenvolvido em Python para resolver questões das notas de aula e acompanhar os cálculos passo a passo.

## Métodos disponíveis

| Opção | Método | O que faz |
| :---: | --- | --- |
| 1 | Bisseção | Encontra uma raiz dividindo o intervalo ao meio. |
| 2 | Newton | Encontra uma raiz usando a derivada, calculada automaticamente. |
| 3 | Euler | Aproxima a solução de uma equação diferencial passo a passo. |

As contas aparecem em tabelas. Bisseção e Newton também mostram o erro relativo entre as aproximações.

## Como executar

Com o **Python 3** instalado, rode no terminal:

```bash
pip install -r requirements.txt
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

*Os demais métodos do trabalho serão adicionados ao longo do projeto.*
