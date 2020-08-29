
HEADER_LENGTH = 100

def menuApresentacao(message):
    mensagem = ("\nSeja Bem-Vindo.\nMeu nome é Amanda. Sou uma atende virtual. Como posso ajuda-lo hoje? \nDigite: \n1 - Para realizar um pedido\n2 - Para cancelar um pedido")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8") 
    return message

def opcaoInvalida(message):
    mensagem = ("\nOpção Invalida")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def pizzaOuBebida(message):
    mensagem = ("\nO que gostaria de pedir?\nDigite:\n1 - Pizza (6 pedaços)\n2 - Bebidas (latas de 500ml)")
    message["data"] = mensagem.encode("utf-8") 
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def opcaoPizza(message):
    mensagem = ("\nDigite:\n1 - Mussarela\n2 - Calabresa\n3 - Frango")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def opcaoBebida(message):
    mensagem = ("\nDigite:\n1 - Coca\n2 - Suco\n3 - Água")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def confirmaPedido(message, prefixo, opcao):
    mensagem = ("\nO seu pedido é " + prefixo + opcao + ".\nDigite:\n1 - Confirmar o pedido\n2 - Para troca o pedido")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def informeCodigoPedido(message):
    mensagem = ("\nInforme o codigo do pedido")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def pedidoConfirmado(message):
    mensagem = ("\nPedido confirmado. O seu codigo é 80.\nInforme o endereço de entrega.")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def repeteMenu(message):
    mensagem = ("\nIrei apresentar o menu novamente.\nDigite: 1")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def pedidoEntregue(message):
    mensagem = ("\nSeu pedido será entregue em 30 - 60 minutos")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def pedidoCancelado(message, numero):
    mensagem = ("\nO pedido #" + numero + " foi cancelado.") 
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message

def menuFinal(message):
    mensagem = ("\nObrigada!")
    message["data"] = mensagem.encode("utf-8")
    message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    return message
