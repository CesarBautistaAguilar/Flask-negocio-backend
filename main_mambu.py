from concurrent.futures import process
from email import message
from unittest import result
from flask import Flask, Response, request, abort
from example import response_simulation, response_desmbolso
from request_config import create_simulation, create_client, create_account, aproved_loan, disbursement_loan, payment_loan
import requests
import json
import os

app = Flask(__name__)

url_base = os.environ.get('URL')
key = os.environ.get('KEY')

headers = {
    'Accept': 'application/json',
    'authorization': f'Bearer {key}',
    'content-type': 'application/json'
}

#Retorna un hola mundo en json
@app.route('/')
def hola_mundo():
    name  =  {
        "message": "New World",
        "status": "OK"
    } 
    return name

#Oferta
@app.route('/simulacion', methods=['GET'])
def go():
    params = dict(request.args)
    payload = create_simulation(params['monto'], params['plazo'], params['dia'])
    r = requests.post(f'{url_base}/loans:previewSchedule', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/loans:previewSchedule status {r.status_code}')
    result = Response(json.dumps(r.json(),default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

#Onboarding
@app.route('/onboarding', methods=['POST'])
def onboarding():
    params = dict(request.json)
    print(f'request {params}')
    """
    #Creation to client
    payload = create_client(params["nombre"], params["a_p"], params["a_m"], params["telefono"], params["correo"], params["rfc"], params["curp"],params["banco"], params["clabe"], params["segundo_nombre"])
    r = requests.post(f'{url_base}/clients', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/clients status {r.status_code}')
    if(r.status_code != 200):
        result =  Response(json.dumps({"message":"Error al crear el cliente"},default=str),mimetype="application/json", status=500)
        result.headers['Access-Control-Allow-Origin'] = '*'
        return result
    encodedKey_client = r.json()["encodedKey"]
    print(f'/encodedKey_client {encodedKey_client}')
    #Creation to loan account
    encodedKey_client = "8a44cf147e209e58017e20f052b90635"
    ##Producto v6.6
    encodedKey_loan = "8a44c0de7eaefe4f017eb6cb8f18609d"
    payload = create_account(encodedKey_client,encodedKey_loan,params["monto"], params["plazo"],  params["dia"], params["interes"])
    r = requests.post(f'{url_base}/loans', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/loans status {r.status_code}')
    if(r.status_code != 201):
        result =  Response(json.dumps({"message":"Error al crear el prestamo"},default=str),mimetype="application/json", status=500)
        result.headers['Access-Control-Allow-Origin'] = '*'
        return result
    id_account = r.json()["id"]
    print(f'id del prestamo: {id_account}')
    #Get schema of payments
    r = requests.get(f'{url_base}/loans/{id_account}/schedule', headers=headers )
    print(f'/loans/{id_account}/schedule status {r.status_code}')
    schema_loan = json.loads(r.text)
    schema_loan["id"] = id_account
    #Aproved loan
    payload = aproved_loan()
    r = requests.post(f'{url_base}/loans/{id_account}:changeState', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/loans/{id_account}:changeState status {r.status_code}')
    #Response flow
    result =  Response(json.dumps(schema_loan,default=str),mimetype="application/json")
    """
    result =  Response(json.dumps(response_simulation,default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

@app.route('/onboarding_v2', methods=['GET'])
def onboarding_v2():
    params = dict(request.args)
    #Creation to client
    payload = create_client(params["nombre"], params["a_p"], params["a_m"], params["telefono"], params["correo"], params["rfc"], params["curp"],params["banco"], params["clabe"], params["segundo_nombre"])
    r = requests.post(f'{url_base}/clients', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/clients status {r.status_code}')
    if(r.status_code != 201):
        result =  Response(json.dumps({"message":"Error al crear el cliente"},default=str),mimetype="application/json", status=500)
        result.headers['Access-Control-Allow-Origin'] = '*'
        return result
    encodedKey_client = r.json()["encodedKey"]
    print(f'/encodedKey_client {encodedKey_client}')
    #Creation to loan account
    ##Producto v6.6
    encodedKey_loan = "8a44c0de7eaefe4f017eb6cb8f18609d"
    payload = create_account(encodedKey_client,encodedKey_loan,params["monto"], params["plazo"],  params["dia"], params["interes"])
    r = requests.post(f'{url_base}/loans', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/loans status {r.status_code}')
    if(r.status_code != 201):
        result =  Response(json.dumps({"message":"Error al crear el prestamo"},default=str),mimetype="application/json", status=500)
        result.headers['Access-Control-Allow-Origin'] = '*'
        return result
    id_account = r.json()["id"]
    print(f'id del prestamo: {id_account}')
    #Get schema of payments
    r = requests.get(f'{url_base}/loans/{id_account}/schedule', headers=headers )
    print(f'/loans/{id_account}/schedule status {r.status_code}')
    schema_loan = json.loads(r.text)
    schema_loan["id"] = id_account
    #Response flow
    result =  Response(json.dumps(schema_loan,default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

@app.route('/desembolso', methods=['GET'])
def desembolso():
    params = dict(request.args)
    id_account = params["id"]
    #Aproved loan
    payload = aproved_loan()
    r = requests.post(f'{url_base}/loans/{id_account}:changeState', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/loans/{id_account}:changeState status {r.status_code}')
    #Desembolsar prestamo
    payload = disbursement_loan()
    r = requests.post(f'{url_base}/loans/{id_account}/disbursement-transactions', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/loans/{id_account}/disbursement-transactions status {r.status_code}')
    result =  Response(json.dumps(r.json(),default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

@app.route('/pagos', methods=['GET'])
def pagos():
    params = dict(request.args)
    id_account = params["id"]
    amount = params["monto"]
    #Aproved loan
    payload = payment_loan(amount)
    r = requests.post(f'{url_base}/loans/{id_account}/repayment-transactions', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/loans/{id_account}/repayment-transactions status {r.status_code}')
    result =  Response(json.dumps(r.json(),default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

#Abortar una peticion
@app.route('/abort')
def abortar():
    abort(401)