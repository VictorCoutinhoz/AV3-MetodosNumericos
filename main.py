import math
from decimal import Decimal

from expressoes.derivada import calcular_derivada
from expressoes.funcoes import ler_funcao, ler_valor
from metodos.bissecao import bissecao
from metodos.euler import euler
from metodos.euler_modificado import euler_modificado
from metodos.newton import newton
from metodos.ponto_medio import ponto_medio


def solicitar(mensagem, converter):
    while True:
        try:
            return converter(input(mensagem).strip())
        except ValueError as erro:
            print(f"Erro: {erro} Tente novamente.")


def ler_positivo(entrada):
    valor = ler_valor(entrada)
    if valor <= 0:
        raise ValueError("O valor deve ser positivo.")
    return valor


def ler_intervalo(entrada):
    if entrada.startswith("[") and entrada.endswith("]"):
        entrada = entrada[1:-1]
    partes = entrada.split(",")
    if len(partes) != 2:
        raise ValueError("Informe um intervalo como 0,1 ou [0, 1].")
    a, b = (ler_valor(parte) for parte in partes)
    if a >= b:
        raise ValueError("O intervalo deve ter a < b.")
    return a, b


def solicitar_funcao(variaveis=("x",)):
    return solicitar(f"f({', '.join(variaveis)}) = ",
                     lambda texto: (texto, ler_funcao(texto, variaveis)))


def numero(valor):
    return format(Decimal(str(valor)), "f")


def mostrar_tabela(cabecalho, linhas):
    if not linhas:
        return
    linhas = [cabecalho] + [[numero(v) if isinstance(v, (int, float)) else v for v in linha] for linha in linhas]
    larguras = [max(len(v) for v in coluna) for coluna in zip(*linhas)]
    for i, linha in enumerate(linhas):
        print(" | ".join(v.rjust(largura) for v, largura in zip(linha, larguras)))
        if i == 0:
            print("-+-".join("-" * largura for largura in larguras))


def erro_relativo(atual, anterior):
    if anterior is None:
        return "—"
    return abs((atual - anterior) / atual) if atual != 0 else "indefinido"


def executar_raiz(opcao):
    expressao, funcao = solicitar_funcao()
    intervalo = None
    if opcao == "1":
        a, b = solicitar("Intervalo (ex.: [1, 2]): ", ler_intervalo)
    else:
        derivada, texto = calcular_derivada(expressao)
        print("f'(x) =", texto)
        entrada = solicitar("p0 ou intervalo (ex.: 1.2 ou [1, 2]): ",
                            lambda s: ler_intervalo(s) if any(c in s for c in ",[]") else ler_valor(s))
        intervalo = entrada if isinstance(entrada, tuple) else None
        p0 = intervalo[0]/2 + intervalo[1]/2 if intervalo else entrada
        print("p0 =", numero(p0))
    tolerancia = solicitar("Tolerância (ex.: 10^-4): ", ler_positivo)
    limite = solicitar("Máximo de iterações (Enter = 1000): ", lambda s: int(s or "1000"))
    historico = []
    try:
        if opcao == "1":
            raiz = bissecao(funcao, a, b, tolerancia, limite, historico)
        else:
            raiz = newton(funcao, derivada, p0, tolerancia, limite, historico)
    finally:
        linhas = []
        if opcao == "1":
            cabecalho = ["Iteração", "a", "b", "p", "f(p)", "Erro relativo"]
            anterior = None
            for i, a, b, p, fp in historico:
                linhas.append([i, a, b, p, fp, erro_relativo(p, anterior)])
                anterior = p
        else:
            cabecalho = ["Iteração", "p anterior", "p", "f(p)", "Erro absoluto", "Erro relativo"]
            for i, anterior, p, fp in historico:
                linhas.append([i, anterior, p, fp, abs(p-anterior), erro_relativo(p, anterior)])
        mostrar_tabela(cabecalho, linhas)
    print(f"\nEquação: {expressao} = 0")
    print(f"Raiz aproximada: {numero(raiz)}; f(p) = {numero(funcao(raiz))}")
    print("Iterações realizadas:", len(historico))
    if intervalo and not intervalo[0] <= raiz <= intervalo[1]:
        print("Atenção: a raiz ficou fora do intervalo informado.")


def executar_edo(opcao):
    metodos = {"3": ("Euler", euler), "4": ("Ponto médio", ponto_medio),
               "5": ("Euler modificado", euler_modificado)}
    nome, metodo = metodos[opcao]
    print(f"\nMétodo de {nome}: y' = f(t, y)")
    expressao, funcao = solicitar_funcao(("t", "y"))
    a, b = solicitar("Intervalo (ex.: [0, 2]): ", ler_intervalo)
    alfa = solicitar("Condição inicial y(a): ", ler_valor)

    def ler_passos(entrada):
        h = ler_positivo(entrada)
        quantidade = (b-a)/h
        if not math.isfinite(quantidade) or quantidade < 1:
            raise ValueError("Passo inválido para esse intervalo.")
        n = round(quantidade)
        if not math.isclose(quantidade, n, rel_tol=0, abs_tol=1e-9):
            raise ValueError("h deve dividir o intervalo em um número inteiro de passos.")
        return n

    n = solicitar("Passo h (ex.: 0.25): ", ler_passos)
    historico = []
    try:
        resultado = metodo(funcao, a, b, alfa, n, historico)
    finally:
        mostrar_tabela(["Passo", "t", "w (aproximação de y)"], historico)
    print(f"\ny' = {expressao}; y({numero(a)}) = {numero(alfa)}")
    print(f"h = {numero((b-a)/n)}; N = {n}")
    print(f"y({numero(b)}) ≈ {numero(resultado)}")


def executar():
    while True:
        try:
            print("\n1 - Bisseção\n2 - Newton\n3 - Euler"
                  "\n4 - Ponto médio\n5 - Euler modificado\n0 - Sair")
            opcao = input("Escolha um método: ").strip()
            if opcao == "0":
                return
            if opcao in ("1", "2"):
                executar_raiz(opcao)
            elif opcao in ("3", "4", "5"):
                executar_edo(opcao)
            else:
                print("Opção inválida.")
        except ValueError as erro:
            print(f"Erro: {erro}")
        except (EOFError, KeyboardInterrupt):
            print("\nCalculadora encerrada.")
            return


if __name__ == "__main__":
    executar()
