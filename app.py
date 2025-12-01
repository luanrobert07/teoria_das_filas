from flask import Flask, render_template
from routes.mm1 import bp as mm1_bp
from routes.mmc import bp as mmc_bp
from routes.mm1k import bp as mm1k_bp
from routes.mmck import bp as mmck_bp
from routes.mm1n import bp as mm1n_bp
from routes.mmcn import bp as mmcn_bp
from routes.mg1 import bp as mg1_bp
from routes.mm1_preemptive import bp as mm1_preemptive_bp
from routes.mm1_non_preemptive import bp as mm1n_non_preemptive_bp
from routes.mmc_preemptive import bp as mmc_preemptive_bp
from routes.mmc_no_preemptive import bp as mmc_no_preemptive_bp
from routes.help import bp as help_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-key"

app.register_blueprint(mm1_bp)
app.register_blueprint(mmc_bp)
app.register_blueprint(mm1k_bp)
app.register_blueprint(mmck_bp)
app.register_blueprint(mm1n_bp)
app.register_blueprint(mmcn_bp)
app.register_blueprint(mg1_bp)
app.register_blueprint(mm1_preemptive_bp)
app.register_blueprint(mm1n_non_preemptive_bp)
app.register_blueprint(mmc_preemptive_bp)
app.register_blueprint(mmc_no_preemptive_bp)
app.register_blueprint(help_bp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)
