class Bebida:
    def __init__(self):
        self._opcao = ""
        self._prefixo = "bebida "

    @property
    def opcao(self):
        return self._opcao

    @property
    def prefixo(self):
        return self._prefixo
    
    @opcao.setter
    def opcao(self, opcaoEscolhida):
        self._opcao = opcaoEscolhida

