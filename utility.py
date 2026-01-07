import csv
import User
import info
#indica gli utenti online
onlineUser=[]

commandList=[
    "CloseDoor",
    "OpenDoor",
    "StatusDoor",
    "ChronDoor",
    "InterruptAlarm"
]

def messaggio(message):
    """Funzione che verifica la struttura del messaggio
    
    :param message: il messaggio
    :return: se il messaggio è corretto o no
    """
    #se si presenta un errore di indice e quindi non esiste un campo
    #il messaggi è sbagliato
    try:
        name=message[1]
        user=userFromNome(name)
        if(user!=None):
            #verifico che il codice di sicurezza sia giusto
            secureC=message[2]
            user.checkAffidability(secureC)
            command=message[3]
            existingCommand=False
            #verifico che il comando inviato sia esistente
            for comm in commandList:
                if command==comm:
                    existingCommand=True
                    break
            if existingCommand==False:
                return False
            return True
        else:
            print("non logged")
            return False
    except IndexError:
        return False

def changeToMqttMessage(message):
    admin=False
    match message[1]:
        case info.NICKNAME_ADMIN:
            admin=True
    psw=info.PIN_GUEST
    if(admin):
        psw=info.PIN_ADMIN
    return str(psw)+"|"+message[3]+"|"

def accesso(nome,psw,websocket):
    """verifica che i dati inseriti siano corretti e esegue il salvataggio tra quelli online

    :param nome: il nome dell'utente interessato 
    :param psw: la password dell'utente 
    :param websocket: il websocket che ha inserito i dati precedenti
    :return: se l'utente è stato aggiuinto o no
    """
    verifica = False
    with open('users.csv', mode='r', newline='', encoding='utf-8') as file:
        lettore = csv.reader(file, delimiter=',')
        for riga in lettore:
            if riga[0]==nome and riga[1]==psw:
                verifica = True
                onlineUser.append(User.User(nome,websocket))
                break
    return verifica

def userFromNome(nome):
    """Questa funzione ritorna l'utente con lo stesso nome.

    :param nome: il nome dell'utente interessato
    :return: l'oggetto User interessato dalla ricerca o None se inesistente
    """
    for user in onlineUser:
        if nome==user.nome:
            return user
        else:
            return None

def userFromWebsocket(websocket):
    """Questa funzione ritorna l'utente con lo stesso websocket.

    :param websocket: il websocket dell'utente interessato
    :return: l'oggetto User interessato dalla ricerca o None se inesistente
    """
    for user in onlineUser:
        if websocket==user.websocket:
            return user
    return None

def removeOnlineUser(websocket):
    global onlineUser
    try:
        onlineUser=onlineUser.remove(userFromWebsocket(websocket))
        if(onlineUser==None):
            onlineUser=[]
    except ValueError:
        return

async def sendTo(user, message):
    await user.send(message)
