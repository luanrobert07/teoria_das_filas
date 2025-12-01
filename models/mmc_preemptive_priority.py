# models/mmc_preemptive_priority.py
from math import factorial
from decimal import Decimal, getcontext

getcontext().prec = 28


def _round(v, places=6):
    try:
        return round(float(v), places)
    except:
        return v


def mmc_priority_preemptive_metrics(arrival_rates, service_rate, s):
    """
    Implementação do modelo M/M/s com prioridades preemptivas (interrupção),
    baseada no código de referência que você enviou.

    Parâmetros:
      arrival_rates: lista [λ1, λ2, ..., λk] (ordem: maior prioridade → menor)
      service_rate: μ (float ou Decimal)
      s: número de servidores (int)

    Retorno:
      dict com chaves "Classe 1", "Classe 2", ... contendo W, Wq, L, Lq (valores arredondados).
    """
    # Validações básicas
    try:
        mi = float(service_rate)
    except:
        return {"Erro": "Taxa de serviço (μ) inválida."}

    try:
        s = int(s)
    except:
        return {"Erro": "Número de servidores (s) inválido."}

    if mi <= 0:
        return {"Erro": "Taxa de serviço deve ser maior que zero"}
    if s <= 0:
        return {"Erro": "Número de servidores deve ser maior que zero"}

    # converter lambdas para floats e validar
    try:
        lambdas = [float(l) for l in arrival_rates]
    except:
        return {"Erro": "Taxas de chegada inválidas."}

    if any(l < 0 for l in lambdas):
        return {"Erro": "Taxas de chegada devem ser maiores ou iguais a zero"}

    lambdas_total = sum(lambdas)
    capacidade = mi * s
    rho = lambdas_total / capacidade if capacidade != 0 else float("inf")

    if rho >= 1:
        return {"Erro": "Soma das taxas deve ser menor que a capacidade do servidor"}

    resultados = {}

    # Caso s == 1 (fórmulas preemptivas clássicas)
    if s == 1:
        for i, lam_i in enumerate(lambdas):
            soma_lambdas = sum(lambdas[j] for j in range(i + 1))
            soma_lambdas_i_menos_1 = sum(lambdas[j] for j in range(i)) if i > 0 else 0.0

            denom = (1.0 - (soma_lambdas_i_menos_1 / mi)) * (1.0 - (soma_lambdas / mi))
            if denom <= 0:
                return {
                    "Erro": f"Denominador inválido na classe {i+1}. Verifique λ e μ."
                }

            W = (1.0 / mi) / denom
            Wq = W - (1.0 / mi)

            L = soma_lambdas * W
            Lq = L - (soma_lambdas / mi)

            resultados[f"Classe {i+1}"] = {
                "W": _round(W),
                "Wq": _round(Wq),
                "L": _round(L),
                "Lq": _round(Lq),
            }

        return resultados

    # Caso s > 1
    def Pw(lambd, mi_local, s_local):
        """Calcula Pw (Erlang-C like) para taxa lambda=lambd, serviço mi_local e s_local servidores."""
        a = lambd / mi_local
        # sum_{k=0}^{s-1} a^k / k!
        sum_terms = sum((a**k) / factorial(k) for k in range(s_local))
        last_term = (
            (a**s_local / factorial(s_local))
            * (s_local * mi_local)
            / (s_local * mi_local - lambd)
        )
        if (s_local * mi_local - lambd) <= 0:
            # retorno sinalizando erro
            return None
        return last_term / (sum_terms + last_term)

    # Ws mantém W calculados para classes anteriores (necessário no algoritmo)
    Ws = []

    for i, lam_i in enumerate(lambdas):
        soma_lambdas = sum(lambdas[j] for j in range(i + 1))

        Pw_bar = Pw(soma_lambdas, mi, s)
        if Pw_bar is None:
            return {
                "Erro": f"Denominador inválido no cálculo de Pw para a classe {i+1}. Verifique λ e μ."
            }

        Wq_bar = Pw_bar / (s * mi - soma_lambdas)
        W_bar = Wq_bar + 1.0 / mi

        if i == 0:
            # primeira classe: W igual ao W_bar (tempo médio ponderado)
            W = W_bar
        else:
            # soma_previas = Σ_{j=0}^{i-1} λ_j * W_j
            soma_previas = sum(lambdas[j] * Ws[j] for j in range(i))
            # rearranjo para obter W_i:
            # soma_lambdas * W_bar = soma_previas + lam_i * W_i  =>  W_i = (soma_lambdas*W_bar - soma_previas)/lam_i
            if lam_i == 0:
                # evita divisão por zero: se λ_i == 0 então W_i não importa (põe 0)
                W = 0.0
            else:
                W = (soma_lambdas * W_bar - soma_previas) / lam_i

        Ws.append(W)

        Wq = W - 1.0 / mi

        L = soma_lambdas * W
        Lq = L - (soma_lambdas / mi)

        resultados[f"Classe {i+1}"] = {
            "W": _round(W),
            "Wq": _round(Wq),
            "L": _round(L),
            "Lq": _round(Lq),
        }

    return resultados
