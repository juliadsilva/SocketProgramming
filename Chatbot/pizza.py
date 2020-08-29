class Pizza:
    def __init__(self):
        self._opcao = ""
        self._prefixo = "pizza de "

    @property
    def opcao(self):
        return self._opcao

    @property
    def prefixo(self):
        return self._prefixo
    
    @opcao.setter
    def opcao(self, opcaoEscolhida):
        self._opcao = opcaoEscolhida

