# routes/mmc_no_preemptive.py
from flask import Blueprint, render_template, request, flash
from models.mmc_no_preemptive_priority import mmc_no_preemptive_priority

bp = Blueprint("mmc_no_preemptive", __name__, url_prefix="/mmc_no_preemptive")


def _to_float(val, default=None):
    try:
        return float(str(val).replace(",", "."))
    except:
        return default


@bp.route("/", methods=["GET", "POST"])
def index():
    params = {"mu": "", "servers": "1", "lambda": []}
    metrics = None

    if request.method == "POST":
        mu = _to_float(request.form.get("mu"))
        servers_raw = request.form.get("servers", "1")

        try:
            servers = int(servers_raw)
        except:
            flash("Número de servidores inválido.", "danger")
            return render_template(
                "model_mmc_no_preemptive.html", params=params, metrics=None
            )

        lambdas = []
        for v in request.form.getlist("lambda[]"):
            x = _to_float(v)
            if x is not None:
                lambdas.append(x)

        params = {"mu": mu, "servers": servers, "lambda": lambdas}

        if mu is None:
            flash("Informe µ válido.", "danger")

        elif servers <= 0:
            flash("Servidores deve ser maior que zero.", "danger")

        elif not lambdas:
            flash("Informe ao menos um λ.", "danger")

        else:
            try:
                metrics = mmc_no_preemptive_priority(lambdas, mu, servers)
                if isinstance(metrics, dict) and "Erro" in metrics:
                    flash(metrics["Erro"], "danger")
                    metrics = None

            except Exception as e:
                flash(str(e), "danger")

    return render_template(
        "model_mmc_no_preemptive.html", params=params, metrics=metrics
    )
