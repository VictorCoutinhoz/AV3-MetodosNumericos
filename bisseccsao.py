from math import isfinite


def bissecao(funcao, a, b, tolerancia=1e-6, max_iteracoes=1000, historico=None):
    # a e b: limites; meio: p; tolerancia: TOL; max_iteracoes: N0.

    # Confere as entradas.
    if not all(isfinite(valor) for valor in (a, b, tolerancia)):
        raise ValueError("Os limites e a tolerância devem ser finitos.")
    if a >= b or tolerancia <= 0:
        raise ValueError("Use a < b e tolerância positiva.")
    if not isinstance(max_iteracoes, int) or max_iteracoes <= 0:
        raise ValueError("O número máximo de iterações deve ser inteiro positivo.")

    def avaliar(x):
        # Calcula f(x) e confere o resultado.
        valor = funcao(x)
        if not isfinite(valor):
            raise ValueError("A função deve retornar valores finitos no intervalo.")
        return valor

    # Passo 1: calcula f(a) e f(b).
    fa, fb = avaliar(a), avaliar(b)
    # Confere se a raiz está em um dos limites.
    if fa == 0:
        return a
    if fb == 0:
        return b
    if (fa > 0) == (fb > 0):
        raise ValueError("A função deve ter sinais opostos nos extremos.")

    # Passos 1, 2 e 5: conta as iterações de 1 até N0.
    for iteracao in range(1, max_iteracoes + 1):
        # Passo 3: calcula o meio e f(meio).
        meio = a / 2 + b / 2
        fm = avaliar(meio)
        # Salva a iteração na tabela.
        if historico is not None:
            historico.append((iteracao, a, b, meio, fm))
        # Passo 4: confere se achou a raiz ou atingiu a tolerância.
        if fm == 0 or (b - a) / 2 < tolerancia:
            return meio
        # Evita continuar sem avanço numérico.
        if meio == a or meio == b:
            raise ValueError("A tolerância excede a precisão disponível.")
        # Passo 6: mantém a metade com sinais opostos.
        if (fa > 0) != (fm > 0):
            b = meio
        else:
            a, fa = meio, fm
    # Passo 7: avisa que o limite de iterações acabou.
    raise ValueError(f"O método falhou após {max_iteracoes} iterações. N0 = {max_iteracoes}.")
