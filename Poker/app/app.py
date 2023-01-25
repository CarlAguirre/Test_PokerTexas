from flask import Flask, jsonify, request
from flask_expects_json import expects_json
import json

app= Flask(__name__)



schema_Hands = {"type": "object", "properties": {"hand1": {"type": "string","minLength": 14, "maxLength": 15}, "hand2": {"type": "string","minLength": 14,"maxLength": 15}},
                    "required": ["hand1", "hand2"]}

@app.route("/poker/validation", methods=['GET'])
def test():
    json = {}
    json["message"] = "Server running poker/validation ...!!!!"
    return jsonify(json)

@app.route("/poker/validation", methods=['POST'])
@expects_json(schema_Hands)

def manos():
    manos_New={
    "hand1": request.json['hand1'],
    "hand2": request.json['hand2']
    }

    manosSeparadas=CardValue(manos_New)
    tipoMano= typeHand(manosSeparadas[0], manosSeparadas[1], manosSeparadas[2],manosSeparadas[3])

    if tipoMano[0] == "HighCard":
        res=HighCard(manosSeparadas[0], manosSeparadas[2], tipoMano[1])
    
    if tipoMano[0] == "Flush":
        res=Flush(manosSeparadas[0], manosSeparadas[1], manosSeparadas[2],manosSeparadas[3])

    if tipoMano[0] == "FourOfAKind":
        res=FourOfAKind(manosSeparadas[0], manosSeparadas[1], manosSeparadas[2],manosSeparadas[3])
    
    if tipoMano[0] == "TwoPair":
        res=TwoPair(manosSeparadas[0], manosSeparadas[1], manosSeparadas[2],manosSeparadas[3])
    
    if tipoMano[0] == "OnePair":
        res=OnePair(manosSeparadas[0], manosSeparadas[2], tipoMano[1])
    

    return jsonify({"winnerHand": res[0],"winnerHandType":res[1], "compositionWinnerHand":res[2]})


# Obtener  listas  de las manos divididas
def CardValue(manos_New):
    
    # iniciando listas de la amano 1
    mano1Numbers= []
    mano1Palos=[]

    # iniciando listas de la amano 2
    mano2Numbers= []
    mano2Palos=[]
    
    a= manos_New['hand1']
    b= manos_New['hand2']
    
    mano1=a.split(" ")
    for carta in mano1:
        mano1Numbers.append(carta[0])
        mano1Palos.append(carta[1])
    
    mano2=b.split(" ")
    for carta in mano2:
        mano2Numbers.append(carta[0])
        mano2Palos.append(carta[1])
    
    print (mano1Numbers, mano1Palos)
    print (mano2Numbers, mano2Palos)
    
    return mano1Numbers, mano1Palos, mano2Numbers, mano2Palos


# Identifificar el tipo de mano
def typeHand(mano1Numbers, mano1Palos, mano2Numbers, mano2Palos):
    tipoMano = ""
    nMayor=""

    #identificando la carta mas alta
    if 'A'in mano1Numbers or 'A'in mano2Numbers:
        nMayor='A'
    else:
        for n in mano1Numbers:
            for j in mano2Numbers:
                if nMayor<j:
                    nMayor=j
            if nMayor<n:
                nMayor=n
    if nMayor == 'A':
        nMayor='As'
    if nMayor == 'J':
        nMayor='Jack'
    if nMayor == 'Q':
        nMayor='Queen'
    if nMayor == 'K':
        nMayor='King'
    #----------Mano Color-----------
    if len(set(mano1Palos))==1 or len(set(mano2Palos))==1:
        tipoMano ="Flush"
    
    #----------Mano Pares-----------
    if tipoMano != "Flush":
        setMano1=set()
        dup= [x for x in mano1Numbers if x in setMano1 or (setMano1.add(x) or False)]
        setMano2=set()
        dup2= [x for x in mano2Numbers if x in setMano2 or (setMano2.add(x) or False)]
    
        if len(dup)==3 or len(dup2)==3:
            tipoMano ="FourOfAKind"
        elif len(dup)==2 or len(dup2):
            tipoMano ="TwoPair"
        elif len(dup)==1 or len(dup2)==1:
            tipoMano ="OnePair"

    if tipoMano == "":
        tipoMano = "HighCard"

    return tipoMano, nMayor

# Validacion Carta alta
def HighCard(mano1Numbers, mano2Numbers, nmayor):
    
    mayorMano1 = CartaMayor(mano1Numbers)
    mayorMano2 = CartaMayor(mano2Numbers)
    
    if mayorMano1=='As':
        winnerHand='hand1'
        winnerHandType='HighCard'
        compositionWinnerHand =[mayorMano1]      
    elif mayorMano2=='As':
        winnerHand='hand2'
        winnerHandType='HighCard'
        compositionWinnerHand =[mayorMano2]
    elif mayorMano1 > mayorMano2:
        winnerHand='hand1'
        winnerHandType='HighCard'
        compositionWinnerHand =[mayorMano1]
    elif mayorMano1 < mayorMano2:
        winnerHand='hand2'
        winnerHandType='HighCard'
        compositionWinnerHand =[mayorMano2]
    return  winnerHand, winnerHandType, compositionWinnerHand
    
# Seleccion de la carta mas alta
def CartaMayor(numbers):
    nMayor=''
    if 'A'in numbers:
        nMayor='A'
    else:
        for n in numbers:
            if nMayor<n:
                nMayor=n

    if nMayor == 'A':
        nMayor='As'
    if nMayor == 'J':
        nMayor='Jack'
    if nMayor == 'Q':
        nMayor='Queen'
    if nMayor == 'K':
        nMayor='King'
    return nMayor


def Flush():
    pass

def FourOfAKind():
    pass


# Validacion 1 par
def OnePair(mano1Numbers, mano2Numbers, nmayor):
    
    setMano1=set()
    dup= [x for x in mano1Numbers if x in setMano1 or (setMano1.add(x) or False)]
    print("dup")
    print(dup)

    setMano2=set()
    dup2= [x for x in mano2Numbers if x in setMano2 or (setMano2.add(x) or False)]
    print("dup2")
    print(dup2)
    mayor1 = CartaMayor(dup)
    mayor2 = CartaMayor(dup2)
    
    if len(dup) == len(dup2):
        if mayor1=='As':
            winnerHand='hand1'
            winnerHandType='OnePair'
            compositionWinnerHand =[mayor1]      
        elif mayor2=='As':
            winnerHand='hand2'
            winnerHandType='OnePair'
            compositionWinnerHand =[mayor1]
        elif mayor1 > mayor2:
            winnerHand='hand1'
            winnerHandType='OnePair'
            compositionWinnerHand =[mayor1]
        elif mayor1 < mayor2:
            winnerHand='hand2'
            winnerHandType='OnePair'
            compositionWinnerHand =[mayor2]
    elif len(dup) > len(dup2):
        winnerHand='hand1'
        winnerHandType='OnePair'
        if dup[0] =='A':
            dup[0] ='As'
        if dup[0] == 'J':
            dup[0]='Jack'
        if dup[0] == 'Q':
            dup[0]='Queen'
        if dup[0] == 'K':
            dup[0]='King'
        compositionWinnerHand = dup

    elif len(dup) < len(dup2):
        winnerHand='hand2'
        winnerHandType='OnePair'
        if dup2[0] =='A':
            dup2[0] ='As'
        if dup2[0] == 'J':
            dup2[0]='Jack'
        if dup2[0] == 'Q':
            dup2[0]='Queen'
        if dup2[0] == 'K':
            dup2[0]='King'
        compositionWinnerHand = dup2

    print("winnerHand:", winnerHand, "winnerHandType:",winnerHandType, "compositionWinnerHand:",compositionWinnerHand)
    
    return  winnerHand, winnerHandType, compositionWinnerHand


# Validacion Dos Pares 
def TwoPair():

    pass





""" def compararManos(manos_New):
    bandera=1
    winnerHandType= ""
    resultado=[]
    manosSeparadas=CardValue(manos_New)

    print("---------------PASO 1-----------------")
    print(winnerHandType)
    print(manosSeparadas[0])
    print(manosSeparadas[2])
        
    Straight()
    if winnerHandType== "Straight":
        pass
    

    ThreeOfAKind()
    if winnerHandType== "ThreeOfAKind":
        pass

    TwoPair()
    if winnerHandType== "TwoPair":
        pass
    

    if bandera==1:
        resultado = OnePair(manosSeparadas[0], manosSeparadas[2])
        
            
        if resultado[1]== "OnePair":

            bandera=0       
            print (bandera)
            print("---------------RESPUESTA OnePair -----------------")
    
 
    if bandera==1:

        resultado = HighCard(manosSeparadas[0], manosSeparadas[2])
        print("---------------AQUIIIIIIIII -----------------")
        print (resultado[1])

        if resultado[1]=="HighCard":
                print("---------------RESPUESTA HighCard -----------------")

                print("winnerHand:", resultado[0], "winnerHandType:",resultado[1], "compositionWinnerHand:",resultado[2])
    
    return resultado """

if __name__ == '__main__':
    app.run (debug=True, port=9999)

