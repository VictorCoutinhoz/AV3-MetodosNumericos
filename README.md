# AV3 — Métodos Numéricos

Calculadora em Python para resolver as questões da disciplina e acompanhar os resultados em tabelas.

## Executar

Com **Python 3.9+**, na pasta do projeto:

```bash
python main.py
```

Escolha um método e informe os dados. Não é necessário instalar bibliotecas.

## Métodos

| Opção | Método |
| :---: | --- |
| 1 | [Bisseção](metodos/bissecao.py) |
| 2 | [Newton](metodos/newton.py) |
| 3 | [Euler](metodos/euler.py) |
| 4 | [Ponto médio](metodos/ponto_medio.py) |
| 5 | [Euler modificado](metodos/euler_modificado.py) |
| 6 | [Runge-Kutta de quarta ordem](metodos/runge_kutta_4ordem.py) |
| 8 | [Adams-Bashforth de quarta ordem](metodos/adams_bashforth_4ordem.py) |

**0** encerra o programa. A opção **7**, RK4 para sistemas, ainda não está disponível.

Expanda um método para ver a ideia, o algoritmo resumido e um exemplo de uso.
Nas EDOs, `w` aproxima `y(t)`, `alfa = y(a)` e `N = (b-a)/h`.

<details>
<summary><strong>1 — Bisseção</strong></summary>

Encontra uma raiz de `f(x) = 0` dividindo o intervalo ao meio. A função deve ser
contínua no intervalo e ter sinais opostos nos extremos, ou uma raiz em um deles.

**Algoritmo resumido**

```text
Se um extremo for raiz, retorne esse extremo.
Repita até o limite de iterações:
    p = a/2 + b/2
    Se f(p) = 0 ou (b-a)/2 < TOL: retorne p
    Se f(a) e f(p) têm sinais opostos: b = p
    Senão: a = p
```

**Como usar:** escolha **1** e informe:

```text
Função: x^3 + 4*x^2 - 10
Intervalo: [1, 2]
Tolerância: 0.002
Máximo de iterações: Enter para usar 1000
```

Resultado: **raiz ≈ 1.365234375**.

</details>

<details>
<summary><strong>2 — Newton</strong></summary>

Encontra uma raiz a partir de um chute, usando a derivada para corrigir cada
aproximação. A derivada é calculada por regras programadas no projeto.

**Algoritmo resumido**

```text
Repita até o limite de iterações:
    Se f(p0) = 0: retorne p0
    Se f'(p0) = 0: informe erro
    p = p0 - f(p0)/f'(p0)
    Se f(p) = 0 ou |p-p0| < TOL: retorne p
    p0 = p
```

**Como usar:** escolha **2** e informe:

```text
Função: x^2 - 2
p0 ou intervalo: 1
Tolerância: 10^-6
Máximo de iterações: Enter para usar 1000
```

Resultado: **raiz ≈ 1.4142135624**. Se informar um intervalo, o programa usa
seu ponto médio como chute; isso não garante que a raiz fique dentro dele.

</details>

<details>
<summary><strong>3 — Euler</strong></summary>

Aproxima a solução de `y' = f(t, y)` usando a inclinação no início de cada passo.

**Algoritmo resumido**

```text
t = a; w = alfa
Para i de 1 até N:
    w = w + h*f(t, w)
    t = a + i*h
```

**Como usar:** escolha **3** e informe:

```text
Função: y - t^2 + 1
Intervalo: [0, 2]
Condição inicial: 0.5
Passo h: 0.2
```

Resultado: **y(2) ≈ 4.8657845**, após 10 passos.

</details>

<details>
<summary><strong>4 — Ponto médio</strong></summary>

É um Runge-Kutta de segunda ordem: estima um valor na metade do passo e usa
a inclinação nesse ponto para avançar.

**Algoritmo resumido**

```text
t = a; w = alfa
Para i de 1 até N:
    k1 = f(t, w)
    k2 = f(t + h/2, w + h*k1/2)
    w = w + h*k2
    t = a + i*h
```

**Como usar:** escolha **4** e informe:

```text
Função: y - t^2 + 1
Intervalo: [0, 2]
Condição inicial: 0.5
Passo h: 0.2
```

Resultado: **y(2) ≈ 5.2903695**, após 10 passos.

</details>

<details>
<summary><strong>5 — Euler modificado</strong></summary>

É um Runge-Kutta de segunda ordem: faz uma previsão com Euler e avança usando
a média das inclinações inicial e prevista no fim do passo.

**Algoritmo resumido**

```text
t = a; w = alfa
Para i de 1 até N:
    k1 = f(t, w)
    k2 = f(t + h, w + h*k1)
    w = w + h*(k1 + k2)/2
    t = a + i*h
```

**Como usar:** escolha **5** e informe:

```text
Função: y - t^2 + 1
Intervalo: [0, 2]
Condição inicial: 0.5
Passo h: 0.2
```

Resultado: **y(2) ≈ 5.2330546**, após 10 passos.

</details>

<details>
<summary><strong>6 — Runge-Kutta de quarta ordem</strong></summary>

Combina quatro inclinações: uma no início, duas no meio e uma no fim do passo.
Os incrementos `k1` a `k4` já incluem o fator `h`.

**Algoritmo resumido**

```text
t = a; w = alfa
Para i de 1 até N:
    k1 = h*f(t, w)
    k2 = h*f(t + h/2, w + k1/2)
    k3 = h*f(t + h/2, w + k2/2)
    k4 = h*f(t + h, w + k3)
    w = w + (k1 + 2*k2 + 2*k3 + k4)/6
    t = a + i*h
```

**Como usar:** escolha **6** e informe:

```text
Função: y - t^2 + 1
Intervalo: [0, 2]
Condição inicial: 0.5
Passo h: 0.2
```

Resultado: **y(2) ≈ 5.3053630**, após 10 passos.

</details>

<details>
<summary><strong>8 — Adams-Bashforth de quarta ordem</strong></summary>

É um método explícito de quatro passos: combina a inclinação atual e as três
anteriores. Precisa de `w0`, `w1`, `w2` e `w3` para começar.

**Algoritmo resumido**

```text
w[0] = alfa
Obtenha w[1], w[2] e w[3]: informados ou calculados com RK4.
t[i] = a + i*h
Para i de 3 até N-1:
    w[i+1] = w[i] + h/24 * (55*f(t[i], w[i]) - 59*f(t[i-1], w[i-1])
                           + 37*f(t[i-2], w[i-2]) - 9*f(t[i-3], w[i-3]))
```

**Como usar:** escolha **8** e informe:

```text
Função: y - t^2 + 1
Intervalo: [0, 2]
Condição inicial: 0.5
Passo h: 0.2
w1,w2,w3: Enter para calcular com RK4
```

Ou informe os três valores separados por vírgulas, correspondentes aos tempos
`a+h`, `a+2h` e `a+3h`. O intervalo deve ter pelo menos quatro passos.

Com os iniciais calculados por RK4: **y(2) ≈ 5.3075082**. O primeiro avanço
por Adams-Bashforth ocorre em `t = 0.8`, com **y(0.8) ≈ 2.1272892**.

</details>

## Dicas de entrada

- Decimais com ponto: `0.25`. Intervalos: `0,2` ou `[0, 2]`.
- Potências: `x^2` ou `x**2`. Tolerância: `10^-4`.
- Funções: `sen(x)`, `cos(x)`, `tan(x)`, `sqrt(x)`, `exp(x)`, `ln(x)` e `abs(x)`. Ângulos em radianos.
- Newton aceita um chute ou intervalo; o intervalo usa o ponto médio como chute.
- Nas EDOs, `h` deve dividir o intervalo em partes iguais. Adams-Bashforth exige pelo menos quatro passos e aceita `w1,w2,w3` informados ou calculados com RK4.

## Organização

- **[main.py](main.py)** — menu, entradas e tabelas.
- **[metodos/](metodos/)** — um arquivo para cada algoritmo.
- **[expressoes/](expressoes/)** — leitura de funções e regras de derivação programadas no projeto.
