

def consultarSaldo(contas: dict, idConta):
    if idConta in contas:  
        dados = contas[idConta]
        print(f"Cliente: {dados['Nome']}")
        print(f"Saldo atual: {dados['Saldo']} €")