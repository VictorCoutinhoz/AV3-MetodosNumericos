from math import isfinite


def newton(funcao, derivada, p0, tolerancia=1e-6, max_iteracoes=1000, historico=None):
    # p0: chute inicial; tolerancia: TOL; max_iteracoes: N0.

    # Confere as entradas.
    if not all(isfinite(valor) for valor in (p0, tolerancia)) or tolerancia <= 0:
        raise ValueError("Use uma aproximação finita e tolerância positiva e finita.")
    if not isinstance(max_iteracoes, int) or max_iteracoes <= 0:
        raise ValueError("O número máximo de iterações deve ser inteiro positivo.")

    # Passos 1, 2 e 5: conta as iterações de 1 até N0.
    for iteracao in range(1, max_iteracoes + 1):
        # Calcula f(p0).
        fp0 = funcao(p0)
        if not isfinite(fp0):
            raise ValueError("A função deve retornar valores finitos.")
        # Para se p0 já for raiz.
        if fp0 == 0:
            return p0
        # Calcula f'(p0).
        dp0 = derivada(p0)
        if not isfinite(dp0):
            raise ValueError("A derivada deve retornar valores finitos.")
        # Evita divisão por zero.
        if dp0 == 0:
            raise ValueError(f"Derivada nula na iteração {iteracao}. Escolha outra aproximação inicial.")
        # Passo 3: calcula o próximo chute pela fórmula de Newton.
        p = p0 - fp0 / dp0
        if not isfinite(p):
            raise ValueError("Newton produziu uma aproximação não finita.")
        # Calcula f(p) e salva a iteração na tabela.
        fp = funcao(p)
        if not isfinite(fp):
            raise ValueError("A função deve retornar valores finitos.")
        if historico is not None:
            historico.append((iteracao, p0, p, fp))
        # Passo 4: para se a diferença entre os chutes for menor que TOL.
        if abs(p - p0) < tolerancia:
            return p
        # Passo 6: atualiza o chute.
        p0 = p
    # Passo 7: avisa que o limite de iterações acabou.
    raise ValueError(f"O método falhou após {max_iteracoes} iterações. N0 = {max_iteracoes}.")
