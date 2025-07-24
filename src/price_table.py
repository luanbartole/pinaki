class IngredientPriceTable:
    def __init__(self, price_data):
        self.price_data = price_data

    def get_unit_price(self, name):
        item = self.price_data.get(name)
        if not item:
            return None
        return item["preco"] / item["quantidade"]

    def update_ingrediente(self, name, preco=None, quantidade=None, unidade=None):
        if name in self.price_data:
            if preco: self.price_data[name]["preco"] = preco
            if quantidade: self.price_data[name]["quantidade"] = quantidade
            if unidade: self.price_data[name]["unidade"] = unidade

    def to_dict(self):
        return self.price_data