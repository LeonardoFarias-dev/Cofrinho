from database import conectar

SCHEMA = """
CREATE TABLE IF NOT EXISTS criancas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL CHECK (idade >= 0),
    saldo INTEGER NOT NULL DEFAULT 0 CHECK (saldo >= 0)
);
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    recompensa INTEGER NOT NULL DEFAULT 0 CHECK (recompensa >= 0),
    status TEXT NOT NULL DEFAULT 'PENDENTE'
        CHECK (status IN ('PENDENTE','AGUARDANDO_APROVACAO','CONCLUIDA')),
    crianca_id INTEGER NOT NULL,
    FOREIGN KEY (crianca_id) REFERENCES criancas(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS metas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor_objetivo INTEGER NOT NULL CHECK (valor_objetivo > 0),
    crianca_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (crianca_id) REFERENCES criancas(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS recompensas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    valor INTEGER NOT NULL CHECK (valor >= 0),
    data TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    crianca_id INTEGER NOT NULL,
    tarefa_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (crianca_id) REFERENCES criancas(id) ON DELETE CASCADE,
    FOREIGN KEY (tarefa_id) REFERENCES tarefas(id) ON DELETE CASCADE
);
"""

def criar_banco():
    with conectar() as conexao:
        conexao.executescript(SCHEMA)

if __name__ == "__main__":
    criar_banco()
    print("Banco cofrinho.db criado/atualizado com sucesso.")
