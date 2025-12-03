import utility
def testMessage():
    print(utility.onlineUser[0].nome)
    name=input("Name: ")
    secureC=input("secureC: ")
    command=input("Command: ")

    print(utility.messaggio(["M",name,secureC,command]))