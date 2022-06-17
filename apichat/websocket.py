#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-


import asyncio
import datetime
import random
import websockets
import banco
import json
import logging

async def show_time(websocket, path):

    banco.init()
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send(message)
        await asyncio.sleep(random.random() * 2 + 1)

        async for message in websocket:
            event = json.loads(message)
            if event["tipo"] == "consulta":
                
                resp = banco.consulta(event['usuario'], event['paciente'], event['tempo'])
                msg = {"tipo": "msgs", "data": []}
                for l in resp:
                    linha = {}

                    linha['texto'] = l[2]
                    linha['de'] = l[4]
                    linha['time'] = l[3].strftime("%Y-%m-%d %H:%M:%S")
                    linha['id'] = l[0]

                    msg["data"].append(linha)

                await websocket.send(json.dumps(msg)) 

            elif event["tipo"] == "nova_mensagem":
                
                resp = banco.nova_mensagem(event['usuario'], event['paciente'], event['de'], event['texto'])

            else:
                
                logging.error("unsupported event: %s", event)

async def main():
    async with websockets.serve(show_time, "localhost", 5010):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())