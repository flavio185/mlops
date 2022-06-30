# save this as app.py
from flask import Flask, jsonify, request
import joblib


app = Flask(__name__)

model = joblib.load(open('model.joblib','rb'))

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/classify", methods=['POST'])
def classify():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    print(data)
    renda = float(data['renda'])
    idade = int(data['idade'])
    etnia = int(data['etnia'])
    sexo = int(data['genero'])
    casapropria = int(data['casa_propria'])
    outrasrendas = int(data['outras_rendas'])
    estadocivil = int(data['estado_civil'])
    escolaridade = int(data['escolaridade'])

    
    dados_cliente = [etnia, 
               sexo, 
               casapropria,
               outrasrendas, 
               estadocivil, 
               escolaridade,
               renda,
               idade]

    # Make classification using model loaded from disk as per the data.
    prediction = model.predict([dados_cliente])

    # Take the first value of prediction
    output = prediction[0]
    return jsonify({"default" :str(output)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
