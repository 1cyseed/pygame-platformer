import math

import pygame

pygame.init()


class Platforms(pygame.sprite.Sprite):
    def __init__(self, loc, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = loc


class Character(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.x_speed = 0
        self.y_speed = 0

        #self.hit_wall_right = False
        #self.hit_wall_left = False  
        #self.touchingPlat = False


    def update(self):
        self.rect.center = (self.rect.center[0] + self.x_speed, self.rect.center[1] + self.y_speed)

    def set_x_speed(self, x_speed):
        self.x_speed = x_speed

    def set_y_speed(self, y_speed):
        self.y_speed = y_speed

class HitBox(pygame.sprite.Sprite):
    def __init__(self, character, side):
        super().__init__()
        if side == 'top': 
            self.rect = pygame.Rect(0, 0, 25, 1)
            self.rect.topleft = (character.rect.left, character.rect.top - 1)

        elif side == 'bottom':
            self.rect = pygame.Rect(0, 0, 25, 1)
            self.rect.topleft = character.rect.bottomleft
        elif side == 'right':
            self.rect = pygame.Rect(0, 0, 1, 25)
            self.rect.topleft = character.rect.topright
        else:
            self.rect = pygame.Rect(0, 0, 1, 25)
            self.rect.topleft = (character.rect.left - 1, character.rect.top)

        self.x, self.y = self.rect.topleft
        #self.image = pygame.Surface((25,5))
        #self.image.fill((255,105,180))


    def update(self):
        self.rect.topleft = (self.x, self.y)

    def updateXY(self, pos):
        self.x, self.y = pos

class Enemy(pygame.sprite.Sprite):
    def __init__(self, loc):
        super().__init__()

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 48, 67))
        self.rect = self.image.get_rect()
        self.rect.center = loc



def main():
    screen = pygame.display.set_mode((1500, 800))
    pygame.display.set_caption("Platformer")


    jump_height = 80
    jump_time = 5


    gravity = jump_height / (2 * (jump_time ** 2))
    jump_speed = math.sqrt(2 * jump_height * gravity)

    startY = 400
    startX = 250

    character = Character((startX,startY))
    hitbox_top = HitBox(character, 'top')
    hitbox_bot = HitBox(character, 'bottom')
    hitbox_rt = HitBox(character, 'right')
    hitbox_lt = HitBox(character, 'left')
    enemy = Enemy((979, 442))



    platforms = []


    plat_file = open('Platforms.TXT', mode='a+')
    plat_file.seek(0)
    read = plat_file.readlines()
    for line in read:
        line.replace('\n', '')
        values = list(map(int, line.split(', ')))
        platforms.append(Platforms((values[0], values[1]), values[2], values[3]))

    temp_platforms = []

    all_sprites_list = pygame.sprite.Group()


    all_sprites_list.add(character)
    all_sprites_list.add(enemy)


    for plat in platforms:
        all_sprites_list.add(plat)
    coords = ()



    clock = pygame.time.Clock()
    ind_of_bottom = 0

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                plat_file.close()
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                coords2 = pygame.mouse.get_pos()
                plat_file.write(
                    f'{coords[0]}, {coords[1]}, {abs(coords[0] - coords2[0])}, {abs(coords[1] - coords2[1])}\n')
                temp_platforms.append(
                    (coords[0], coords[1], abs(coords[0] - coords2[0]), abs(coords[1] - coords2[1])))

        top_collisions = hitbox_top.rect.collidelistall(platforms)
        bot_collisions = hitbox_bot.rect.collidelistall(platforms)
        rt_collisions = hitbox_rt.rect.collidelistall(platforms)
        lt_collisions = hitbox_lt.rect.collidelistall(platforms)
        
       



        if rt_collisions or lt_collisions:
            character.set_x_speed(0)
            if rt_collisions:
                if bot_collisions and bot_collisions[0] != rt_collisions[0]:
                    character.rect.right = platforms[rt_collisions[0]].rect.left
                   
                    

            if lt_collisions:
                if bot_collisions and bot_collisions[0] != lt_collisions[0]:
                    character.rect.left = platforms[lt_collisions[0]].rect.right


        if top_collisions or bot_collisions:
            character.set_y_speed(0)
            if bot_collisions:
                character.rect.bottom = platforms[bot_collisions[0]].rect.top
            if top_collisions and not bot_collisions:
                character.rect.top = platforms[top_collisions[0]].rect.bottom + 1


        keys = pygame.key.get_pressed()


        if keys[pygame.K_a] and not lt_collisions:
            character.set_x_speed(-5)

#       elif character.hit_wall_left:
#           character.hit_wall_left = False
#           character.set_x_speed(0)

        if keys[pygame.K_d] and not rt_collisions:
            character.set_x_speed(5)

 #       elif character.hit_wall_right:
 #           if not keys[pygame.K_a]:
#
 #               character.set_x_speed(0)
#
 #           character.hit_wall_right = False


        if not(keys[pygame.K_d] or keys[pygame.K_a]):
            character.set_x_speed(0)

        if keys[pygame.K_SPACE] and bot_collisions:
            character.set_y_speed(jump_speed * -1)
        elif not bot_collisions:
            character.set_y_speed(character.y_speed + gravity)


        if character.rect.top >= screen.get_height():
            character.rect.center = (startX, startY)





        screen.fill((135, 206, 235))




        for plat in temp_platforms:
            pygame.draw.rect(screen, (0, 0, 0), plat, 3)

        all_sprites_list.update()
        #hitbox.updateXY(character.rect.center)
        #hitbox.update()

        hitbox_top.updateXY((character.rect.left, character.rect.top - 1))
        hitbox_bot.updateXY(character.rect.bottomleft)
        hitbox_rt.updateXY(character.rect.topright)
        hitbox_lt.updateXY((character.rect.left -1, character.rect.top))
        hitbox_top.update()
        hitbox_bot.update()
        hitbox_rt.update()
        hitbox_lt.update()



        all_sprites_list.draw(screen)



        clock.tick(60)


        pygame.display.update()


if __name__ == '__main__':
    main()

