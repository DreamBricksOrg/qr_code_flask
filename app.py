from flask import Flask, render_template, request, send_file
from utils import gerar_codigos_unicos, gerar_qr_codes, salvar_em_zip
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        quantidade = int(request.form.get("quantidade"))
        codigos = gerar_codigos_unicos(quantidade)
        zip_path = salvar_em_zip(codigos)
        return send_file(zip_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)