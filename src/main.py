from src.recipe_manager import RecipeManager
from src.recipe import Recipe
from src.price_table import IngredientPriceTable
from src.config import CostConfig
import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES_DIR = os.path.join(BASE_DIR, "data", "recipes")
PRICES_FILE = os.path.join(BASE_DIR, "data", "ingredients.json")

manager = RecipeManager(recipes_dir=RECIPES_DIR)
price_table = IngredientPriceTable(file_path=PRICES_FILE)  # Você pode depois carregar de um JSON
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

def menu_prices(last_purchase_date):
    while True:
        print("\n=== MENU PREÇOS DE INGREDIENTES ===\n")
        print("1. Adicionar ou atualizar preço de ingrediente")
        print("2. Excluir preço de ingrediente")
        print("3. Listar preços de ingredientes")
        print("4. Voltar ao menu principal")
        choice = input("Escolha uma opção: ")

        match choice:
            case '1':
                name = input("\nNome do ingrediente: ").strip().lower()
                price_str = input("Preço total da embalagem (R$): ").strip().replace(',', '.')
                quantity_str = input("Quantidade da embalagem: ").strip()
                unit = input("Unidade da embalagem (ex: g, ml): ").strip()
                purchase_date = input("Data da compra (YYYY-MM-DD) [Enter para usar a última data]: ").strip()

                if not purchase_date:
                    if last_purchase_date is None:
                        print("Você deve informar a data da compra ao menos uma vez.")
                        continue
                    else:
                        purchase_date = last_purchase_date
                else:
                    try:
                        datetime.datetime.strptime(purchase_date, "%Y-%m-%d")
                        last_purchase_date = purchase_date
                    except ValueError:
                        print("Formato de data inválido. Use YYYY-MM-DD.")
                        continue

                try:
                    price = float(price_str)
                    quantity = float(quantity_str)
                    price_table.update_ingredient(name, price, quantity, unit, purchase_date)
                    price_table.save()
                    print(f"Ingrediente '{name}' atualizado com sucesso.")
                    break
                except ValueError:
                    print("Preço ou quantidade inválidos. Tente novamente.")

            case '2':
                name = input("\nNome do ingrediente a excluir: ").strip().lower()
                if name in price_table.price_data:
                    price_table.remove_ingredient(name)
                    price_table.save()
                    print(f"Ingrediente '{name}' removido com sucesso.")
                else:
                    print("Ingrediente não encontrado.")

            case '3':
                if not price_table.price_data:
                    print("\nNenhum preço cadastrado.")
                else:
                    print("\nPreços cadastrados:")
                    for name in sorted(price_table.price_data):
                        info = price_table.price_data[name]
                        purchase_date = info.get('purchase_date', 'Data não informada')
                        print(
                            f"- {name}: R$ {info['preco']} por {info['quantidade']} {info['unidade']} ({purchase_date})")

            case '4':
                break

            case _:
                print("Opção inválida! Tente novamente.")
    return last_purchase_date

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
    last_purchase_date = None

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
                last_purchase_date = menu_prices(last_purchase_date)
            case '3':
                print("Função calcular custo ainda não implementada.")
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