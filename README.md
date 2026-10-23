# Cofrinho em Família

Aplicação web educativa em Flask + SQLite para cadastrar crianças, tarefas, recompensas virtuais e metas de economia.

## Executar

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Depois:
```bash
pip install -r requirements.txt
python criar_banco.py
python app.py
```

Acesse `http://127.0.0.1:5000`.

## Fluxo de demonstração
1. Entre na Área do responsável e cadastre uma criança.
2. Cadastre uma meta e uma tarefa.
3. Abra o painel da criança e marque a tarefa como realizada.
4. Volte ao responsável e aprove a tarefa.
5. Confira saldo, progresso e histórico.

As moedas são exclusivamente educativas e não representam dinheiro real.
