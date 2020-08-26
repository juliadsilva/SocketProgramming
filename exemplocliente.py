#Programa Python para implementar o lado do cliente na sala de chat.
import socket 
import select 
import sys 
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

IP_address = "127.0.0.1"
Port = 1234 

server.connect((IP_address, Port)) 
  
while True: 
  
    #Mantém uma lista de possíveis fluxos de entrada
    sockets_list = [sys.stdin, server] 
  
    #Existem duas situações de entrada possíveis.
    #O usuário deseja fornecer dados manuais para enviar a outras pessoas,
    #ou o servidor está enviando uma mensagem para ser impressa no
    #tela. Selecione os retornos de sockets_list, o fluxo que
    #é um leitor para entrada. Por exemplo, se o servidor quiser
    #para enviar uma mensagem, então a condição if se manterá verdadeira
    #abaixo. Se o usuário deseja enviar uma mensagem, o outro
    #condição será avaliada como verdadeira

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print (message)
        else: 
            message = sys.stdin.readline() 
            server.send(message) 
            sys.stdout.write("<Voce>") 
            sys.stdout.write(message) 
            sys.stdout.flush() 

server.close() 