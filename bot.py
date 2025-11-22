import asyncio
import json
from telethon import TelegramClient

STATE_FILE = "state.json"

ALVO_PADRAO = "sylweir"

CONTAS = [
    {
        "session": "peter",
        "api_id": 32762064,
        "api_hash": "802a1c71d828f65ea81a246c05771b83",
        "grupo": -1002982380151,
        "modo": "responder_outro_usuario",
        "usuario_alvo_especial": "occisdamon"
    },
    {
        "session": "phineas",
        "api_id": 32889491,
        "api_hash": "bd8abe48d3593f6220d59928681d31ac",
        "grupo": -1002279117860,
        "modo": "responder_padrao"
    },
    {
        "session": "pedro",
        "api_id": 30792499,
        "api_hash": "4083fcd8d49ba5d2fd873762a6b9c548",
        "grupo": -1002982380151,
        "modo": "responder_padrao"
    },
    {
        "session": "haru",
        "api_id": 30345897,
        "api_hash": "6ccd6c9574a7f124a0a20d190b8a75f5",
        "grupo": -1002641311067,
        "modo": "responder_padrao"
    },
    {
        "session": "jamie",
        "api_id": 38610464,
        "api_hash": "b7036497622dfb57321cb5d5b00fd6c0",
        "grupo": -4781471846,
        "modo": "responder_padrao"
    },
    {
        "session": "mae",
        "api_id": 30621745,
        "api_hash": "bc82d88b03b06029727f201f75e0e3b9",
        "grupo": -1002279117860,
        "modo": "responder_padrao"
    },
    {
        "session": "lele",
        "api_id": 39581386,
        "api_hash": "7bec41daa5c32268a2a2db77fc7ce1e8",
        "grupo": -1002279117860,
        "modo": "responder_padrao"
    },
    {
        "session": "rafa",
        "api_id": 36957655,
        "api_hash": "b11851f8da479758164bb273bcff675b",
        "grupo": -1002279117860,
        "modo": "responder_padrao"
    }
]

SLEEP_INTERVAL = 10800

def carregar_estado():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def salvar_estado(estado):
    with open(STATE_FILE, "w") as f:
        json.dump(estado, f)

async def rodar_conta(info, estado):
    session = info["session"]
    client = TelegramClient(session, info["api_id"], info["api_hash"])
    await client.start()

    while True:
        try:
            msgs = await client.get_messages(info["grupo"], limit=50)
            alvo = info.get("usuario_alvo_especial", ALVO_PADRAO)

            msg_alvo = next((m for m in msgs if m.sender and m.sender.username == alvo), None)

            if msg_alvo:
                ultimo_id = estado.get(session)
                if ultimo_id != msg_alvo.id:
                    await client.send_message(info["grupo"], "/cenoura", reply_to=msg_alvo.id)
                    estado[session] = msg_alvo.id
                    salvar_estado(estado)
        except Exception:
            pass

        await asyncio.sleep(SLEEP_INTERVAL)

async def main():
    estado = carregar_estado()
    tarefas = [asyncio.create_task(rodar_conta(c, estado)) for c in CONTAS]
    await asyncio.gather(*tarefas)

if __name__ == "__main__":
    asyncio.run(main())
