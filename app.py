from flask import Flask, render_template, request, redirect, url_for 
from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc #biblioteca para conexao com o SQL SERVER


#Criação da aplicacao Flask
app = Flask(__name__)

#Função responsavel por conectar o banco de dados SQL SERVER
def conectar_banco ():
        return pyodbc.connect(
            "DRIVER={SQL Server};"   # Driver do SQL Server
            "SERVER=localhost\\SQLEXPRESS;"   # Servidor local 
            "DATABASE=ControleGastosDB;"   # Nome do Banco
            "Trusted_Connection=yes;"  # Authenticacao do Windows
        )

# ROTA PRINCIPAl LISTAR
@app.route("/")
def index():
    #Conecta o banco
    conn = conectar_banco()
    cursor = conn.cursor()

    # Executa consulta para buscar todos os gastos
    cursor.execute("SELECT * FROM Gastos")
    gastos = cursor.fetchall()
        
    # Fecha a conexão
    conn.close()

    # Volta para a pagina principal enviando a lista de gastos
    return render_template("index.html", gastos=gastos)


# ROTA PARA ADICIONAR GASTO
@app.route("/adicionar", methods=["POST"])
def adicionar():
    # Captura dados do formulario
    descricao = request.form["descricao"]
    valor = float(request.form["valor"])
        
    # Conecta o banco
    conn = conectar_banco()
    cursor = conn.cursor()

    # Insere novo gasto no banco (usando parametros para evitar SQL injection)
    cursor.execute(
        "INSERT INTO Gastos (Descricao, Valor) VALUES (?, ?)",
        (descricao, valor)
    )
    # Salva alterações
    conn.commit()
    conn.close()
        
    return redirect(url_for("index"))


# ROTA PARA EXCLUIR GASTO
@app.route("/excluir/<int:id>")
def excluir(id):
    # Conecta com o banco
    conn = conectar_banco()
    cursor = conn.cursor()

    # Remove o registro pelo ID
    cursor.execute("DELETE FROM Gastos WHERE Id = ?", (id))

    # Salva alteracoes
    conn.commit()
    conn.close()

    return redirect (url_for("resumo"))


# ROTA DE EDITAR
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    # Conecta com o banco
    conn = conectar_banco()
    cursor = conn.cursor()
    # Se o metodo for POST, significa que o usuario enviou o formula
    if request.method == "POST":
        descricao = request.form["descricao"]
        valor = float(request.form["valor"])

    # Atualiza o gasto no banco
        cursor.execute(
            "UPDATE Gastos SET Descricao = ?, Valor = ? WHERE Id = ?",
            (descricao, valor, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("resumo"))

    # Se for GET, busca o gasto para preencher o formulario
    cursor.execute("SELECT * FROM Gastos WHERE Id = ?", (id,))
    gasto = cursor.fetchone()
    conn.close()

    return render_template("editar.html", gasto=gasto)

# ROTA DO RESUMO
@app.route("/resumo")
def resumo():
    conn = conectar_banco()
    cursor = conn.cursor()

    # Busca todos os gastos
    cursor.execute("SELECT * FROM Gastos")
    gastos = cursor.fetchall()

    conn.close()

    # Verifica se não há registros
    if len(gastos) == 0:
        return render_template("resumo.html", vazio=True)

    # Calculo estatísticos
    total = sum(g[2] for g in gastos) #Soma total
    media = total / len(gastos)       #Media
    maior = max(g[2] for g in gastos) #Maior valor
    menor = min(g[2] for g in gastos) #Menor valor

    # Envia os dados para o formulario
    return render_template(
    "resumo.html",
    vazio=False,
    total=total,
    media=media,
    maior=maior,
    menor=menor,
    gastos=gastos
    )

# Executa o servidor flask em modo debug
if __name__ == "__main__":
        app.run(debug=True)
