#Funcao getaddrinfo lista os endere ̧cos IP e n ́umeros de portapara host hostname e servico servname

import  socket
from  pprint  import  pprint

addrinfo = socket.getaddrinfo('uol.com.br', 'www')

pprint(addrinfo)

