import ast
import math
import operator
import re
from decimal import Decimal

import sympy

from bisseccsao import bissecao
from newton import newton
from euler import euler


OPERACOES = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow,
    ast.UAdd: operator.pos, ast.USub: operator.neg,
}
FUNCOES = {nome: getattr(math, nome) for nome in ("sin", "cos", "tan", "sqrt", "exp", "log")}
FUNCOES["abs"] = abs
CONSTANTES = {"pi": math.pi, "e": math.e}


def formatar_numero(valor):
    return format(Decimal(str(valor)), "f")


def ler_funcao(expressao, simbolica=False, variaveis=("x",)):
    funcoes = FUNCOES if not simbolica else {
        **{nome: getattr(sympy, nome) for nome in FUNCOES if nome != "abs"},
        "abs": sympy.Abs,
    }
    constantes = CONSTANTES if not simbolica else {"pi": sympy.pi, "e": sympy.E}
    nomes = "|".join(variaveis)
    expressao = re.sub(
        r"\b(sen|sin|cos|tan)\s*(\d+(?:\.\d+)?)\s*\*?\s*(" + nomes + r")\b",
        r"\1(\2*\3)", expressao,
    )
    expressao = re.sub(r"(\d)\s*(" + nomes + r")\b", r"\1*\2", expressao.strip())
    expressao = re.sub(r"\b(sen|sin|cos|tan)\s*(" + nomes + r")\b", r"\1(\2)", expressao)
    expressao = re.sub(r"\bsen\b", "sin", expressao)
    expressao = re.sub(r"\bln\b", "log", expressao)
    try:
        arvore = ast.parse(expressao.replace("^", "**"), mode="eval")
    except SyntaxError as erro:
        raise ValueError("Função inválida. Exemplo: x^3 + 4*x^2 - 10") from erro

    def avaliar(no, x):
        if isinstance(no, ast.Constant) and type(no.value) in (int, float):
            return sympy.Rational(str(no.value)) if simbolica else float(no.value)
        if isinstance(no, ast.Name):
            if no.id in x:
                return x[no.id]
            if no.id in constantes:
                return constantes[no.id]
        if isinstance(no, ast.BinOp) and type(no.op) in OPERACOES:
            return OPERACOES[type(no.op)](avaliar(no.left, x), avaliar(no.right, x))
        if isinstance(no, ast.UnaryOp) and type(no.op) in (ast.UAdd, ast.USub):
            return OPERACOES[type(no.op)](avaliar(no.operand, x))
        if (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
                and no.func.id in funcoes and len(no.args) == 1 and not no.keywords):
            return funcoes[no.func.id](avaliar(no.args[0], x))
        raise ValueError(f"Use apenas {', '.join(variaveis)}, números, operações e funções matemáticas permitidas.")

    def funcao(*valores):
        if len(valores) != len(variaveis):
            raise ValueError(f"Informe valores para {', '.join(variaveis)}.")
        x = dict(zip(variaveis, valores))
        try:
            valor = avaliar(arvore.body, x)
            if not isinstance(valor, (int, float)) or not math.isfinite(valor):
                raise ValueError("A função deve produzir um número real finito.")
            return valor
        except (ArithmeticError, TypeError) as erro:
            ponto = ', '.join(f"{nome} = {formatar_numero(valor)}" for nome, valor in x.items())
            raise ValueError(f"Não foi possível calcular a função em {ponto}.") from erro

    if simbolica:
        return avaliar(arvore.body, {nome: sympy.Symbol(nome, real=True) for nome in variaveis})
    return funcao


def calcular_derivada(expressao):
    x = sympy.Symbol("x", real=True)
    expressao_derivada = sympy.diff(ler_funcao(expressao, simbolica=True), x)
    calcular = sympy.lambdify(x, expressao_derivada, modules="math")

    def derivada(valor):
        try:
            resultado = calcular(valor)
            if not isinstance(resultado, (int, float)) or not math.isfinite(resultado):
                raise ValueError("A derivada deve produzir um número real finito.")
            return resultado
        except (ArithmeticError, TypeError) as erro:
            raise ValueError(f"Não foi possível calcular a derivada em x = {formatar_numero(valor)}.") from erro

    texto = sympy.pretty(expressao_derivada, use_unicode=True, wrap_line=False)
    texto = re.sub(r"\bsin\b", "sen", texto)
    texto = re.sub(r"\d+(?:\.\d*)?[eE][+-]?\d+", lambda item: formatar_numero(item.group()), texto)
    return derivada, texto


def mostrar_iteracoes(historico):
    if not historico:
        return
    linhas = [["Iteração", "a", "b", "p", "f(p)", "Erro relativo"]]
    anterior = None
    for iteracao, a, b, p, fp in historico:
        erro = erro_relativo(p, anterior)
        linhas.append([str(iteracao), *(formatar_numero(valor) for valor in (a, b, p, fp)), erro])
        anterior = p
    print("\nIterações da bisseção")
    print("Erro relativo = |(p atual - p anterior) / p atual|")
    mostrar_tabela(linhas)


def mostrar_tabela(linhas):
    larguras = [max(len(valor) for valor in coluna) for coluna in zip(*linhas)]
    for indice, linha in enumerate(linhas):
        print(" | ".join(valor.rjust(largura) for valor, largura in zip(linha, larguras)))
        if indice == 0:
            print("-+-".join("-" * largura for largura in larguras))


def executar_bissecao():
    print("\nBisseção — aproxima uma raiz de f(x) = 0.")
    print("Exemplo de função: x^3 + 4*x^2 - 10")
    print("Decimais com ponto, não vírgula: 0.002.")
    expressao, funcao = solicitar_funcao()
    a, b = solicitar("Intervalo (ex.: 1,2 ou [1, 2]): ", ler_intervalo)
    tolerancia, max_iteracoes = solicitar_limites()
    fa, fb = funcao(a), funcao(b)
    historico = []
    try:
        raiz = bissecao(funcao, a, b, tolerancia, max_iteracoes, historico=historico)
    finally:
        mostrar_iteracoes(historico)
    print("\nResultado")
    print(f"Equação: {expressao} = 0")
    print(f"Intervalo inicial: [{formatar_numero(a)}, {formatar_numero(b)}]")
    print(f"f(a) = {formatar_numero(fa)}; f(b) = {formatar_numero(fb)}")
    mostrar_resultado(funcao, raiz, historico)


def ler_valor(expressao):
    if ler_funcao(expressao, simbolica=True).free_symbols:
        raise ValueError("Informe um valor numérico, sem x (ex.: pi/2 ou 10^-4).")
    return ler_funcao(expressao)(0)


def ler_intervalo(entrada):
    entrada = entrada.strip()
    if entrada.startswith("[") and entrada.endswith("]"):
        entrada = entrada[1:-1]
    elif "[" in entrada or "]" in entrada:
        raise ValueError("Feche os colchetes ou use apenas a,b. Exemplo: 0,1.")
    partes = entrada.split(",")
    if len(partes) != 2:
        raise ValueError("Informe dois extremos separados por vírgula. Exemplo: 0,1.")
    a, b = (ler_valor(parte) for parte in partes)
    if a >= b:
        raise ValueError("O intervalo deve ter a < b.")
    return a, b


def solicitar(mensagem, converter):
    while True:
        try:
            return converter(input(mensagem).strip())
        except ValueError as erro:
            print(f"Erro: {str(erro).rstrip('.')}. Tente novamente.")


def solicitar_funcao(variaveis=("x",)):
    def converter(expressao):
        ler_funcao(expressao, simbolica=True, variaveis=variaveis)
        return expressao, ler_funcao(expressao, variaveis=variaveis)

    return solicitar(f"f({', '.join(variaveis)}) = ", converter)


def solicitar_limites():
    def tolerancia(entrada):
        valor = ler_valor(entrada)
        if valor <= 0:
            raise ValueError("A tolerância deve ser positiva.")
        return valor

    def iteracoes(entrada):
        valor = int(entrada or "1000")
        if valor <= 0:
            raise ValueError("O limite deve ser um inteiro positivo.")
        return valor

    return (
        solicitar("Tolerância (ex.: 0.002 ou 10^-4): ", tolerancia),
        solicitar("Máximo de iterações (Enter = 1000): ", iteracoes),
    )


def erro_relativo(atual, anterior):
    if anterior is None:
        return "—"
    if atual == 0:
        return "indefinido"
    return formatar_numero(abs((atual - anterior) / atual))


def mostrar_resultado(funcao, raiz, historico):
    print(f"Iterações realizadas: {len(historico)}")
    print(f"Raiz aproximada: {formatar_numero(raiz)}")
    print(f"f(p) = {formatar_numero(funcao(raiz))}")


def executar_newton():
    print("\nNewton — derivada calculada automaticamente.")
    print("Exemplo: x^2 - 2. Decimais com ponto.")
    expressao, funcao = solicitar_funcao()
    derivada, texto_derivada = calcular_derivada(expressao)
    print("f'(x):\n" + texto_derivada)
    entrada = solicitar("p0 ou intervalo (ex.: 1.2 ou 1.2,2): ",
                        lambda texto: ler_intervalo(texto) if "," in texto or "[" in texto or "]" in texto else ler_valor(texto))
    intervalo = entrada if isinstance(entrada, tuple) else None
    p0 = intervalo[0] / 2 + intervalo[1] / 2 if intervalo else entrada
    if intervalo:
        print(f"Ponto médio: p0 = (a + b) / 2 = {formatar_numero(p0)}")
    tolerancia, max_iteracoes = solicitar_limites()
    historico = []
    try:
        raiz = newton(funcao, derivada, p0, tolerancia, max_iteracoes, historico=historico)
    finally:
        if historico:
            linhas = [["Iteração", "p anterior", "p", "f(p)", "Erro absoluto", "Erro relativo"]]
            for iteracao, anterior, p, fp in historico:
                erro = abs(p - anterior)
                relativo = erro_relativo(p, anterior)
                linhas.append([str(iteracao), *(formatar_numero(v) for v in (anterior, p, fp, erro)), relativo])
            print("\nIterações de Newton")
            print("Erro absoluto = |p - p anterior|; relativo = |(p - p anterior) / p|.")
            mostrar_tabela(linhas)
    print("\nResultado de Newton")
    print(f"Equação: {expressao} = 0")
    print("Derivada:\n" + texto_derivada)
    if intervalo is not None:
        print(f"Intervalo informado: [{formatar_numero(intervalo[0])}, {formatar_numero(intervalo[1])}]")
    print(f"Aproximação inicial: {formatar_numero(p0)}")
    print(f"Tolerância entre aproximações: {formatar_numero(tolerancia)}")
    mostrar_resultado(funcao, raiz, historico)
    if intervalo is not None and not intervalo[0] <= raiz <= intervalo[1]:
        print("Atenção: a raiz encontrada ficou fora do intervalo informado.")


def executar_euler():
    print("\nEuler — aproxima a solução de y' = f(t, y).")
    print("Exemplo: y - t^2 + 1. Decimais com ponto.")
    expressao, funcao = solicitar_funcao(("t", "y"))
    a, b = solicitar("Intervalo (ex.: 0,2 ou [0, 2]): ", ler_intervalo)
    alfa = solicitar("Condição inicial y(a) (ex.: 0.5): ", ler_valor)

    def passo(entrada):
        h = ler_valor(entrada)
        if h <= 0:
            raise ValueError("h deve ser positivo.")
        quantidade = (b - a) / h
        if not math.isfinite(quantidade):
            raise ValueError("Não foi possível calcular o número de passos.")
        n = round(quantidade)
        if n < 1 or not math.isclose(quantidade, n, rel_tol=0, abs_tol=1e-9):
            raise ValueError("h deve dividir o intervalo em um número inteiro de passos.")
        return h, n

    h, n = solicitar("Tamanho do passo h (ex.: 0.25): ", passo)
    historico = []
    try:
        resultado = euler(funcao, a, b, alfa, n, historico=historico)
    finally:
        if historico:
            linhas = [["Passo", "t", "w (aproximação de y)"]]
            linhas.extend([str(i), formatar_numero(t), formatar_numero(w)] for i, t, w in historico)
            print("\nPassos de Euler (linha 0 = condição inicial)")
            mostrar_tabela(linhas)
    print("\nResultado de Euler")
    print(f"y' = {expressao}; y({formatar_numero(a)}) = {formatar_numero(alfa)}")
    print(f"Passo h = {formatar_numero(h)}; N = {n}")
    print(f"y({formatar_numero(b)}) ≈ {formatar_numero(resultado)}")


METODOS = {"1": ("Bisseção", executar_bissecao), "2": ("Newton", executar_newton),
           "3": ("Euler", executar_euler)}


def executar():
    while True:
        print("\nCalculadora de métodos numéricos")
        for identificador, (nome, _) in METODOS.items():
            print(f"{identificador} - {nome}")
        print("0 - Sair")
        try:
            opcao = input("Escolha um método: ").strip()
            if opcao == "0":
                return
            if opcao not in METODOS:
                print("Opção inválida.")
                continue
            METODOS[opcao][1]()
        except ValueError as erro:
            print(f"Erro: {erro}")
        except (EOFError, KeyboardInterrupt):
            print("\nCalculadora encerrada.")
            return


if __name__ == "__main__":
    executar()
