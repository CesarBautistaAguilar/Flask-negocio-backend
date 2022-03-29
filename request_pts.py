import random
from datetime import datetime

urls_base = 'https://m775p.sandbox.mambu.com/api'

headerss = {
    'Accept': 'application/vnd.mambu.v2+json',
    'authorization': 'Basic Q0JhdXRpc3RhOmg9OXZRUFhNQkE=',
    'content-type': 'application/json'
}

def creation_time():
    fecha = str(datetime.today()).split(' ')
    fecha_salida = f'{fecha[0]}T{fecha[1][0:8]}:00-06:00'
    return fecha_salida

def generate_id():
    result = ''
    for i in range(15):
        result += str(random.randint(0, 9))
    return result

def generate_numers():
    result = ''
    for i in range(4):
        result += str(random.randint(0, 9))
    return int(result)

def create_simulation_pts(monto, plazo, dia):
    ofert_body = {
        "headerRQ": {
            "msgId": "02b25c5e-7c5f-4c27-96f0-f2790c028aab",
            "timestamp": creation_time()
        },
        "securityRQ": {
            "profile": "",
            "hostId": "",
            "userId": "",
            "channelId": "BACKOFFICE"
        },
        "messageRQ": {
            "loanAmount": int(monto),
            "productTypeKey": "8a44d30d7efd20c8017efd22a4eb0003",
            "scheduleSettings": {
                "repaymentInstallments": int(plazo),
                "fixedDaysOfMonth": [
                    int(dia)
                ]
            }
        }
    }
    return ofert_body

def create_client_pts(nombre, a_p, a_m, telefono, correo, rfc, curp,banco, clabe, idcliente ,segundo_nombre=""):
    client_body = {
    "headerRQ": {
        "msgId": "eecb8402-9111-499c-8396-e9efef573bc0",
        "timestamp": creation_time()
    },
    "securityRQ": {
        "channelId": "BACKOFFICE",
        "profile": "",
        "hostId": "",
        "userId": ""
    },
    "messageRQ": {
            "id":  idcliente,
            "firstName": nombre,
            "middleName": segundo_nombre,
            "lastName": a_p,
            "mobilePhone": telefono,
            "emailAddress": correo,
            "assignedBranchKey": "8a44b1847f4efa4a017f4fc87a6d02f3",
            "preferredLanguage": "SPANISH",
            "idDocuments": [
                {
                    "documentType": "RFC",
                    "documentId": rfc
                },
                {
                    "documentType": "CURP",
                    "documentId": curp
                }
            ],
            "_Datos_Personales_Adicional_Clie": {
                "Apellido_Materno": a_m
            },
            "_Información_Bancaria_Clientes": {
                "Tipo_Cuenta": "test",
                "Banco": banco,
                "Tipo_Operacion": "depositos",
                "Clabe": clabe
            }
        }
    }
    return client_body

def create_account_pts(encodedKey_client,encodedKey_loan,monto, plazo, dia, interes, desembolso, pago):
    if(not desembolso):
        desembolso = creation_time()
    print(desembolso)
    account_body = {
        "headerRQ": {
            "msgId": "02b25c5e-7c5f-4c27-96f0-f2790c028aab",
            "timestamp": creation_time()
        },
        "securityRQ": {
            "profile": "",
            "hostId": "",
            "userId": "",
            "channelId": "BACKOFFICE"
        },
        "messageRQ": {
            "accountHolderKey": encodedKey_client,
            "accountHolderType": "CLIENT",
            "loanAmount": monto,
            "productTypeKey": encodedKey_loan,
            "disbursementDetails": {
                "firstRepaymentDate": pago,
                "expectedDisbursementDate": desembolso
            },
            "scheduleSettings": {
                "gracePeriod": 0,
                "repaymentInstallments": plazo,
                "fixedDaysOfMonth": [
                    dia
                ]
            },
            "interestSettings": {
                "interestRate": interes
            }
        }
    }
    if(not pago):
        del account_body["messageRQ"]["disbursementDetails"]["firstRepaymentDate"]
    print(account_body)
    return account_body

def aproved_account_pts(numer_clabe,fecha):
    aproved_body = {
        "headerRQ": {
            "timestamp": creation_time(),
            "msgId": "4b68b519-9086-44e5-ba57-7f086e7d22bd"
        },
        "messageRQ": {
            "disbursementDetails": {
                "expectedDisbursementDate": fecha,
                "targetDepositAccountKey": numer_clabe,
                "paymentMethod": "40"
            },
            "securityRQ": {
                "profile": "",
                "hostId": "",
                "userId": "",
                "channelId": "BACKOFFICE"
            }
        }
    }
    return aproved_body

def disbur_account_pts():
    disbur_body = {
        "transactionDetails": {
            "transactionChannelId": "stp"
        }
    }
    return disbur_body

def clabe_return_pts(client_id):
    body = {
        "headerRQ": {
            "timestamp": creation_time(),
            "msgId": "d4f555b4-2ffa-4a8a-851a-181e58742bdf",
            "msgIdOrg": ""
        },
        "messageRQ": {
            "bPExternalId": client_id
        },
        "securityRQ": {
            "profile": "",
            "hostId": "",
            "userId": "",
            "channelId": "BACKOFFICE"
        }
    }
    return body

def payment_loan_pts(amount):
    payment_body = {
        "amount": int(amount),
        "transactionDetails": {
            "transactionChannelId": "pagoStp"
        }
    }
    return payment_body

def disbur_account_stp_pts(idCliente,idCuenta, monto):
    disbur_body = {
        "headerRQ": {
            "timestamp": creation_time(),
            "msgId": "cb67a83a-d810-436a-9f54-3e8ff50c693a",
        },
        "securityRQ": {
            "channelId": "STP_OUT",
            "profile": "",
            "hostId": "",
            "userId": ""
        },
        "messageRQ": {
            "digitalService": "TRANSF_LOCAL_EXTERNAL_STP",
            "general": {
            "transactionDetails": "Transferencia interna",
            "transactionId": idCuenta,
            "transactionDescription": "",
            "chargesType": "",
            "transactionAmount": int(monto),
            "channelReference": ""
            },
            "orderer": {
            "additionals": {}
            },
            "beneficiaries": [
            {
                "beneficiaryType": "",
                "beneficiaryId": "",
                "bankId": "0001",
                "account": {
                "legacyId": {
                    "branchId": "",
                    "accountType": "",
                    "accountNumber": "",
                    "tokenizedAccount": ""
                },
                "othersId": {
                    "identificationType": "BPEXTERNALID",
                    "identificationId": idCliente,
                    "tokenizedAccount": ""
                }
                },
                "transactionReference": "transferencia a terceros",
                "beneficiaryCustomerName": "",
                "beneficiaryCustomerPhone": "",
                "beneficiaryCustomerAddress": "",
                "beneficiaryCustomerCity": "",
                "additionals": {
                "loanReqId": idCuenta
                }
            }
            ]
        }
    }
    return disbur_body

def state_change(id):
    body = {
        "id": id,
        "empresa": "MP_FINANCIERA",
        "folioOrigen": "",
        "estado": "SENT",
        "causaDevolucion": "",
        "tsLiquidacion": "1634919027297"
    }
    return body

def search_loans(idclient):
    body = {
        "sortingCriteria": {
            "field": "encodedKey",
            "order": "ASC"
        },
        "filterCriteria": [
            {
                "field": "accountHolderKey",
                "value": idclient,
                "operator": "EQUALS"
            }
        ]
    }
    return body

def create_pago_pts(clientFullName, monto, fechaoperacion, clientCLABE, referencianumerica):
    ofert_body ={
        "abono": {
            "id": generate_numers(),
            "fechaOperacion": int(fechaoperacion),
            "institucionOrdenante": 846,
            "institucionBeneficiaria": 90646,
            "claveRastreo": str(generate_numers()),
            "monto": float(monto),
            "nombreBeneficiario": clientFullName,
            "tipoCuentaBeneficiario": 40,
            "cuentaBeneficiario": clientCLABE,
            "rfcCurpBeneficiario": "ND",
            "conceptoPago": str(referencianumerica), 
            "referenciaNumerica": 1234568,
            "empresa": "MP_FINANCIERA",
            "tsLiquidacion": "1634919027297"
        }
    }
    return ofert_body