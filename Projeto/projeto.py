from contas import contas
import getpass
from datetime import datetime
import os

def limparEcra():
    os.system('cls' if os.name == 'nt' else 'clear')

def login(contas: dict):
    while True:
        idConta = input("Insira o ID da conta (ex: 014): ")
        conta = contas.get(idConta)
        if not conta:
            print("Conta não encontrada")
            continue
        
    
        pin = getpass.getpass("Insira o seu PIN: ").strip()
        if len(pin) != 4:
            print("PIN inválido (tem de ter 4 dígitos).")
            continue

        if pin == str(conta.get("PIN", "")):
            print(f"\nAutenticado. Bem-Vindo, {conta.get('Nome','')}!")
            input("Prima ENTER para continuar...")
            return idConta
        else: 
            print("Acesso negado. PIN incorreto.")
    limparEcra()

def menu():
    limparEcra()
    print("\n=== MULTIBANCO ===\n")
    print("1. Consultar Saldo\n")
    print("2. Realizar Levantamento\n")
    print("3. Realizar Depósito\n")
    print("4. Realizar Transferência\n")
    print("5. Consultar Movimentos\n")
    print("6. Sair")

def main(contas, idConta):
    
    while True:
        menu()
        opcao = input("Opção: ").strip()
        match opcao:
            case "1":
                limparEcra()
                consultarSaldo(contas, idConta)
            case "2":
                limparEcra()
                levantamentos(contas, idConta)
            case "3":
                limparEcra()
                depositos(contas, idConta)
            case "4":
                limparEcra()
                transferencias(contas, idConta)
            case "5":
                limparEcra()
                consultarMovimentos(contas, idConta)
            case "6":
                limparEcra()
                print("Obrigado por utilizar o nosso multibanco e até já!")
                break
            case _:
                return "Opção Invalida"
            
def gerarIDT(contas):
    max_id = 0
    
    for conta in contas.values():
        for x in conta.get("Transferencias", []):
            trans_id = x.get("Transferencia_ID")
            if isinstance(trans_id, str) and trans_id.isdigit():
                max_id = max(max_id, int(trans_id))
            elif isinstance(trans_id, int):
                max_id = max(max_id, trans_id)
    return f"{max_id + 1:03d}"


def consultarSaldo(contas: dict, idConta):
    if idConta in contas:  
        dados = contas[idConta]
        print(f"Cliente: {dados['Nome']}")
        print(f"Saldo atual: {dados['Saldo']} €")
    else:
        print("Conta não encontrada!") 
    input("Prima ENTER para continuar...")

def gerarIDTransf():
    global ultimoID
    ultimoID += 1
    return f"T{ultimoID:05}"
     
def levantamentos(contas: dict, idConta):
    if idConta in contas:  
        dados = contas[idConta]
        print(f"Cliente: {dados['Nome']}")
        print(f"Saldo atual: {dados['Saldo']} €")
        
        try:
            valorL=float(input("Insira o valor a levantar: ").replace(",","."))
        except ValueError:
            print("Valor Invalido!")
            input("Prima ENTER para continuar...")
            return
        saldoAtual= float(dados["Saldo"])
        if valorL <= 0:
            print("Tem de ser um valor < 0 !")
            input("Prima ENTER para continuar...")
            return
        if valorL > saldoAtual:
            print("Saldo Insuficiente! ")
        else:
            saldoAtual -= valorL
            dados["Saldo"]= round(saldoAtual, 2)
            print(f"Levantamento de {valorL:.2f} € realizado com sucesso.")
            print(f"O seu Saldo Atual é de {saldoAtual:.2f} €")
            
            agora=datetime.now()
            total_transf = 0
            for conta in contas.values():
                total_transf += len(conta.get("Transferencias", []))
            id_transferencia = f"{total_transf + 1:03d}"
 
            transf = {
                "Transferencia_ID": gerarIDT(contas),
                "Data": agora.strftime("%Y-%m-%d"),
                "Hora": agora.strftime("%H:%M"),
                "Valor": -valorL,
                "IBAN Conta Destinatário": "Levantamento"
            }
            dados["Transferencias"].append(transf)
    else:
        print("Conta não encontrada!") 
    input("Prima ENTER para continuar...")
        
def depositos(contas: dict, idConta):
    if idConta in contas:  
        dados = contas[idConta]
        print(f"Cliente: {dados['Nome']}")
        print(f"Saldo atual: {dados['Saldo']} €")
        
        try:
            valorD=float(input("Insira o valor a depositar: ").replace(",","."))
        except ValueError:
            print("Valor Inválido!")
            input("Prima ENTER para continuar...")
            return
        saldoAtual= float(dados["Saldo"])
        if valorD <= 0:
            print("Tem de ser um valor < 0 !")
            input("Prima ENTER para continuar...")
        if valorD > 1000000:
            print("Máximo de deposito e de 1 milhão! ")
        else:
            saldoAtual += valorD
            dados["Saldo"] = round(saldoAtual, 2)
            print(f"Deposito de {valorD:.2f} € realizado com sucesso.")
            print(f"O seu Saldo Atual é de {saldoAtual:.2f} €")
            
            agora=datetime.now()
            total_transf = 0
            for conta in contas.values():
                total_transf += len(conta.get("Transferencias", []))
            id_transferencia = f"{total_transf + 1:03d}"
            
            transf = {
                "Transferencia_ID": gerarIDT(contas),
                "Data": agora.strftime("%Y-%m-%d"),
                "Hora": agora.strftime("%H:%M"),
                "Valor": +valorD,
                "IBAN Conta Destinatário": "Deposito"
            }
            dados["Transferencias"].append(transf)
    else:
        print("Conta não encontrada!") 
    input("Prima ENTER para continuar...")


def transferencias(contas: dict, idConta: str ):
    conta_origem = contas[idConta]
    print(f"Cliente: {conta_origem['Nome']}")
    print(f"Saldo atual: {conta_origem['Saldo']}€")
    
    idDestino = input("Insira o ID da conta de destino: ").strip()
    if idDestino not in contas:
        print("Conta de destino não encontrada!")
        input("Prima ENTER para continuar...")
        return

    if idDestino == idConta:
        print("Não pode transferir para a mesma conta!")
        input("Prima ENTER para continuar...")
        return
    
    try:
        valor = float(input("Insira o valor a transferir: ").replace(",","."))
        if valor <= 0:
            print("Valor inválido!")
            input("Prima ENTER para continuar...")
            return
    except ValueError:
        print("Valor inválido!")
        input("Prima ENTER para continuar...")
        return
        
    if conta_origem["Saldo"] < valor:
        print("Saldo insuficiente!")
        input("Prima ENTER para continuar...")
        return
    
    conta_origem["Saldo"] -= valor
    contas[idDestino]["Saldo"] += valor
    
    print(f"Transferência de {valor:.2f} € realizada com sucesso para {contas[idDestino]['Nome']}.")
    input("Prima ENTER para continuar...")
    
    agora = datetime.now()
    data = agora.strftime("%Y-%m-%d")
    hora = agora.strftime("%H:%M")
    

    id_transferencia = gerarIDT(contas)
    
    transf_origem = {
        "Transferencia_ID": id_transferencia,
        "IBAN Conta Remetente": conta_origem.get("IBAN", ""),
        "Data": data,
        "Hora": hora,
        "Valor": -valor,
        "IBAN Conta Destinatário": contas[idDestino].get("IBAN", ""),
    }
    
    transf_destino = {
        "Transferencia_ID": id_transferencia,
        "IBAN Conta Remetente": conta_origem.get("IBAN", ""),
        "Data": data,
        "Hora": hora,
        "Valor": valor,
        "IBAN Conta Destinatário": contas[idDestino].get("IBAN", ""),
    }
    conta_origem["Transferencias"].append(transf_origem)
    contas[idDestino]["Transferencias"].append(transf_destino)
    
def consultarMovimentos(contas: dict, idConta: str):
    dados = contas.get(idConta)
    
    movimentos = dados.get("Transferencias", [])
    if not movimentos:
        print("\nNenhum movimento registado.")
        input("Prima ENTER para continuar...")
        return

    def obter_data_hora(m):
        data = m.get("Data", "1900-01-01")
        hora = m.get("Hora", "00:00")
        try:
            return datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")
        except ValueError:
            return datetime.min

    def tipo_e_descricao(m):
        try:
            v = float(m.get("Valor", 0.0))
        except (TypeError, ValueError):
            v = 0.0

        destino = m.get("IBAN Conta Destinatário", "")
        remetente = m.get("IBAN Conta Remetente", "")


        if destino == "Levantamento":
            return "Levantamento", "Levantamento em numerário", v
        if destino == "Deposito":
            return "Depósito", "Depósito em numerário", v

        if v < 0:
            return "Transferência (Enviada)", f"Para {destino}", v
        else:
            return "Transferência (Recebida)", f"De {remetente}", v

    ultimos = sorted(movimentos, key=obter_data_hora, reverse=True)[:10]

    print("\n=== Últimos movimentos ===")
    for m in ultimos:
        dt = obter_data_hora(m)
        tipo, descricao, valor = tipo_e_descricao(m)
        print(f"{dt:%Y-%m-%d %H:%M} — {tipo}: {valor:+.2f} € — {descricao}")

    input("Prima ENTER para continuar...")


idConta = login(contas)
if idConta:    
    main(contas, idConta)


        