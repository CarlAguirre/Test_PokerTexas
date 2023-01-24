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

    res=compararManos(manos_New)
#"winnerHand:", resultado[0], "winnerHandType:",resultado[1], "compositionWinnerHand:",resultado[2]
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
    

def compararManos(manos_New):
    bandera=1
    winnerHandType= ""
    resultado=[]
    manosSeparadas=CardValue(manos_New)

    print("---------------PASO 1-----------------")
    print(winnerHandType)
    print(manosSeparadas[0])
    print(manosSeparadas[2])
        
    """ Straight()
    if winnerHandType== "Straight":
        pass
    

    ThreeOfAKind()
    if winnerHandType== "ThreeOfAKind":
        pass

    TwoPair()
    if winnerHandType== "TwoPair":
        pass
    """

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
    
    return resultado






# Validacion Carta alta
def HighCard(mano1Numbers, mano2Numbers):
    
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
    print 
    nMayor=''
    if 'A'in numbers:
        nMayor='As'
    if 'J'in numbers:
        nMayor='Jack'
    if 'Q'in numbers:
        nMayor='Queen'
    if 'K'in numbers:
        nMayor='King'

    else:
        for n in numbers:
            if nMayor<n:
                nMayor=n
    return nMayor


# Validacion 1 par
def OnePair(mano1Numbers, mano2Numbers):
    
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
        compositionWinnerHand = dup

    elif len(dup) < len(dup2):
        winnerHand='hand2'
        winnerHandType='OnePair'
        compositionWinnerHand = dup2


    print("winnerHand:", winnerHand, "winnerHandType:",winnerHandType, "compositionWinnerHand:",compositionWinnerHand)
    
    return  winnerHand, winnerHandType, compositionWinnerHand






    winnerHand='hand2'
    winnerHandType='OnePair'
    compositionWinnerHand =[mayorMano2]


    return  winnerHand, winnerHandType, compositionWinnerHand
    

# Validacion Dos Pares 
def TwoPair():

    pass

# Validacion 3 Cartas del mismo valor
def ThreeOfAKind():

    pass

# Validacion Escalera
def Straight():

    pass



if __name__ == '__main__':
    app.run (debug=True, port=9999)