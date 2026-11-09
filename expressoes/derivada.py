import ast

from .funcoes import analisar, ler_funcao


def texto(no):
    if isinstance(no, ast.Constant) and no.value in (0, 1):
        return str(int(no.value))
    expressao = ast.unparse(no)
    if isinstance(no, (ast.BinOp, ast.UnaryOp)):
        return f"({expressao})"
    return expressao


def operacao(a, sinal, b):
    # Simplificações básicas para não exibir termos como 0*x e 1*x.
    if sinal in ("+", "-") and b == "0":
        return a
    if sinal == "+" and a == "0":
        return b
    if sinal == "*" and "0" in (a, b):
        return "0"
    if sinal == "*" and a == "1":
        return b
    if sinal in ("*", "/", "^") and b == "1":
        return a
    if sinal == "^" and b == "0":
        return "1"
    return f"({a} {sinal} {b})"


def derivar(no):
    # Constante: c' = 0. Variável: x' = 1.
    if isinstance(no, ast.Constant):
        return "0"
    if isinstance(no, ast.Name):
        return "1" if no.id == "x" else "0"
    if isinstance(no, ast.UnaryOp):
        du = derivar(no.operand)
        return operacao("-1", "*", du) if isinstance(no.op, ast.USub) else du

    if isinstance(no, ast.BinOp):
        u, v = texto(no.left), texto(no.right)
        du, dv = derivar(no.left), derivar(no.right)
        if du == "0" and dv == "0":
            return "0"
        if isinstance(no.op, ast.Add):
            return operacao(du, "+", dv)
        if isinstance(no.op, ast.Sub):
            return operacao(du, "-", dv)
        if isinstance(no.op, ast.Mult):
            # (u*v)' = u'*v + u*v'
            return operacao(operacao(du, "*", v), "+", operacao(u, "*", dv))
        if isinstance(no.op, ast.Div):
            # (u/v)' = (u'*v - u*v') / v²
            numerador = operacao(operacao(du, "*", v), "-", operacao(u, "*", dv))
            return operacao(numerador, "/", operacao(v, "^", "2"))
        if dv == "0":
            # (u^c)' = c*u^(c-1)*u'
            expoente = str(no.right.value - 1) if isinstance(no.right, ast.Constant) else operacao(v, "-", "1")
            return operacao(operacao(v, "*", operacao(u, "^", expoente)), "*", du)
        if du == "0":
            # (c^v)' = c^v*ln(c)*v'
            return operacao(operacao(operacao(u, "^", v), "*", f"log({u})"), "*", dv)
        # (u^v)' = u^v * (v'*ln(u) + v*u'/u)
        soma = operacao(operacao(dv, "*", f"log({u})"), "+", operacao(v, "*", operacao(du, "/", u)))
        return operacao(operacao(u, "^", v), "*", soma)

    # Regra da cadeia: (g(u))' = g'(u)*u'.
    u = texto(no.args[0])
    du = derivar(no.args[0])
    if du == "0":
        return "0"
    regras = {
        "sin": f"cos({u})",
        "cos": f"(-sin({u}))",
        "tan": f"(1 / cos({u})^2)",
        "sqrt": f"(1 / (2*sqrt({u})))",
        "exp": f"exp({u})",
        "log": f"(1 / ({u}))",
        "abs": f"(({u}) / abs({u}))",
    }
    return operacao(regras[no.func.id], "*", du)


def calcular_derivada(expressao):
    texto = derivar(analisar(expressao))
    return ler_funcao(texto), texto.replace("**", "^").replace("sin", "sen")
