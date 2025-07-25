from src.recipe_manager import RecipeManager
from src.recipe import Recipe
from src.price_table import IngredientPriceTable
from src.config import CostConfig
from src.calculator import Calculator
from src.ui import RichUI
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
ui = RichUI()

def register_recipe_flow(manager: RecipeManager, ui: RichUI):
    print("\nCadastro de nova receita")
    name = input("Nome da receita: ").strip()
    category = input("Categoria (massa, recheio, calda, montagem): ").strip().lower()

    while True:
        try:
            servings = int(input("Rendimento (quantos bolos): "))
            break
        except ValueError:
            print("Por favor, digite um número inteiro válido para o rendimento.")

    if category == "montagem":
        layers = []
        while True:
            description = input("\nDescrição da camada (ex: Base, Topo, Finalização): ").strip()
            components = []
            while True:
                comp_name = input(" - Nome do componente (ou ENTER para terminar a camada): ").strip()
                if not comp_name:
                    break

                while True:
                    try:
                        quantity = float(input("   Quantidade usada (ex: 25): "))
                        break
                    except ValueError:
                        print("Por favor, digite um número válido para a quantidade.")

                unit = input("   Unidade (g/ml): ").strip()
                components.append({
                    "nome": comp_name,
                    "quantidade": quantity,
                    "unidade": unit
                })
            layers.append({
                "descricao": description,
                "componentes": components
            })
            more = input("Adicionar outra camada? (s/n): ").strip().lower()
            if more != "s":
                break
        recipe = Recipe(name, servings, category=category, layers=layers)
    else:
        ingredients = []
        while True:
            ingredient_name = input(" - Nome do ingrediente (ou ENTER para terminar): ").strip()
            if not ingredient_name:
                break

            while True:
                try:
                    quantity = float(input("   Quantidade usada (ex: 100): "))
                    break
                except ValueError:
                    print("Por favor, digite um número válido para a quantidade.")

            unit = input("   Unidade (g/ml): ").strip()
            ingredients.append({
                "nome": ingredient_name,
                "quantidade": quantity,
                "unidade": unit
            })
        recipe = Recipe(name, servings, category=category, ingredients=ingredients)

    manager.register_recipe(recipe)
    print(f"\n✅ Receita '{name}' cadastrada com sucesso!\n")

def recipes_menu():
    while True:
        ui.print_menu("MENU RECEITAS", {
            "1": "Cadastrar nova receita",
            "2": "Editar receita",
            "3": "Excluir receita",
            "4": "Listar receitas",
            "5": "Voltar ao menu principal"
        })
        escolha = input("Escolha uma opção: ")

        match escolha:
            case '1':
                register_recipe_flow(manager, ui)
            case '2':
                edit_recipe_flow(manager, ui)
            case '3':
                nome = input("Nome da receita a excluir: ")
                success = manager.delete_recipe(nome)
                if success:
                    print("Receita excluída com sucesso.")
                else:
                    print("Receita não encontrada.")
            case '4':
                recipes = manager.list_recipes()
                if not recipes:
                    ui.print_warning("Nenhuma receita encontrada.")
                else:
                    ui.print_all_recipes_table(recipes)
            case '5':
                break
            case _:
                print("Opção inválida! Tente novamente.")

def edit_recipe_flow(manager: RecipeManager, ui: RichUI):
    name = input("Nome da receita a editar: ")
    recipe = manager.load_recipe(name)
    if recipe is None:
        ui.print_warning("Receita não encontrada")
        return

    # Mostra a tabela dos ingredientes
    new_name = input(f"Novo nome [{recipe.name}]: ").strip()
    if new_name:
        manager.edit_recipe_name(recipe, new_name)

    new_servings = input(f"Novo rendimento [{recipe.servings}]: ").strip()
    if new_servings:
        try:
            manager.edit_recipe_servings(recipe, int(new_servings))
        except ValueError:
            print("Rendimento inválido, mantendo o valor atual.")

    while True:
        ui.print_recipe_ingredients_numbered(recipe)
        print("\n1. Editar um ingrediente")
        print("2. Adicionar um ingrediente")
        print("3. Remover ingrediente")
        print("4. Terminar edição de ingredientes")
        option = input("Escolha uma opção: ")

        if option == '1':
            index = input("Número do ingrediente para editar: ")
            if index.isdigit() and 1 <= int(index) <= len(recipe.ingredients):
                ing = recipe.ingredients[int(index) - 1]
                nome = input(f"Nome [{ing['nome']}]: ").strip() or None
                quantidade_str = input(f"Quantidade [{ing['quantidade']}]: ").strip()
                quantidade = float(quantidade_str) if quantidade_str else None
                unidade = input(f"Unidade [{ing['unidade']}]: ").strip() or None
                manager.update_ingredient(recipe, int(index) - 1, nome, quantidade, unidade)
            else:
                print("Ingrediente inválido")

        elif option == '2':
            nome = input("Nome do novo ingrediente: ").strip()
            if not nome:
                print("Nome inválido.")
                continue
            try:
                quantidade = float(input("Quantidade: "))
            except ValueError:
                print("Quantidade inválida.")
                continue
            unidade = input("Unidade: ").strip()
            manager.add_ingredient(recipe, nome, quantidade, unidade)

        elif option == '3':
            index = input("Número do ingrediente para remover: ")
            if index.isdigit() and 1 <= int(index) <= len(recipe.ingredients):
                manager.remove_ingredient(recipe, int(index) - 1)
                print("Ingrediente removido.")
            else:
                print("Ingrediente inválido")

        elif option == '4':
            break
        else:
            print("Opção inválida.")

    # Salvar a receita editada
    manager.save_recipe(recipe)
    print("Receita atualizada com sucesso.")



def ingredient_prices_menu(last_purchase_date):
    while True:
        ui.print_menu("MENU PREÇOS DE INGREDIENTES", {
            "1": "Adicionar ou atualizar preço de ingrediente",
            "2": "Excluir preço de ingrediente",
            "3": "Listar preços de ingredientes",
            "4": "Voltar ao menu principal"
        })
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
                    ui.print_ingredient_prices_table(price_table.price_data)
            case '4':
                break

            case _:
                print("Opção inválida! Tente novamente.")
    return last_purchase_date

def cost_config_menu():
    while True:
        ui.print_menu("MENU CUSTOS E LUCRO", {
            "1": "Configurar custos adicionais (embalagem, colher, lacre)",
            "2": "Configurar outras despesas (água, luz)",
            "3": "Configurar percentual de mão de obra",
            "4": "Configurar percentual de lucro",
            "5": "Ver configurações atuais",
            "6": "Voltar ao menu principal"
        })

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
                ui.print_cost_config_table(config)

            case '6':
                break


            case _:
                print("Opção inválida! Tente novamente.")

def calculate_recipe_cost():
    montagem_recipes = [r for r in manager.list_recipes() if r.category == "montagem"]

    if not montagem_recipes:
        ui.print_warning("Nenhuma receita com categoria 'montagem' foi encontrada.")
        return

    ui.print_all_recipes_table(montagem_recipes)

    choice = input("Escolha o número da receita para calcular o custo: ").strip()
    print()
    if not choice.isdigit() or not (1 <= int(choice) <= len(montagem_recipes)):
        ui.print_error("Opção inválida.")
        return

    selected_recipe = montagem_recipes[int(choice) - 1]
    recipe = manager.load_recipe(selected_recipe.name)

    if not recipe:
        ui.print_error("Erro ao carregar a receita.")
        return

    calculator = Calculator(recipe, price_table, config, manager)
    compute_result = calculator.compute()

    patterns_colors = {
        "Calculando camada:": "blue",
        "Componente": "blue"
    }
    prefix_map = {
        "Calculando camada:": "✅",
        "Componente": "→"
    }

    ui.print_colored_lines(compute_result.get("infos", []), patterns_colors, prefix_map)

    for warning_msg in compute_result.get("warnings", []):
        ui.print_warning(warning_msg)

    resultado = compute_result["resultado"]

    # Adiciona servings ao resultado para usar na UI
    resultado['servings'] = recipe.servings

    print(f"\n=== CUSTO DA RECEITA DE MONTAGEM: {recipe.name} ===")
    print(f"Rendimento: {recipe.servings}\n")

    # Imprime tabelas total e unidade
    ui.print_production_profit_tables(resultado, config)




def main():
    last_purchase_date = None

    while True:
        ui.print_menu("CALCULADORA DE BOLINHOS", {
            "1": "Receitas",
            "2": "Preços de Ingredientes",
            "3": "Calcular custo de uma receita",
            "4": "Custos adicionais e lucro",
            "5": "Gerar relatório",
            "6": "Sair"
        })
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