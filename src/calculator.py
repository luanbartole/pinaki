class Calculator:
    def __init__(self, recipe, price_table, config):
        self.recipe = recipe
        self.price_table = price_table
        self.config = config

    def compute(self):
        ingredient_total = 0
        breakdown = []

        for item in self.recipe.ingredients:
            price_info = self.price_table.price_data.get(item["nome"])
            if not price_info:
                continue # or raise error

            if item["unidade"] != price_info["unidade"]:
                continue # you may add conversion logic

            unit_price = price_info["preco"] / price_info["quantidade"]
            cost = item["quantidade"] * unit_price
            ingredient_total += cost

            breakdown.append({
                "nome": item["nome"],
                "quantidade": item["quantidade"],
                "unidade": item["unidade"],
                "unit_price": unit_price,
                "cost": cost
            })

        extras = self.config.packaging + self.config.spoon + self.config.expenses
        labor = self.config.calculate_labor(ingredient_total)
        total_cost = ingredient_total + extras + labor
        cost_per_unit = total_cost / self.recipe.servings
        price_per_unit = cost_per_unit * (1 + self.config.profit_percent / 100)
        profit_per_unit = price_per_unit - cost_per_unit

        return {
            "ingredientes": breakdown,
            "custo_ingredientes": ingredient_total,
            "extras": extras,
            "mao_de_obra": labor,
            "custo_total": total_cost,
            "por_bolo": cost_per_unit,
            "preco_venda": price_per_unit,
            "lucro_unitario": profit_per_unit
        }