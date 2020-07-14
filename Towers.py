class Towers:

        """
        Classes of towers:
        Pistol Cat
        Rifler Cat
        Ranger Cat
        Angry Cat
        """

    def __init__(self, screen):
        pass

#Towers 
class Pistol(Towers):

    sprite = "Sprites\Towers\PistolCatSprite.png"

    def __init__(self):
        self.range = 10 # 1 range unit = 10 pixel radius
        self.damage = 1 # Damage is equal to units unravelled per attack