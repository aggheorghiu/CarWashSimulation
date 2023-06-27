class Stack:
    """ Implementação do TDA Stack baseada em list """

    def __init__(self, source_collection = None):
        """Define o estado inicial de self com sourceCollection """
        self._items = []
        self._size = 0

    # metodos gerais de coleção
    
    def is_empty(self):
        """ Retorna True se len(self) é 0, senão False """
        return self._size == 0

    def __len__(self):
        """ Retorna o numero de elementos do stack """
        return self._size

    def __str__(self):
        """ Retorna a representação em string de self """
        return str(self._items) + " :  " + str(self._size) + " elementos"

    def clear(self):
        """ Torna self vazio"""
        pass

    def __iter__(self):
        """ Suporta a iteração sobre self """
        return None

    # metodos específicos da pilha

    def peek(self):
        """ Retorna o item que está no topo de self.
             precondição: self não é vazio."""
        if not self.is_empty():
            return self._items[self._size - 1] # + à direita
        else:
            raise KeyError(" pilha vazia!")

    def push(self, item):
        """ Sobrepoe item a self
            pos-condição: item foi sobreposto a self """
        self._items.append(item)
        self._size += 1

    def pop(self):
        """ Remove elemento do topo de self e retorna esse elemento.
             precondição: self não é vazio.
             pos-condição: topo foi removido de self """
        if len(self) > 0:
            self._size -= 1
            return self._items.pop()
        else:
            raise KeyError(" pilha vazia!")


