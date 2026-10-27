import ast
import math
import operator
from decimal import Decimal

from bisseccsao import bissecao


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


def ler_funcao(expressao):
    try:
        arvore = ast.parse(expressao.replace("^", "**"), mode="eval")
    except SyntaxError as erro:
        raise ValueError("Função inválida. Exemplo: x^3 + 4*x^2 - 10") from erro

    def avaliar(no, x):
        if isinstance(no, ast.Constant) and type(no.value) in (int, float):
            return float(no.value)
        if isinstance(no, ast.Name):
            if no.id == "x":
                return x
            if no.id in CONSTANTES:
                return CONSTANTES[no.id]
        if isinstance(no, ast.BinOp) and type(no.op) in OPERACOES:
            return OPERACOES[type(no.op)](avaliar(no.left, x), avaliar(no.right, x))
        if isinstance(no, ast.UnaryOp) and type(no.op) in (ast.UAdd, ast.USub):
            return OPERACOES[type(no.op)](avaliar(no.operand, x))
        if (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
                and no.func.id in FUNCOES and len(no.args) == 1 and not no.keywords):
            return FUNCOES[no.func.id](avaliar(no.args[0], x))
        raise ValueError("Use apenas x, números, operações e funções matemáticas permitidas.")

    def funcao(x):
        try:
            valor = avaliar(arvore.body, x)
            if not isinstance(valor, (int, float)) or not math.isfinite(valor):
                raise ValueError("A função deve produzir um número real finito.")
            return valor
        except (ArithmeticError, TypeError) as erro:
            raise ValueError(f"Não foi possível calcular a função em x = {formatar_numero(x)}.") from erro

    return funcao


def mostrar_iteracoes(historico):
    if not historico:
        return
    linhas = [["Iteração", "a", "b", "p", "f(p)", "Erro relativo"]]
    anterior = None
    for iteracao, a, b, p, fp in historico:
        erro = "—" if anterior is None else (
            "indefinido" if p == 0 else formatar_numero(abs((p - anterior) / p))
        )
        linhas.append([str(iteracao), *(formatar_numero(valor) for valor in (a, b, p, fp)), erro])
        anterior = p
    larguras = [max(len(valor) for valor in coluna) for coluna in zip(*linhas)]
    print("\nIterações da bisseção")
    print("Erro relativo = |(p atual - p anterior) / p atual| (sem porcentagem).")
    for indice, linha in enumerate(linhas):
        print(" | ".join(valor.rjust(largura) for valor, largura in zip(linha, larguras)))
        if indice == 0:
            print("-+-".join("-" * largura for largura in larguras))


def executar_bissecao():
    print("\nBisseção — aproxima uma raiz de f(x) = 0.")
    print("Exemplo de função: x^3 + 4*x^2 - 10")
    print("Decimais com ponto, não vírgula: 0.002.")
    funcao = ler_funcao(input("f(x) = "))
    a = float(input("Início do intervalo (a, ex.: 1): "))
    b = float(input("Fim do intervalo (b > a, ex.: 2): "))
    tolerancia = float(input("Tolerância (erro máximo, ex.: 0.002): "))
    max_iteracoes = int(input("Máximo de iterações (Enter = 1000): ").strip() or "1000")
    fa, fb = funcao(a), funcao(b)
    historico = []
    try:
        raiz = bissecao(funcao, a, b, tolerancia, max_iteracoes, historico=historico)
    finally:
        mostrar_iteracoes(historico)
    print("\nResultado")
    print(f"Intervalo inicial: [{formatar_numero(a)}, {formatar_numero(b)}]")
    print(f"f(a) = {formatar_numero(fa)}; f(b) = {formatar_numero(fb)}")
    print(f"Iterações realizadas: {len(historico)}")
    print(f"Raiz aproximada: {formatar_numero(raiz)}")
    print(f"f(p) = {formatar_numero(funcao(raiz))}")


METODOS = {"1": ("Bisseção", executar_bissecao)}


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
