import pygame, sys, os

from settings import WINDOW_HEIGHT, WINDOW_WIDTH
from random import randint, uniform

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups: pygame.sprite.Group):
        super().__init__(groups)

        player_surf = pygame.image.load(os.path.abspath("graphics/player.png")).convert_alpha()
        player_size = pygame.math.Vector2(player_surf.get_size()) * 1.5
        self.scaled_image = pygame.transform.scale(player_surf, player_size)
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center = pos)
        self.font = pygame.font.Font(os.path.abspath('graphics/subatomic.ttf'), 50)

        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 400

        self.lifes = 3

        self.can_shoot = True
        self.shoot_time = None

    def __bullet_timer(self):
        if not self.can_shoot:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.shoot_time > 900:
                self.can_shoot = True

    def __bullet_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

            Bullet(bullet_group, self.rect.center, -self.angle)

    def __point_at(self, x, y):
        self.direction = pygame.math.Vector2(x, y) - self.rect.center

        self.angle = self.direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def __display_reload(self):
        reload_text = "RELOADING"
        text_surface = self.font.render(reload_text, True, (255,255,255))
        text_rect = text_surface.get_rect(bottomright = (1280, 720))

        if self.can_shoot == False:
            display_surface.blit(text_surface, text_rect)
            pygame.draw.rect(display_surface, 'yellow', text_rect.inflate(30,30), width=10, border_radius=5)

    def __move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def imortal(self):
        print("imortal")

    def __input_pos(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_s]:
            self.direction.y = 1
        elif keys[pygame.K_w]:
            self.direction.y = -1
        else:
            self.direction.y = 0

    def update(self, dt):
        self.__bullet_timer()
        self.__bullet_shoot()
        self.__input_pos()
        self.__move(dt)
        self.__point_at(*pygame.mouse.get_pos())
        self.__display_reload()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, pos):
        super().__init__(groups)

        enemy_surf = pygame.image.load(os.path.abspath("graphics/enemy.png")).convert_alpha()
        enemy_size = pygame.math.Vector2(enemy_surf.get_size()) * uniform(2, 4)
        self.scaled_image = pygame.transform.scale(enemy_surf,enemy_size)

        self.image = self.scaled_image
        self.rect = self.image.get_rect(center = pos)

        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(500, 600)

    def __damage(self, player: Player):
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            self.kill()

            player.lifes -= 1

            player.imortal()

            if player.lifes <= 0:
                pygame.quit()
                sys.exit()
            
    def update(self, dt, player):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        self.__damage(player)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, pos, angle):
        super().__init__(groups)

        bullet_surface = pygame.image.load(os.path.abspath('graphics/bullet.png')).convert_alpha()
        bullet_size = pygame.math.Vector2(bullet_surface.get_size())
        self.scaled_image = pygame.transform.scale(bullet_surface,bullet_size)
        self.angle = angle

        self.image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.rect = self.image.get_rect(midbottom = pos)

        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.diretion = pygame.math.Vector2(0, -1).rotate(self.angle)
        self.speed = 700

    def __enemy_colision(self):
        if pygame.sprite.spritecollide(self, enemy_group, True, pygame.sprite.collide_mask):
            self.kill()

    def update(self):
        self.pos += self.diretion * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        self.__enemy_colision()

class Score:
    def __init__(self, player):
        self.player = player

        self.font = pygame.font.Font(os.path.abspath('graphics/subatomic.ttf'), 50)

    def display(self):
        score_text = f'Lifes: {player.lifes}'
        text_surface = self.font.render(score_text, True, (255,255,255))
        text_rect = text_surface.get_rect(topleft = (5, 5))

        display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(display_surface, 'white', text_rect.inflate(30,30), width=10, border_radius=5)

class Strawberry(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, pos):
        super().__init__(groups)

        strawberry_surf = pygame.image.load(os.path.abspath("graphics/strawberry.png")).convert_alpha()
        strawberry_size = pygame.math.Vector2(strawberry_surf.get_size()) * uniform(3, 5)
        self.scaled_image = pygame.transform.scale(strawberry_surf,strawberry_size)

        self.image = self.scaled_image
        self.rect = self.image.get_rect(center = pos)

        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)

    def __life_colision(self, player: Player):
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            self.kill()

            if player.lifes == 3:
                return
            
            player.lifes += 1
            
    def update(self, dt, player):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

        self.__life_colision(player)

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shooter Game")
clock = pygame.time.Clock()

background_surface = pygame.image.load(os.path.abspath("graphics/map.png")).convert()

player_group = pygame.sprite.GroupSingle()
strawberry_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

player = Player((600, 400), player_group)
score = Score(player)

strawberry_timer = pygame.event.custom_type()
pygame.time.set_timer(strawberry_timer, 5000)

enemy_timer = pygame.event.custom_type()
pygame.time.set_timer(enemy_timer, 400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == strawberry_timer:
            strawberry_y_pos = randint(-10, -10)
            strawberry_x_pos = randint(-10, WINDOW_WIDTH + 10)
            Strawberry(strawberry_group, (strawberry_x_pos, strawberry_y_pos))

        if event.type == enemy_timer:
            enemy_y_pos = randint(-150, -50)
            enemy_x_pos = randint(0, WINDOW_WIDTH)
            Enemy(enemy_group, (enemy_x_pos, enemy_y_pos))

    dt = clock.tick() / 1000

    display_surface.blit(background_surface, (0, 0))

    score.display()

    player_group.update(dt)
    strawberry_group.update(dt, player)
    enemy_group.update(dt, player)
    bullet_group.update()

    player_group.draw(display_surface)
    strawberry_group.draw(display_surface)
    enemy_group.draw(display_surface)
    bullet_group.draw(display_surface)

    pygame.display.update()