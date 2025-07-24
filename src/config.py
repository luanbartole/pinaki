class CostConfig:
    def __init__(self, data):
        self.packaging = data.get("embalagem", 0)
        self.spoon = data.get("colher", 0)
        self.expenses = data.get("outras_despesas", 0)
        self.labor_percent = data.get("mao_de_obra_percent", 0)
        self.profit_percent = data.get("lucro_percent", 0)

    def calculate_labor(self, ingredient_cost):
        return (self.labor_percent / 100) * ingredient_cost

    def to_dict(self):
        return {
            "embalagem": self.packaging,
            "colher": self.spoon,
            "outras_despesas": self.expenses,
            "mao_de_obra_percent": self.labor_percent,
            "lucro_percent": self.profit_percent
        }