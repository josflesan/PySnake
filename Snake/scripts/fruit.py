import pygame
from random import randint as r

class Fruit(pygame.sprite.Sprite):

    width, height = [28, 28]

    def __init__(self, colour, sw, sh, mgx, mgy):
        pygame.sprite.Sprite.__init__(self)

        # List of possible spawn positions in x
        spawn_pos_x = [x for x in range(15 + mgx, sw-mgx, 30)]
        # List of possible spawn positions in y
        spawn_pos_y = [y for y in range(15 + mgy, sh-mgy, 30)]

        posx = spawn_pos_x[r(0, len(spawn_pos_x)-1)]
        posy = spawn_pos_y[r(0, len(spawn_pos_y)-1)]

        self.image = pygame.Surface([Fruit.width, Fruit.height])
        self.image.fill(colour)

        self.colour = colour 

        self.rect = self.image.get_rect(center=(14, 14))
        self.rect.x = posx
        self.rect.y = posy
    
    def update(self, surface:pygame.Surface):
        surface.blit(self.image, [self.rect.x - 13, self.rect.y - 13])

    def eaten(self, snake:pygame.sprite.Sprite, sw, sh, sfx, fruits:list):
        if pygame.sprite.collide_rect(snake, self): # If there's a collision between the 2 sprites...
            ind = fruits.index(self)  # Obtain index of fruit touched
            del fruits[ind]  # Delete that fruit from the list
            sfx.play()  # Play munch sound effect
            return True
