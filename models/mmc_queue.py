import math


def mmc_queue_metrics(
    arrival_rate,
    service_rate,
    num_servers,
    waiting_time_w,
    waiting_time_wq,
    num_clients,
):
    """
    Cálculo completo para o modelo M/M/s.
    """

    # Verificar estabilidade
    if service_rate * num_servers <= arrival_rate:
        return {"Erro": "O sistema é instável (λ >= c * μ)."}

    rho = arrival_rate / (num_servers * service_rate)

    # ---------- P0 ----------
    sum_terms = sum(
        (arrival_rate / service_rate) ** n / math.factorial(n)
        for n in range(num_servers)
    )

    last_term = (
        (arrival_rate / service_rate) ** num_servers / math.factorial(num_servers)
    ) * (1 / (1 - rho))

    P0 = 1 / (sum_terms + last_term)

    # ---------- Probabilidade de formação de fila ----------
    P_queue = (
        P0 * (arrival_rate / service_rate) ** num_servers / math.factorial(num_servers)
    ) * (1 / (1 - rho))

    # ---------- Lq ----------
    L_q = P_queue * rho / (1 - rho)

    # ---------- L ----------
    L = L_q + arrival_rate / service_rate

    # ---------- Wq ----------
    W_q = L_q / arrival_rate

    # ---------- W ----------
    W = W_q + 1 / service_rate

    # ---------- Probabilidade de W > t ----------
    if waiting_time_w < 0 or waiting_time_wq < 0:
        return {"Erro": "Os tempos de espera devem ser >= 0."}

    exp_term_w = math.exp(-service_rate * waiting_time_w)
    bracket_num = 1 - math.exp(
        -service_rate
        * waiting_time_w
        * (num_servers - 1 - (arrival_rate / service_rate))
    )
    bracket_den = num_servers - 1 - (arrival_rate / service_rate)

    if bracket_den == 0:
        P_W_greater_t = exp_term_w
    else:
        P_W_greater_t = exp_term_w * (
            1
            + (
                P0
                * (arrival_rate / service_rate) ** num_servers
                / (math.factorial(num_servers) * (1 - rho))
            )
            * (bracket_num / bracket_den)
        )

    # ---------- Probabilidade de Wq > t ----------
    P_Wq_equals_0 = sum(
        ((arrival_rate / service_rate) ** n / math.factorial(n)) * P0
        for n in range(num_servers)
    )

    P_Wq_greater_t = (1 - P_Wq_equals_0) * math.exp(
        -service_rate * (num_servers - rho * num_servers) * waiting_time_wq
    )

    # ---------- Probabilidade de ter n clientes ----------
    if num_clients < num_servers:
        P_n = (
            (arrival_rate / service_rate) ** num_clients / math.factorial(num_clients)
        ) * P0
    else:
        P_n = (
            (arrival_rate / service_rate) ** num_clients
            / (math.factorial(num_servers) * num_servers ** (num_clients - num_servers))
        ) * P0

    # ---------- Probabilidade N > n ----------
    def P_k(k):
        if k < num_servers:
            return ((arrival_rate / service_rate) ** k / math.factorial(k)) * P0
        else:
            return (
                (arrival_rate / service_rate) ** k
                / (math.factorial(num_servers) * num_servers ** (k - num_servers))
            ) * P0

    P_more_than_n = 1 - sum(P_k(k) for k in range(num_clients + 1))

    # ---------- Probabilidade N ≤ n ----------
    P_up_to_n = 1 - P_more_than_n

    return {
        "Taxa de Ocupação (ρ)": rho,
        "Probabilidade do sistema estar vazio (P0)": P0,
        "Probabilidade de Fila (P_queue)": P_queue,
        "Número Médio na Fila (Lq)": L_q,
        "Número Médio no Sistema (L)": L,
        "Tempo Médio na Fila (Wq)": W_q,
        "Tempo Médio no Sistema (W)": W,
        "Probabilidade de W > t": P_W_greater_t,
        "Probabilidade de Wq > t": P_Wq_greater_t,
        # As três que você pediu:
        "P(n) — Probabilidade de haver n clientes": P_n,
        "P(N > n) — Probabilidade de haver mais que n clientes": P_more_than_n,
        "P(N ≤ n) — Probabilidade de haver até n clientes": P_up_to_n,
    }
