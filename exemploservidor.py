#!/usr/bin/env  python

import socket 
import select 
import sys 
#from thread import *
  
#Configure inicialmente o soquete 
#socket.SOCK_STREAM - TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

IP_address = "127.0.0.1"
PORT = 1234 
  
server.bind((IP_address, PORT)) 
server.listen(100) 
  
list_of_clients = [] 

    
def clientthread(servidor, addr): 
  
     # envia uma mensagem ao cliente cujo objeto de usuário é servidor
    servidor.send("Seja bem vindo") 
  
    while True: 
            try: 
                message = servidor.recv(2048) 
                if message: 
  
                    #imprime a mensagem e o endereço do usuário que acabou de enviar a mensagem no servidor terminal
                    print ("<" + addr[0] + "> " + message)
  
                    #Chama a função de transmissão para enviar mensagem a todos
                    message_to_send = "<" + addr[0] + "> " + message 
                    broadcast(message_to_send, servidor) 
  
                else: 
                    #A mensagem pode ​​não ter conteúdo se a conexão está quebrado, neste caso removemos a conexão
                    remove(servidor) 
  
            except: 
                continue
  
#Usando a função abaixo, transmitimos a mensagem para todos clientes cujo objeto não é o mesmo que envia a mensagem
def broadcast(message, servidorection): 
    for clients in list_of_clients: 
        if clients!=servidorection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
  
                #se o link estiver quebrado, removemos o cliente 
                remove(clients) 

#A função a seguir simplesmente remove o objeto da lista que foi criada no início de o programa
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
  
    #Aceita uma solicitação de conexão e armazena dois parâmetros, servidor que é um objeto socket para aquele usuário, e addr
    #que contém o endereço IP do cliente que apenas     conectado
    servidor, addr = server.accept() 
  
    #Mantém uma lista de clientes para facilitar a transmissão uma mensagem para todas as pessoas disponíveis na sala de chat 
    list_of_clients.append(servidor) 
  
    #imprime o endereço do usuário que acabou de se conectar 
    print (addr[0] + " conectado")
  
    #cria um tópico individual para cada usuário que conecta
    #start_new_thread(clientthread,(servidor,addr))     
  
servidor.close() 
server.close() 