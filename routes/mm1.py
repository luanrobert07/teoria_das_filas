from flask import Blueprint, render_template, request, flash
from models.mm1_queue import mm1_queue_metrics

bp = Blueprint("mm1", __name__, url_prefix="/mm1")


def _to_float(value, default=0.0):
    """
    Converte string para float, aceitando vírgula como decimal.
    """
    try:
        return float(str(value).replace(",", "."))
    except:
        return default


@bp.route("/", methods=["GET", "POST"])
def index():
    params = {}
    metrics = None

    if request.method == "POST":

        # ---------------- PARÂMETROS ----------------
        lam = _to_float(request.form.get("lambda"))
        mu = _to_float(request.form.get("mu"))
        t_w = _to_float(request.form.get("t_w", 0))
        t_wq = _to_float(request.form.get("t_wq", 0))

        n_field = request.form.get("n", "0")
        try:
            n = int(n_field)
        except:
            n = 0

        params = {
            "lambda": lam,
            "mu": mu,
            "t_w": t_w,
            "t_wq": t_wq,
            "n": n,
        }

        # ---------------- EXECUÇÃO DO MODELO ----------------
        try:
            metrics = mm1_queue_metrics(lam, mu, t_w, t_wq, n)

            if "Erro" in metrics:
                flash(metrics["Erro"], "danger")
                return render_template("model_mm1.html", params=params)

        except Exception as e:
            flash(f"Erro ao executar o M/M/1: {e}", "danger")
            return render_template("model_mm1.html", params=params)

        # ---------------- GERAÇÃO DA TABELA P(0) → P(20) ----------------
        rho = (
            metrics.get("Taxa de Ocupação (ρ)")
            or metrics.get("\nTaxa de Ocupação (ρ)")
            or 0
        )

        # P0 pode aparecer com 2 chaves diferentes → capturar corretamente
        P0 = (
            metrics.get("Probabilidade de Não Esperar (P_0)")
            or metrics.get("Probabilidade de o Sistema Ocioso (P(n=0))")
            or (1 - rho)
        )

        prob_table = {}
        for k in range(21):  # Gera P(0) até P(20)
            prob_table[k] = round(P0 * (rho ** k), 6)

        metrics["prob_table"] = prob_table

    # Render final
    return render_template("model_mm1.html", params=params, metrics=metrics)
