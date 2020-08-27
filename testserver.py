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
                           
                           mensagem = ("O questionario possui duas questões de multipla escolha. Envie somente a resposta desejada. Digite <Inicar> para começar o teste.")
                           message["data"] = mensagem.encode("utf-8")
                           message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")                            
                           client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])
                           STEP = 2

                        elif STEP == 2:

                            if messagemrecebida == "Iniciar": 
                                #Realizar o pedido 
                                mensagem = ("Questão 01: Em que lugar o Papel foi inventado há mais de 2000 anos atrás? a) Na China b) Na Atlântida c) No Egito, pelos Judeus d) Na Mongólia e) No Japão")
                                message["data"] = mensagem.encode("utf-8") 
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])  
                                STEP = 3; 

                            else: 
                                mensagem = ("Opççao Invalida")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])
     
                        #STEP = 3 --> Conferir questão 01 e enviar questão 02
                        elif STEP == 3:
                            if messagemrecebida == "a":
                                questaoum = 1

                            else: 
                                questaoum = 0
                              
                            mensagem = ("Questão 02: O Réptil predador pré-histórico mais feroz que existiu, foi: a) O Dinossauro Rex b) O Tiranossauro Rex  c) O Velociraptor d)  O Bocassauro e)  O Mastodonte")
                            message["data"] = mensagem.encode("utf-8")
                            message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                            client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                            STEP = 4 
                            

                        #STEP = 4 --> Conferir questão 02 e enviar resultado
                        elif STEP == 4:
                            
                            if messagemrecebida == "b":
                                questaodois = 1

                            else: 
                                questaodois = 0

                            if questaoum == 1 and questaodois == 1:
                                mensagem = ("Parabens!!! Você acertou a duas quesões.")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])
                            
                            elif questaoum == 1 and questaodois == 0:
                                mensagem = ("Que pena! Você acertou apenas a primeira questão. A resposta da questão dois era b) O Tiranossauro Rex")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])

                            elif questaoum == 0 and questaodois == 1:
                                mensagem = ("Que pena! Você acertou apenas a segunda questão. A resposta da questão dois era a) Na China")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])

                            else: 
                                mensagem = ("Infelizmente você errou as duas qeustões. A respota da questão um era a) Na China e da questão dois b) O Tiranossauro Rex")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])

                            sockets_list.remove(notified_socket)
                            del clients[notified_socket] 

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]