from concurrent.futures import process
from email import message
from unittest import result
from flask import Flask, Response, request, abort
from request_pts import create_simulation_pts, create_client_pts, create_account_pts, aproved_account_pts,disbur_account_stp_pts ,state_change, payment_loan_pts,search_loans,create_pago_pts, headerss
import requests
import json
import os
from example import response_desmbolso, response_aprobacion

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
    payload = create_simulation_pts(params['monto'], params['plazo'], params['dia'])
    r = requests.post(f'{url_base}/mangosta/loans/0/preview-schedule', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/mangosta/loans/0/preview-schedule status {r.status_code}')
    print(f'/mangosta/loans/0/preview-schedule response {r.text}')
    if(r.status_code != 200):
        result =  Response(json.dumps({"message":"Error al crear el cliente"},default=str),mimetype="application/json", status=500)
        result.headers['Access-Control-Allow-Origin'] = '*'
        return result
    process = json.loads(r.text)
    schema_loan = process["messageRS"]["response"]
    result = Response(json.dumps(schema_loan,default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

#Onboarding
@app.route('/onboarding_v2', methods=['GET'])
def onboarding_v2():
    params = dict(request.args)
    message_error_pts = ''
    #Creation to client
    payload = create_client_pts(params["nombre"], params["a_p"], params["a_m"], params["telefono"], params["correo"], params["rfc"], params["curp"],params["banco"], params["clabe"], params["idcliente"],params["segundo_nombre"])
    print(str(payload))
    r = requests.post(f'{url_base}/mangosta/client/0/create', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/mangosta/client/0/create status {r.status_code}')
    print(f'/mangosta/client/0/create response {r.text}')
    if(r.status_code != 200):
        print("################### INTENTO CONSULTA ###################")
        message_error_pts = str(r.json()["statusRS"]["description"]).split(':')
        print(message_error_pts)
        print(message_error_pts[0])
        print("################### INTENTO CONSULTA ###################")
        if(message_error_pts[0] != 'El Cliente ya existe con el ID'):
            print("################### ENTRE A LA EXCEPCION ###################")
            result =  Response(json.dumps({"message":"Error al crear el cliente"},default=str),mimetype="application/json", status=500)
            result.headers['Access-Control-Allow-Origin'] = '*'
            return result
    loan_clabe = r.json()["messageRS"]["repaymentClabe"]
    encodedKey_client = r.json()["messageRS"]["response"]["encodedKey"]
    id_client = r.json()["messageRS"]["response"]["id"]
    print(f'/encodedKey cliente {encodedKey_client}')
    print(f'/cuenta clabe {loan_clabe}')
    print(f'/id del cliente {id_client}')
    #Creation to loan account
    #loan_clabe = "646180288000003996"
    #encodedKey_client="8a44b4727f9deba5017f9ec89f1b4719"
    #id_client="771473739096324"
    ##Producto v6.6
    encodedKey_loan = "8a44d30d7efd20c8017efd22a4eb0003"
    payload = create_account_pts(encodedKey_client,encodedKey_loan,params["monto"], params["plazo"],  params["dia"], params["interes"],  params["desembolso"], params["primer_pago"])
    print(payload)
    r = requests.post(f'{url_base}/mangosta/loans/0/create', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/mangosta/loans/0/create status {r.status_code}')
    print(f'/mangosta/loans/0/create response {r.text}')
    if(r.status_code != 201):
        result =  Response(json.dumps({"message":"Error al crear el prestamo"},default=str),mimetype="application/json", status=500)
        result.headers['Access-Control-Allow-Origin'] = '*'
        return result
    id_account = r.json()["messageRS"]["response"]["id"]
    referencia = r.json()["messageRS"]["reference"]
    loanAmount = r.json()["messageRS"]["response"]["loanAmount"]
    print(f'id del prestamo: {id_account}')
    #Get schema of payments
    r = requests.get(f'{url_base}/mangosta/loans/{id_account}/schedule', headers=headers,  verify=False)
    print(f'/mangosta/loans/{id_account}/schedule status {r.status_code}')
    schema_loan = json.loads(r.text)["messageRS"]["response"]
    schema_loan["id"] = id_account
    schema_loan["idClient"] = id_client
    schema_loan["referencia"] = referencia
    schema_loan["clabe"] = loan_clabe
    schema_loan["montoPrestamo"] = loanAmount
    #Response flow
    result =  Response(json.dumps(schema_loan,default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

#Aprobacion
@app.route('/aprobacion', methods=['GET'])
def aprobacion():
    params = dict(request.args)
    print(params)
    id_account = params["id_prestamo"]
    numer_clabe = params["clabe"]
    day_dis = params["fecha"]
    payload = aproved_account_pts(numer_clabe, day_dis)
    print(payload)
    r = requests.post(f'{url_base}/mangosta/loans/{id_account}/approve', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/mangosta/loans/{id_account}/approve status {r.status_code}')
    print(f'/mangosta/loans/{id_account}/approve response {r.text}')
    result =  Response(json.dumps(r.json()["messageRS"]["response"],default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

#Desembolso
@app.route('/desembolso', methods=['GET'])
def desembolso():
    params = dict(request.args)
    id_account = params["idcuenta"]
    amount = params["monto"]
    id_client = params["idcliente"]
    #Desembolsar prestamo
    payload = disbur_account_stp_pts(id_client,id_account, amount)
    print(payload)
    r = requests.post(f'{url_base}/mangosta/loans/0/disbursement', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/mangosta/loans/0/disbursement status {r.status_code}')
    print(f'mangosta/loans/0/disbursement response {r.text}')
    response_stp = r.json()
    id_change = r.json()["messageRS"]["response"][0]["confirmations"][1]["confirmationNumber"]
    print(f'valor de cambio {id_change}')
    #state_change
    payload = state_change(id_change)
    r = requests.post(f'{url_base}/mangosta/orderStp/0/changeStatus', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/mangosta/orderStp/0/changeStatus status {r.status_code}')
    print(f'mangosta/orderStp/0/changeStatus response {r.text}')
    result =  Response(json.dumps(response_stp,default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

#Usuario
@app.route('/usuario', methods=['GET'])
def usuario():
    params = dict(request.args)
    id_client = params["idcliente"]
    user = {}
    #Busca cliente por ID
    r = requests.get(f'https://m775p.sandbox.mambu.com/api/clients/{id_client}?detailsLevel=FULL', headers=headerss, verify=False )
    print(f'/clients/{id_client}?detailsLevel=FULL status {r.status_code}')
    print(f'/clients/{id_client}?detailsLevel=FULL response {r.text}')
    process = json.loads(r.text)
    encodedkey_client = process["encodedKey"]
    user["id"]=process["id"]
    user["firstName"]=process["firstName"]
    user["lastName"]=process["lastName"]
    user["emailAddress"]=process["emailAddress"]
    user["mobilePhone"]=process["mobilePhone"]
    user["clabe"]=process["_Información_Bancaria_Clientes"]["Clabe"]
    user["materno"]=process["_Datos_Personales_Adicional_Clie"]["Apellido_Materno"]
    #Obtiene todas las cuentas de prestamo asociadas al encodedkey del cliente
    print(f'encodedkey_client = {encodedkey_client}')
    payload = search_loans(encodedkey_client)
    r = requests.post(f'https://m775p.sandbox.mambu.com/api/loans:search?detailsLevel=BASIC', headers=headerss, verify=False, data=json.dumps(payload) )
    print(f'{encodedkey_client}/loans:search?detailsLevel=BASIC status {r.status_code}')
    loans=json.loads(r.text)
    search_due = loans
    index_due = 0
    for i in search_due:
        due_mount = due_loan(i["id"])
        search_due[index_due]["due_mount"] = due_mount
        index_due += 1
    response = {
        'user': user,
        'loans': search_due
    }
    result =  Response(json.dumps(response,default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

#Pagos
@app.route('/pagos-online', methods=['GET'])
def pagos():
    params = dict(request.args)
    payload = create_pago_pts(params["clientFullName"], params["monto"], params["fechaoperacion"], params["clientCLABE"], params["referencianumerica"])
    print(payload)
    r = requests.post(f'{url_base}/mangosta/loans/repayment/0/receive', headers=headers, verify=False, data=json.dumps(payload) )
    print(f'/mangosta/loans/repayment/0/receive {r.status_code}')
    print(f'/mangosta/loans/repayment/0/receive response {r.text}')
    result =  Response(json.dumps(r.json(),default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

#Saldos
@app.route('/saldos', methods=['GET'])
def saldos():
    params = dict(request.args)
    id_account = params["idprestamo"]
    #Busca cliente por ID
    r = requests.get(f'{url_base}/mangosta/loans/{id_account}/schedule', headers=headers,  verify=False)
    print(f'/mangosta/loans/{id_account}/schedule status {r.status_code}')
    print(f'/mangosta/loans/{id_account}/schedule response {r.text}')
    schema_loan = json.loads(r.text)["messageRS"]["response"]
    result =  Response(json.dumps(schema_loan,default=str),mimetype="application/json")
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result

#Abortar una peticion
@app.route('/abort')
def abortar():
    abort(401)

def due_loan(id_account):
    deuda = 0
    r = requests.get(f'https://m775p.sandbox.mambu.com/api/loans/{id_account}/schedule', headers=headerss, verify=False )
    schema_loan = dict(json.loads(r.text))
    for i in schema_loan["installments"]:
        if( i["state"] == 'LATE'):
            deuda += float(i["principal"]["amount"]["due"])
            deuda += float(i["interest"]["amount"]["due"])
            deuda += float(i["fee"]["amount"]["due"])
            deuda += float(i["penalty"]["amount"]["due"])
    print(f'{id_account} => {deuda}')
    return deuda