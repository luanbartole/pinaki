def main():
    while True:
        print("\n=== CALCULADORA DE BOLINHOS ===\n")
        print("1. Cadastrar nova receita")
        print("2. Atualizar preços de ingredientes")
        print("3. Calcular custo de uma receita")
        print("4. Configurar custos adicionais e lucro")
        print("5. Gerar relatório")
        print("6. Sair")
        choice = input("Escolha uma opção: ")

        match choice:
            case '1':
                print("Função de cadastro de receita ainda não implementada.")
            case '2':
                print("Função de atualização de preços ainda não implementada.")
            case '3':
                print("Função de cálculo de custo ainda não implementada.")
            case '4':
                print("Função de configurar custos ainda não implementada.")
            case '5':
                print("Função de gerar relatório ainda não implementada.")
            case '6':
                print("Saindo... Até a próxima!")
                break
            case _:
                print("Opção inválida! Por favor, escolha uma opção entre 1 e 6.")


if __name__ == "__main__":
    main()