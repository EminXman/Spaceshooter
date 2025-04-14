import pygame
import random

# Skärmstorlek och inställningar
skärmens_bredd = 850  # Bredden på spelområdet
skärmens_höjd = 700  # Höjden på spelområdet

pygame.init()  # Initiera pygame för att använda dess funktioner

# Skapa skärmen (uppdaterad med nya dimensioner)
skärm = pygame.display.set_mode((skärmens_bredd, skärmens_höjd))  # Skapa en skärm med angivna dimensioner
pygame.display.set_caption("Space Shooter")  # Sätt titeln på spel-fönstret

# Spelstatus
paus = 0  # Variabel för att hantera paus eller väntetid i spelet

# Ladda bilder
original_bild = pygame.image.load("assets/sprites/SpaceShip.png")  # Ladda spelarens rymdskepp
original_bild_spelare_2 = pygame.image.load("assets/sprites/png-transparent-brown-and-black-game-item-illustration-space-shooting-spacecraft-sprite-computer-icons-spaceship-game-symmetry-video-game.png")  # Ladda rymdskepp för spelare 2
backgrund_mörkblå = pygame.image.load("assets/backgrounds/bg.png")  # Ladda bakgrundsbild
backgrund_stjärnor = pygame.image.load("assets/backgrounds/stars-A.png")  # Ladda stjärnbakgrund
sprite_jetstråle = pygame.image.load("assets/sprites/fire.png")  # Ladda jetstråle för rymdskepp
sprite_skott = pygame.image.load("assets/sprites/bullet.png")  # Ladda skottbild
sprite_ateroid_liten = pygame.image.load("assets/sprites/small-A.png")  # Ladda asteroidbild

pygame.mixer.init()  # Initiera pygame-mixer för att spela ljud och musik

# Ladda och spela bakgrundsmusik
pygame.mixer.music.load("assets/music/Mesmerizing Galaxy Loop.mp3")  # Ladda bakgrundsmusik
pygame.mixer.music.set_volume(0.1)  # Sätt volymen för musiken
pygame.mixer.music.play(-1)  # Spela musiken i en oändlig loop

sound_liten_explosion = pygame.mixer.Sound("assets/sounds/scfi_explosion.wav")  # Ladda ljud för liten explosion
sound_stor_explosion = pygame.mixer.Sound("assets/sounds/huge_explosion.wav")  # Ladda ljud för stor explosion

sound_liten_explosion.set_volume(0.7)  # Justera volymen för ljudet för liten explosion
sound_stor_explosion.set_volume(0.9)  # Justera volymen för ljudet för stor explosion

try:
    font = pygame.font.Font("assets/fonts/ZenDots-Regular.ttf", 74)  # Ladda font för rubriker
except FileNotFoundError:
    print("Fonten 'ZenDots-Regular.ttf' hittades inte. Använder standardfont.")
    font = pygame.font.SysFont(None, 74)  # Använd standardfont om den angivna fonten inte hittas

try:
    font_poäng = pygame.font.Font("assets/fonts/ZenDots-Regular.ttf", 30)  # Ladda font för poäng
except FileNotFoundError:
    print("Fonten 'ZenDots-Regular.ttf' hittades inte. Använder standardfont.")
    font_poäng = pygame.font.SysFont(None, 30)  # Använd standardfont om den angivna fonten inte hittas

text_gamover = font.render("GAME OVER", True, (255, 0, 0))  # Skapa text för "GAME OVER"
text_gamover_rect = text_gamover.get_rect(center=(skärmens_bredd // 2, skärmens_höjd // 2))  # Placera "GAME OVER"-texten i mitten av skärmen

# Lista för skott
skott_lista = []  # Skott för en spelare

# Lista för skott för båda spelarna
skott_lista_spelare_1 = []  # Skott för spelare 1
skott_lista_spelare_2 = []  # Skott för spelare 2

expolsioner = []  # Lista för explosioner

svart = (0, 0, 0)  # Färg för svart
FÄRG_LISTA = [(255, 0, 0), (255, 165, 0), (255, 255, 0),]  # Lista med färger för partiklar: Röd, orange, gul

# Bakgrundsposition
backgrund_y = 0  # Startposition för bakgrunden

# Skala spelarens sprite
sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))  # Skala spelarens rymdskepp
sprite_spelare_2 = pygame.transform.scale(original_bild_spelare_2, (original_bild.get_width() // 2, original_bild.get_height() // 2))  # Skala rymdskepp för spelare 2

# Spelarens position och hastighet
spelare_x = skärmens_bredd // 2 - 120  # Startposition för spelare 1
spelare_y = skärmens_höjd - 200  # Startposition för spelare 1
spelarens_hastighet = 3  # Hastighet för spelare 1

# Spelare 2 position och hastighet
spelare_2_x = skärmens_bredd // 2 + 120  # Startposition för spelare 2
spelare_2_y = skärmens_höjd - 200  # Startposition för spelare 2
spelare_2_hastighet = 3  # Hastighet för spelare 2

# Variabel för att hålla reda på tiden mellan skott
skott_frekvens = 20  # Justera detta värde för att ändra tiden mellan skott

# Variabler för att hålla reda på tiden mellan skott för varje spelare
skott_räknare_spelare_1 = 0  # Räknare för skott för spelare 1
skott_räknare_spelare_2 = 0  # Räknare för skott för spelare 2

# Variabel för att hålla reda på tiden mellan asteroider
asteroid_räknare = 0  # Räknare för asteroider
asteroid_frekvens = 50  # Justera detta värde för att ändra tiden mellan asteroider

# Klass för skott
class Skott:
    def __init__(self, x, y):
        self.x = x  # Startposition för skottet
        self.y = y  # Startposition för skottet
        self.hastighet = 10  # Hastighet för skottet
        self.bild = sprite_skott  # Bild för skottet

    def flytta(self):
        self.y -= self.hastighet  # Flytta skottet uppåt

    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))  # Rita skottet på skärmen

# Klass för små asteroider
class AsteroidLiten:
    def __init__(self, x, y):
        self.x = x  # Startposition för asteroiden
        self.y = y  # Startposition för asteroiden
        self.hastighet_x = random.uniform(-2, 2)  # Slumpmässig horisontell hastighet
        self.hastighet_y = 4  # Vertikal hastighet
        self.bild = sprite_ateroid_liten  # Bild för asteroiden
        self.kollisions_rektangel_asteroid = pygame.Rect(self.x, self.y, self.bild.get_width(), self.bild.get_height())  # Kollisionsrektangel för asteroiden

    def flytta(self):
        self.x += self.hastighet_x  # Flytta horisontellt
        self.y += self.hastighet_y  # Flytta vertikalt

        # Begränsa rörelsen inom skärmens bredd
        if self.x < 0 or self.x > skärmens_bredd - self.bild.get_width():
            self.hastighet_x *= -1  # Byt riktning om asteroiden når kanten

        self.kollisions_rektangel_asteroid.topleft = (self.x, self.y)  # Uppdatera kollisionsrektangeln

    def rita(self, skärm):
        skärm.blit(self.bild, (self.x, self.y))  # Rita asteroiden på skärmen
        # pygame.draw.rect(skärm, (255, 0, 0), self.kollisions_rektangel_asteroid, 2)  # Kommenterad för att dölja rektangeln
    
    def kollidera(self, kollisions_rektangel_spelare):
        if self.kollisions_rektangel_asteroid.colliderect(kollisions_rektangel_spelare):  # Kontrollera kollision med spelaren
            sound_stor_explosion.play()  # Spela ljudet vid kollision
            print("Kollision med asteroid!")
            return True
        return False
    
    def kollidera_med_skott(self, objekt_lista):
        for skott in objekt_lista:
            if self.kollisions_rektangel_asteroid.colliderect(pygame.Rect(skott.x, skott.y, sprite_skott.get_width(), sprite_skott.get_height())):  # Kontrollera kollision med skott
                print("Kollision med skott!")
                gränssnitts_hanteraren.poäng += 1  # Öka poängen vid kollision med skott
                objekt_lista.remove(skott)  # Ta bort skottet från listan
                explosion = [Partiklar(self.x + 20, self.y + 20) for _ in range(100)]  # Skapa explosionseffekt
                expolsioner.append(explosion)  # Lägg till explosionen i listan
                sound_liten_explosion.play()  # Spela ljudet för liten explosion
                return True
        return False

class Partiklar:
    def __init__(self, x, y, färg=None):
        self.x = x  # Startposition för partikeln
        self.y = y  # Startposition för partikeln
        self.livslängd = random.randint(20, 50)  # Livslängd för partikeln
        self.hastighet_x = random.uniform(-2, 2)  # Horisontell hastighet
        self.hastighet_y = random.uniform(-2, 2)  # Vertikal hastighet
        self.radius = random.randint(3, 6)  # Storlek på partikeln
        self.färg = färg if färg else random.choice(FÄRG_LISTA)  # Färg på partikeln

    def uppdatera(self):
        self.x += self.hastighet_x  # Uppdatera positionen horisontellt
        self.y += self.hastighet_y  # Uppdatera positionen vertikalt
        self.livslängd -= 1  # Minska livslängden

    def rita(self, skärm):
        if self.livslängd > 0:  # Rita partikeln om den fortfarande lever
            pygame.draw.circle(skärm, self.färg, (int(self.x), int(self.y)), self.radius)

class Rymdskepp:
    def __init__(self, x, y, sprite, jetstråle_sprite=None):
        self.rymdskepp_x = x  # Startposition för rymdskeppet
        self.rymdskepp_y = y  # Startposition för rymdskeppet
        self.sprite_rymdskepp = sprite  # Bild för rymdskeppet

        # Jetmotor behövs inte för spelare 2
        if jetstråle_sprite:
            self.jetstråle_x = self.rymdskepp_x + 13  # Startposition för jetstrålen
            self.jetstråle_y = self.rymdskepp_y + 46  # Startposition för jetstrålen
            self.sprite_jetstråle = jetstråle_sprite  # Bild för jetstrålen
        else:
            self.jetstråle_x = None
            self.jetstråle_y = None
            self.sprite_jetstråle = None

        self.rymdskepp_hastighet = 10  # Hastighet för rymdskeppet
        self.exploderat = False  # Status för om rymdskeppet har exploderat
        self.kollisions_rektangel = pygame.Rect(self.rymdskepp_x, self.rymdskepp_y, self.sprite_rymdskepp.get_width(), self.sprite_rymdskepp.get_height())  # Kollisionsrektangel för rymdskeppet
        self.exploderat_x = 0  # Position för explosionen
        self.exploderat_y = 0  # Position för explosionen

    def flytta(self, riktning):
        if not self.exploderat:  # Flytta rymdskeppet om det inte har exploderat
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

            self.kollisions_rektangel.topleft = (self.rymdskepp_x, self.rymdskepp_y)  # Uppdatera kollisionsrektangeln

    def ändra_hastighet(self, ny_hastighet):
        self.rymdskepp_hastighet = ny_hastighet  # Ändra hastigheten för rymdskeppet

    def rita(self, skärm):
        if not self.exploderat:  # Rita rymdskeppet om det inte har exploderat
            skärm.blit(self.sprite_rymdskepp, (self.rymdskepp_x, self.rymdskepp_y))
            if self.sprite_jetstråle:  # Rita jetmotor endast om den finns
                skärm.blit(self.sprite_jetstråle, (self.jetstråle_x, self.jetstråle_y))
        else:
            self.kollisions_rektangel = pygame.Rect(0, 0, 0, 0)  # Ta bort kollisionsrektangeln om rymdskeppet har exploderat

    def kollidera(self, asteroid):
        if not self.exploderat:  # Kontrollera kollision om rymdskeppet inte har exploderat
            if self.kollisions_rektangel.colliderect(asteroid.kollisions_rektangel_asteroid):
                print("Kollision!")
                self.exploderat = True
                self.exploderat_x = self.rymdskepp_x
                self.exploderat_y = self.rymdskepp_y
                explosion = [Partiklar(self.exploderat_x + 60, self.exploderat_y + 46) for _ in range(100)]  # Skapa explosionseffekt
                expolsioner.append(explosion)  # Lägg till explosionen i listan
                sound_stor_explosion.play()  # Spela ljudet för stor explosion
                return True
        return False

class Gränsnitt:
    """ Klass för gränssnittet """
    def __init__(self):
        self.poäng = 0  # Startpoäng för spelet
    
    def uppdatera_poäng():
        poäng += 1  # Öka poängen

gränssnitts_hanteraren = Gränsnitt()  # Skapa en instans av gränssnittshanteraren

class Meny:
    """Klass för att hantera huvudmenyn."""
    def __init__(self, skärm, font, font_poäng, skärmens_bredd, skärmens_höjd):
        self.skärm = skärm  # Skärmen där menyn ska visas
        self.font = font  # Font för rubriker
        self.font_poäng = font_poäng  # Font för poäng
        self.skärmens_bredd = skärmens_bredd  # Bredden på skärmen
        self.skärmens_höjd = skärmens_höjd  # Höjden på skärmen

    def visa(self):
        """Visa huvudmenyn och hantera val."""
        meny_körs = True
        while meny_körs:
            self.skärm.fill((0, 0, 0))  # Fyll skärmen med svart
            titel_text = self.font.render("SPACE SHOOTER", True, (255, 255, 255))  # Skapa text för titeln
            titel_rect = titel_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd // 4))  # Placera titeln i mitten av skärmen
            self.skärm.blit(titel_text, titel_rect)  # Visa titeln

            en_spelare_text = self.font_poäng.render("1. Starta spel för 1 spelare", True, (255, 255, 255))  # Skapa text för alternativet "1 spelare"
            en_spelare_rect = en_spelare_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd // 2 - 50))  # Placera texten
            self.skärm.blit(en_spelare_text, en_spelare_rect)  # Visa texten

            två_spelare_text = self.font_poäng.render("2. Starta spel för 2 spelare", True, (255, 255, 255))  # Skapa text för alternativet "2 spelare"
            två_spelare_rect = två_spelare_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd // 2 + 50))  # Placera texten
            self.skärm.blit(två_spelare_text, två_spelare_rect)  # Visa texten

            avsluta_text = self.font_poäng.render("3. Avsluta spelet", True, (255, 255, 255))  # Skapa text för alternativet "Avsluta"
            avsluta_rect = avsluta_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd // 2 + 150))  # Placera texten
            self.skärm.blit(avsluta_text, avsluta_rect)  # Visa texten

            instruktion_text = self.font_poäng.render("Tryck 1, 2 eller 3 för att välja", True, (200, 200, 200))  # Skapa instruktionstext
            instruktion_rect = instruktion_text.get_rect(center=(self.skärmens_bredd // 2, self.skärmens_höjd - 100))  # Placera instruktionstexten
            self.skärm.blit(instruktion_text, instruktion_rect)  # Visa instruktionstexten

            pygame.display.update()  # Uppdatera skärmen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Avsluta spelet om fönstret stängs
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:  # Hantera tangenttryckningar
                    if event.key == pygame.K_1:  # Starta spel för 1 spelare
                        return 1
                    if event.key == pygame.K_2:  # Starta spel för 2 spelare
                        return 2
                    if event.key == pygame.K_3:  # Avsluta spelet
                        pygame.quit()
                        exit()

# Lista för asteroider
asteroid_liten_lista = []  # Lista för små asteroider

def visa_gameover_skärm():
    """Visa Game Over-skärmen och gå tillbaka till huvudmenyn."""
    skärm.fill((0, 0, 0))  # Fyll skärmen med svart
    skärm.blit(text_gamover, text_gamover_rect)  # Visa "GAME OVER"-texten
    pygame.display.update()  # Uppdatera skärmen
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
meny = Meny(skärm, font, font_poäng, skärmens_bredd, skärmens_höjd)  # Skapa en instans av menyn

while True:
    antal_spelare = meny.visa()  # Visa menyn och få antalet spelare

    # Återställ spelet innan det startas
    återställ_spelet()

    # Skapa instanser för spelare baserat på valet
    spelare_1 = Rymdskepp(spelare_x, spelare_y, sprite_spelare, sprite_jetstråle)  # Skapa spelare 1
    spelare_2 = None
    if antal_spelare == 2:
        spelare_2 = Rymdskepp(spelare_2_x, spelare_2_y, sprite_spelare_2)  # Skapa spelare 2 (ingen jetmotor)

    spelare_1.ändra_hastighet(4)  # Sätt hastigheten för spelare 1 till samma som asteroiden
    if spelare_2:
        spelare_2.ändra_hastighet(4)  # Sätt hastigheten för spelare 2 till samma som asteroiden

    # Huvudloopen för spelet
    spelet_körs = True
    while spelet_körs:
        skärm.fill((0, 0, 30))  # Fyll skärmen med en mörkblå färg

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Avsluta spelet om fönstret stängs
                pygame.quit()
                exit()

        skärm.blit(backgrund_mörkblå, (0, 0))  # Rita bakgrunden
        skärm.blit(backgrund_stjärnor, (0, backgrund_y))  # Rita stjärnbakgrunden
        skärm.blit(backgrund_stjärnor, (0, backgrund_y - skärmens_höjd))  # Rita stjärnbakgrunden igen för att skapa en loop

        backgrund_y += 2  # Flytta bakgrunden nedåt
        if backgrund_y > skärmens_höjd:  # Återställ bakgrundens position om den når botten
            backgrund_y = 0

        keys = pygame.key.get_pressed()  # Hämta tangenttryckningar

        # Rörelse för spelare 1 (WASD)
        if not spelare_1.exploderat:  # Kontrollera om spelare 1 inte har exploderat
            if keys[pygame.K_a]:  # Flytta vänster
                spelare_1.flytta("vänster")
            if keys[pygame.K_d]:  # Flytta höger
                spelare_1.flytta("höger")
            if keys[pygame.K_w]:  # Flytta upp
                spelare_1.flytta("upp")
            if keys[pygame.K_s]:  # Flytta ner
                spelare_1.flytta("ner")
            if keys[pygame.K_SPACE] and skott_räknare_spelare_1 >= skott_frekvens:  # Skjut skott
                skott_lista_spelare_1.append(Skott(spelare_1.rymdskepp_x + 20, spelare_1.rymdskepp_y))
                skott_räknare_spelare_1 = 0

        # Rörelse för spelare 2 (piltangenter) om det är ett 2-spelarläge
        if spelare_2 and not spelare_2.exploderat:  # Kontrollera om spelare 2 inte har exploderat
            if keys[pygame.K_LEFT]:  # Flytta vänster
                spelare_2.flytta("vänster")
            if keys[pygame.K_RIGHT]:  # Flytta höger
                spelare_2.flytta("höger")
            if keys[pygame.K_UP]:  # Flytta upp
                spelare_2.flytta("upp")
            if keys[pygame.K_DOWN]:  # Flytta ner
                spelare_2.flytta("ner")
            if keys[pygame.K_k] and skott_räknare_spelare_2 >= skott_frekvens:  # Skjut skott
                skott_lista_spelare_2.append(Skott(spelare_2.rymdskepp_x + 20, spelare_2.rymdskepp_y))
                skott_räknare_spelare_2 = 0

        # Rita spelare
        spelare_1.rita(skärm)  # Rita spelare 1
        if spelare_2:
            spelare_2.rita(skärm)  # Rita spelare 2

        # Hantera skott för spelare 1
        for skott_obj in reversed(skott_lista_spelare_1):  # Loopa igenom skott för spelare 1
            skott_obj.flytta()  # Flytta skottet
            skott_obj.rita(skärm)  # Rita skottet
            if skott_obj.y < -100:  # Ta bort skottet om det är utanför skärmen
                skott_lista_spelare_1.remove(skott_obj)

        # Hantera skott för spelare 2
        if spelare_2:
            for skott_obj in reversed(skott_lista_spelare_2):  # Loopa igenom skott för spelare 2
                skott_obj.flytta()  # Flytta skottet
                skott_obj.rita(skärm)  # Rita skottet
                if skott_obj.y < -100:  # Ta bort skottet om det är utanför skärmen
                    skott_lista_spelare_2.remove(skott_obj)

        # Öka räknarna för skott för varje spelare
        skott_räknare_spelare_1 += 1  # Öka räknaren för spelare 1
        if spelare_2:
            skott_räknare_spelare_2 += 1  # Öka räknaren för spelare 2

        if asteroid_räknare >= asteroid_frekvens:  # Skapa en ny asteroid om räknaren når frekvensen
            asteroid_liten_lista.append(AsteroidLiten(random.randint(0, skärmens_bredd - sprite_ateroid_liten.get_width()), -sprite_ateroid_liten.get_height()))
            asteroid_räknare = 0

        asteroider_att_ta_bort = []  # Lista för att hålla reda på vilka asteroider som ska tas bort

        for asteroid_liten in asteroid_liten_lista:  # Loopa igenom asteroider
            asteroid_liten.flytta()  # Flytta asteroiden
            if asteroid_liten.kollidera(spelare_1.kollisions_rektangel):  # Kontrollera kollision med spelare 1
                spelare_1.kollidera(asteroid_liten)
            if spelare_2 and asteroid_liten.kollidera(spelare_2.kollisions_rektangel):  # Kontrollera kollision med spelare 2
                spelare_2.kollidera(asteroid_liten)
            if asteroid_liten.kollidera_med_skott(skott_lista_spelare_1):  # Kontrollera kollision med skott för spelare 1
                asteroider_att_ta_bort.append(asteroid_liten)  # Lägg till asteroiden i listan för borttagning
            if spelare_2 and asteroid_liten.kollidera_med_skott(skott_lista_spelare_2):  # Kontrollera kollision med skott för spelare 2
                asteroider_att_ta_bort.append(asteroid_liten)  # Lägg till asteroiden i listan för borttagning
            asteroid_liten.rita(skärm)  # Rita asteroiden
            if asteroid_liten.y > skärmens_höjd:  # Ta bort asteroiden om den är utanför skärmen
                asteroider_att_ta_bort.append(asteroid_liten)  # Lägg till asteroiden i listan för borttagning

        # Ta bort asteroider efter loopen
        for asteroid in asteroider_att_ta_bort:
            if asteroid in asteroid_liten_lista:
                asteroid_liten_lista.remove(asteroid)

        asteroid_räknare += 1  # Öka räknaren varje gång spelet uppdateras

        for explosion in expolsioner:  # Loopa igenom explosioner
            for partikel in explosion:  # Loopa igenom partiklar i explosionen
                partikel.uppdatera()  # Uppdatera partikeln
                partikel.rita(skärm)  # Rita partikeln

        explosioner = [[p for p in explosion if p.livslängd > 0] for explosion in expolsioner]  # Ta bort döda partiklar
        explosioner = [e for e in explosioner if len(e) > 0]  # Ta bort tomma explosioner

        if spelare_1.exploderat and (not spelare_2 or spelare_2.exploderat):  # Kontrollera om båda spelarna har exploderat
            paus += 1    
            if paus >= 120:  # Vänta tills explosionseffekten är klar
                if visa_gameover_skärm():  # Visa "Game Over"-skärmen och gå tillbaka till menyn
                    spelet_körs = False  # Avsluta spelet
        
        score_text = font_poäng.render(f"Poäng: {gränssnitts_hanteraren.poäng}", True, (255, 255, 255))  # Skapa text för poängen
        skärm.blit(score_text, (10, 10))  # Visa poängen i det övre vänstra hörnet
        
        pygame.display.update()  # Uppdatera skärmen

pygame.quit()  # Avsluta pygame