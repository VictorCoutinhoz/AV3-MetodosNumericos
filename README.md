# AV3 — Métodos Numéricos

Trabalho da disciplina de Métodos Numéricos, desenvolvido em Python para resolver questões das notas de aula e acompanhar os cálculos passo a passo.

Até agora, estão prontos os métodos da **Bisseção** e de **Newton**. O programa mostra as iterações, o erro relativo e a raiz encontrada. No Newton, a derivada é calculada automaticamente com o SymPy.

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

Os demais métodos pedidos no trabalho ainda serão adicionados.
