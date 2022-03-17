response_aprobacion = {
    "headerRS": {
        "msgId": "b58fce8b-6934-4f26-b1ab-1e4370c74efa",
        "msgIdOrg": "5e2b7bd0-aa78-4268-8fea-988a064cfc97",
        "timestamp": "2022-03-16T09:07:53-06:00"
    },
    "statusRS": {
        "code": 200,
        "description": "Aprobación Realizada"
    },
    "messageRS": {
        "response": {
            "encodedKey": "8a44ba937f91f75b017f93446d672369",
            "id": "1700000449",
            "accountHolderType": "CLIENT",
            "accountHolderKey": "8a44ba937f91f75b017f933f35362182",
            "creationDate": "2022-03-16T09:06:49-06:00",
            "approvedDate": "2022-03-16T09:07:53-06:00",
            "lastModifiedDate": "2022-03-16T09:07:52-06:00",
            "accountState": "APPROVED",
            "productTypeKey": "8a44d30d7efd20c8017efd22a4eb0003",
            "loanName": "MVP Credito simple v6.8",
            "loanAmount": 35000.0000000000,
            "paymentMethod": "HORIZONTAL",
            "assignedBranchKey": "8a44b1847f4efa4a017f4fc87a6d02f3",
            "accruedInterest": 0,
            "taxRate": 16.0000000000,
            "lastTaxRateReviewDate": "2022-03-16T09:06:50-06:00",
            "accruedPenalty": 0,
            "allowOffset": False,
            "arrearsTolerancePeriod": 5,
            "accountArrearsSettings": {
                "encodedKey": "8a44ba937f91f75b017f93446d67236c",
                "toleranceCalculationMethod": "ARREARS_TOLERANCE_PERIOD",
                "dateCalculationMethod": "LAST_LATE_REPAYMENT",
                "nonWorkingDaysMethod": "INCLUDED",
                "tolerancePeriod": 5
            },
            "latePaymentsRecalculationMethod": "OVERDUE_INSTALLMENTS_INCREASE",
            "balances": {
                "redrawBalance": 0,
                "principalDue": 0,
                "principalPaid": 0,
                "principalBalance": 0,
                "interestDue": 0,
                "interestPaid": 0,
                "interestBalance": 0,
                "interestFromArrearsBalance": 0,
                "interestFromArrearsDue": 0,
                "interestFromArrearsPaid": 0,
                "feesDue": 0,
                "feesPaid": 0,
                "feesBalance": 0,
                "penaltyDue": 0,
                "penaltyPaid": 0,
                "penaltyBalance": 0,
                "holdBalance": 0
            },
            "disbursementDetails": {
                "encodedKey": "8a44ba937f91f75b017f93446d67236a",
                "firstRepaymentDate": "2022-04-01T00:00:00-06:00",
                "transactionDetails": {
                    "encodedKey": "8a44ba937f91f75b017f93446d67236b",
                    "transactionChannelKey": "8a4450517ceb53d9017ced2ebe034042",
                    "internalTransfer": False
                },
                "fees": []
            },
            "prepaymentSettings": {},
            "penaltySettings": {
                "loanPenaltyCalculationMethod": "NONE"
            },
            "scheduleSettings": {
                "hasCustomSchedule": True,
                "principalRepaymentInterval": 1,
                "gracePeriod": 0,
                "gracePeriodType": "NONE",
                "repaymentInstallments": 12,
                "shortMonthHandlingMethod": "LAST_DAY_IN_MONTH",
                "fixedDaysOfMonth": [
                    1
                ],
                "scheduleDueDatesMethod": "FIXED_DAYS_OF_MONTH",
                "periodicPayment": 0,
                "repaymentScheduleMethod": "FIXED"
            },
            "interestSettings": {
                "interestRateSource": "FIXED_INTEREST_RATE",
                "accrueInterestAfterMaturity": False,
                "interestApplicationMethod": "REPAYMENT_DUE_DATE",
                "interestBalanceCalculationMethod": "ONLY_PRINCIPAL",
                "interestCalculationMethod": "DECLINING_BALANCE_DISCOUNTED",
                "interestChargeFrequency": "ANNUALIZED",
                "interestRate": 45.00000000000000000000,
                "interestType": "SIMPLE_INTEREST",
                "accrueLateInterest": True
            },
            "futurePaymentsAcceptance": "ACCEPT_OVERPAYMENTS",
            "currency": {
                "code": "MXN"
            }
        }
    }
}

response_desmbolso = {
    "headerRS": {
        "msgId": "bd9d3762-6c83-4e66-b3cf-a2b1ef26b761",
        "msgIdOrg": "cb67a83a-d810-436a-9f54-3e8ff50c693a",
        "timestamp": "2022-03-15T15:04:37-06:00"
    },
    "statusRS": {
        "code": 0,
        "description": "Se registró numero de orden"
    },
    "messageRS": {
        "url": "/own-channels/debit-transfer/local/online/single-currency/third-account/account/AK-REPAYMENT-823516994410199888/transfer",
        "response": [
            {
                "externalReference": "",
                "additionals": {},
                "isError": False,
                "PTSId": "PI1033",
                "errorCode": 0,
                "message": "",
                "confirmations": [
                    {
                        "postingId": "ae147d07-be43-4358-a752-9ec7e3633237",
                        "responseType": "ONLINE",
                        "confirmationNumber": "1700000418",
                        "data": [
                            {
                                "FLOW_GROUP": "NORMAL",
                                "TRANSACTION_CURRENCY": "MXN",
                                "EXCHANGE_RATE": "1",
                                "SETTLEMENT_DATE": "2022-03-15",
                                "ROUND": 1,
                                "ORDINA0073": "10",
                                "OPERATION_SIGN": "D",
                                "COMISSION_AMOUNT": 0,
                                "TRANSACTIONID": "8bd8e0c5-c1e8-4a74-9d04-10ed1f30851c",
                                "VALUE_DATE": "2022-03-15",
                                "TRANSACTION_TYPE": "TRANSF_LOCAL_EXTERNAL_STP_PTS_TRANSFER_DO-LCL-SCUR",
                                "OPERATION_SUBCODE": "PRINCIPAL",
                                "CONVERTED_AMOUNT": 15000,
                                "TRANSACTION_AMOUNT": 15000,
                                "TAX_AMOUNT": 0,
                                "OPERATION_CODE": "PRINCIPAL_AMOUNT",
                                "AMOUNT": 15000,
                                "Ordina0078": "10",
                                "OUTPUT_CHANNEL": "STP_OUT",
                                "ACCOUNT_COUNTERT": "DA483916EE4D5236E0530100007F4843",
                                "REFERENCE": "Transferencia interna",
                                "SUBJECT": "ORDERER",
                                "INPUT_CHANNEL": "STP_OUT",
                                "ACCOUNT_TO_POST": "D4C24C5EF2D32BFAE0530100007F74B4"
                            }
                        ],
                        "errorCode": "0",
                        "operation": "TRANSF_LOCAL_EXTERNAL_STP_PTS_TRANSFER_DO-LCL-SCUR.TWO_MESSAGE_DEBIT_CREDIT.DEBIT",
                        "roundId": "1",
                        "ordinal": "10"
                    },
                    {
                        "postingId": "99dbe70f-f57a-445d-9faa-fd80ee6d2560",
                        "responseType": "DEFERRED",
                        "confirmationNumber": 15002122,
                        "data": {
                            "resultado": {
                                "id": 15002122
                            }
                        },
                        "errorCode": "0",
                        "operation": "TRANSF_LOCAL_EXTERNAL_STP_PTS_TRANSFER_DO-LCL-SCUR.TWO_MESSAGE_DEBIT_CREDIT.CREDIT",
                        "roundId": "1",
                        "ordinal": "20"
                    }
                ],
                "roundId": "1",
                "transactionId": "1700000418"
            }
        ]
    }
}