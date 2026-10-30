from math import isfinite


def euler(funcao, a, b, alfa, n, historico=None):
    # a e b: intervalo; alfa: y(a); n: número de passos.
    if not all(isfinite(valor) for valor in (a, b, alfa)) or a >= b:
        raise ValueError("Use valores finitos e um intervalo com a < b.")
    if type(n) is not int or n <= 0:
        raise ValueError("N deve ser um inteiro positivo.")

    # Passo 1: calcula h e começa na condição inicial.
    h = (b - a) / n
    if not isfinite(h) or h <= 0:
        raise ValueError("Não foi possível calcular um passo finito e positivo.")
    t, w = a, alfa
    if historico is not None:
        historico.append((0, t, w))

    # Passo 2: conta os passos de 1 até N.
    for i in range(1, n + 1):
        # Passo 3: usa a inclinação atual para calcular o próximo valor.
        inclinacao = funcao(t, w)
        if not isfinite(inclinacao):
            raise ValueError("A função deve retornar valores finitos.")
        proximo_t = b if i == n else a + i * h
        if proximo_t <= t:
            raise ValueError("O passo é pequeno demais para a precisão disponível.")
        w = w + h * inclinacao
        t = proximo_t
        if not isfinite(w):
            raise ValueError("Euler produziu uma aproximação não finita.")
        # Passo 4: salva t e w para mostrar na tabela.
        if historico is not None:
            historico.append((i, t, w))

    # Passo 5: termina e devolve a aproximação em b.
    return w
