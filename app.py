from flask import Flask, render_template, request, redirect, url_for, flash, abort
from database import conectar
from criar_banco import criar_banco

app = Flask(__name__)
app.config["SECRET_KEY"] = "cofrinho-em-familia-chave-local"
criar_banco()

def inteiro_positivo(valor, permitir_zero=False):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None
    if numero < 0 or (not permitir_zero and numero == 0):
        return None
    return numero

def obter_crianca(conexao, crianca_id):
    crianca = conexao.execute("SELECT * FROM criancas WHERE id = ?", (crianca_id,)).fetchone()
    if not crianca:
        abort(404)
    return crianca

@app.route("/")
def index():
    with conectar() as conexao:
        criancas = conexao.execute("SELECT * FROM criancas ORDER BY nome").fetchall()
    return render_template("index.html", criancas=criancas)

@app.route("/responsavel")
def responsavel():
    with conectar() as conexao:
        criancas = conexao.execute("""
            SELECT c.*, m.nome AS meta_nome, m.valor_objetivo,
                   CASE WHEN m.valor_objetivo > 0 THEN MIN(100, ROUND(c.saldo * 100.0 / m.valor_objetivo, 1)) ELSE 0 END AS progresso
            FROM criancas c LEFT JOIN metas m ON m.crianca_id = c.id
            ORDER BY c.nome
        """).fetchall()
        tarefas = conexao.execute("""
            SELECT t.*, c.nome AS crianca_nome FROM tarefas t
            JOIN criancas c ON c.id = t.crianca_id
            ORDER BY CASE t.status WHEN 'AGUARDANDO_APROVACAO' THEN 0 WHEN 'PENDENTE' THEN 1 ELSE 2 END, t.id DESC
        """).fetchall()
    return render_template("responsavel.html", criancas=criancas, tarefas=tarefas)

@app.post("/criancas")
def cadastrar_crianca():
    nome = request.form.get("nome", "").strip()
    idade = inteiro_positivo(request.form.get("idade"), permitir_zero=True)
    saldo = inteiro_positivo(request.form.get("saldo", 0), permitir_zero=True)
    if not nome or idade is None or saldo is None:
        flash("Preencha nome, idade e saldo com valores válidos.", "erro")
        return redirect(url_for("responsavel"))
    with conectar() as conexao:
        conexao.execute("INSERT INTO criancas (nome, idade, saldo) VALUES (?, ?, ?)", (nome, idade, saldo))
    flash("Criança cadastrada com sucesso!", "sucesso")
    return redirect(url_for("responsavel"))

@app.post("/tarefas")
def cadastrar_tarefa():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    recompensa = inteiro_positivo(request.form.get("recompensa"), permitir_zero=True)
    crianca_id = inteiro_positivo(request.form.get("crianca_id"))
    if not titulo or recompensa is None or crianca_id is None:
        flash("Informe título, recompensa não negativa e criança responsável.", "erro")
        return redirect(url_for("responsavel"))
    with conectar() as conexao:
        if not conexao.execute("SELECT 1 FROM criancas WHERE id = ?", (crianca_id,)).fetchone():
            flash("Criança não encontrada.", "erro")
            return redirect(url_for("responsavel"))
        conexao.execute("INSERT INTO tarefas (titulo, descricao, recompensa, crianca_id) VALUES (?, ?, ?, ?)",
                        (titulo, descricao, recompensa, crianca_id))
    flash("Tarefa criada!", "sucesso")
    return redirect(url_for("responsavel"))

@app.post("/tarefas/<int:tarefa_id>/realizar")
def realizar_tarefa(tarefa_id):
    with conectar() as conexao:
        cursor = conexao.execute("UPDATE tarefas SET status = 'AGUARDANDO_APROVACAO' WHERE id = ? AND status = 'PENDENTE'", (tarefa_id,))
        tarefa = conexao.execute("SELECT crianca_id FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        if not tarefa: abort(404)
        if cursor.rowcount == 0:
            flash("Esta tarefa não está pendente.", "erro")
        else:
            flash("Tarefa enviada para aprovação!", "sucesso")
    return redirect(url_for("painel_crianca", crianca_id=tarefa["crianca_id"]))

@app.post("/tarefas/<int:tarefa_id>/aprovar")
def aprovar_tarefa(tarefa_id):
    conexao = conectar()
    try:
        conexao.execute("BEGIN IMMEDIATE")
        tarefa = conexao.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        if not tarefa: abort(404)
        if tarefa["status"] != "AGUARDANDO_APROVACAO":
            conexao.rollback()
            flash("Somente tarefas aguardando aprovação podem ser aprovadas.", "erro")
            return redirect(url_for("responsavel"))
        if conexao.execute("SELECT 1 FROM recompensas WHERE tarefa_id = ?", (tarefa_id,)).fetchone():
            conexao.rollback()
            flash("Esta tarefa já gerou uma recompensa.", "erro")
            return redirect(url_for("responsavel"))
        conexao.execute("INSERT INTO recompensas (descricao, valor, crianca_id, tarefa_id) VALUES (?, ?, ?, ?)",
                        (f"Recompensa pela tarefa: {tarefa['titulo']}", tarefa["recompensa"], tarefa["crianca_id"], tarefa_id))
        conexao.execute("UPDATE criancas SET saldo = saldo + ? WHERE id = ?", (tarefa["recompensa"], tarefa["crianca_id"]))
        conexao.execute("UPDATE tarefas SET status = 'CONCLUIDA' WHERE id = ?", (tarefa_id,))
        conexao.commit()
        flash("Tarefa aprovada e moedas adicionadas!", "sucesso")
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()
    return redirect(url_for("responsavel"))

@app.post("/metas")
def cadastrar_meta():
    nome = request.form.get("nome", "").strip()
    valor = inteiro_positivo(request.form.get("valor_objetivo"))
    crianca_id = inteiro_positivo(request.form.get("crianca_id"))
    if not nome or valor is None or crianca_id is None:
        flash("Informe uma meta e um valor maior que zero.", "erro")
        return redirect(url_for("responsavel"))
    with conectar() as conexao:
        if not conexao.execute("SELECT 1 FROM criancas WHERE id = ?", (crianca_id,)).fetchone():
            flash("Criança não encontrada.", "erro")
            return redirect(url_for("responsavel"))
        conexao.execute("""
            INSERT INTO metas (nome, valor_objetivo, crianca_id) VALUES (?, ?, ?)
            ON CONFLICT(crianca_id) DO UPDATE SET nome=excluded.nome, valor_objetivo=excluded.valor_objetivo
        """, (nome, valor, crianca_id))
    flash("Meta salva!", "sucesso")
    return redirect(url_for("responsavel"))

@app.route("/crianca/<int:crianca_id>")
def painel_crianca(crianca_id):
    with conectar() as conexao:
        crianca = obter_crianca(conexao, crianca_id)
        tarefas = conexao.execute("SELECT * FROM tarefas WHERE crianca_id = ? ORDER BY id DESC", (crianca_id,)).fetchall()
        meta = conexao.execute("SELECT * FROM metas WHERE crianca_id = ?", (crianca_id,)).fetchone()
        recompensas = conexao.execute("SELECT * FROM recompensas WHERE crianca_id = ? ORDER BY datetime(data) DESC, id DESC", (crianca_id,)).fetchall()
    progresso_real = (crianca["saldo"] / meta["valor_objetivo"] * 100) if meta else 0
    progresso_visual = min(100, progresso_real)
    return render_template("crianca.html", crianca=crianca, tarefas=tarefas, meta=meta,
                           recompensas=recompensas, progresso_real=progresso_real, progresso_visual=progresso_visual)

@app.route("/meta/<int:crianca_id>")
def pagina_meta(crianca_id):
    with conectar() as conexao:
        crianca = obter_crianca(conexao, crianca_id)
        meta = conexao.execute("SELECT * FROM metas WHERE crianca_id = ?", (crianca_id,)).fetchone()
    progresso_real = (crianca["saldo"] / meta["valor_objetivo"] * 100) if meta else 0
    return render_template("meta.html", crianca=crianca, meta=meta, progresso_real=progresso_real,
                           progresso_visual=min(100, progresso_real))

@app.errorhandler(404)
def nao_encontrado(_):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
