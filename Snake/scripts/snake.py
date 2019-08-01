import pygame

class Snake(pygame.sprite.Sprite):
    
    width, height, step = [28, 28, 30]

    def __init__(self, colour, posx, posy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([Snake.width, Snake.height])
        self.image.fill(colour)

        self.rect = self.image.get_rect(center=(14, 14))
        # center kw argument in get_rect allows us to draw Surface from centre
        self.rect.x = posx
        self.rect.y = posy

    def move(self, dx, dy, body_parts:list):

        positions = [[i.rect.x, i.rect.y] for i in body_parts]  # Store array of body part positions

        if len(body_parts) == 1:  # HEAD MOVEMENT
            h = body_parts[0]
            h.rect.move_ip(dx*Snake.step, dy*Snake.step)

        else:
            for i in range(len(body_parts)):

                if i == 0:  # HEAD_MOVEMENT
                    h = body_parts[0]
                    # Save head's position before movement in the positions array
                    positions[0] = [h.rect.x, h.rect.y]
                    h.rect.move_ip(dx*Snake.step, dy*Snake.step)

                else:
                    # Find offset from one body part to the next
                    # Move each piece by calculated offset
                    
                    xstep = Snake.step * ((positions[i-1][0] - positions[i][0]) // Snake.step)
                    ystep = Snake.step * ((positions[i-1][1] - positions[i][1]) // Snake.step)

                    positions[i] = [body_parts[i].rect.x, body_parts[i].rect.y]  # Save part's last position
                    
                    body_parts[i].rect.move_ip(xstep, ystep)  # Move body part

    def check_bound(self, xbound, ybound, mgx, mgy):
        # BOUNDARY DETECTION ~ COMMON TO ALL

        if (self.rect.x + 14) > xbound-mgx:
            self.rect.x = mgx - 15
            pygame.time.wait(10)
        elif (self.rect.x - 14) < mgx:
            self.rect.x = (xbound - mgx) + 15
            pygame.time.wait(10)

        if (self.rect.y + 14) > ybound - mgy:
            self.rect.y = mgy - 15
            pygame.time.wait(10)
        elif (self.rect.y - 14) < mgy:
            self.rect.y = (ybound - mgy) + 15
            pygame.time.wait(10)

    def game_over(self, death, body_parts:list):
        for part in range(1, len(body_parts)):
            if pygame.sprite.collide_rect(self, body_parts[part]) and len(body_parts) > 5:
                death() 

    def update(self, surface:pygame.Surface, sw, sh, mgx, mgy):
        if (mgx < self.rect.x < sw - mgx) and (mgy < self.rect.y < sh - mgy):
            # Only show the part if within window
            surface.blit(self.image, [self.rect.x - 14, self.rect.y - 14])
