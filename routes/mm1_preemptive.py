from flask import Blueprint, render_template, request, flash
from models.mm1_preemptive_priority import mm1_priority_preemptive_metrics

bp = Blueprint("mm1_preemptive", __name__, url_prefix="/mm1_preemptive")


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

        lambdas_raw = request.form.getlist("lambda[]")
        mu = _to_float(request.form.get("mu", 0))

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
            flash("Informe ao menos uma taxa λ.", "danger")

        else:
            try:
                metrics = mm1_priority_preemptive_metrics(lambdas, mu)

                if isinstance(metrics, dict) and "Erro" in metrics:
                    flash(metrics["Erro"], "danger")
                    metrics = None

            except Exception as e:
                flash(str(e), "danger")

    return render_template("model_mm1_preemptive.html",
                           params=params,
                           metrics=metrics)
