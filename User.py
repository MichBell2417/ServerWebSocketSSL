import random
class User:
    def __init__(self, nome, websocket):
        self.nome=nome
        self.websocket=websocket
        self.secureC=random.randint(1000,9999) #prendiamo valori di 5 cifre

    def checkAffidability(self, code):
        if(self.secureC==code):
            return True
        else:
            return False