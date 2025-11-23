from flask import Blueprint, render_template, request, flash
from models.mmcn_queue import mmcn_queue_metrics

bp = Blueprint("mmcn", __name__, url_prefix="/mmcn")

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
            s = int(request.form.get("s", 1))
        except:
            s = 1
        try:
            N = int(request.form.get("N", 0))
        except:
            N = 0
        CE = _to_float(request.form.get("CE", 0))
        CA = _to_float(request.form.get("CA", 0))

        params = {"lambda": lam, "mu": mu, "s": s, "N": N, "CE": CE, "CA": CA}
        try:
            metrics = mmcn_queue_metrics(lam, mu, s, N, CE, CA)
            if isinstance(metrics, dict) and "Erro" in metrics:
                flash(metrics["Erro"], "danger")
                metrics = None
        except Exception as e:
            flash(f"Erro ao executar M/M/c/N: {e}", "danger")

    return render_template("model_mmcn.html", params=params, metrics=metrics)
