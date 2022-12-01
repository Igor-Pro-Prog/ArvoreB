#Arvore B, Estrutura de Dados 2
#Implementação de akgumas funcoes da arvore B
class BTree:
    def __init__(self, t):
        self.t = t
        self.root = Node(t, True)
        self.root.n = 0

    # Funcao para percorrer a arvore
    def traverse(self):
        if self.root:
            self.root.traverse()

    # Funcao para buscar uma chave na arvore
    def search(self, k):
        return self.root.search(k)

    # Funcao para inserir uma chave na arvore
    def insert(self, k):
        # Se a raiz estiver cheia, a arvore cresce em altura
        if self.root.n == 2 * self.t - 1:
            # Cria um novo no vazio
            s = Node(self.t, False)

            # Faz a raiz atual como filho do novo no
            s.C[0] = self.root

            # Divide a raiz atual em dois
            # s.C[0] e s.C[1] sao os novos filhos
            s.splitChild(0, self.root)

            # Apos dividir a raiz, decidir qual dos dois
            # filhos vai receber a nova chave
            i = 0
            if s.keys[0] < k:
                i += 1
            s.C[i].insertNonFull(k)

            # Mudar a raiz
            self.root = s
        else:
            # Se a raiz nao estiver cheia, chamar o metodo
            # insertNonFull da raiz
            self.root.insertNonFull(k)

    # Funcao para remover uma chave da arvore
    def remove(self, k):
        if self.root:
            # Chama o metodo remove da raiz
            self.root.remove(k)

            # Se a raiz ficar vazia, faz a segunda folha
            # como nova raiz se houver mais de uma folha
            # Caso contrario, seta a raiz como None
            if self.root.n == 0:
                tmp = self.root
                if self.root.leaf:
                    self.root = None
                else:
                    self.root = self.root.C[0]
                # Libera a memoria
                del tmp

    def __str__(self):
        if self.root:
            return self.root.__str__()
        return ''   

# Classe que representa um no da arvore B
class Node:
    def __init__(self, t, leaf):
        # Ordem da arvore
        self.t = t

        # Lista de chaves
        self.keys = [0 for i in range(2 * t - 1)]

        # Lista de filhos
        self.C = [None for i in range(2 * t)]

        # Numero de chaves presentes no no
        self.n = 0

        # Se o no eh uma folha
        self.leaf = leaf

    # Funcao para percorrer o no
    def traverse(self):
        # Indice para percorrer as chaves
        i = 0
        # Primeiro percorre todos os filhos antes da primeira chave
        # Se o no nao for uma folha, entao ele possui n+1 filhos
        # O primeiro filho tem todos os valores menores que a primeira chave
        while i < self.n:
            # Se o no nao for uma folha, antes de imprimir a chave
            # o filho antes da chave i eh percorrido
            if not self.leaf:
                self.C[i].traverse()
            print(' ', self.keys[i])
            i += 1

        # Pelo menos um filho apos a ultima chave
        if not self.leaf:
            self.C[i].traverse()

    # Funcao para buscar uma chave no no
    def search(self, k):
        # Encontra a primeira chave maior ou igual a k
        i = 0
        while i < self.n and k > self.keys[i]:
            i += 1

        # Se a chave encontrada for igual a k, retorna o no
        if self.keys[i] == k:
            return self

        # Se a chave nao for encontrada aqui e o no for uma folha
        if self.leaf:
            return None

        # Se a chave nao for encontrada aqui, busca na subarvore correspondente
        return self.C[i].search(k)

    # Funcao para inserir uma chave em um no que nao esta cheio
    def insertNonFull(self, k):
        # Inicializa o indice como o indice da ultima chave
        i = self.n - 1

        # Se o no for uma folha
        if self.leaf:
            # Acha a localizacao da nova chave e move todas as chaves maiores
            # uma posicao a frente
            while i >= 0 and self.keys[i] > k:
                self.keys[i + 1] = self.keys[i]
                i -= 1

            # Insere a nova chave na localizacao encontrada
            self.keys[i + 1] = k
            self.n += 1
        else:
            # Acha o filho que vai receber a nova chave
            while i >= 0 and self.keys[i] > k:
                i -= 1

            # Checa se o filho encontrado esta cheio
            if self.C[i + 1].n == 2 * self.t - 1:
                # Se o filho encontrado estiver cheio, divide ele
                self.splitChild(i + 1, self.C[i + 1])

                # Depois de dividir o filho, a chave do meio do filho
                # sobe e o filho eh dividido em dois. A nova chave
                # pode ser inserida em um dos dois filhos. Decide qual
                # dos dois vai receber a nova chave
                if self.keys[i + 1] < k:
                    i += 1
            self.C[i + 1].insertNonFull(k)

    # Funcao para dividir o filho y do no. i eh o indice de y em C[]
    # O no y deve estar cheio quando esta funcao eh chamada
    def splitChild(self, i, y):
        # Cria um novo no que vai guardar (t-1) chaves de y
        z = Node(y.t, y.leaf)
        z.n = self.t - 1

        # Copia as ultimas (t-1) chaves de y para z
        for j in range(self.t - 1):
            z.keys[j] = y.keys[j + self.t]

        # Copia os ultimos t filhos de y para z
        if not y.leaf:
            for j in range(self.t):
                z.C[j] = y.C[j + self.t]

        # Reduz o numero de chaves em y
        y.n = self.t - 1

        # Como este no vai ter um novo filho, cria um espaco de mais
        for j in range(self.n, i, -1):
            self.C[j + 1] = self.C[j]

        # Faz o filho z ser o filho i+1 do no atual
        self.C[i + 1] = z

        # A chave y.t de y sobe e o numero de chaves no no atual aumenta
        for j in range(self.n - 1, i - 1, -1):
            self.keys[j + 1] = self.keys[j]

        self.keys[i] = y.keys[self.t - 1]
        self.n += 1

    # Funcao para remover a chave k do subarvore com raiz neste no
    def remove(self, k):
        # Encontra a chave a ser removida
        idx = self.findKey(k)

        # A chave a ser removida esta neste no
        if idx < self.n and self.keys[idx] == k:

            # Se o no eh uma folha, remove a chave diretamente
            if self.leaf:
                self.removeFromLeaf(idx)
            else:
                self.removeFromNonLeaf(idx)
        else:

            # Se o no eh uma folha, a chave nao esta presente na arvore
            if self.leaf:
                print('A chave ', k, ' nao esta presente na arvore')
                return

            # A chave a ser removida esta presente em um filho deste no
            # O filho que vai ter a chave removida possui pelo menos t chaves
            flag = False
            if idx == self.n:
                flag = True

            # Se o filho encontrado tiver menos que t chaves, preenche-o
            if self.C[idx].n < self.t:
                self.fill(idx)

            # Se o ultimo filho foi preenchido, ele deve ter sido fusionado
            # com o filho anterior e agora tem t-1 chaves. Portanto, o filho
            # anterior deve ser mergido com o filho encontrado
            if flag and idx > self.n:
                self.C[idx - 1].remove(k)
            else:
                self.C[idx].remove(k)

    # Funcao para remover a chave k presente em um no folha
    def removeFromLeaf(self, idx):
        # Move todas as chaves posteriores uma posicao atras
        for i in range(idx + 1, self.n):
            self.keys[i - 1] = self.keys[i]

        # Reduz o numero de chaves
        self.n -= 1

    # Funcao para remover a chave k presente em um no nao folha
    def removeFromNonLeaf(self, idx):
        k = self.keys[idx]

        # Se o filho anterior a chave k tem pelo menos t chaves
        if self.C[idx].n >= self.t:
            # Encontra o predecessor de k no subarvore com raiz no filho
            # anterior a k. Copia o predecessor para k e remove o predecessor
            # no filho anterior a k
            pred = self.getPredecessor(idx)
            self.keys[idx] = pred
            self.C[idx].remove(pred)

        # Se o filho apos a chave k tem pelo menos t chaves
        elif self.C[idx + 1].n >= self.t:
            # Encontra o sucessor de k no subarvore com raiz no filho
            # apos a k. Copia o sucessor para k e remove o sucessor
            # no filho apos a k
            succ = self.getSuccessor(idx)
            self.keys[idx] = succ
            self.C[idx + 1].remove(succ)

        # Se ambos os filhos anterior e apos a chave k tem t-1 chaves
        # Entao fusiona k e todos os filhos apos a chave k em um filho
        # que tem 2t-1 chaves. Agora o filho anterior a k contem 2t-1 chaves
        else:
            self.merge(idx)
            self.C[idx].remove(k)

    # Funcao para obter o predecessor da chave k presente no no idx
    def getPredecessor(self, idx):
        # Continua indo para o filho mais a direita ate chegar em uma folha
        cur = self.C[idx]
        while not cur.leaf:
            cur = cur.C[cur.n]

        # Retorna a ultima chave do no encontrado
        return cur.keys[cur.n - 1]

    # Funcao para obter o sucessor da chave k presente no no idx
    def getSuccessor(self, idx):
        # Continua indo para o filho mais a esquerda ate chegar em uma folha
        cur = self.C[idx + 1]
        while not cur.leaf:
            cur = cur.C[0]

        # Retorna a primeira chave do no encontrado
        return cur.keys[0]
    
    # Funcao para preencher o filho C[idx] que tem menos que t-1 chaves
    def fill(self, idx):
        # Se o filho anterior a C[idx] tem pelo menos t chaves
        if idx != 0 and self.C[idx - 1].n >= self.t:
            self.borrowFromPrev(idx)

        # Se o filho apos a C[idx] tem pelo menos t chaves
        elif idx != self.n and self.C[idx + 1].n >= self.t:
            self.borrowFromNext(idx)

        # Fusiona C[idx] com seu irmão
        # Se o filho C[idx] eh o ultimo filho, fusiona com o anterior
        # Caso contrario, fusiona com o proximo
        else:
            if idx != self.n:
                self.merge(idx)
            else:
                self.merge(idx - 1)
