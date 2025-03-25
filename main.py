import pygame
import random

# Skärmstorlek
skärmens_bredd = 800
skärmens_höjd = 600

# Skapa skärmen
skärm = pygame.display.set_mode((skärmens_bredd, skärmens_höjd))
pygame.display.set_caption("Space Shooter")

# Spelstatus
spelet_körs = True

# Ladda bilder
original_bild = pygame.image.load("assets/sprites/SpaceShip.png")
backgrund_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
backgrund_stjärnor = pygame.image.load("assets/backgrounds/stars-A.png")
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png")
sprite_skott = pygame.image.load("assets/sprites/bullet.png")
sprite_ateroid_liten = pygame.image.load("assets/sprites/small-A.png")

# Lista för skott
skott_lista = []

# Bakgrundsposition
backgrund_y = 0

# Skala spelarens sprite
sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))

# Spelarens position och hastighet
spelare_x = skärmens_bredd // 2 - 120
spelare_y = skärmens_höjd - 200
spelarens_hastighet = 3
jetstråle_x = spelare_x + 25
jetstråle_y = spelare_y - 25

# Variabel för att hålla reda på tiden mellan skott
skott_räknare = 0
skott_frekvens = 20  # Justera detta värde för att ändra tiden mellan skott

# Variabel för att hålla reda på tiden mellan asteroider
asteroid_räknare = 0
asteroid_frekvens = 50  # Justera detta värde för att ändra tiden mellan asteroider

# Klass för skott
class Skott:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hastighet = 10
        self.bild = sprite_skott

    def flytta(self):
        self.y -= self.hastighet

    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))

# Klass för små asteroider
class AsteroidLiten:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hastighet = 4
        self.bild = sprite_ateroid_liten

    def flytta(self):
        self.y += self.hastighet

    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))

# Lista för asteroider
asteroid_liten_lista = []

# Huvudloopen för spelet
while spelet_körs:
    skärm.fill((0, 0, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spelet_körs = False

    skärm.blit(backgrund_mörkblå, (0, 0))
    skärm.blit(backgrund_stjärnor, (0, backgrund_y))
    skärm.blit(backgrund_stjärnor, (0, backgrund_y - skärmens_höjd))

    backgrund_y += 2
    if backgrund_y > skärmens_höjd:
        backgrund_y = 0

    skärm.blit(sprite_spelare, (spelare_x, spelare_y))
    skärm.blit(sprite_jetstråle, (jetstråle_x, jetstråle_y))

    jetstråle_x = spelare_x + (sprite_spelare.get_width() // 2) - (sprite_jetstråle.get_width() // 2)
    jetstråle_y = spelare_y + sprite_spelare.get_height() - (sprite_jetstråle.get_height() // 2)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and spelare_x > 0:
        spelare_x -= spelarens_hastighet
        jetstråle_x -= spelarens_hastighet
    if keys[pygame.K_d] and spelare_x < skärmens_bredd - sprite_spelare.get_width():
        spelare_x += spelarens_hastighet
        jetstråle_x += spelarens_hastighet
    if keys[pygame.K_w] and spelare_y > 0:
        spelare_y -= spelarens_hastighet
        jetstråle_y -= spelarens_hastighet
    if keys[pygame.K_s] and spelare_y < skärmens_höjd - sprite_spelare.get_width() + 26:
        spelare_y += spelarens_hastighet
        jetstråle_y += spelarens_hastighet
    if keys[pygame.K_SPACE] and skott_räknare >= skott_frekvens:
        skott_lista.append(Skott(spelare_x + 20, spelare_y))
        skott_räknare = 0

    for skott_obj in reversed(skott_lista):
        skott_obj.flytta()
        skott_obj.rita(skärm)
        if skott_obj.y < -100:
            skott_lista.remove(skott_obj)

    skott_räknare += 1  # Öka räknaren varje gång spelet uppdateras

    if asteroid_räknare >= asteroid_frekvens:
        asteroid_liten_lista.append(AsteroidLiten(random.randint(0, skärmens_bredd - sprite_ateroid_liten.get_width()), 100))
        asteroid_räknare = 0

    for asteroid_liten in reversed(asteroid_liten_lista):
        asteroid_liten.flytta()
        asteroid_liten.rita(skärm)
        if asteroid_liten.y > skärmens_höjd:
            asteroid_liten_lista.remove(asteroid_liten)

    asteroid_räknare += 1  # Öka räknaren varje gång spelet uppdateras

    pygame.display.update()

pygame.quit()