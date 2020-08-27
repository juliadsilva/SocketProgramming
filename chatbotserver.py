#!/usr/bin/env  python
#Programa de chat para atendimento de uma pizzaria - Servidor
#Julia Daniele Moreira - 1714

import socket
import select
import sys

HEADER_LENGTH = 100
IP = "127.0.0.1"
PORT = 8080


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

                #armazena a messagem recebida para ser comparada
                messagemrecebida = str(message["data"].decode("utf-8"))

                print(f'Mensagem recebida de {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            
                for client_socket in clients:
                    if client_socket == notified_socket:

                        #Envio de mensagens ao cliente
                        
                        #Primeiro passo: apresentação do menu de opções
                        if STEP == 1:
                           
                           mensagem = ("Seja Bem-Vindo. Meu nome é Amanda. Sou uma atende virtual. Como posso ajuda-lo hoje? Digite: 1 - Para realizar um pedido ou 2 - Para cancelar um pedido")
                           message["data"] = mensagem.encode("utf-8")
                           message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")                            
                           client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])
                           STEP = 2

                        elif STEP == 2:

                            if messagemrecebida == "1": 
                                #Realizar o pedido 
                                mensagem = ("O que gostaria de pedir? Digite: 1 - Pizza (6 pedaços) ou 2 - Bebidas (latas de 500ml")
                                message["data"] = mensagem.encode("utf-8") 
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])  
                                STEP = 3; 

                            elif messagemrecebida == "2":
                                #Cancelar o pedido
                                mensagem = ("Informe o codigo do pedido")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])  
                                STEP = 8; 

                            else: 
                                mensagem = ("Opççao Invalida")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])


       
                        #STEP = 3 -->  Realizar o pedido
                        elif STEP == 3:
                            #Pedido de pizza
                            if messagemrecebida == "1": 
                                mensagem = ("Digite 1 - Mussarela ou 2 - Calabresa 3 - Frango")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                                STEP = 4 
                            
                            #Pedido de bebida
                            elif messagemrecebida == "2":
                                mensagem = ("Digite 1 - Coca ou 2 - Suco ou 3 - Água")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])  
                                STEP = 5

                        #STEP = 4 --> Confimar o pedido de pizza
                        elif STEP == 4:
                            
                            if messagemrecebida == "1": 
                                mensagem = ("O seu pedido é pizza de Mussarela. Digite 1 - Confirmar o pedido 2 - Para troca o pedido")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])  
                                STEP = 6
                                
                            elif messagemrecebida == "2": 
                                mensagem = ("O seu pedido é pizza de Calabreza. Digite 1 - Confirmar o pedido 2 - Para troca o pedido")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                                STEP = 6

                            elif messagemrecebida == "3":
                                mensagem = ("O seu pedido é pizza de Frango. Digite 1 - Confirmar o pedido 2 - Para troca o pedido")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                                STEP = 6

                            else:
                                mensagem = ("Opção Invalida")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])
                        
                        #STEP = 5 --> Confimar o pedido de bebidas
                        elif STEP == 5:
                            
                            if messagemrecebida == "1": 
                                mensagem = ("O seu pedido é a bebida Coca. Digite 1 - Confirmar o pedido 2 - Para troca o pedido")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])  
                                STEP = 6
                                
                            elif messagemrecebida == "2": 
                                mensagem = ("O seu pedido é a bebida Suco. Digite 1 - Confirmar o pedido 2 - Para troca o pedido")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                                STEP = 6


                            elif messagemrecebida == "3":
                                mensagem = ("O seu pedido é a bebida Agua. Digite 1 - Confirmar o pedido 2 - Para troca o pedido")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                                STEP = 6

                            else:
                                mensagem = ("Opção Invalida")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])

                        #STEP = 6 --> Pedido realizado
                        elif STEP == 6:
                            if messagemrecebida == "1": 
                                mensagem = ("Pedido confirmado. O seu codigo é 80. Informe o endereço de entrega.")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])  
                                STEP = 7
                                
                            elif messagemrecebida == "2": 
                                mensagem = ("Irei apresentar o menu novamente. Digite 1")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                                STEP = 2
                            
                            else:
                                mensagem = ("Opção Invalida")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])

                        #STEP = 7 -- Confirmar dados do cliete 
                        elif STEP == 7:
                            mensagem = ("Seu pedido será entregue em 30 - 60 minutos")
                            message["data"] = mensagem.encode("utf-8")
                            message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                            client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                            STEP = 0

                        #Cancelar o pedido
                        elif STEP == 8:
                            
                            mensagem = ("O pedido " + messagemrecebida + " foi cancelado.") 
                            message["data"] = mensagem.encode("utf-8")
                            message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                            client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])
                            STEP = 0

                        else:
                           mensagem = ("Obrigada! Tenha um bom dia.")
                           message["data"] = mensagem.encode("utf-8")
                           message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                           client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])  
                           sockets_list.remove(notified_socket)
                           del clients[notified_socket]


        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]