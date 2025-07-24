import os
import json
from recipe import Recipe


class RecipeManager:
    def __init__(self, recipes_dir):
        self.recipes_dir = recipes_dir
        os.makedirs(self.recipes_dir, exist_ok=True)

    def register_recipe(self):
        print("\nCadastro de nova receita")
        name = input("Nome da receita: ").strip()
        category = input("Categoria (massa, recheio, calda, montagem): ").strip().lower()

        # Validação para rendimento (servings)
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

                    # Validação para quantidade do componente
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

                # Validação para quantidade do ingrediente
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

        self.save_recipe(recipe)
        print(f"\n✅ Receita '{name}' cadastrada com sucesso!\n")

    def save_recipe(self, recipe: Recipe):
        file_path = os.path.join(self.recipes_dir, f"{recipe.name.lower().replace(' ', '_')}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(recipe.to_dict(), f, ensure_ascii=False, indent=2)

    def load_recipe(self, recipe_name: str) -> Recipe | None:
        file_path = os.path.join(self.recipes_dir, f"{recipe_name.lower().replace(' ', '_')}.json")
        if not os.path.isfile(file_path):
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            print(f"Erro ao carregar a receita '{recipe_name}'. O arquivo está vazio ou corrompido.")
            return None
        return Recipe.from_dict(data)

    def list_recipes(self) -> list[str]:
        files = os.listdir(self.recipes_dir)
        # Remove extension and replace underscores with spaces for display
        recipes = [os.path.splitext(f)[0].replace('_',' ') for f in files if f.endswith('.json')]
        return recipes

    def edit_recipe(self, recipe_name: str):
        recipe = self.load_recipe(recipe_name)
        if recipe is None:
            print("Receita não encontrada")
            return False # Indica que não editou

        print(f"\nEditando receita: {recipe.name}")
        print("Deixe em branco para manter o valor atual.")

        new_name = input(f"\nNovo nome [{recipe.name}]: ").strip()
        if new_name:
            recipe.name = new_name

        new_servings = input(f"Novo rendimento [{recipe.servings}]: ").strip()
        if new_servings:
            try:
                recipe.servings = int(new_servings)
            except ValueError:
                print("Rendimento inválido, mantendo o valor atual.")

        while True:
            print("\nIngredientes atuais: ")
            for i, ingredient in enumerate(recipe.ingredients):
                print(f"{i+1}. {ingredient['nome']} - {ingredient['quantidade']} {ingredient['unidade']}")
            print("\nOpções:")
            print("1. Editar um ingrediente")
            print("2. Adicionar um ingrediente")
            print("3. Remover ingrediente")
            print("4. Terminar edição de ingredientes")
            option = input("Escolha uma opção: ")

            match option:
                case '1':
                    index = input("\nNúmero do ingrediente para editar: ")
                    if index.isdigit() and 1 <= int(index) <= len(recipe.ingredients):
                        ingredient = recipe.ingredients[int(index)-1]
                        ing_name = input(f"Nome [{ingredient['nome']}]: ").strip()
                        if ing_name:
                            ingredient['nome'] = ing_name
                        quantity = input(f"Quantidade [{ingredient['quantidade']}]: ").strip()
                        if quantity:
                            try:
                                ingredient['quantidade'] = float(quantity)
                            except ValueError:
                                print("Quantidade inválida, mantendo o valor atual.")
                        unit = input(f"Unidade [{ingredient['unidade']}]: ").strip()
                        if unit:
                            ingredient['unidade'] = unit
                    else:
                        print("Ingrediente inválido")

                case '2':
                    ing_name = input("\nNome do novo ingrediente: ").strip()
                    if not ing_name:
                        print("Nome Inválido.")
                        continue
                    try:
                        quantity = float(input("Quantidade: "))
                    except ValueError:
                        print("Quantidade inválida.")
                        continue
                    unit = input("Unidade: ").strip()
                    recipe.ingredients.append({
                        "nome": ing_name,
                        "quantidade": quantity,
                        "unidade": unit
                    })

                case '3':
                    index = input("\nNúmero do ingrediente para remover: ")
                    if index.isdigit() and 1 <= int(index) <= len(recipe.ingredients):
                        del recipe.ingredients[int(index)-1]
                        print("Ingrediente removido.")
                    else:
                        print("Ingrediente inválido")

                case '4':
                    break

                case _:
                    print("Opção inválida.")


        old_file = os.path.join(self.recipes_dir, f"{recipe_name.lower().replace(' ', '_')}.json")
        new_file = os.path.join(self.recipes_dir, f"{recipe.name.lower().replace(' ', '_')}.json")

        if old_file != new_file and os.path.isfile(old_file):
            os.remove(old_file)

            self.save_recipe(recipe)
            print("Receita atualizada com sucesso.")
            return True

