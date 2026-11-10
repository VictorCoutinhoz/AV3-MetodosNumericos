from math import isfinite


def runge_kutta_4ordem(funcao, a, b, alfa, n, historico=None):
    # Runge-Kutta de quarta ordem: intervalo [a, b], y(a) = alfa, n passos.
    if not all(isfinite(valor) for valor in (a, b, alfa)) or a >= b:
        raise ValueError("Use valores finitos e um intervalo com a < b.")
    if type(n) is not int or n <= 0:
        raise ValueError("N deve ser um inteiro positivo.")

    # Passo 1: calcula h e começa na condição inicial.
    h = (b - a) / n
    if not isfinite(h) or h <= 0:
        raise ValueError("Não foi possível calcular um passo finito e positivo.")

    def avaliar(t, w):
        if not all(isfinite(valor) for valor in (t, w)):
            raise ValueError("Runge-Kutta produziu um estágio não finito.")
        valor = funcao(t, w)
        if not isfinite(valor):
            raise ValueError("A função deve retornar valores finitos.")
        return valor

    t, w = a, alfa
    if historico is not None:
        historico.append((0, t, w))

    # Passo 2: repete o cálculo nos n passos.
    for i in range(1, n + 1):
        proximo_t = b if i == n else a + i * h
        if proximo_t <= t:
            raise ValueError("O passo é pequeno demais para a precisão disponível.")
        # Passo 3: calcula os quatro incrementos (cada k já inclui h).
        k1 = h * avaliar(t, w)
        k2 = h * avaliar(t + h/2, w + k1/2)
        k3 = h * avaliar(t + h/2, w + k2/2)
        k4 = h * avaliar(t + h, w + k3)
        # Passo 4: combina os incrementos e avança no tempo.
        w = w + (k1 + 2*k2 + 2*k3 + k4)/6
        t = proximo_t
        if not isfinite(w):
            raise ValueError("Runge-Kutta produziu uma aproximação não finita.")
        # Passo 5: salva a aproximação para a tabela.
        if historico is not None:
            historico.append((i, t, w))

    # Passo 6: encerra e devolve a aproximação em b.
    return w
