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

## Acessar pelo celular (mesma rede Wi-Fi)

Ao iniciar, o terminal mostra dois endereços:

```
Neste computador: http://127.0.0.1:5001
Na rede local:    http://10.131.130.223:5001
```

No celular ou em outro dispositivo conectado ao **mesmo Wi-Fi**, abra o endereço de **rede local**.

> No macOS a porta 5000 costuma estar ocupada pelo AirPlay Receiver. Por isso o app detecta automaticamente a próxima porta livre (geralmente **5001**). Use sempre a porta que aparecer no terminal.
>
> Para escolher a porta manualmente: `PORT=8080 python app.py` (macOS/Linux) ou `set PORT=8080 && python app.py` (Windows).

Se ainda não abrir:
- Libere o Python no firewall do computador (macOS: Ajustes do sistema > Rede > Firewall).
- Verifique se o roteador não está com "isolamento de clientes" (AP isolation) ativado.
- Confirme que os dois dispositivos estão realmente na mesma rede (não em dados móveis ou rede de visitantes).

## Fluxo de demonstração
1. Entre na Área do responsável e cadastre uma criança.
2. Cadastre uma meta e uma tarefa.
3. Abra o painel da criança e marque a tarefa como realizada.
4. Volte ao responsável e aprove a tarefa.
5. Confira saldo, progresso e histórico.

As moedas são exclusivamente educativas e não representam dinheiro real.
