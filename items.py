import pandas
import requests
from io import BytesIO


DATA = 'https://docs.google.com/spreadsheet/ccc?key=12iocznEgCgCTOjPxEkRHxLV18fzHV2WqtdJQZFwTjtY&output=csv'


class Items:
    def __init__(self, hash_lang):
        self.items = None
        self.hash_lang = hash_lang
        self.refresh()

    def find(self, item_hash):
        if item_hash:
            item_data = self.items.loc[self.items[f'Hash {self.hash_lang}'] == item_hash]
            if not item_data.empty:
                return item_data, "Item data found"
            else:
                return item_data, "Item data not found"
        else:
            return pandas.DataFrame(), "No item on screen"

    def refresh(self):
        response = requests.get(DATA)
        self.items = pandas.read_csv(BytesIO(response.content))
        print("Data loaded\n")
