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
    
    
    return jsonify(CardValue(manos_New))


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
    
    """ miset= set(mano1Numbers)
    
    print (miset) """
    return mano1Numbers, mano1Palos, mano2Numbers, mano2Palos
    

# Validacion Carta alta
def HighCard(mano1Numbers, mano1Palos, mano2Numbers, mano2Palos):
    
    mayorMano1 = CartaMayor(mano1Numbers)
    mayorMano2 = CartaMayor(mano2Numbers)
    
    if mayorMano1 > mayorMano2:
        return jsonify({'winnerHand': {'hand1'}, 'winnerHandType':{'HighCard'},'compositionWinnerHand': {'mayorMano1'}})
    else:
        return jsonify({'winnerHand': {'hand2'}, 'winnerHandType':{'HighCard'},'compositionWinnerHand': {'mayorMano2'}})
    



def CartaMayor(numbers):
    nMayor=0
    for n in numbers:
        if nMayor<n:
            nMayor=n
    return nMayor


# Validacion 1 par
def OnePair():

    pass

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