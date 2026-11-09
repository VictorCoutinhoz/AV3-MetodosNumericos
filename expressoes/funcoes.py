import ast
import math
import re


TIPOS = (ast.BinOp, ast.UnaryOp, ast.Call, ast.Name, ast.Constant, ast.Load,
         ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.UAdd, ast.USub)
FUNCOES = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "sqrt": math.sqrt, "exp": math.exp, "log": math.log, "abs": abs,
}
CONSTANTES = {"pi": math.pi, "e": math.e}


def analisar(expressao, variaveis=("x",)):
    # Aceita as abreviações usadas nas questões: sen3x, cos2t e 2x.
    nomes = "|".join(variaveis)
    expressao = expressao.strip().replace("^", "**")
    expressao = re.sub(r"\bsen\b", "sin", expressao)
    expressao = re.sub(r"\bln\b", "log", expressao)
    if variaveis:
        expressao = re.sub(
            r"\b(sen|sin|cos|tan)\s*(\d+(?:\.\d+)?)\s*\*?\s*(" + nomes + r")\b",
            r"\1(\2*\3)", expressao,
        )
        expressao = re.sub(r"\bsen(?=\()", "sin", expressao)
        expressao = re.sub(r"(\d)\s*(" + nomes + r")\b", r"\1*\2", expressao)
        expressao = re.sub(r"\b(sin|cos|tan)\s*(" + nomes + r")\b", r"\1(\2)", expressao)
    try:
        raiz = ast.parse(expressao, mode="eval").body
    except SyntaxError as erro:
        raise ValueError("Função inválida. Exemplo: x^3 + 4*x^2 - 10.") from erro

    # Só libera operações matemáticas antes de compilar a expressão.
    for no in ast.walk(raiz):
        if type(no) not in TIPOS:
            raise ValueError("Use apenas operações matemáticas.")
        if isinstance(no, ast.Constant):
            try:
                finito = type(no.value) in (int, float) and math.isfinite(no.value)
            except OverflowError:
                finito = False
            if not finito:
                raise ValueError("Use apenas números finitos.")
        if isinstance(no, ast.Name) and no.id not in (*variaveis, *CONSTANTES, *FUNCOES):
            raise ValueError(f"Nome não permitido: {no.id}.")
        if isinstance(no, ast.Call):
            if (not isinstance(no.func, ast.Name) or no.func.id not in FUNCOES
                    or len(no.args) != 1 or no.keywords):
                raise ValueError("Use funções matemáticas com um argumento.")
    return raiz


def ler_funcao(expressao, variaveis=("x",)):
    raiz = analisar(expressao, variaveis)
    codigo = compile(ast.Expression(raiz), "<funcao>", "eval")

    def funcao(*valores):
        if len(valores) != len(variaveis):
            raise ValueError(f"Informe valores para {', '.join(variaveis)}.")
        try:
            nomes = {**FUNCOES, **CONSTANTES, **dict(zip(variaveis, valores))}
            resultado = eval(codigo, {"__builtins__": {}}, nomes)
            if not isinstance(resultado, (int, float)) or not math.isfinite(resultado):
                raise ValueError("A função deve produzir um número real finito.")
            return resultado
        except (ArithmeticError, TypeError, ValueError) as erro:
            raise ValueError("Não foi possível calcular a função nesse ponto. Confira o domínio.") from erro

    return funcao


def ler_valor(expressao):
    # Sem variáveis: aceita números e expressões como pi/2 e 10^-4.
    return ler_funcao(expressao, variaveis=())()
