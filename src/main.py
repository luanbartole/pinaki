def menu_receitas():
    while True:
        print("\n=== MENU RECEITAS ===\n")
        print("1. Cadastrar nova receita")
        print("2. Editar receita")
        print("3. Excluir receita")
        print("4. Listar receitas")
        print("5. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            print("Função cadastrar receita ainda não implementada.")
        elif escolha == '2':
            print("Função editar receita ainda não implementada.")
        elif escolha == '3':
            print("Função excluir receita ainda não implementada.")
        elif escolha == '4':
            print("Função listar receitas ainda não implementada.")
        elif escolha == '5':
            break
        else:
            print("Opção inválida! Tente novamente.")


def menu_precos():
    while True:
        print("\n=== MENU PREÇOS DE INGREDIENTES ===\n")
        print("1. Atualizar preço de ingrediente")
        print("2. Listar preços de ingredientes")
        print("3. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            print("Função atualizar preço ainda não implementada.")
        elif escolha == '2':
            print("Função listar preços ainda não implementada.")
        elif escolha == '3':
            break
        else:
            print("Opção inválida! Tente novamente.")


def menu_custos():
    while True:
        print("\n=== MENU CUSTOS E LUCRO ===\n")
        print("1. Configurar custos adicionais")
        print("2. Configurar lucro desejado")
        print("3. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            print("Função configurar custos adicionais ainda não implementada.")
        elif escolha == '2':
            print("Função configurar lucro ainda não implementada.")
        elif escolha == '3':
            break
        else:
            print("Opção inválida! Tente novamente.")


def main():
    while True:
        print("\n=== CALCULADORA DE BOLINHOS ===\n")
        print("1. Receitas")
        print("2. Preços de Ingredientes")
        print("3. Calcular custo de uma receita")
        print("4. Custos adicionais e lucro")
        print("5. Gerar relatório")
        print("6. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            menu_receitas()
        elif choice == '2':
            menu_precos()
        elif choice == '3':
            menu_custos()
        elif choice == '4':
            menu_custos()
        elif choice == '5':
            print("Função gerar relatório ainda não implementada.")
        elif choice == '6':
            print("Saindo... Até a próxima!")
            break
        else:
            print("Opção inválida! Por favor, escolha uma opção entre 1 e 6.")


if __name__ == "__main__":
    main()
