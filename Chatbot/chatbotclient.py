#!/usr/bin/env  python
#Programa de chat para atendimento de uma pizzaria - Cliente
#Julia Daniele Moreira - 1714

import socket
import select
import errno
import sys

from threading import Thread

HEADER_LENGTH = 100

IP = "127.0.0.1"
PORT = 8080
my_username = input("Nome: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

#Classe para enviar a msg
class Sender(Thread):
    def __init__ (self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            
            #Lendo a mensagem a ser enviada
            message = input(f'{my_username} > ')

            #Se houver messagem
            if message:

                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)


#Classe para receber a mensagem      
class Reciever(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            try:
                #Loop sobre as mensagens recebidas e imprimi-las
                while True:

                    #Receba o "cabeçalho" contendo o comprimento do nome de usuário, seu tamanho é definido e constante
                    username_header = client_socket.recv(HEADER_LENGTH)

                    #Se não recebemos dados, o servidor fecha a conexão
                    if not len(username_header):
                        print('Conexão fechada pelo servidor')
                        sys.exit()

                    

                    #Recebendo a mensagem
                    message_header = client_socket.recv(HEADER_LENGTH)
                    message_length = 10000 #tamanho da msg recebida
                    message = client_socket.recv(message_length).decode('utf-8')

                    #Mostrando a mensagem com o nome do servidor
                    print(f'\r{"Amanda"} > {message}')
                    print(f'{my_username} > ')

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Erro: {}'.format(str(e)))
                    sys.exit()

            except Exception as e:
                print('Erro: '.format(str(e)))
                sys.exit()


if __name__ == "__main__":
    sender = Sender()
    reciever = Reciever()

    sender.start()
    reciever.start()