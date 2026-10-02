from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect("database.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        local TEXT NOT NULL,
        contato TEXT NOT NULL,
        tipo TEXT NOT NULL,
        resolvido INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

criar_tabela()

@app.route("/")
def index():
    filtro = request.args.get("filtro", "todos")

    conn = conectar()
    cursor = conn.cursor()

    if filtro == "perdido":
        cursor.execute("SELECT * FROM itens WHERE tipo='Perdido'")
    elif filtro == "encontrado":
        cursor.execute("SELECT * FROM itens WHERE tipo='Encontrado'")
    else:
        cursor.execute("SELECT * FROM itens")

    itens = cursor.fetchall()
    conn.close()

    return render_template("index.html", itens=itens)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():

    if request.method == "POST":

        nome = request.form["nome"]
        descricao = request.form["descricao"]
        local = request.form["local"]
        contato = request.form["contato"]
        tipo = request.form["tipo"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO itens
        (nome, descricao, local, contato, tipo)
        VALUES (?, ?, ?, ?, ?)
        """, (nome, descricao, local, contato, tipo))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("cadastrar.html")

@app.route("/resolver/<int:id>")
def resolver(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE itens
    SET resolvido = 1
    WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)