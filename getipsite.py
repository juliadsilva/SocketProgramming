#Funcao gethostbyname retorna o enderecoo IPV4 do site

#!/usr/bin/env  python

import  socket
ip = socket.gethostbyname('uol.com.br')
print(ip)