import pygame
import random

# Skärmstorlek och inställningar
skärmens_bredd = 850
skärmens_höjd = 700

pygame.init()  # Säkerställ att pygame är initierat innan något annat används

# Skapa skärmen (uppdaterad med nya dimensioner)
skärm = pygame.display.set_mode((skärmens_bredd, skärmens_höjd))
pygame.display.set_caption("Space Shooter")

# Spelstatus
paus = 0

# Ladda bilder
original_bild = pygame.image.load("assets/sprites/SpaceShip.png")
original_bild_spelare_2 = pygame.image.load("assets/sprites/png-transparent-brown-and-black-game-item-illustration-space-shooting-spacecraft-sprite-computer-icons-spaceship-game-symmetry-video-game.png")
backgrund_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
backgrund_stjärnor = pygame.image.load("assets/backgrounds/stars-A.png")
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png")
sprite_skott = pygame.image.load("assets/sprites/bullet.png")
sprite_ateroid_liten = pygame.image.load("assets/sprites/small-A.png")

pygame.mixer.init()

pygame.mixer.music.load("assets/music/Mesmerizing Galaxy Loop.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # Spela musiken i loop

sound_liten_explosion = pygame.mixer.Sound("assets/sounds/scfi_explosion.wav")
sound_stor_explosion = pygame.mixer.Sound("assets/sounds/huge_explosion.wav")

sound_liten_explosion.set_volume(0.7)  # Justera volymen för ljudet
sound_stor_explosion.set_volume(0.9)  # Justera volymen för ljudet

try:
    font = pygame.font.Font("assets/fonts/ZenDots-Regular.ttf", 74)
except FileNotFoundError:
    print("Fonten 'ZenDots-Regular.ttf' hittades inte. Använder standardfont.")
    font = pygame.font.SysFont(None, 74)  # Använd standardfont om den angivna fonten inte hittas

try:
    font_poäng = pygame.font.Font("assets/fonts/ZenDots-Regular.ttf", 30)  
except FileNotFoundError:
    print("Fonten 'ZenDots-Regular.ttf' hittades inte. Använder standardfont.")
    font_poäng = pygame.font.SysFont(None, 30)

text_gamover = font.render("GAME OVER", True, (255, 0, 0))
text_gamover_rect = text_gamover.get_rect(center=(skärmens_bredd // 2, skärmens_höjd // 2))

# Lista för skott
skott_lista = []

# Lista för skott för båda spelarna
skott_lista_spelare_1 = []
skott_lista_spelare_2 = []

expolsioner = []

svart = (0, 0, 0)
FÄRG_LISTA = [(255, 0, 0), (255, 165, 0), (255, 255, 0),] # Röd, orange, gul

# Bakgrundsposition
backgrund_y = 0

# Skala spelarens sprite
sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))
sprite_spelare_2 = pygame.transform.scale(original_bild_spelare_2, (original_bild.get_width() // 2, original_bild.get_height() // 2))

# Spelarens position och hastighet
spelare_x = skärmens_bredd // 2 - 120
spelare_y = skärmens_höjd - 200
spelarens_hastighet = 3

# Spelare 2 position och hastighet
spelare_2_x = skärmens_bredd // 2 + 120
spelare_2_y = skärmens_höjd - 200
spelare_2_hastighet = 3

# Variabel för att hålla reda på tiden mellan skott
skott_frekvens = 20  # Justera detta värde för att ändra tiden mellan skott

# Variabler för att hålla reda på tiden mellan skott för varje spelare
skott_räknare_spelare_1 = 0
skott_räknare_spelare_2 = 0

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
        self.hastighet_x = random.uniform(-2, 2)  # Slumpmässig horisontell hastighet
        self.hastighet_y = 4  # Vertikal hastighet
        self.bild = sprite_ateroid_liten
        self.kollisions_rektangel_asteroid = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())

    def flytta(self):
        self.x += self.hastighet_x  # Flytta horisontellt
        self.y += self.hastighet_y  # Flytta vertikalt

        # Begränsa rörelsen inom skärmens bredd
        if self.x < 0 or self.x > skärmens_bredd - self.bild.get_width():
            self.hastighet_x *= -1  # Byt riktning om asteroiden når kanten

        self.kollisions_rektangel_asteroid.topleft = (self.x, self.y)

    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))
        # pygame.draw.rect(skärm, (255, 0, 0), self.kollisions_rektangel_asteroid, 2)  # Kommenterad för att dölja rektangeln
    
    def kollidera(self, kollisions_rektangel_spelare):
        if self.kollisions_rektangel_asteroid.colliderect(kollisions_rektangel_spelare):
            sound_stor_explosion.play()  # Spela ljudet vid kollision
            print("Kollision med asteroid!")
            return True
        return False
    
    def kollidera_med_skott(self, objekt_lista):

        for skott in objekt_lista:
            if self.kollisions_rektangel_asteroid.colliderect(pygame.Rect(skott.x, skott.y, sprite_skott.get_width(), sprite_skott.get_height())):
                print("Kollision med skott!")
                gränssnitts_hanteraren.poäng += 1  # Öka poängen vid kollision med skott
                objekt_lista.remove(skott)
                explosion = [Partiklar(self.x + 20, self.y + 20) for _ in range(100)]
                expolsioner.append(explosion)
                sound_liten_explosion.play()
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
    def __init__(self, x, y, sprite, jetstråle_sprite=None):
        self.rymdskepp_x = x
        self.rymdskepp_y = y
        self.sprite_rymdskepp = sprite

        # Jetmotor behövs inte för spelare 2
        if jetstråle_sprite:
            self.jetstråle_x = self.rymdskepp_x + 13
            self.jetstråle_y = self.rymdskepp_y + 46
            self.sprite_jetstråle = jetstråle_sprite
        else:
            self.jetstråle_x = None
            self.jetstråle_y = None
            self.sprite_jetstråle = None

        self.rymdskepp_hastighet = 10
        self.exploderat = False
        self.kollisions_rektangel = pygame.Rect(self.rymdskepp_x, self.rymdskepp_y, self.sprite_rymdskepp.get_width(), self.sprite_rymdskepp.get_height())
        self.exploderat_x = 0
        self.exploderat_y = 0

    def flytta(self, riktning):
        if not self.exploderat:
            if riktning == "vänster" and self.rymdskepp_x > 0:
                self.rymdskepp_x -= self.rymdskepp_hastighet
                if self.jetstråle_x is not None:
                    self.jetstråle_x -= self.rymdskepp_hastighet
            elif riktning == "höger" and self.rymdskepp_x < skärmens_bredd - self.sprite_rymdskepp.get_width():
                self.rymdskepp_x += self.rymdskepp_hastighet
                if self.jetstråle_x is not None:
                    self.jetstråle_x += self.rymdskepp_hastighet
            elif riktning == "upp" and self.rymdskepp_y > 0:
                self.rymdskepp_y -= self.rymdskepp_hastighet
                if self.jetstråle_y is not None:
                    self.jetstråle_y -= self.rymdskepp_hastighet
            elif riktning == "ner" and self.rymdskepp_y < skärmens_höjd - self.sprite_rymdskepp.get_height():
                self.rymdskepp_y += self.rymdskepp_hastighet
                if self.jetstråle_y is not None:
                    self.jetstråle_y += self.rymdskepp_hastighet

            self.kollisions_rektangel.topleft = (self.rymdskepp_x, self.rymdskepp_y)

    def ändra_hastighet(self, ny_hastighet):
        self.rymdskepp_hastighet = ny_hastighet

    def rita(self, skärm):
        if not self.exploderat:
            skärm.blit(self.sprite_rymdskepp, (self.rymdskepp_x, self.rymdskepp_y))
            if self.sprite_jetstråle:  # Rita jetmotor endast om den finns
                skärm.blit(self.sprite_jetstråle, (self.jetstråle_x, self.jetstråle_y))
        else:
            self.kollisions_rektangel = pygame.Rect(0, 0, 0, 0)

    def kollidera(self, asteroid):
        if not self.exploderat:
            if self.kollisions_rektangel.colliderect(asteroid.kollisions_rektangel_asteroid):
                print("Kollision!")
                self.exploderat = True
                self.exploderat_x = self.rymdskepp_x
                self.exploderat_y = self.rymdskepp_y
                explosion = [Partiklar(self.exploderat_x + 60, self.exploderat_y + 46) for _ in range(100)]
                expolsioner.append(explosion)
                sound_stor_explosion.play()
                return True
        return False
    
class Gränsnitt:
    """ Klass för gränssnittet """
    def __init__(self):
        self.poäng = 0
    
    def uppdatera_poäng():
        poäng += 1
        

gränssnitts_hanteraren = Gränsnitt()

class Meny:
    """Klass för att hantera huvudmenyn."""
    def __init__(self, skärm, font, font_poäng, skärmens_bredd, skärmens_höjd):
        self.skärm = skärm
        self.font = font
        self.font_poäng = font_poäng
        self.skärmens_bredd = skärmens_bredd
        self.skärmens_höjd = skärmens_höjd

    def visa(self):
        """Visa huvudmenyn och hantera val."""
        meny_körs = True
        while meny_körs:
            self.skärm.fill((0, 0, 0))  # Fyll skärmen med svart
            titel_text = self.font.render("SPACE SHOOTER", True, (255, 255, 255))
            titel_rect = titel_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd // 4))
            self.skärm.blit(titel_text, titel_rect)

            en_spelare_text = self.font_poäng.render("1. Starta spel för 1 spelare", True, (255, 255, 255))
            en_spelare_rect = en_spelare_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd // 2 - 50))
            self.skärm.blit(en_spelare_text, en_spelare_rect)

            två_spelare_text = self.font_poäng.render("2. Starta spel för 2 spelare", True, (255, 255, 255))
            två_spelare_rect = två_spelare_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd // 2 + 50))
            self.skärm.blit(två_spelare_text, två_spelare_rect)

            avsluta_text = self.font_poäng.render("3. Avsluta spelet", True, (255, 255, 255))
            avsluta_rect = avsluta_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd // 2 + 150))
            self.skärm.blit(avsluta_text, avsluta_rect)

            instruktion_text = self.font_poäng.render("Tryck 1, 2 eller 3 för att välja", True, (200, 200, 200))
            instruktion_rect = instruktion_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd - 100))
            self.skärm.blit(instruktion_text, instruktion_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1  # Starta spel för 1 spelare
                    if event.key == pygame.K_2:
                        return 2  # Starta spel för 2 spelare
                    if event.key == pygame.K_3:
                        pygame.quit()
                        exit()  # Avsluta spelet

# Lista för asteroider
asteroid_liten_lista = []

def visa_gameover_skärm():
    """Visa Game Over-skärmen och gå tillbaka till huvudmenyn."""
    skärm.fill((0, 0, 0))  # Fyll skärmen med svart
    skärm.blit(text_gamover, text_gamover_rect)  # Visa "GAME OVER"-texten
    pygame.display.update()
    pygame.time.wait(3000)  # Vänta i 3 sekunder innan spelet avslutas
    return True  # Signalera att vi ska tillbaka till huvudmenyn

def återställ_spelet():
    """Återställ spelet till startläget."""
    global asteroid_liten_lista, skott_lista_spelare_1, skott_lista_spelare_2, expolsioner
    global skott_räknare_spelare_1, skott_räknare_spelare_2, asteroid_räknare, paus

    asteroid_liten_lista = []  # Rensa listan med asteroider
    skott_lista_spelare_1 = []  # Rensa skott för spelare 1
    skott_lista_spelare_2 = []  # Rensa skott för spelare 2
    expolsioner = []  # Rensa explosioner

    skott_räknare_spelare_1 = 0  # Återställ skotträknare för spelare 1
    skott_räknare_spelare_2 = 0  # Återställ skotträknare för spelare 2
    asteroid_räknare = 0  # Återställ asteroidräknaren
    paus = 0  # Återställ pausvariabeln

# Huvudprogram
meny = Meny(skärm, font, font_poäng, skärmens_bredd, skärmens_höjd)

while True:
    antal_spelare = meny.visa()  # Visa menyn och få antalet spelare

    # Återställ spelet innan det startas
    återställ_spelet()

    # Skapa instanser för spelare baserat på valet
    spelare_1 = Rymdskepp(spelare_x, spelare_y, sprite_spelare, sprite_jetstråle)
    spelare_2 = None
    if antal_spelare == 2:
        spelare_2 = Rymdskepp(spelare_2_x, spelare_2_y, sprite_spelare_2)  # Ingen jetmotor för spelare 2

    spelare_1.ändra_hastighet(4)  # Sätt hastigheten för spelare 1 till samma som asteroiden
    if spelare_2:
        spelare_2.ändra_hastighet(4)  # Sätt hastigheten för spelare 2 till samma som asteroiden

    # Huvudloopen för spelet
    spelet_körs = True
    while spelet_körs:
        skärm.fill((0, 0, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        skärm.blit(backgrund_mörkblå, (0, 0))
        skärm.blit(backgrund_stjärnor, (0, backgrund_y))
        skärm.blit(backgrund_stjärnor, (0, backgrund_y - skärmens_höjd))

        backgrund_y += 2
        if backgrund_y > skärmens_höjd:
            backgrund_y = 0

        keys = pygame.key.get_pressed()

        # Rörelse för spelare 1 (WASD)
        if not spelare_1.exploderat:
            if keys[pygame.K_a]:
                spelare_1.flytta("vänster")
            if keys[pygame.K_d]:
                spelare_1.flytta("höger")
            if keys[pygame.K_w]:
                spelare_1.flytta("upp")
            if keys[pygame.K_s]:
                spelare_1.flytta("ner")
            if keys[pygame.K_SPACE] and skott_räknare_spelare_1 >= skott_frekvens:
                skott_lista_spelare_1.append(Skott(spelare_1.rymdskepp_x + 20, spelare_1.rymdskepp_y))
                skott_räknare_spelare_1 = 0

        # Rörelse för spelare 2 (piltangenter) om det är ett 2-spelarläge
        if spelare_2 and not spelare_2.exploderat:
            if keys[pygame.K_LEFT]:
                spelare_2.flytta("vänster")
            if keys[pygame.K_RIGHT]:
                spelare_2.flytta("höger")
            if keys[pygame.K_UP]:
                spelare_2.flytta("upp")
            if keys[pygame.K_DOWN]:
                spelare_2.flytta("ner")
            if keys[pygame.K_k] and skott_räknare_spelare_2 >= skott_frekvens:
                skott_lista_spelare_2.append(Skott(spelare_2.rymdskepp_x + 20, spelare_2.rymdskepp_y))
                skott_räknare_spelare_2 = 0

        # Rita spelare
        spelare_1.rita(skärm)
        if spelare_2:
            spelare_2.rita(skärm)

        # Hantera skott för spelare 1
        for skott_obj in reversed(skott_lista_spelare_1):
            skott_obj.flytta()
            skott_obj.rita(skärm)
            if skott_obj.y < -100:
                skott_lista_spelare_1.remove(skott_obj)

        # Hantera skott för spelare 2
        if spelare_2:
            for skott_obj in reversed(skott_lista_spelare_2):
                skott_obj.flytta()
                skott_obj.rita(skärm)
                if skott_obj.y < -100:
                    skott_lista_spelare_2.remove(skott_obj)

        # Öka räknarna för skott för varje spelare
        skott_räknare_spelare_1 += 1
        if spelare_2:
            skott_räknare_spelare_2 += 1

        if asteroid_räknare >= asteroid_frekvens:
            asteroid_liten_lista.append(AsteroidLiten(random.randint(0, skärmens_bredd - sprite_ateroid_liten.get_width()), -sprite_ateroid_liten.get_height()))
            asteroid_räknare = 0

        asteroider_att_ta_bort = []  # Lista för att hålla reda på vilka asteroider som ska tas bort

        for asteroid_liten in asteroid_liten_lista:
            asteroid_liten.flytta()
            if asteroid_liten.kollidera(spelare_1.kollisions_rektangel):
                spelare_1.kollidera(asteroid_liten)
            if spelare_2 and asteroid_liten.kollidera(spelare_2.kollisions_rektangel):
                spelare_2.kollidera(asteroid_liten)
            if asteroid_liten.kollidera_med_skott(skott_lista_spelare_1):
                asteroider_att_ta_bort.append(asteroid_liten)  # Lägg till asteroiden i listan för borttagning
            if spelare_2 and asteroid_liten.kollidera_med_skott(skott_lista_spelare_2):
                asteroider_att_ta_bort.append(asteroid_liten)  # Lägg till asteroiden i listan för borttagning
            asteroid_liten.rita(skärm)
            if asteroid_liten.y > skärmens_höjd:
                asteroider_att_ta_bort.append(asteroid_liten)  # Lägg till asteroiden i listan för borttagning

        # Ta bort asteroider efter loopen
        for asteroid in asteroider_att_ta_bort:
            if asteroid in asteroid_liten_lista:
                asteroid_liten_lista.remove(asteroid)

        asteroid_räknare += 1  # Öka räknaren varje gång spelet uppdateras

        for explosion in expolsioner:
            for partikel in explosion:
                partikel.uppdatera()
                partikel.rita(skärm)

        explosioner = [[p for p in explosion if p.livslängd > 0] for explosion in expolsioner]
        explosioner = [e for e in explosioner if len(e) > 0]

        if spelare_1.exploderat and (not spelare_2 or spelare_2.exploderat):
            paus += 1    
            if paus >= 120:  # Vänta tills explosionseffekten är klar
                if visa_gameover_skärm():  # Visa "Game Over"-skärmen och gå tillbaka till menyn
                    spelet_körs = False  # Avsluta spelet
        
        score_text = font_poäng.render(f"Poäng: {gränssnitts_hanteraren.poäng}", True, (255, 255, 255))
        skärm.blit(score_text, (10, 10))  # Visa poängen i det övre vänstra hörnet
        
        pygame.display.update()

pygame.quit()