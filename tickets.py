import random

class Tickets():
    def __init__(self, name, probability, price) -> None:
        """fonction utilisé pour faire un mini jeu de casino

        Args:
            name (str): nom du ticket
            probability (int): probabilité de gagner; exemple : probability = 10; = 1/10
            price (int) : prix du ticket
        """        
        
        
    
        self.name = name
        self.probability = probability
        self.price = price
    
    
    def play(self):
        
        result = random.randint(1, self.probability)
        
        if result == 1:
            return True
        else:
            return False
        
    
    
    def remove_money(self, account, amount):
        account = account - amount
        
        