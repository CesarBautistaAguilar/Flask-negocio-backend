def create_client(nombre, a_p, a_m, telefono, correo, rfc, curp,banco, clabe, segundo_nombre=""):
    client_body = {
        "preferredLanguage": "SPANISH",
        "firstName": nombre,
        "middleName": segundo_nombre,
        "lastName": a_p,
        "mobilePhone": telefono,
        "emailAddress": correo,
        "assignedBranchKey": "8a44b1847f4efa4a017f4fc87a6d02f3",
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
    return client_body

def create_simulation(monto, plazo, dia):
    ofert_body = {
        "loanAmount": int(monto),
        "productTypeKey": "8a44b8407e8c54a0017e8c9013710227",
        "scheduleSettings": {
            "repaymentInstallments": int(plazo),
            "fixedDaysOfMonth": [
                int(dia)
            ]
        }
    }
    return ofert_body

def create_account(encodedKey_client,encodedKey_loan,monto, plazo, dia, interes):
    account_body = {
        "accountHolderKey": encodedKey_client,
        "accountHolderType": "CLIENT",
        "loanAmount": monto,
        "productTypeKey": encodedKey_loan,
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
    return account_body

def aproved_loan():
    aproved_body = {
        "action": "APPROVE",
        "notes": "aprobacion demo"
    }
    return aproved_body

def disbursement_loan():
    disbursement_body = {
        "transactionDetails": {
            "transactionChannelId": "cash"
        }
    }
    return disbursement_body

def payment_loan(amount):
    payment_body = {
        "amount": amount,
        "transactionDetails": {
            "transactionChannelId": "cash"
        }
    }
    return payment_body