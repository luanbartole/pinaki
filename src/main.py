from src.recipe_manager import RecipeManager
from src.recipe import Recipe
from src.price_table import IngredientPriceTable
from src.config import CostConfig
import os

manager = RecipeManager()
price_table = IngredientPriceTable({})  # Você pode depois carregar de um JSON
config = CostConfig({})

def menu_recipes():
    while True:
        print("\n=== MENU RECEITAS ===\n")
        print("1. Cadastrar nova receita")
        print("2. Editar receita")
        print("3. Excluir receita")
        print("4. Listar receitas")
        print("5. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        match escolha:
            case '1':
                name = input("\nNome da receita: ")
                servings = int(input("Rendimento (quantos bolos): "))
                ingredients = []
                print("Adicione os ingredientes (deixe o nome vazio para encerrar): ")
                while True:
                    nome = input("Nome do Ingrediente: ")
                    if not nome:
                        break
                    quantidade = float(input("Quantidade: "))
                    unidade = input("Unidade (ex: g, ml): ")
                    ingredients.append({
                        "nome": nome,
                        "quantidade": quantidade,
                        "unidade": unidade
                    })
                recipe = Recipe(name, servings, ingredients)
                manager.save_recipe(recipe)
                print("Receita salva com sucesso.")

            case '2':
                name = input("Nome da receita a editar: ")
                manager.edit_recipe(name)

            case '3':
                nome = input("Nome da receita a excluir: ")
                file_path = os.path.join(manager.recipes_dir, f"{nome.lower().replace(' ', '_')}.json")
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print("Receita excluída com sucesso.")
                else:
                    print("Receita não encontrada.")

            case '4':
                receitas = manager.list_recipes()
                if not receitas:
                    print("Nenhuma receita cadastrada.")
                else:
                    print("Receitas cadastradas:")
                    for r in receitas:
                        print(f" - {r}")
            case '5':
                break

            case _:
                print("Opção inválida! Tente novamente.")

def menu_prices():
    while True:
        print("\n=== MENU PREÇOS DE INGREDIENTES ===\n")
        print("1. Atualizar preço de ingrediente")
        print("2. Listar preços de ingredientes")
        print("3. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        match escolha:
            case '1':
                print("Função atualizar preço ainda não implementada.")
            case '2':
                print("Função listar preços ainda não implementada.")
            case '3':
                break
            case _:
                print("Opção inválida! Tente novamente.")

def menu_costs():
    while True:
        print("\n=== MENU CUSTOS E LUCRO ===\n")
        print("1. Configurar custos adicionais")
        print("2. Configurar lucro desejado")
        print("3. Voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        match escolha:
            case '1':
                print("Função configurar custos adicionais ainda não implementada.")
            case '2':
                print("Função configurar lucro ainda não implementada.")
            case '3':
                break
            case _:
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

        match choice:
            case '1':
                menu_recipes()
            case '2':
                menu_prices()
            case '3':
                print("Função calcular custo ainda não implementada.")  # ou menu_calculo()
            case '4':
                menu_costs()
            case '5':
                print("Função gerar relatório ainda não implementada.")
            case '6':
                print("Saindo... Até a próxima!")
                break
            case _:
                print("Opção inválida! Por favor, escolha uma opção entre 1 e 6.")

if __name__ == "__main__":
    main()
