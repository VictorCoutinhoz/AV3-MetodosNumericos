from math import isfinite


def bissecao(funcao, a, b, tolerancia=1e-6, max_iteracoes=1000, historico=None):
    if not all(isfinite(valor) for valor in (a, b, tolerancia)):
        raise ValueError("Os limites e a tolerância devem ser finitos.")
    if a >= b or tolerancia <= 0:
        raise ValueError("Use a < b e tolerância positiva.")
    if not isinstance(max_iteracoes, int) or max_iteracoes <= 0:
        raise ValueError("O número máximo de iterações deve ser inteiro positivo.")

    def avaliar(x):
        valor = funcao(x)
        if not isfinite(valor):
            raise ValueError("A função deve retornar valores finitos no intervalo.")
        return valor

    fa, fb = avaliar(a), avaliar(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if (fa > 0) == (fb > 0):
        raise ValueError("A função deve ter sinais opostos nos extremos.")

    for iteracao in range(1, max_iteracoes + 1):
        meio = a / 2 + b / 2
        fm = avaliar(meio)
        if historico is not None:
            historico.append((iteracao, a, b, meio, fm))
        if fm == 0 or (b - a) / 2 < tolerancia:
            return meio
        if meio == a or meio == b:
            raise ValueError("A tolerância excede a precisão disponível.")
        if (fa > 0) != (fm > 0):
            b = meio
        else:
            a, fa = meio, fm
    raise ValueError(f"O método falhou após {max_iteracoes} iterações. N0 = {max_iteracoes}.")
