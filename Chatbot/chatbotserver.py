#!/usr/bin/env  python
#Programa de chat para atendimento de uma pizzaria - Servidor
#Julia Daniele  - 1714

import socket
import select
import sys
import menuUtilsChatBot

from pizza import Pizza
from bebida import Bebida


HEADER_LENGTH = 100
IP = "127.0.0.1"
PORT = 8080
PIZZAS_DISPONIVEIS = ["Mussarela" , "Calabreza", "Frango"]
BEBIDAS_DISPONIVEIS = ["Coca" , "Suco", "Agua"]

#Configure inicialmente o soquete 
#socket.SOCK_STREAM - TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()
server_socket.setblocking(False)

sockets_list = [server_socket]
clients = {}

#Variavel auxiliar para controle de passos de atendimento
STEP = 1

#Exibi a quem o servidor está conectado
print("Conectado: " +IP+":"+str(PORT))

#Função para o recebimento de mensagens do cliente
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        
        message_length = 10000
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        print("[ERROR] A mensagem não pode ser lida")
        return False

def send_message(client_socket, user, message):
    client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])


if __name__ == "__main__":
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                user = receive_message(client_socket)
                if user is False:
                    continue
                
                sockets_list.append(client_socket)

                clients[client_socket] = user
                
                print('Aceitando nova conexão de {}:{}, username: {}'.format(*client_address, user["data"].decode("utf-8")))
            
            else:
                message = receive_message(notified_socket)
                if message is False:
                    print('Conexão fechada de: {}'.format(clients[notified_socket]["data"].decode("utf-8")))
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
               
                user = clients[notified_socket]

                #Armazena a mensagem recebida para ser comparada
                mensagemrecebida = str(message["data"].decode("utf-8"))

                print(f'Mensagem recebida de {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            
                for client_socket in clients:
                    if client_socket == notified_socket:

                        #Envio de mensagens ao cliente
                        
                        #Primeiro passo: apresentação do menu de opções
                        if STEP == 1:
                           send_message(client_socket, user, menuUtilsChatBot.menuApresentacao(message))
                           STEP = 2

                        #Segundo passo: tratamento da opção do primeiro menu
                        elif STEP == 2:
                            if mensagemrecebida == "1": 
                                #Realizar o pedido 
                                send_message(client_socket, user, menuUtilsChatBot.pizzaOuBebida(message))
                                STEP = 3 
                            elif mensagemrecebida == "2":
                                #Cancelar o pedido
                                send_message(client_socket, user, menuUtilsChatBot.informeCodigoPedido(message))
                                STEP = 8 
                            else: 
                                send_message(client_socket, user, menuUtilsChatBot.opcaoInvalida(message))
                                STEP = 1

                        #STEP = 3 -->  Realizar o pedido
                        elif STEP == 3:
                            if mensagemrecebida == "1":
                                send_message(client_socket, user, menuUtilsChatBot.opcaoPizza(message))
                                STEP = 4
                            elif mensagemrecebida == "2":
                               send_message(client_socket, user, menuUtilsChatBot.opcaoBebida(message))
                               STEP = 5

                        #STEP = 4 --> Confimar o pedido de pizza
                        elif STEP == 4:
                            pizza = Pizza()
                            opcao = int(mensagemrecebida) - 1 

                            if opcao >= 0 and opcao <= 2:
                                pizza.opcao = PIZZAS_DISPONIVEIS[opcao]
                                send_message(client_socket, user, menuUtilsChatBot.confirmaPedido(message, pizza.prefixo, pizza.opcao))
                                STEP = 6
                            else:
                                send_message(client_socket, user, menuUtilsChatBot.opcaoInvalida(message))
                                STEP = 1

                        #STEP = 5 --> Confimar o pedido de bebidas
                        elif STEP == 5:
                            bebida = Bebida()
                            opcao = int(mensagemrecebida) - 1

                            if opcao >= 0 and opcao <= 2:
                                bebida.opcao = BEBIDAS_DISPONIVEIS[opcao]
                                send_message(client_socket, user, menuUtilsChatBot.confirmaPedido(message, bebida.prefixo, bebida.opcao))
                                STEP = 6
                            else:
                                send_message(client_socket, user, menuUtilsChatBot.opcaoInvalida(message))
                                STEP = 1

                        #STEP = 6 --> Pedido realizado
                        elif STEP == 6:
                            if mensagemrecebida == "1": 
                                send_message(client_socket,user,menuUtilsChatBot.pedidoConfirmado(message))
                                STEP = 7
                            elif mensagemrecebida == "2": 
                                send_message(client_socket,user,menuUtilsChatBot.repeteMenu(message))
                                STEP = 2
                            else:
                                send_message(client_socket, user, menuUtilsChatBot.opcaoInvalida(message))
                                STEP = 1

                        #STEP = 7 -- Confirmar dados do cliete 
                        elif STEP == 7:
                           send_message(client_socket, user, menuUtilsChatBot.pedidoEntregue(message))     
                           STEP = 0

                        #Cancelar o pedido
                        elif STEP == 8:
                            send_message(client_socket, user, menuUtilsChatBot.pedidoCancelado(message,mensagemrecebida))
                            STEP = 0
                        else:
                            send_message(client_socket, user, menuUtilsChatBot.menuFinal(message))
                            sockets_list.remove(notified_socket)
                            del clients[notified_socket]

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]