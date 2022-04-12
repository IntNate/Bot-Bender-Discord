import random

class Tickets():
    def __init__(self, name, probability) -> None:
        """fonction utilisé pour faire un mini jeu de casino

        Args:
            name (str): nom du ticket
            probability (int): probabilité de gagner; exemple : probability = 10; = 1/10
        """        
        
        
        
        self.name = name
        self.probability = probability
 
    
    
    def play(self):
        
        result = random.randint(1, self.probability)
        
        if result == 1:
            return True
        else:
            return False
        