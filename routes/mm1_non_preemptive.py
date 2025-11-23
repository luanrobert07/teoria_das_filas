from flask import Blueprint, render_template, request, flash
from models.mm1_non_preemptive_priority import mm1_priority_non_preemptive_metrics

bp = Blueprint("mm1_non_preemptive", __name__, url_prefix="/mm1_non_preemptive")


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

        mu = _to_float(request.form.get("mu", 0))
        lambdas_raw = request.form.getlist("lambda[]")

        lambdas = []
        for x in lambdas_raw:
            f = _to_float(x, None)
            if f is not None:
                lambdas.append(f)

        params = {
            "lambda": lambdas,
            "mu": mu
        }

        if len(lambdas) == 0:
            flash("Informe pelo menos um valor de λ.", "danger")
        else:
            try:
                metrics = mm1_priority_non_preemptive_metrics(lambdas, mu)

                if "Erro" in metrics:
                    flash(metrics["Erro"], "danger")
                    metrics = None

            except Exception as e:
                flash(str(e), "danger")

    return render_template(
        "model_mm1_non_preemptive.html",
        params=params,
        metrics=metrics
    )
