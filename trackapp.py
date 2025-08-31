from flask import Flask, render_template, request, redirect, url_for
from models import db, Incident

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///incidents.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.before_first_request
def init_db():
    db.create_all()

@app.route("/")
def index():
    q = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template("list.html", incidents=q)

@app.route("/new", methods=["GET", "POST"])
def create_incident():
    if request.method == "POST":
        inc = Incident(
            title=request.form["title"],
            severity=request.form.get("severity", "Low"),
            status=request.form.get("status", "Open"),
            notes=request.form.get("notes", "")
        )
        db.session.add(inc); db.session.commit()
        return redirect(url_for("index"))
    return render_template("form.html", inc=None)

@app.route("/edit/<int:inc_id>", methods=["GET", "POST"])
def edit_incident(inc_id):
    inc = Incident.query.get_or_404(inc_id)
    if request.method == "POST":
        inc.title = request.form["title"]
        inc.severity = request.form.get("severity", inc.severity)
        inc.status = request.form.get("status", inc.status)
        inc.notes = request.form.get("notes", inc.notes)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("form.html", inc=inc)

@app.post("/delete/<int:inc_id>")
def delete_incident(inc_id):
    inc = Incident.query.get_or_404(inc_id)
    db.session.delete(inc); db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
