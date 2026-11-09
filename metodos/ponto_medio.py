from math import isfinite


def ponto_medio(funcao, a, b, alfa, n, historico=None):
    # a e b: intervalo; alfa: y(a); n: número de passos.
    if not all(isfinite(valor) for valor in (a, b, alfa)) or a >= b:
        raise ValueError("Use valores finitos e um intervalo com a < b.")
    if type(n) is not int or n <= 0:
        raise ValueError("N deve ser um inteiro positivo.")

    h = (b - a) / n
    if not isfinite(h) or h <= 0:
        raise ValueError("Não foi possível calcular um passo finito e positivo.")
    t, w = a, alfa
    if historico is not None:
        historico.append((0, t, w))

    for i in range(1, n + 1):
        proximo_t = b if i == n else a + i * h
        if proximo_t <= t:
            raise ValueError("O passo é pequeno demais para a precisão disponível.")
        # Inclinação inicial e inclinação estimada no meio do passo.
        k1 = funcao(t, w)
        if not isfinite(k1):
            raise ValueError("A função deve retornar valores finitos.")
        k2 = funcao(t + h/2, w + h*k1/2)
        if not isfinite(k2):
            raise ValueError("A função deve retornar valores finitos.")
        w = w + h*k2
        t = proximo_t
        if not isfinite(w):
            raise ValueError("Ponto médio produziu uma aproximação não finita.")
        if historico is not None:
            historico.append((i, t, w))

    return w
