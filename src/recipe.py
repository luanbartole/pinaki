class Recipe:
    def __init__(self, name, servings, ingredients=None, category="general", layers=None):
        self.name = name
        self.servings = servings
        self.category = category  # massa, recheio, calda, montagem -> translated as mass, filling, syrup, assembly or general
        self.ingredients = ingredients or []
        self.layers = layers or []

    def to_dict(self):
        base = {
            "name": self.name,
            "servings": self.servings,
            "category": self.category
        }
        if self.category == "montagem":
            base["layers"] = self.layers
        else:
            base["ingredients"] = self.ingredients
        return base

    @staticmethod
    def from_dict(data):
        return Recipe(
            name=data["name"],
            servings=data["servings"],
            category=data.get("category", "general"),
            ingredients=data.get("ingredients", []),
            layers=data.get("layers", [])
        )
