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

                # Calcular custo base e peso total da sub-receita
                sub_calc = Calculator(sub_recipe, self.price_table, self.config, self.recipe_manager)
                sub_result = sub_calc._compute_base_cost()

                total_sub_cost = sub_result["custo_total"]
                total_sub_weight = sub_result["peso_total"]
                servings = sub_recipe.servings

                if total_sub_weight is None or total_sub_weight == 0:
                    print(f"AVISO: Peso total da sub-receita '{comp_name}' inválido. Pulando.")
                    continue

                weight_per_serving = total_sub_weight / servings
                used_weight = comp_qty  # assume que a unidade é compatível com g/ml

                proportional_cost = (used_weight / total_sub_weight) * total_sub_cost

                print(
                    f"  Componente '{comp_name}': {comp_qty}{comp_unit} -> custo proporcional: R$ {proportional_cost:.2f}")

                total_cost += proportional_cost

        # Cálculos parciais com base em UMA unidade (1 bolo de pote)
        extras = self.config.calculate_total_extra_costs(total_cost)
        labor = self.config.calculate_labor(total_cost)
        profit = self.config.calculate_profit(total_cost)

        # Número de bolos gerados pela montagem
        total_servings = self.recipe.servings

        # Cálculo do custo total da receita inteira (e não só de 1 unidade)
        total_ingredients_cost = total_cost * total_servings
        total_extras = extras * total_servings
        total_labor = labor * total_servings
        total_profit = profit * total_servings

        final_total_cost = total_ingredients_cost + total_extras + total_labor
        final_sale_price = total_ingredients_cost + total_labor + total_profit + total_extras

        return {
            "custo_ingredientes": total_ingredients_cost,
            "extras": total_extras,
            "mao_de_obra": total_labor,
            "lucro": total_profit,
            "custo_total": final_total_cost,
            "lucro_unitario": total_profit / total_servings,
            "preco_venda": final_sale_price,
            "por_bolo": final_total_cost / total_servings
        }

    def _compute_base_cost(self):
        ingredient_cost = 0.0
        total_weight = 0.0

        for ingredient in self.recipe.ingredients:
            name = ingredient["nome"]
            qty = ingredient["quantidade"]
            unit = ingredient["unidade"]

            # Pular ingredientes sem preço (como água)
            if name not in self.price_table.price_data:
                continue

            # Calcular custo do ingrediente
            unit_price = self.price_table.get_unit_price(name, unit)
            if unit_price is None:
                continue

            ingredient_cost += unit_price * qty

            # Calcular peso total (convertendo unidades quando necessário)
            if unit in ["g", "ml"]:
                total_weight += qty
            elif unit == "kg":
                total_weight += qty * 1000
            elif unit == "l":
                total_weight += qty * 1000
            # Para ovos (un), usar peso médio de 50g por ovo
            elif unit == "un" and name == "ovo":
                total_weight += qty * 50  # 50g por ovo

        return {
            "custo_total": ingredient_cost,
            "peso_total": total_weight
        }
