from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

gastos = []

@app.route("/excluir/<int:index>")
def exluir(index):
    gastos.pop(index)
    return redirect(url_for("resumo"))

@app.route("/editar/<int:index>", methods=["GET", "POST"])
def editar(index):

    if request.method == "POST":
        gastos[index]["descricao"] = request.form["descricao"]
        gastos[index]["valor"] = float(request.form["valor"])
        return redirect(url_for("resumo"))

    return render_template("editar.html", gasto=gastos[index])


@app.route("/apagar")
def apagar():
    gastos.clear()
    return redirect(url_for("resumo"))

@app.route("/")
def index():
    return render_template("index.html", gastos=gastos)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    valor = float(request.form["valor"])
    descricao = request.form["descricao"]

    gastos.append({
        "valor": valor,
        "descricao": descricao
    })

    return redirect(url_for("index"))

@app.route("/resumo")
def resumo():
    if not gastos:
        return render_template("resumo.html", vazio=True)

    total = sum(g["valor"] for g in gastos)
    media = total / len(gastos)
    maior = max(g["valor"] for g in gastos)
    menor = min(g["valor"] for g in gastos)

    return render_template(
       "resumo.html",
       vazio=False,
       total=total,
       media=media,
       maior=maior,
       menor=menor,
       gastos=gastos
    )

if __name__ == "__main__":
    app.run(debug=True)