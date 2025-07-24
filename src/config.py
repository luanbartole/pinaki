import json

class CostConfig:
    def __init__(self, data):
        self.packaging_total = data.get("embalagem_total", 0)
        self.packaging_qty = data.get("embalagem_qtd", 1)

        self.spoon_total = data.get("colher_total", 0)
        self.spoon_qty = data.get("colher_qtd", 1)

        self.seal_total = data.get("lacre_total", 0)
        self.seal_qty = data.get("lacre_qtd", 1)

        self.expense_percent = data.get("outras_despesas_percent", 20)  # default 20%
        self.labor_percent = data.get("mao_de_obra_percent", 100)
        self.profit_percent = data.get("lucro_percent", 100)

    def packaging_unit_cost(self):
        return self.packaging_total / self.packaging_qty if self.packaging_qty else 0

    def spoon_unit_cost(self):
        return self.spoon_total / self.spoon_qty if self.spoon_qty else 0

    def seal_unit_cost(self):
        return self.seal_total / self.seal_qty if self.seal_qty else 0

    def calculate_labor(self, ingredient_cost):
        return (self.labor_percent / 100) * ingredient_cost

    def calculate_profit(self, ingredient_cost):
        return (self.profit_percent / 100) * ingredient_cost

    def calculate_variable_expenses_percent(self, ingredient_cost):
        # despesas percentuais (água, luz, etc)
        return (self.expense_percent / 100) * ingredient_cost

    def calculate_total_extra_costs(self, ingredient_cost):
        # soma custos fixos unitários + despesas percentuais
        unit_extras = (
            self.packaging_unit_cost() +
            self.spoon_unit_cost() +
            self.seal_unit_cost()
        )
        percent_expenses = self.calculate_variable_expenses_percent(ingredient_cost)
        return unit_extras + percent_expenses

    def to_dict(self):
        return {
            "embalagem_total": self.packaging_total,
            "embalagem_qtd": self.packaging_qty,
            "colher_total": self.spoon_total,
            "colher_qtd": self.spoon_qty,
            "lacre_total": self.seal_total,
            "lacre_qtd": self.seal_qty,
            "outras_despesas_percent": self.expense_percent,
            "mao_de_obra_percent": self.labor_percent,
            "lucro_percent": self.profit_percent
        }

    def update_extras(self, pack_total, pack_qty, spoon_total, spoon_qty, seal_total, seal_qty):
        self.packaging_total = pack_total
        self.packaging_qty = pack_qty
        self.spoon_total = spoon_total
        self.spoon_qty = spoon_qty
        self.seal_total = seal_total
        self.seal_qty = seal_qty

    def update_expense_percent(self, percent):
        self.expense_percent = percent

    def update_labor_percent(self, percent):
        self.labor_percent = percent

    def update_profit_percent(self, percent):
        self.profit_percent = percent

    def summary(self):
        return (
            f"Embalagem: R$ {self.packaging_total:.2f} por {self.packaging_qty} unidades "
            f"(R$ {self.packaging_unit_cost():.2f} cada)\n"
            f"Colher: R$ {self.spoon_total:.2f} por {self.spoon_qty} unidades "
            f"(R$ {self.spoon_unit_cost():.2f} cada)\n"
            f"Lacre: R$ {self.seal_total:.2f} por {self.seal_qty} unidades "
            f"(R$ {self.seal_unit_cost():.2f} cada)\n"
            f"Outras despesas: {self.expense_percent:.2f}% (água, luz, etc.)\n"
            f"Mão de obra: {self.labor_percent:.2f}%\n"
            f"Lucro desejado: {self.profit_percent:.2f}%"
        )

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return CostConfig(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return CostConfig({})
