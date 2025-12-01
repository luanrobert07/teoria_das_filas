from flask import Blueprint, render_template, request, flash
from models.mm1k_queue import mm1k_queue_metrics

bp = Blueprint("mm1k", __name__, url_prefix="/mm1k")


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
        K = int(request.form.get("K", 0))
        CE = _to_float(request.form.get("CE"))
        CA = _to_float(request.form.get("CA"))
        n_raw = request.form.get("n", "0")

        try:
            n = int(n_raw)
        except:
            n = 0

        params = {
            "lambda": lam,
            "mu": mu,
            "K": K,
            "CE": CE,
            "CA": CA,
            "n": n,
        }

        try:
            metrics = mm1k_queue_metrics(lam, mu, K, CE, CA, n)

            if "Erro" in metrics:
                flash(metrics["Erro"], "danger")
                return render_template("model_mm1k.html", params=params)

        except Exception as e:
            flash(f"Erro ao executar M/M/1/K: {e}", "danger")
            return render_template("model_mm1k.html", params=params)

        prob_list = metrics.get("Probabilidade de existir n clientes (Pn)", [])

        prob_table = {}
        for i, val in enumerate(prob_list):
            prob_table[i] = val

        metrics["prob_table"] = prob_table

    return render_template("model_mm1k.html", params=params, metrics=metrics)
