#!/usr/bin/env  python
#Programa questionario
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

#Variavel auxiliar para controle de passos
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
                
                sockets_list.append(client_socket)

                clients[client_socket] = user
                
                print('Aceitando nova conexão de {}:{}'.format(*client_address))
            
            else:
                message = receive_message(notified_socket)
                if message is False:
                    print('Conexão fechada de: {}'.format(clients[notified_socket]["data"].decode("utf-8")))
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
               
                user = clients[notified_socket]

                #armazena a mensagem recebida para ser comparada
                mensagemrecebida = str(message["data"].decode("utf-8"))

                print(f'Mensagem recebida: {message["data"].decode("utf-8")}')
            
                for client_socket in clients:
                    if client_socket == notified_socket:

                    #Envio de mensagens ao cliente
                        
                        #Primeira questão
                        if STEP == 1:
                           
                            mensagem = ("Questão 01: O termo técnico para designar a parte fisica do computador é: \na) Software \nb) Hardware \nc) Firmware \nd) Middleware")
                            message["data"] = mensagem.encode("utf-8") 
                            message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                            client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])  
                            STEP = 2; 
   
                        elif STEP == 2:                  
                            questaoum = mensagemrecebida;

                            mensagem = ("Questão 02: A menor quantidade de informações binária chama-se: \na) Bit \nb) Byte \nc) Microbyte \nd) Minibitfoi")
                            message["data"] = mensagem.encode("utf-8")
                            message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                            client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                            STEP = 3
                            
                        elif STEP == 3:

                            STEP = 4
                            questaodois = mensagemrecebida;

                            mensagem = ("Respostas:\nQuestão 01: Sua resposta foi: " + questaoum + ".")
                            message["data"] = mensagem.encode("utf-8")
                            message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                            client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 

                            if questaoum == "b" or questaoum == "B":
                                mensagem = ("Você acertou. Parabêns! \nDigite 'ok' para continuar.")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                            
                            else:
                                mensagem = ("Resposta errada.\nA alternativa correta era b) Hardware.\nDigite 'ok' para continuar.")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                          
                        elif STEP == 4:

                            mensagem = ("Questão 02: Sua resposta foi: " + questaodois + ".")
                            message["data"] = mensagem.encode("utf-8")
                            message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                            client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 

                            if questaodois == "a" or questaodois == "A":
                                mensagem = ("Você acertou. Parabêns!")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                            
                            else:
                                mensagem = ("Resposta errada. \n A alternativa correta era a) Bit.")
                                message["data"] = mensagem.encode("utf-8")
                                message["header"] = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")      
                                client_socket.send(user["header"] + user["data"] + message["header"] + message["data"]) 
                            
                            sockets_list.remove(notified_socket)
                            del clients[notified_socket] 

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]