from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

arquivo_excel = "contatos.xlsx"

# cria o excel se não existir
if not os.path.exists(arquivo_excel):
    df = pd.DataFrame(columns=["nomes", "telefones", "status"])
    df.to_excel(arquivo_excel, index=False)

@app.route("/")
def index():
    df = pd.read_excel(arquivo_excel, dtype=str)

    # garante que não quebre se estiver vazio
    if df.empty:
        df = pd.DataFrame(columns=["nomes", "telefones", "status"])

    df["telefones"] = df["telefones"].str.strip()
    df["status"] = df["status"].fillna("não enviada")

    return render_template("index.html", contatos=df.to_dict("records"))

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form["nome"].strip()
    telefone = request.form["telefone"].strip()

    df = pd.read_excel(arquivo_excel, dtype=str)

    novo = pd.DataFrame([{
        "nomes": nome,
        "telefones": telefone,
        "status": "não enviada"
    }])

    df = pd.concat([df, novo], ignore_index=True)
    df.to_excel(arquivo_excel, index=False)

    return redirect("/")

@app.route("/deletar", methods=["POST"])
def deletar():
    telefone = request.form["telefone"].strip()

    df = pd.read_excel(arquivo_excel, dtype=str)
    df["telefones"] = df["telefones"].str.strip()

    df = df[df["telefones"] != telefone]
    df.to_excel(arquivo_excel, index=False)

    return redirect("/")

@app.route("/marcar", methods=["POST"])
def marcar():
    telefone = request.form["telefone"].strip()

    df = pd.read_excel(arquivo_excel, dtype=str)
    df["telefones"] = df["telefones"].str.strip()

    df.loc[df["telefones"] == telefone, "status"] = "enviada"
    df.to_excel(arquivo_excel, index=False)

    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
