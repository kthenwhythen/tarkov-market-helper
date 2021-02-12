import pandas


class Items:
    def __init__(self):
        self.items = None
        self.refresh()

    def find(self, item_hash):
        if item_hash:
            item_data = self.items.loc[self.items['Hash EN'] == item_hash]
            if not item_data.empty:
                return item_data, "Item data found"
            else:
                return item_data, "Item data not found"
        else:
            return pandas.DataFrame(), "No item on screen"

    def refresh(self):
        self.items = pandas.read_csv("data.csv")
        print("Local data updated\n")
