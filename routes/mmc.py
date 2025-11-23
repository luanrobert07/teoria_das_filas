import math
from flask import Blueprint, render_template, request, flash
from models.mmc_queue import mmc_queue_metrics

bp = Blueprint("mmc", __name__, url_prefix="/mmc")


def _to_float(value, default=0.0):
    try:
        return float(str(value).replace(",", "."))
    except:
        return default


@bp.route("/", methods=["GET", "POST"])
def index():
    params = {}
    metrics = None

    if request.method == "POST":
        lam = _to_float(request.form.get("lambda"))
        mu = _to_float(request.form.get("mu"))
        c = int(request.form.get("c", 1))
        t_w = _to_float(request.form.get("t_w"))
        t_wq = _to_float(request.form.get("t_wq"))

        n_raw = request.form.get("n", "0")
        try:
            n = int(n_raw)
        except:
            n = 0

        params = {
            "lambda": lam,
            "mu": mu,
            "c": c,
            "t_w": t_w,
            "t_wq": t_wq,
            "n": n,
        }

        try:
            metrics = mmc_queue_metrics(lam, mu, c, t_w, t_wq, n)

            if "Erro" in metrics:
                flash(metrics["Erro"], "danger")
                return render_template("model_mmc.html", params=params)

        except Exception as e:
            flash(f"Erro ao executar o modelo M/M/s: {e}", "danger")
            return render_template("model_mmc.html", params=params)

        # ----------- GERAR TABELA P(0→N) -----------
        prob_table = {}

        P0 = metrics.get("Probabilidade do sistema estar vazio (P0)") or 0
        rho = metrics.get("\nTaxa de Ocupação (ρ)") or 0

        for i in range(n + 1):
            if i < c:
                val = (pow(lam / mu, i) / math.factorial(i)) * P0
            else:
                val = (
                    pow(lam / mu, i)
                    / (math.factorial(c) * pow(c, i - c))
                ) * P0

            prob_table[i] = round(val, 6)

        metrics["prob_table"] = prob_table

    return render_template("model_mmc.html", params=params, metrics=metrics)
