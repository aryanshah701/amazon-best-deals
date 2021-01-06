class Product:

    def __init__(self, title, previous_price, discount_price):
        self.title = title
        self.previous_price = previous_price
        self.discount_price = discount_price

    def get_discount(self):
        return self.previous_price - self.discount_price

    def get_previous_price(self):
        return self.previous_price

    def get_price(self):
        return self.discount_price
    
    def get_title(self):
        return self.title