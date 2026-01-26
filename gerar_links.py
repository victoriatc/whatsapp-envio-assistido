import pandas as pd
import urllib.parse

mensagem = "Victoria é linda"
arquivo_excel = "contatos.xlsx"
arquivo_html = "index.html"

df = pd.read_excel(arquivo_excel)
mensagem_encoded = urllib.parse.quote(mensagem)

html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Envio WhatsApp</title>
</head>
<body>
<h2>Envio de mensagens</h2>
"""

for _, row in df.iterrows():
    nome = row["nomes"]
    telefone = str(row["telefones"]).replace(".0", "").strip()

    if len(telefone) >= 10:
        link = f"https://wa.me/55{telefone}?text={mensagem_encoded}"
        html += f'''
        <p>
          <a class="whatsapp-link" href="{link}" target="_blank">
            Enviar para {nome}
          </a>
        </p>
        '''

html += """
</body>
</html>
"""

with open(arquivo_html, "w", encoding="utf-8") as f:
    f.write(html)

print("index.html criado com sucesso!")
