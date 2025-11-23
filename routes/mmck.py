from flask import Blueprint, render_template, request, flash
from models.mmck_queue import mmc_k_queue_metrics

bp = Blueprint("mmck", __name__, url_prefix="/mmck")

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
            c = int(request.form.get("c", 1))
        except:
            c = 1

        try:
            K = int(request.form.get("K", 0))
        except:
            K = 0

        CE = _to_float(request.form.get("CE", 0))
        CA = _to_float(request.form.get("CA", 0))

        try:
            n = int(request.form.get("n", 0))
        except:
            n = 0

        params = {
            "lambda": lam,
            "mu": mu,
            "c": c,
            "K": K,
            "CE": CE,
            "CA": CA,
            "n": n,
        }

        try:
            metrics = mmc_k_queue_metrics(lam, mu, c, K, CE, CA, n)

            if isinstance(metrics, dict) and "Erro" in metrics:
                flash(metrics["Erro"], "danger")
                metrics = None

        except Exception as e:
            flash(f"Erro ao executar M/M/c/K: {e}", "danger")
            metrics = None

    return render_template("model_mmck.html", params=params, metrics=metrics)
