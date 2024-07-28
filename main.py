import create_module
import convert_module
import minimize_module
import base_module

caracteres_especiais = "!@#$%&*()-+=<>:;^~.,][}{?/"

class SistemaPrincipal:
    def __init__(self):
        self.caracteres_especiais = caracteres_especiais

    def verificar_existencia(self):
        print("\nVerificando a existência de um NFA e/ou DFA criado...\n")
        base_module.VerificadorExistencia.verificar_existencia()

    def menu_principal(self):
        while True:
            print("Menu Principal")
            print("1. Criar e Testar")
            print("2. Converter AFN para AFD")
            print("3. Minimizar AFD")
            print("4. Sair")
            opcao = int(input("Insira uma das opções: "))
            if opcao == 1:
                criador_automato = create_module.AutomatonCreator(self.caracteres_especiais)
                criador_automato.criar_automato()
            elif opcao == 2:
                valor_conversao = convert_module.NFAtoDFAConverter()
                valor_conversao.converter_nfa_para_dfa()
            elif opcao == 3:
                minimize_module.minimiza_afd()
            elif opcao == 4:
                break

if __name__ == "__main__":
    sistema_auto_lab = SistemaPrincipal()
    sistema_auto_lab.verificar_existencia()
    sistema_auto_lab.menu_principal()