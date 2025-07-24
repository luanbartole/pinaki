from src.recipe_manager import RecipeManager
from src.recipe import Recipe
from src.price_table import IngredientPriceTable
from src.config import CostConfig
from src.calculator import Calculator
import datetime
import os
from collections import defaultdict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES_DIR = os.path.join(BASE_DIR, "data", "recipes")
PRICES_FILE = os.path.join(BASE_DIR, "data", "ingredients.json")
CONFIG_FILE = os.path.join(BASE_DIR, "data", "config.json")

manager = RecipeManager(recipes_dir=RECIPES_DIR)
price_table = IngredientPriceTable(file_path=PRICES_FILE)
config = CostConfig.load(CONFIG_FILE)


def recipes_menu():
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
                manager.register_recipe()  # Call your new function here
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
                recipes = manager.list_recipes()
                if not recipes:
                    print("Nenhuma receita encontrada.")
                else:
                    print("\nReceitas cadastradas:")

                    # Agrupar por categoria
                    categorized = defaultdict(list)
                    for r in recipes:
                        category = getattr(r, "category", "sem categoria")
                        categorized[category].append(r.name)

                    # Imprimir por categoria
                    for category, names in categorized.items():
                        print(f"[{category.upper()}]")
                        for name in names:
                            print(f" - {name}")

            case '5':
                break
            case _:
                print("Opção inválida! Tente novamente.")


def ingredient_prices_menu(last_purchase_date):
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

def cost_config_menu():
    while True:
        print("\n=== MENU CUSTOS E LUCRO ===\n")
        print("1. Configurar custos adicionais (embalagem, colher, lacre)")
        print("2. Configurar outras despesas (água, luz)")
        print("3. Configurar percentual de mão de obra")
        print("4. Configurar percentual de lucro")
        print("5. Ver configurações atuais")
        print("6. Voltar ao menu principal")

        choice = input("Escolha uma opção: ")

        match choice:
            case '1':
                try:
                    pack_total_str = input("\nPreço total das embalagens (R$) [Enter para manter atual]: ").replace(",",
                                                                                                                    ".")
                    pack_qty_str = input("Quantidade de embalagens compradas [Enter para manter atual]: ")

                    spoon_total_str = input("\nPreço total das colheres (R$) [Enter para manter atual]: ").replace(",",
                                                                                                                   ".")
                    spoon_qty_str = input("Quantidade de colheres compradas [Enter para manter atual]: ")

                    seal_total_str = input("\nPreço total dos lacres (R$) [Enter para manter atual]: ").replace(",",
                                                                                                                ".")
                    seal_qty_str = input("Quantidade de lacres comprados [Enter para manter atual]: ")

                    pack_total = float(pack_total_str) if pack_total_str else config.packaging_total
                    pack_qty = int(pack_qty_str) if pack_qty_str else config.packaging_qty

                    spoon_total = float(spoon_total_str) if spoon_total_str else config.spoon_total
                    spoon_qty = int(spoon_qty_str) if spoon_qty_str else config.spoon_qty

                    seal_total = float(seal_total_str) if seal_total_str else config.seal_total
                    seal_qty = int(seal_qty_str) if seal_qty_str else config.seal_qty

                    config.update_extras(pack_total, pack_qty, spoon_total, spoon_qty, seal_total, seal_qty)
                    config.save(CONFIG_FILE)
                    print("Custos atualizados com sucesso.")
                except ValueError:
                    print("Valores inválidos. Use números.")

            case '2':
                try:
                    expense_percent = float(
                        input("\nPercentual de outras despesas (água, luz, etc.) [%] (padrão: 20): ").replace(",", "."))
                    config.update_expense_percent(expense_percent)
                    config.save(CONFIG_FILE)
                    print("Outras despesas atualizadas com sucesso.")
                except ValueError:
                    print("Valor inválido.")

            case '3':
                try:
                    labor_percent = float(input("\nPercentual de mão de obra (%): ").replace(",", "."))
                    config.update_labor_percent(labor_percent)
                    config.save(CONFIG_FILE)
                    print("Percentual de mão de obra atualizado com sucesso.")
                except ValueError:
                    print("Valor inválido. Use um número.")

            case '4':
                try:
                    profit_percent = float(input("\nPercentual de lucro desejado (%): ").replace(",", "."))
                    config.update_profit_percent(profit_percent)
                    config.save(CONFIG_FILE)
                    print("Percentual de lucro atualizado com sucesso.")
                except ValueError:
                    print("Valor inválido. Use um número.")

            case '5':
                print("\n=== CONFIGURAÇÔES ATUAIS ===")
                print(config.summary())

            case '6':
                break


            case _:
                print("Opção inválida! Tente novamente.")

def calculate_recipe_cost():
    recipes = sorted([
        r.name for r in manager.list_recipes()
        if r.category == "montagem"
    ])

    if not recipes:
        print("\n⚠️ Nenhuma receita com categoria 'montagem' foi encontrada.")
        return  # or loop/exit back to menu

    print("\nReceitas disponíveis:")
    for i, recipe_name in enumerate(recipes, 1):
        print(f"{i}. {recipe_name}")

    choice = input("Escolha o número da receita para calcular o custo: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(recipes)):
        print("Opção inválida.")
        return

    selected_recipe_name = recipes[int(choice) - 1]
    recipe = manager.load_recipe(selected_recipe_name)

    if not recipe:
        print("Erro ao carregar a receita.")
        return

    if recipe.category != "montagem":
        print("Só é possível calcular o custo de receitas do tipo 'montagem'.")
        return

    calculator = Calculator(recipe, price_table, config, manager)
    result = calculator.compute()

    servings = recipe.servings

    unit_fixed_costs = (
        config.packaging_unit_cost() +
        config.spoon_unit_cost() +
        config.seal_unit_cost()
    )

    total_variable_expenses = config.calculate_variable_expenses_percent(result['custo_ingredientes'])

    # Aqui pega os percentuais diretamente do config para exibir
    expense_pct = config.expense_percent
    labor_pct = config.labor_percent
    profit_pct = config.profit_percent

    print(f"\n=== CUSTO DA RECEITA DE MONTAGEM: {recipe.name} ===")
    print(f"Rendimento: {servings}\n")

    print("Produção e Lucro (Total):")
    print(f"- Custo total dos ingredientes: R$ {result['custo_ingredientes']:.2f}")
    print(f"- Custos fixos unitários x rendimento: R$ {unit_fixed_costs * servings:.2f}")
    print(f"- Outras despesas ({expense_pct:.0f}% sobre ingredientes): R$ {total_variable_expenses:.2f}")
    print(f"- Mão de obra ({labor_pct:.0f}% sobre ingredientes): R$ {result['mao_de_obra']:.2f}")
    print(f"- Custo total (ingredientes + extras + mão): R$ {result['custo_total']:.2f}")
    print(f"- Lucro total estimado ({profit_pct:.0f}%): R$ {result['lucro']:.2f}")
    print(f"- Preço de venda sugerido: R$ {result['preco_venda']:.2f}")

    print("\nProdução e Lucro (Unidade):")
    print(f"- Custos fixos unitários (embalagem, colher, lacre): R$ {unit_fixed_costs:.2f}")
    print(f"- Outras despesas ({expense_pct:.0f}% sobre ingredientes): R$ {(total_variable_expenses / servings):.2f}")
    print(f"- Mão de obra ({labor_pct:.0f}% sobre ingredientes): R$ {(result['mao_de_obra'] / servings):.2f}")
    print(f"- Custo por bolo (unidade): R$ {result['por_bolo']:.2f}")
    print(f"- Lucro unitário estimado ({profit_pct:.0f}% sobre ingredientes): R$ {result['lucro_unitario']:.2f}")
    print(f"- Preço de venda sugerido (unidade): R$ {result['preco_venda'] / servings:.2f}")

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
                recipes_menu()
            case '2':
                last_purchase_date = ingredient_prices_menu(last_purchase_date)
            case '3':
                calculate_recipe_cost()
            case '4':
                cost_config_menu()
            case '5':
                print("Função gerar relatório ainda não implementada.")
            case '6':
                print("Saindo... Até a próxima!")
                break
            case _:
                print("Opção inválida! Por favor, escolha uma opção entre 1 e 6.")


if __name__ == "__main__":
    main()