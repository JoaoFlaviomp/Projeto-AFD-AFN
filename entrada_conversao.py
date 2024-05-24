class AFN:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states


class AFD:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states


def convert_afn_to_afd(afn):
    start_state = frozenset([afn.start_state])
    queue = [start_state]
    visited = set()
    transitions = {}
    final_states = set()

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        transitions[current] = {}

        for symbol in afn.alphabet:
            next_state = frozenset(
                state
                for substate in current
                for state in afn.transitions.get((substate, symbol), [])
            )
            transitions[current][symbol] = next_state
            if next_state not in visited and next_state not in queue:
                queue.append(next_state)

        if any(state in afn.final_states for state in current):
            final_states.add(current)

    return AFD(
        states=visited,
        alphabet=afn.alphabet,
        transitions=transitions,
        start_state=start_state,
        final_states=final_states
    )


def get_input():
    states = set(input("Digite os estados (separados por espaço): ").split())
    alphabet = set(input("Digite o alfabeto (separado por espaço): ").split())
    transitions = {}

    print("Digite as transições (no formato 'estado símbolo estado_destino', uma por linha, termine com 'fim'):")
    while True:
        trans = input().strip()
        if trans.lower() == 'fim':
            break
        state, symbol, dest = trans.split()
        if (state, symbol) in transitions:
            transitions[(state, symbol)].add(dest)
        else:
            transitions[(state, symbol)] = {dest}

    start_state = input("Digite o estado inicial: ").strip()
    final_states = set(
        input("Digite os estados de aceitação (separados por espaço): ").split())

    return AFN(states, alphabet, transitions, start_state, final_states)


def print_afn(afn):
    print("\nAFN Inserido:")
    print("Estados:", afn.states)
    print("Alfabeto:", afn.alphabet)
    print("Transições:")
    for (state, symbol), destinations in afn.transitions.items():
        for dest in destinations:
            print(f"  {state} --{symbol}--> {dest}")
    print("Estado Inicial:", afn.start_state)
    print("Estados de Aceitação:", afn.final_states)


def main():
    afn = get_input()
    print_afn(afn)
    afd = convert_afn_to_afd(afn)

    print("\nEstados do AFD:", afd.states)
    print("Alfabeto do AFD:", afd.alphabet)
    print("Transições do AFD:")
    for state, trans in afd.transitions.items():
        for symbol, next_state in trans.items():
            print(f"  {state} --{symbol}--> {next_state}")
    print("Estado inicial do AFD:", afd.start_state)
    print("Estados finais do AFD:", afd.final_states)


if __name__ == "__main__":
    main()