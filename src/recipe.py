class Recipe:
    def __init__(self, name, servings, ingredients):
        self.name = name
        self.servings = servings
        self.ingredients = ingredients # list of dicts with name, quantity, unit

    def to_dict(self):
        return {
            "nome": self.name,
            "rendimento_bolos": self.servings,
            "ingredientes": self.ingredients
        }

    @staticmethod
    def from_dict(data):
        return Recipe(
            name=data["nome"],
            servings=data["rendimento_bolos"],
            ingredients=data["ingredientes"]
        )
