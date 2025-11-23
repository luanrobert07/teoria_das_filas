from flask import Blueprint, render_template, request, flash
from models.mm1n_queue import mm1n_queue_metrics

bp = Blueprint("mm1n", __name__, url_prefix="/mm1n")

def _to_float(val, default=0.0):
    try:
        return float(str(val).replace(",", "."))
    except:
        return default

@bp.route("/", methods=["GET", "POST"])
def index():
    params = {}
    metrics = None

    if request.method == "POST":
        lam = _to_float(request.form.get("lambda"))
        mu  = _to_float(request.form.get("mu"))

        try:
            N = int(request.form.get("N", 0))
        except:
            N = 0

        CE = _to_float(request.form.get("CE", 0))
        CA = _to_float(request.form.get("CA", 0))

        params = {"lambda": lam, "mu": mu, "N": N, "CE": CE, "CA": CA}

        try:
            metrics = mm1n_queue_metrics(lam, mu, N, CE, CA)
            if isinstance(metrics, dict) and "Erro" in metrics:
                flash(metrics["Erro"], "danger")
                metrics = None

        except Exception as e:
            flash(f"Erro ao executar M/M/1/N: {e}", "danger")
            metrics = None

    return render_template("model_mm1n.html", params=params, metrics=metrics)
