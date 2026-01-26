from flask import Flask, render_template_string, request, redirect
import pandas as pd
import os

app = Flask(__name__)

arquivo_excel = "contatos.xlsx"


if not os.path.exists(arquivo_excel):
    df = pd.DataFrame(columns=["nomes", "telefones", "status"])
    df.to_excel(arquivo_excel, index=False)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Envio WhatsApp</title>
<style>
body { font-family: Arial; background: #f4f6f8; margin:0; padding:0; }
.container { max-width:500px; margin:70px auto; background:#fff; padding:20px; border-radius:12px; box-shadow:0 10px 25px rgba(0,0,0,0.08); }
h2 { margin-top:0; color:#333; }
.contato { display:flex; justify-content:space-between; align-items:center; padding:10px; border-bottom:1px solid #eee; }
.contato:last-child { border-bottom:none; }
.contato span { font-weight:500; color:#444;  }
.contato a, .contato button { background:#25d366; color:white; padding:6px 12px; border-radius:8px; text-decoration:none; border:none; cursor:pointer; }
.contato button:hover, .contato a:hover { background:#1ebe5d; }
</style>
<script>
function atualizarLinks() {
    const msg = encodeURIComponent(document.getElementById("msg").value);
    document.querySelectorAll("a[data-tel]").forEach(a=>{
        a.href = "https://wa.me/55"+a.dataset.tel+"?text="+msg;
    });
}
function enviarTodos() {
    const links = document.querySelectorAll("a[data-tel]");
    let delay = 0;
    links.forEach(link=>{
        setTimeout(()=>{ window.open(link.href, "_blank"); }, delay);
        delay += 6000;
    });
}
</script>
</head>
<body>
<div class="container">
<h2>📲 Envio WhatsApp</h2>

<form method="POST" action="/adicionar">
<input name="nome" placeholder="Nome" required>
<input name="telefone" placeholder="Telefone" required>
<button type="submit">Adicionar</button>
</form>

<label>Mensagem:</label>
<textarea id="msg" rows="3" placeholder="Digite a mensagem..." oninput="atualizarLinks()"></textarea>
<button onclick="enviarTodos()">Enviar para todos</button>

<div>
{% for c in contatos %}
<div class="contato">
<span>{{ c.nomes }} <small>— {{ c.status }}</small></span>


<a data-tel="{{ c.telefones }}" target="_blank">Enviar</a>

<form method="POST" action="/deletar" style="display:inline;">
<input type="hidden" name="telefone" value="{{ c.telefones }}">
<button type="submit">Deletar</button>
</form>

<form method="POST" action="/marcar" style="display:inline;">
<input type="hidden" name="telefone" value="{{ c.telefones }}">
<button type="submit">Marcar enviada</button>
</form>

</div>
{% endfor %}
</div>

</div>
</body>
</html>
"""


@app.route("/")
def index():
    df = pd.read_excel(arquivo_excel, dtype=str)
    df["telefones"] = df["telefones"].str.strip()
    df["status"] = df["status"].fillna("não enviada")
    return render_template_string(HTML_TEMPLATE, contatos=df.to_dict("records"))


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
    app.run(debug=True)
