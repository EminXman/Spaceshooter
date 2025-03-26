import pygame
import random

from scripts.partikeleffekt import Partikel

# Skärmstorlek
skärmens_bredd = 800
skärmens_höjd = 600

# Skapa skärmen
skärm = pygame.display.set_mode((skärmens_bredd, skärmens_höjd))
pygame.display.set_caption("Space Shooter")

# Spelstatus
spelet_körs = True
spelare_1_exploderat = False  # Definerar variabel för att spåra om spelaren har exploderat
paus = 0

# Ladda bilder
original_bild = pygame.image.load("assets/sprites/SpaceShip.png")
backgrund_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
backgrund_stjärnor = pygame.image.load("assets/backgrounds/stars-A.png")
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png")
sprite_skott = pygame.image.load("assets/sprites/bullet.png")
sprite_ateroid_liten = pygame.image.load("assets/sprites/small-A.png")

# Lista för skott
skott_lista = []

expolsioner = []

svart = (0, 0, 0)
FÄRG_LISTA = [(255, 0, 0), (255, 165, 0), (255, 255, 0),] # Röd, orange, gul

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
        self.kollisions_rektangel_asteroid = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())

    def flytta(self):
        self.y += self.hastighet
        self.kollisions_rektangel_asteroid.topleft = (self.x, self.y)

    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))
        pygame.draw.rect(skärm, (255, 0, 0), self.kollisions_rektangel_asteroid, 2)
    
    def kollidera(self, kollisions_rektangel_spelare):
        if self.kollisions_rektangel_asteroid.colliderect(kollisions_rektangel_spelare):
            print("Kollision med asteroid!")
            return True
        return False
       

class Partiklar:
    def __init__(self, x, y, färg=None):
        self.x = x
        self.y = y
        self.livslängd = random.randint(20, 50)
        self.hastighet_x = random.uniform(-2, 2)
        self.hastighet_y = random.uniform(-2, 2)
        self.radius = random.randint(3, 6)
        self.färg = färg if färg else random.choice(FÄRG_LISTA)

    def uppdatera(self):
        self.x += self.hastighet_x
        self.y += self.hastighet_y
        self.livslängd -= 1

    def rita(self, skärm):
        if self.livslängd > 0:
            pygame.draw.circle(skärm, self.färg, (int(self.x), int(self.y)), self.radius) 

class Rymdskepp:
    def __init__(self):
        self.rymdskepp_x = skärmens_bredd // 2 - 120
        self.rymdskepp_y = skärmens_höjd - 200
        self.sprite_rymdskepp = sprite_spelare

        self.jetstråle_x = self.rymdskepp_x + 13
        self.jetstråle_y = self.rymdskepp_y + 46
        self.sprite_jetstråle = sprite_jetstråle

        self.rymdskepp_hastighet = 10

        self.exploderat =  False

        self.kollisions_rektangel = pygame.Rect(self.rymdskepp_x, self.rymdskepp_y, self.sprite_rymdskepp.get_width(), self.sprite_rymdskepp.get_height()) 

        self.exploderat_x = 0
        self.exploderat_y = 0

    def flytta(self, riktning):

        if not self.exploderat:
            if riktning == "vänster" and self.rymdskepp_x > 0:
                self.rymdskepp_x -= self.rymdskepp_hastighet
                self.jetstråle_x -= self.rymdskepp_hastighet
            elif riktning == "höger" and self.rymdskepp_x < skärmens_bredd - self.sprite_rymdskepp.get_width():
                self.rymdskepp_x += self.rymdskepp_hastighet
                self.jetstråle_x += self.rymdskepp_hastighet
            elif riktning == "upp" and self.rymdskepp_y > 0:
                self.rymdskepp_y -= self.rymdskepp_hastighet
                self.jetstråle_y -= self.rymdskepp_hastighet
            elif riktning == "ner" and self.rymdskepp_y < skärmens_höjd - self.sprite_rymdskepp.get_width() + 26:
                self.rymdskepp_y += self.rymdskepp_hastighet
                self.jetstråle_y += self.rymdskepp_hastighet

            self.kollisions_rektangel.topleft = (self.rymdskepp_x, self.rymdskepp_y)
    def rita(self, skärm):
        if not self.exploderat:
            skärm.blit(self.sprite_rymdskepp, (self.rymdskepp_x, self.rymdskepp_y))
            skärm.blit(self.sprite_jetstråle, (self.jetstråle_x, self.jetstråle_y))

            pygame.draw.rect(skärm, (255, 0, 0), self.kollisions_rektangel, 2)
        else:
            self.kollisions_rektangel = pygame.React(0,0,0,0)

    def kollidera(self, rymdskepp):
        global spelare_1_exploderat  # Global variabel för att hålla reda på om spelaren har exploderat
        if not spelare_1_exploderat:
            if (self.kollisions_rektangel.colliderect(rymdskepp)):
                print ("Kollision!")
                spelare_1_exploderat = True
                self.exploderat_x = self.rymdskepp_x
                self.exploderat_y = self.rymdskepp_y
                explosion = [Partikel(self.exploderat_x + 60, self.exploderat_y + 46) for _ in range(100)]
                explosioner.append(explosion)


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

    kollisions_rektangel_spelare = pygame.Rect(spelare_x, spelare_y, sprite_spelare.get_width(), sprite_spelare.get_height())

    pygame.draw.rect(skärm, (255, 0, 0), kollisions_rektangel_spelare, 2)

    for asteroid_liten in reversed(asteroid_liten_lista):
        asteroid_liten.flytta()
        asteroid_liten.kollidera(kollisions_rektangel_spelare)
        asteroid_liten.rita(skärm)
        if asteroid_liten.y > skärmens_höjd:
            asteroid_liten_lista.remove(asteroid_liten)

    asteroid_räknare += 1  # Öka räknaren varje gång spelet uppdateras

    for explosion in expolsioner:
        for partikel in explosion:
            partikel.uppdatera()
            partikel.rita(skärm)

    explosioner = [[p for p in explosion if p.livslängd > 0] for explosion in expolsioner]
    explosioner = [e for e in explosioner if len(e) > 0]

    if (spelare_1_exploderat == True):
        paus += 1    
        if paus >= 120:
            spelet_körs = False

    pygame.display.update()

pygame.quit()