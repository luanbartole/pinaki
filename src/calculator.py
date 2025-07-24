# src/calculator.py

class Calculator:
    def __init__(self, recipe, price_table, config, recipe_manager):
        self.recipe = recipe
        self.price_table = price_table
        self.config = config
        self.recipe_manager = recipe_manager

    def compute(self):
        if self.recipe.category != "montagem":
            raise ValueError("Só é possível calcular custo para receitas do tipo 'montagem'.")

        total_cost = 0.0

        for layer in self.recipe.layers:
            print(f"\nCalculando camada: {layer['descricao']}")

            for component in layer["componentes"]:
                comp_name = component["nome"]
                comp_qty = component["quantidade"]
                comp_unit = component["unidade"]

                sub_recipe = self.recipe_manager.load_recipe(comp_name)
                if sub_recipe is None:
                    print(f"AVISO: Receita '{comp_name}' não encontrada, pulando.")
                    continue

                if sub_recipe.category == "montagem":
                    print(f"AVISO: Sub-receita '{comp_name}' também é montagem. Ignorando para evitar recursão.")
                    continue

                # Calcular custo base da sub-receita (massa, recheio, calda)
                sub_calc = Calculator(sub_recipe, self.price_table, self.config, self.recipe_manager)
                sub_result = sub_calc._compute_base_cost()

                custo_total_sub = sub_result["custo_total"]
                rendimento_sub = sub_recipe.servings

                proportional_cost = (comp_qty / rendimento_sub) * custo_total_sub

                print(f"  Componente '{comp_name}': {comp_qty}{comp_unit} -> custo proporcional: R$ {proportional_cost:.2f}")

                total_cost += proportional_cost

        extras = self.config.calculate_total_extra_costs(total_cost)
        labor = self.config.calculate_labor(total_cost)
        partial_cost = total_cost + extras + labor
        sale_price = self.config.calculate_profit(partial_cost)

        return {
            "custo_ingredientes": total_cost,
            "extras": extras,
            "mao_de_obra": labor,
            "custo_total": partial_cost,
            "preco_venda": sale_price,
            "por_bolo": partial_cost / self.recipe.servings,
            "lucro_unitario": sale_price - partial_cost
        }

    def _compute_base_cost(self):
        ingredient_cost = 0.0
        for ingredient in self.recipe.ingredients:
            name = ingredient["nome"]
            qty = ingredient["quantidade"]
            unit = ingredient["unidade"]

            unit_price = self.price_table.get_unit_price(name)
            if unit_price is None:
                print(f"AVISO: Preço não encontrado para ingrediente '{name}'. Pulando.")
                continue
            ingredient_cost += unit_price * qty

        # Para sub-receitas, normalmente não soma extras nem mão de obra separadamente
        total_cost = ingredient_cost
        return {
            "custo_ingredientes": ingredient_cost,
            "extras": 0,
            "mao_de_obra": 0,
            "custo_total": total_cost
        }
