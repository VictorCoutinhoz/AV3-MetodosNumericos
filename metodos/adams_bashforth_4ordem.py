from math import isfinite

from .runge_kutta_4ordem import runge_kutta_4ordem


def adams_bashforth_4ordem(funcao, a, b, alfa, n, historico=None, iniciais=None):
    # iniciais: w1, w2 e w3. Se omitidos, são calculados com RK4.
    if not all(isfinite(valor) for valor in (a, b, alfa)) or a >= b:
        raise ValueError("Use valores finitos e um intervalo com a < b.")
    if type(n) is not int or n < 4:
        raise ValueError("Adams-Bashforth precisa de pelo menos quatro passos.")
    if iniciais is not None:
        if len(iniciais) != 3 or not all(isfinite(valor) for valor in iniciais):
            raise ValueError("Informe três valores finitos para w1, w2 e w3.")

    h = (b - a) / n
    if not isfinite(h) or h <= 0:
        raise ValueError("Não foi possível calcular um passo finito e positivo.")

    def avaliar(t, w):
        valor = funcao(t, w)
        if not isfinite(valor):
            raise ValueError("A função deve retornar valores finitos.")
        return valor

    # Prepara os quatro valores iniciais: w0, w1, w2 e w3.
    inicio = []
    try:
        if iniciais is None:
            runge_kutta_4ordem(funcao, a, a + 3*h, alfa, 3, inicio)
        else:
            for i, w in enumerate([alfa, *iniciais]):
                t = a + i*h
                if i > 0 and t <= inicio[-1][1]:
                    raise ValueError("O passo é pequeno demais para a precisão disponível.")
                inicio.append((i, t, w))
    finally:
        if historico is not None:
            historico.extend(inicio)

    # Inclinações da mais antiga à mais recente.
    f0, f1, f2, f3 = [avaliar(t, w) for _, t, w in inicio]
    _, t, w = inicio[-1]
    for i in range(3, n):
        proximo_t = b if i == n - 1 else a + (i + 1)*h
        if proximo_t <= t:
            raise ValueError("O passo é pequeno demais para a precisão disponível.")
        # Fórmula de Adams-Bashforth de quatro passos, como no material.
        w = w + h*(55*f3 - 59*f2 + 37*f1 - 9*f0)/24
        t = proximo_t
        if not isfinite(w):
            raise ValueError("Adams-Bashforth produziu uma aproximação não finita.")
        if historico is not None:
            historico.append((i + 1, t, w))
        if i < n - 1:
            f0, f1, f2, f3 = f1, f2, f3, avaliar(t, w)

    return w
