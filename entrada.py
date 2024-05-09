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

# Função principal


def main():
    # Criação de um objeto AFN
    afn = AFN()

    # Entrada dos estados
    print("Digite os estados (separados por espaços):")
    states = input().split()
    for state in states:
        afn.add_state(state)

    # Entrada do alfabeto
    print("Digite o alfabeto (separado por espaços):")
    alphabet = input().split()
    for symbol in alphabet:
        afn.add_alphabet(symbol)

    # Entrada das transições
    print("Digite as transições no formato 'estado símbolo próximo_estado' (digite 'fim' para terminar):")
    while True:
        transition_input = input().split()
        # Verifica se a entrada é 'fim' para terminar a entrada das transições
        if transition_input[0] == 'fim':
            break
        from_state, symbol, to_state = transition_input
        afn.add_transition(from_state, symbol, to_state)

    # Entrada do estado inicial
    print("Digite o estado inicial:")
    start_state = input()
    afn.set_start_state(start_state)

    # Entrada dos estados de aceitação
    print("Digite os estados de aceitação (separados por espaços):")
    accept_states = input().split()
    for state in accept_states:
        afn.add_accept_state(state)

    # Exibição do AFN inserido
    print("\nAFN inserido:")
    print("Estados:", afn.states)
    print("Alfabeto:", afn.alphabet)
    print("Transições:")
    for transition, to_states in afn.transitions.items():
        print(transition[0], "--", transition[1], "-->", to_states)
    print("Estado Inicial:", afn.start_state)
    print("Estados de Aceitação:", afn.accept_states)


# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()
