# Definição da classe AFN (Autômato Finito Não-Determinístico)
class AFN:
    def __init__(self):
        # Inicialização dos atributos
        self.states = set()  # Conjunto de estados
        self.alphabet = set()  # Alfabeto
        self.transitions = {}  # Dicionário de transições
        self.start_state = None  # Estado inicial
        self.accept_states = set()  # Conjunto de estados de aceitação

    # Método para adicionar um estado ao conjunto de estados
    def add_state(self, state):
        self.states.add(state)

    # Método para adicionar um símbolo ao alfabeto
    def add_alphabet(self, symbol):
        self.alphabet.add(symbol)

    # Método para adicionar uma transição ao dicionário de transições
    def add_transition(self, from_state, symbol, to_state):
        # Se a transição ainda não existir, cria um novo conjunto para armazenar os próximos estados
        if (from_state, symbol) not in self.transitions:
            self.transitions[(from_state, symbol)] = set()
        # Adiciona o próximo estado ao conjunto de próximos estados para a transição
        self.transitions[(from_state, symbol)].add(to_state)

    # Método para definir o estado inicial
    def set_start_state(self, state):
        self.start_state = state

    # Método para adicionar um estado de aceitação ao conjunto de estados de aceitação
    def add_accept_state(self, state):
        self.accept_states.add(state)


# Função para converter AFN para AFD
def converter_afn_para_afd(afn):
    afd = AFD()  # Cria um novo objeto AFD
    # Inicializa o conjunto de estados do AFD
    afd.states = {frozenset([afn.start_state])}
    afd.alphabet = afn.alphabet  # Copia o alfabeto do AFN para o AFD
    afd.transitions = {}  # Inicializa as transições do AFD
    # Define o estado inicial do AFD
    afd.start_state = frozenset([afn.start_state])

    # Função para obter o conjunto de estados alcançáveis a partir de um conjunto de estados e um símbolo
    def obter_transicao(estados, simbolo):
        novos_estados = set()
        for estado in estados:
            if (estado, simbolo) in afn.transitions:
                novos_estados.update(afn.transitions[(estado, simbolo)])
        return novos_estados

    # Enquanto houver novos estados a serem processados
    estados_a_processar = list(afd.states)
    while estados_a_processar:
        # Remove o primeiro estado da lista
        estado_afd = estados_a_processar.pop(0)
        for simbolo in afd.alphabet:
            novo_estado_afd = frozenset(obter_transicao(
                estado_afd, simbolo))  # Obtém os próximos estados
            if novo_estado_afd:  # Se houver próximos estados
                afd.transitions.setdefault(estado_afd, {})[
                    simbolo] = novo_estado_afd
                if novo_estado_afd not in afd.states:  # Se o novo estado não estiver no conjunto de estados do AFD
                    # Adiciona o novo estado ao conjunto de estados do AFD
                    afd.states.add(novo_estado_afd)
                    # Adiciona o novo estado para processamento futuro
                    estados_a_processar.append(novo_estado_afd)

    # Determina os estados de aceitação do AFD
    afd.accept_states = {estado_afd for estado_afd in afd.states if any(
        aceitacao in estado_afd for aceitacao in afn.accept_states)}

    return afd


# Definição da classe AFD (Autômato Finito Determinístico)
class AFD:
    def __init__(self):
        # Inicialização dos atributos
        self.states = set()  # Conjunto de estados
        self.alphabet = set()  # Alfabeto
        self.transitions = {}  # Dicionário de transições
        self.start_state = None  # Estado inicial
        self.accept_states = set()  # Conjunto de estados de aceitação


# Função para exibir o AFD resultante
def exibir_afd(afd):
    print("\nAFD resultante:")
    print("Estados:", end=" {")
    for estado in afd.states:
        print(estado, end=", ")
    print("}")
    print("Alfabeto:", afd.alphabet)
    print("Transições:")
    for estado, transicoes in afd.transitions.items():
        for simbolo, destino in transicoes.items():
            print(f"{estado} -- {simbolo} --> {destino}")
    print("Estado Inicial:", afd.start_state)
    print("Estados de Aceitação:", end=" {")
    for estado in afd.accept_states:
        print(estado, end=", ")
    print("}")


# Função principal
def main():
    # Criação de um objeto AFN
    afn = AFN()

    # Entrada dos estados
    print("Digite os estados (separados por espaços):")
    afn.states.update(input().split())

    # Entrada do alfabeto
    print("Digite o alfabeto (separado por espaços):")
    afn.alphabet.update(input().split())

    # Entrada das transições
    print("Digite as transições no formato 'estado símbolo próximo_estado' (digite 'fim' para terminar):")
    while True:
        transition_input = input().split()
        # Verifica se a entrada é 'fim' para terminar a entrada das transições
        if transition_input[0] == 'fim':
            break
        afn.add_transition(*transition_input)

    # Entrada do estado inicial
    print("Digite o estado inicial:")
    afn.start_state = input()

    # Entrada dos estados de aceitação
    print("Digite os estados de aceitação (separados por espaços):")
    afn.accept_states.update(input().split())

   # Exibição do AFN inserido
    print("\nAFN inserido:")
    print("Estados:", afn.states)
    print("Alfabeto:", afn.alphabet)
    print("Transições:")
    for transition, to_states in afn.transitions.items():
        print(transition[0], "--", transition[1], "-->", to_states)
    print("Estado Inicial:", afn.start_state)
    print("Estados de Aceitação:", afn.accept_states)

    # Converter o AFN para AFD
    afd = converter_afn_para_afd(afn)

    # Exibir o AFD resultante
    exibir_afd(afd)


# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()
