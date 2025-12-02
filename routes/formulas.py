from flask import Blueprint, render_template

bp = Blueprint("formulas", __name__, url_prefix="/formulas")


@bp.route("/")
def index():
    return render_template("model_formulas.html")
