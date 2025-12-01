# models/mmc_no_preemptive_priority.py
import math
from decimal import Decimal, getcontext

getcontext().prec = 28


def _round(v, casas=6):
    try:
        return round(float(v), casas)
    except:
        return v


def mmc_no_preemptive_priority(arrival_rates, service_rate, servers):
    """
    Modelo M/M/s com prioridade SEM interrupção.
    Fórmulas iguais às do seu professor/exemplo.
    """

    # ----------------------
    # Validações
    # ----------------------
    try:
        mi = float(service_rate)
    except:
        return {"Erro": "Taxa de serviço (µ) inválida"}

    try:
        servers = int(servers)
    except:
        return {"Erro": "Número de servidores (s) inválido"}

    if mi <= 0:
        return {"Erro": "µ deve ser maior que zero"}
    if servers <= 0:
        return {"Erro": "s deve ser maior que zero"}

    try:
        lambdas_ = [float(l) for l in arrival_rates]
    except:
        return {"Erro": "Taxas λ inválidas"}

    if any(l < 0 for l in lambdas_):
        return {"Erro": "λ deve ser >= 0"}

    lambda_total = sum(lambdas_)
    capacidade = servers * mi
    rho = lambda_total / capacidade

    if lambda_total >= capacidade:
        return {"Erro": "Sistema instável: λ_total ≥ s·µ"}

    # ----------------------
    # Cálculo comum
    # ----------------------
    r = lambda_total / mi
    s = servers

    soma_r = sum((r**j) / math.factorial(j) for j in range(s))
    r_pow_s = r**s

    # termo base do denominador
    termo = (math.factorial(s) * (s * mi - lambda_total) / r_pow_s) * soma_r + s * mi

    resultados = {}

    # ----------------------
    # Computar classe por classe
    # ----------------------
    for i, lam_i in enumerate(lambdas_):
        soma_prev = sum(lambdas_[:i])
        soma_i = soma_prev + lam_i

        termo2 = 1.0 - soma_prev / capacidade
        termo3 = 1.0 - soma_i / capacidade

        if termo <= 0 or termo2 <= 0 or termo3 <= 0:
            return {"Erro": f"Divisão inválida na classe {i+1}. Verifique λ e µ."}

        # Fórmulas do professor
        Wq = 1.0 / (termo * termo2 * termo3)
        W = Wq + 1.0 / mi

        L = lam_i * W
        Lq = L - lam_i / mi

        resultados[f"Classe {i+1}"] = {
            "W": _round(W),
            "Wq": _round(Wq),
            "L": _round(L),
            "Lq": _round(Lq),
            "ρ_total": _round(rho),
        }

    return resultados
