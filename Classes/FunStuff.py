from random import choice

class FunStuff:
    """docstring for FunStuff"""
    def __init__(self):
        self.foodlist = ["Hamburger", "Geschnetzeltes", "Bolognese", 
        "Korean Chicken", "Bulgogi", "Wraps", 
        "Curry", "Lasagne", "Flammkuchen", 
        "Pizza", "Gefüllte Paprika", "Gemüsesuppe", "Fenchel Gemüse",
        "Reis mit Gemüse (asia)", "Sushi", "Beith ma'tomat",
        "Japchae", "Lachsnudeln", "Garnelennudeln", "Salat"]


    def foodchoice(self):
        food = choice(self.foodlist).title()
        return food


