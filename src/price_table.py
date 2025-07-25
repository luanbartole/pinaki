import os
import json

class IngredientPriceTable:
    def __init__(self, price_data=None, file_path=None):
        self.file_path = file_path
        self.price_data = price_data if price_data is not None else {}

        if self.file_path:
            self.load()

    def load(self):
        try:
            if os.path.isfile(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.price_data = json.load(f)
            else:
                self.price_data = {}
        except (json.JSONDecodeError, IOError):
            print("Erro ao carregar o arquivo de preços. Inicializando vazio.")
            self.price_data = {}

    def save(self):
        try:
            if self.file_path:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.price_data, f, ensure_ascii=False, indent=2)
        except IOError:
            print("Erro ao salvar o arquivo de preços.")

    def get_unit_price(self, name, unidade=None):
        item = self.price_data.get(name)
        if not item:
            return None

        preco = item["preco"]
        quantidade = item["quantidade"]
        unidade_cadastrada = item.get("unidade")

        # Se unidade não informada, assume a unidade cadastrada e retorna preço por unidade
        if unidade is None or unidade_cadastrada == unidade:
            return preco / quantidade

        # Conversões simples
        conversoes = {
            ("kg", "g"): 1000,
            ("g", "kg"): 1 / 1000,
            ("l", "ml"): 1000,
            ("ml", "l"): 1 / 1000,
        }

        chave = (unidade_cadastrada, unidade)
        if chave in conversoes:
            fator = conversoes[chave]
            quantidade_convertida = quantidade * fator
            return preco / quantidade_convertida

        print(f"Unidade incompatível: cadastro '{unidade_cadastrada}', pedido '{unidade}'.")
        return None

    def update_ingredient(self, name, preco=None, quantidade=None, unidade=None, purchase_date=None):
        if name not in self.price_data:
            self.price_data[name] = {}
        if preco is not None:
            self.price_data[name]["preco"] = preco
        if quantidade is not None:
            self.price_data[name]["quantidade"] = quantidade
        if unidade is not None:
            self.price_data[name]["unidade"] = unidade
        if purchase_date is not None:
            self.price_data[name]["purchase_date"] = purchase_date

    def remove_ingredient(self, name):
        if name in self.price_data:
            del self.price_data[name]

    def to_dict(self):
        return self.price_data
