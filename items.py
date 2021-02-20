from pandas import DataFrame, read_csv
from requests import get
from io import BytesIO


DATA = 'https://docs.google.com/spreadsheet/ccc?key=12iocznEgCgCTOjPxEkRHxLV18fzHV2WqtdJQZFwTjtY&output=csv'


class Items:
    def __init__(self, hash_lang):
        """
        Init of Items data

        Arguments:
        hash_lang -- chosen lang of game client
        """
        self.items = None
        self.hash_lang = hash_lang
        self.update_data()

    def find(self, item_hash):
        """
        Method will return item_hash and item_state
        """
        if item_hash:
            item_data = self.items.loc[self.items[f'Hash {self.hash_lang}'] == item_hash]

            if not item_data.empty:
                return item_data, "Item data found"

            else:
                return item_data, "Item data not found"

        else:
            return DataFrame(), "No item on screen"

    def update_data(self):
        """
        Method will get data from google spreadsheets
        """
        response = get(DATA)
        self.items = read_csv(BytesIO(response.content))
        print("Data loaded\n")
