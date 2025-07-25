from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text
import os

class RichUI:
    def __init__(self):
        self.console = Console()

    @staticmethod
    def clear_screen():
        print("\n" * 3)

    def print_title(self, title):
        self.console.print(f"\n[bold blue]{title}[/bold blue]")

    def print_warning(self, msg):
        self.console.print(f"[bold yellow]⚠️ {msg}[/bold yellow]")

    def print_success(self, msg):
        self.console.print(f"[bold green]✅ {msg}[/bold green]")

    def print_error(self, msg):
        self.console.print(f"[bold red]❌ {msg}[/bold red]")

    def print_panel(self, title, content, style="cyan"):
        panel = Panel(content, title=title, style=style)
        self.console.print(panel)

    def print_menu(self, title, options: dict[str, str]):
        print()
        table = Table(title=f"[bold cyan]{title}[/bold cyan]", box=box.DOUBLE)
        table.add_column("Opção", style="bold white", justify="center")
        table.add_column("Descrição", style="green")
        for key, desc in options.items():
            table.add_row(f"[bold yellow]{key}[/bold yellow]", desc)
        self.console.print(table)

    def print_all_recipes_table(self, recipe_list):
        self.clear_screen()  # limpa a tela antes de imprimir
        table = Table(title="[bold magenta]Receitas Cadastradas[/bold magenta]", box=box.ROUNDED)
        table.add_column("Nº", justify="right", style="bold white")
        table.add_column("Nome da Receita", style="cyan", no_wrap=False)
        table.add_column("Categoria", style="green", no_wrap=True)

        for idx, recipe in enumerate(recipe_list, start=1):
            table.add_row(str(idx), recipe.name, recipe.category.capitalize())

        self.console.print(table)

    def print_recipe_ingredients(self, recipe):
        table = Table(title=f"[bold green]Ingredientes de {recipe.name}[/bold green]", box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column("Ingrediente", style="cyan")
        table.add_column("Quantidade", justify="right")
        table.add_column("Unidade", justify="center")

        for ing in recipe.ingredients:
            table.add_row(ing["nome"], str(ing["quantidade"]), ing["unidade"])

        self.console.print(table)

    def print_recipe_ingredients_numbered(self, recipe):
        self.clear_screen()
        table = Table(title=f"Ingredientes da receita: [bold green]{recipe.name}[/bold green]", box=box.SIMPLE_HEAVY)
        table.add_column("Nº", style="bold yellow", justify="right", width=4)
        table.add_column("Nome", style="cyan")
        table.add_column("Quantidade", justify="right")
        table.add_column("Unidade", justify="center")

        for i, ing in enumerate(recipe.ingredients, start=1):
            table.add_row(str(i), ing["nome"], str(ing["quantidade"]), ing["unidade"])

        self.console.print(table)

    def print_layers(self, recipe):
        if not hasattr(recipe, "layers"):
            self.print_warning("Esta receita não possui camadas.")
            return

        for layer in recipe.layers:
            table = Table(title=f"[bold yellow]{layer['descricao']}[/bold yellow]", box=box.SIMPLE_HEAVY)
            table.add_column("Componente")
            table.add_column("Quantidade", justify="right")
            table.add_column("Unidade", justify="center")

            for comp in layer["componentes"]:
                table.add_row(comp["nome"], str(comp["quantidade"]), comp["unidade"])

            self.console.print(table)

    def print_ingredient_prices_table(self, price_data: dict):
        """
        Imprime uma tabela formatada com os preços dos ingredientes.
        price_data: dicionário onde a chave é o nome do ingrediente e o valor é outro dict com 'preco', 'quantidade', 'unidade' e 'purchase_date'
        """
        self.clear_screen()
        table = Table(title="[bold magenta]Preços dos Ingredientes[/bold magenta]", box=box.ROUNDED)
        table.add_column("Ingrediente", style="cyan", no_wrap=True, width=30)
        table.add_column("Preço", justify="right")
        table.add_column("Quant.", justify="right")
        table.add_column("Unid.", justify="center")
        table.add_column("Data", justify="center", no_wrap=True, width=12)

        for nome, info in sorted(price_data.items()):
            preco = f"{info.get('preco', 'N/A'):.2f}" if isinstance(info.get('preco'), (int, float)) else "N/A"
            quantidade = f"{info.get('quantidade', 'N/A'):.15g}"
            unidade = info.get('unidade', 'N/A')
            data = info.get('purchase_date', 'N/A')
            table.add_row(nome, preco, quantidade, unidade, data)

        self.console.print(table)

    def print_cost_config_table(self, config):
        self.clear_screen()

        # Tabela 1: Custos Unitários
        table_units = Table(title="[bold magenta]Configurações de Custos Unitários[/bold magenta]",
                            box=box.ROUNDED)
        table_units.add_column("Item", style="cyan", no_wrap=True)
        table_units.add_column("Total (R$)", justify="right")
        table_units.add_column("Quantidade", justify="right")
        table_units.add_column("Custo Unitário (R$)", justify="right")

        table_units.add_row(
            "Embalagem",
            f"{config.packaging_total:.2f}",
            f"{config.packaging_qty}",
            f"{config.packaging_unit_cost():.2f}"
        )
        table_units.add_row(
            "Colher",
            f"{config.spoon_total:.2f}",
            f"{config.spoon_qty}",
            f"{config.spoon_unit_cost():.2f}"
        )
        table_units.add_row(
            "Lacre",
            f"{config.seal_total:.2f}",
            f"{config.seal_qty}",
            f"{config.seal_unit_cost():.2f}"
        )

        # Tabela 2: Percentuais
        table_percent = Table(title="[bold magenta]Configurações de Percentuais[/bold magenta]", box=box.SQUARE)
        table_percent.add_column("Tipo", style="cyan")
        table_percent.add_column("Percentual (%)", justify="right")

        table_percent.add_row("Outras despesas (água, luz, etc.)", f"{config.expense_percent:.2f}")
        table_percent.add_row("Mão de obra", f"{config.labor_percent:.2f}")
        table_percent.add_row("Lucro desejado", f"{config.profit_percent:.2f}")

        self.console.print(table_units)
        print()  # linha em branco para separar
        self.console.print(table_percent)

    def print_production_profit_tables(self, result, config):
        servings = result.get("servings", 1)

        unit_fixed_costs = (
            config.packaging_unit_cost() +
            config.spoon_unit_cost() +
            config.seal_unit_cost()
        )
        unit_fixed_costs_total = unit_fixed_costs * servings

        total_variable_expenses = config.calculate_variable_expenses_percent(result['custo_ingredientes'])
        total_variable_expenses_unit = total_variable_expenses / servings if servings else 0

        expense_pct = config.expense_percent
        labor_pct = config.labor_percent
        profit_pct = config.profit_percent

        table_total = Table(title="[bold magenta]Produção e Lucro (Total)[/bold magenta]", box=box.SQUARE)
        table_total.add_column("Item", style="cyan")
        table_total.add_column("Valor (R$)", justify="right")

        table_total.add_row("Ingredientes", f"{result['custo_ingredientes']:.2f}")
        table_total.add_row("Insumos e embalagens (embalagem, colher, lacre)", f"{unit_fixed_costs_total:.2f}")
        table_total.add_row(f"Outras despesas ({expense_pct:.0f}% sobre ingredientes)", f"{total_variable_expenses:.2f}")
        table_total.add_row(f"Mão de obra ({labor_pct:.0f}% sobre ingredientes)", f"{result['mao_de_obra']:.2f}")
        table_total.add_row("Custo de Produção", f"{result['custo_total']:.2f}")
        table_total.add_row(f"Lucro ({profit_pct:.0f}% sobre ingredientes)", f"{result['lucro']:.2f}")
        table_total.add_row("Preço de venda sugerido", f"{result['preco_venda']:.2f}")

        table_unit = Table(title="[bold magenta]Produção e Lucro (Unidade)[/bold magenta]", box=box.SQUARE)
        table_unit.add_column("Item", style="cyan")
        table_unit.add_column("Valor (R$)", justify="right")

        table_unit.add_row("Ingredientes", f"{result['custo_ingredientes'] / servings:.2f}" if servings else "0.00")
        table_unit.add_row("Insumos e embalagens (embalagem, colher, lacre)", f"{unit_fixed_costs:.2f}")
        table_unit.add_row(f"Outras despesas ({expense_pct:.0f}% sobre ingredientes)", f"{total_variable_expenses_unit:.2f}")
        table_unit.add_row(f"Mão de obra ({labor_pct:.0f}% sobre ingredientes)", f"{result['mao_de_obra'] / servings:.2f}" if servings else "0.00")
        table_unit.add_row("Custo de Produção", f"{result['por_bolo']:.2f}")
        table_unit.add_row(f"Lucro ({profit_pct:.0f}% sobre ingredientes)", f"{result['lucro_unitario']:.2f}")
        table_unit.add_row("Preço de venda sugerido (unidade)", f"{result['preco_venda'] / servings:.2f}" if servings else "0.00")

        self.console.print(table_total)
        print()
        self.console.print(table_unit)

    def print_colored_lines(self, lines: list[str], patterns_colors: dict[str, str], prefix_map: dict[str, str] = None):
        """
        Imprime linhas com cores e prefixos configuráveis,
        adicionando uma linha em branco antes das linhas que contenham "Calculando camada:".
        """
        for line in lines:
            applied = False
            for pattern, color in patterns_colors.items():
                if pattern in line:
                    # Adiciona linha em branco antes se o padrão for "Calculando camada:"
                    if pattern == "Calculando camada:":
                        self.console.print("")  # linha em branco

                    prefix = prefix_map.get(pattern, "") if prefix_map else ""
                    to_print = f"{prefix} {line.strip()}" if prefix else line.strip()
                    self.console.print(f"[bold {color}]{to_print}[/bold {color}]")
                    applied = True
                    break
            if not applied:
                self.console.print(line.strip())