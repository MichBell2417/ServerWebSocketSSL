import csv
from datetime import datetime
def messaggio(richiesta,utentiOnline):
    try:
        nome = richiesta[0]
        messaggio = richiesta[1]
        return True
    except IndexError:
        return False

def accesso(richiesta):
    verifica = False
    nome = richiesta[1]
    psw = richiesta[2]
    with open('log.csv', mode='r', newline='', encoding='utf-8') as file:
        lettore = csv.reader(file, delimiter=',')
        for riga in lettore:
            print(riga)
            if riga[0]==nome and riga[1]==psw :
                #print("coretto")
                verifica = True
                break
    return verifica

def deleteByWebSocket(users, websocket):
    for user in users:
        if user.getWebsocket() == websocket:
            users.remove(user)
            print(user.getNome() + " si è disconnesso")
    return users

async def sendOnlineUsers(utenti):
    message="U|"
    for i in range(len(utenti)):
        if not i==0:
            message+="|"+utenti[i].getNome()
        else:
            message+=utenti[i].getNome()
    await sendBroadcast(utenti, message)

async def sendBroadcast(utenti, message):
    for client in utenti:
        await client.getWebsocket().send(message)

async def sendTo(user, message):
    await user.send(message)