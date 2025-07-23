import os
import json
from recipe import Recipe

RECIPES_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes')

class RecipeManager:
    def __init__(self, recipes_dir=RECIPES_DIR):
        self.recipes_dir = recipes_dir
        os.makedirs(self.recipes_dir, exist_ok=True)

    def save_recipe(self, recipe: Recipe):
        file_path = os.path.join(self.recipes_dir, f"{recipe.name.lower().replace(' ', '_')}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(recipe.to_dict(), f, ensure_ascii=False, indent=2)

    def load_recipe(self, recipe_name: str) -> Recipe | None:
        file_path = os.path.join(self.recipes_dir, f"{recipe_name.lower().replace(' ', '_')}.json")
        if not os.path.isfile(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Recipe.from_dict(data)

    def list_recipes(self) -> list[str]:
        files = os.listdir(self.recipes_dir)
        # Remove extension and replace underscores with spaces for display
        recipes = [os.path.splitext(f)[0].replace('_',' ') for f in files if f.endswith('.json')]
        return recipes