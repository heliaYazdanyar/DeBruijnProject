class Params:
    def __init__(self):
        self.size_dataset = 1000          # number of requests (artificial datasets)
        self.n_items = 10                # number of items (artificial datasets)

    def set_n_items(self, n):
        self.n_items = n

    def set_size_dataset(self, n):
        self.size_dataset = n


param = Params()
