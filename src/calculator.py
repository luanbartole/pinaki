class Calculator:
    def __init__(self, recipe, price_table, config, recipe_manager):
        self.recipe = recipe
        self.price_table = price_table
        self.config = config
        self.recipe_manager = recipe_manager

    def compute(self):
        warnings = []
        infos = []

        if self.recipe.category != "montagem":
            raise ValueError("Só é possível calcular custo para receitas do tipo 'montagem'.")

        total_cost = 0.0

        for layer in self.recipe.layers:
            infos.append(f"Calculando camada: {layer['descricao']}")

            for component in layer["componentes"]:
                comp_name = component["nome"]
                comp_qty = component["quantidade"]
                comp_unit = component["unidade"]

                sub_recipe = self.recipe_manager.load_recipe(comp_name)
                if sub_recipe is None:
                    warnings.append(f"Receita '{comp_name}' não encontrada, pulando.")
                    continue

                if sub_recipe.category == "montagem":
                    warnings.append(f"Sub-receita '{comp_name}' também é montagem. Ignorando para evitar recursão.")
                    continue

                sub_calc = Calculator(sub_recipe, self.price_table, self.config, self.recipe_manager)
                sub_result = sub_calc._compute_base_cost()

                total_sub_cost = sub_result["custo_total"]
                total_sub_weight = sub_result["peso_total"]
                servings = sub_recipe.servings

                if total_sub_weight is None or total_sub_weight == 0:
                    warnings.append(f"Peso total da sub-receita '{comp_name}' inválido. Pulando.")
                    continue

                weight_per_serving = total_sub_weight / servings
                used_weight = comp_qty  # assume unidade compatível

                proportional_cost = (used_weight / total_sub_weight) * total_sub_cost

                infos.append(
                    f"  Componente '{comp_name}': {comp_qty}{comp_unit} -> custo proporcional: R$ {proportional_cost:.2f}")

                total_cost += proportional_cost

        extras = self.config.calculate_total_extra_costs(total_cost)
        labor = self.config.calculate_labor(total_cost)
        profit = self.config.calculate_profit(total_cost)

        total_servings = self.recipe.servings

        total_ingredients_cost = total_cost * total_servings
        total_extras = extras * total_servings
        total_labor = labor * total_servings
        total_profit = profit * total_servings

        final_total_cost = total_ingredients_cost + total_extras + total_labor
        final_sale_price = total_ingredients_cost + total_labor + total_profit + total_extras

        resultado = {
            "custo_ingredientes": total_ingredients_cost,
            "extras": total_extras,
            "mao_de_obra": total_labor,
            "lucro": total_profit,
            "custo_total": final_total_cost,
            "lucro_unitario": total_profit / total_servings if total_servings else 0,
            "preco_venda": final_sale_price,
            "por_bolo": final_total_cost / total_servings if total_servings else 0
        }

        return {
            "resultado": resultado,
            "warnings": warnings,
            "infos": infos
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
                if name.lower() != "água":  # ignora avisos para 'água'
                    print(
                        f"AVISO: Ingrediente '{name}' da receita '{self.recipe.name}' não tem preço cadastrado. Ignorando.")
                continue

            # Calcular custo do ingrediente
            unit_price = self.price_table.get_unit_price(name, unit)
            if unit_price is None:
                print(
                    f"AVISO: Ingrediente '{name}' da receita '{self.recipe.name}' não tem preço para unidade '{unit}'. Ignorando.")
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
