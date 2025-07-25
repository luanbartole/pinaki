import os
import json
from recipe import Recipe


class RecipeManager:
    def __init__(self, recipes_dir):
        self.recipes_dir = recipes_dir
        os.makedirs(self.recipes_dir, exist_ok=True)

    def register_recipe(self, recipe: Recipe):
        self.save_recipe(recipe)

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
            return None
        return Recipe.from_dict(data)

    def list_recipes(self) -> list[Recipe]:
        recipes = []
        for file in os.listdir(self.recipes_dir):
            if file.endswith(".json"):
                recipe = self.load_recipe(file[:-5])
                if recipe:
                    recipes.append(recipe)
        return recipes

    def edit_recipe_name(self, recipe: Recipe, new_name: str):
        recipe.name = new_name

    def edit_recipe_servings(self, recipe: Recipe, new_servings: int):
        recipe.servings = new_servings

    def update_ingredient(self, recipe: Recipe, index: int, nome=None, quantidade=None, unidade=None):
        ing = recipe.ingredients[index]
        if nome is not None:
            ing['nome'] = nome
        if quantidade is not None:
            ing['quantidade'] = quantidade
        if unidade is not None:
            ing['unidade'] = unidade

    def add_ingredient(self, recipe: Recipe, nome: str, quantidade: float, unidade: str):
        recipe.ingredients.append({
            "nome": nome,
            "quantidade": quantidade,
            "unidade": unidade
        })

    def remove_ingredient(self, recipe: Recipe, index: int):
        del recipe.ingredients[index]

    def delete_recipe(self, recipe_name: str):
        file_path = os.path.join(self.recipes_dir, f"{recipe_name.lower().replace(' ', '_')}.json")
        if os.path.isfile(file_path):
            os.remove(file_path)
            return True
        return False
