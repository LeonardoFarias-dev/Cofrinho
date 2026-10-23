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

Acesse `http://127.0.0.1:5001`.

## Acessar pelo celular (mesma rede Wi-Fi)

Ao iniciar, o terminal mostra os endereços:

```
Neste computador: http://SEU_IP
Na rede local:    http://SEU_IP_LOCAL:5001
```

No celular ou em outro dispositivo conectado ao mesmo Wi-Fi, abra o endereço da rede local.

Para escolher outra porta: `PORT=8080 python app.py` (macOS/Linux) ou `set PORT=8080 && python app.py` (Windows).

## Fluxo de demonstração
1. Entre na Área do responsável e cadastre uma criança.
2. Cadastre uma meta e uma tarefa.
3. Abra o painel da criança e marque a tarefa como realizada.
4. Volte ao responsável e aprove a tarefa.
5. Confira saldo, progresso e histórico.

As moedas são exclusivamente educativas e não representam dinheiro real.
