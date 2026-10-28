from math import isfinite


def newton(funcao, derivada, p0, tolerancia=1e-6, max_iteracoes=1000, historico=None):
    if not all(isfinite(valor) for valor in (p0, tolerancia)) or tolerancia <= 0:
        raise ValueError("Use uma aproximação finita e tolerância positiva e finita.")
    if not isinstance(max_iteracoes, int) or max_iteracoes <= 0:
        raise ValueError("O número máximo de iterações deve ser inteiro positivo.")

    for iteracao in range(1, max_iteracoes + 1):
        fp0 = funcao(p0)
        if not isfinite(fp0):
            raise ValueError("A função deve retornar valores finitos.")
        if fp0 == 0:
            return p0
        dp0 = derivada(p0)
        if not isfinite(dp0):
            raise ValueError("A derivada deve retornar valores finitos.")
        if dp0 == 0:
            raise ValueError(f"Derivada nula na iteração {iteracao}. Escolha outra aproximação inicial.")
        p = p0 - fp0 / dp0
        if not isfinite(p):
            raise ValueError("Newton produziu uma aproximação não finita.")
        fp = funcao(p)
        if not isfinite(fp):
            raise ValueError("A função deve retornar valores finitos.")
        if historico is not None:
            historico.append((iteracao, p0, p, fp))
        if abs(p - p0) < tolerancia:
            return p
        p0 = p
    raise ValueError(f"O método falhou após {max_iteracoes} iterações. N0 = {max_iteracoes}.")
