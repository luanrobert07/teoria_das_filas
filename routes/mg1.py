from flask import Blueprint, render_template, request, flash
from models.mg1_queue import mg1_queue_metrics
from models.mg1_preemptive_priority import mg1_preemptive_priority_metrics
from models.mg1_non_preemptive_priority import mg1_non_preemptive_priority_metrics

bp = Blueprint("mg1", __name__, url_prefix="/mg1")


def _to_float(val, default=0.0):
    try:
        return float(str(val).replace(",", "."))
    except:
        return default


@bp.route("/", methods=["GET", "POST"])
def index():
    mode = request.form.get("mode", "mg1")   # mg1 | preemptivo | npreemptivo
    params = {}
    metrics = None
    prob_table = None

    if request.method == "POST":

        # -------------------------
        # MODELO 1 — M/G/1 padrão
        # -------------------------
        if mode == "mg1":

            lam = _to_float(request.form.get("lambda"))
            mu  = _to_float(request.form.get("mu"))
            var = _to_float(request.form.get("sigma2"))

            params = {"lambda": lam, "mu": mu, "sigma2": var}

            try:
                metrics = mg1_queue_metrics(lam, mu, var)

                # Gerar tabela P(n) usando aproximação geométrica
                rho = metrics.get("Taxa de Ocupação (ρ)", 0)
                P0  = metrics.get("\nProbabilidade de Não Esperar (P0)", 0)

                table = {}
                for n in range(21):
                    table[n] = round(P0 * (rho ** n), 6)

                prob_table = table

            except Exception as e:
                flash(str(e), "danger")

        # -------------------------
        # MODELO 2 — Preemptivo
        # -------------------------
        elif mode == "preemptivo":
            try:
                lambdas   = [_to_float(x) for x in request.form.getlist("lambda[]")]
                services  = [_to_float(x) for x in request.form.getlist("service[]")]
                variances = [_to_float(x) for x in request.form.getlist("var[]")]

                params = {"lambda": lambdas, "service": services, "var": variances}
                metrics = mg1_preemptive_priority_metrics(lambdas, services, variances)

            except Exception as e:
                flash(str(e), "danger")

        # -------------------------
        # MODELO 3 — Não-preemptivo
        # -------------------------
        elif mode == "npreemptivo":
            try:
                lambdas   = [_to_float(x) for x in request.form.getlist("lambda[]")]
                services  = [_to_float(x) for x in request.form.getlist("service[]")]
                variances = [_to_float(x) for x in request.form.getlist("var[]")]

                params = {"lambda": lambdas, "service": services, "var": variances}
                metrics = mg1_non_preemptive_priority_metrics(lambdas, services, variances)

            except Exception as e:
                flash(str(e), "danger")

    return render_template(
        "model_mg1.html",
        mode=mode,
        params=params,
        metrics=metrics,
        prob_table=prob_table
    )
